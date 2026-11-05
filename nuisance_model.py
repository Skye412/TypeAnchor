"""Nuisance-aware residual and semantic competition modules (v0)."""
import torch
from torch import nn
from torch.nn import functional as F

class NuisanceHead(nn.Module):
    """Four-level query/reference residual head and n-way semantic competition.

    Inputs are patch tokens without CLS: query list [B,N,D], refs list
    [B,K,N,D], and text embeddings [n_anchors,E]. Matching uses Euclidean distance.
    Anchor layout: 0 normal, 1-4 defect types, 5 generic defect, 6.. nuisances
    (n_anchors=13 full set, 6 = no-nuisance-anchor ablation).
    """
    def __init__(self, token_dim=1024, text_dim=768, grid=37, hidden=128, temperature=.07, sigma=1.5, n_anchors=13):
        super().__init__()
        self.grid=grid; self.temperature=temperature; self.n_anchors=n_anchors
        self.visual=nn.ModuleList([nn.Sequential(nn.Linear(token_dim,token_dim//4),nn.GELU(),nn.Linear(token_dim//4,token_dim)) for _ in range(4)])
        self.projections=nn.ModuleList([nn.Linear(token_dim,text_dim) for _ in range(4)])
        self.res_heads=nn.ModuleList([nn.Conv2d(2*token_dim,hidden,1) for _ in range(4)])
        self.seg=nn.Sequential(nn.Conv2d(hidden,hidden,3,padding=1),nn.ReLU(),nn.Conv2d(hidden,1,1))
        self.image=nn.Sequential(nn.Linear(hidden*8,hidden),nn.ReLU(),nn.Linear(hidden,2))
        y,x=torch.meshgrid(torch.arange(-2,3),torch.arange(-2,3),indexing='ij')
        kernel=torch.exp(-(x*x+y*y)/(2*sigma*sigma)).float().view(1,1,5,5)
        self.register_buffer('kernel',kernel)

    def forward(self,queries,references,text,output_size=518):
        if text.shape[0]!=self.n_anchors: raise ValueError('Unexpected anchor count')
        n_a=self.n_anchors
        z=[]; semantic=[]
        for i,(q,ref) in enumerate(zip(queries,references)):
            b,n,d=q.shape
            if n!=self.grid**2: raise ValueError('Unexpected patch grid')
            # Reference selection and matching use frozen backbone features.
            bank=ref.reshape(b,-1,d)
            with torch.no_grad():
                indices=torch.cat([torch.cdist(part,bank).argmin(-1) for part in q.split(256,dim=1)],dim=1)
                nearest=bank.gather(1,indices.unsqueeze(-1).expand(-1,-1,d))
            adapted=q+self.visual[i](q)
            feat=torch.cat((adapted,(adapted-nearest).abs()),dim=-1).transpose(1,2).reshape(b,2*d,self.grid,self.grid)
            z.append(F.relu(self.res_heads[i](feat)))
            semantic.append(F.normalize(self.projections[i](adapted),dim=-1) @ F.normalize(text,dim=-1).T / self.temperature)
        combined=torch.stack(z).sum(0)
        res_logits=self.seg(combined)
        pooled=torch.cat([torch.cat([a.mean((2,3)),a.amax((2,3))],1) for a in z],1)
        image_logits=self.image(pooled)
        scores=torch.stack(semantic).mean(0).transpose(1,2).reshape(-1,n_a,self.grid,self.grid)
        weights=res_logits.sigmoid()
        denominator=F.conv2d(weights,self.kernel,padding=2).clamp_min(1e-8)
        smooth=F.conv2d(scores*weights,self.kernel.expand(n_a,1,-1,-1),padding=2,groups=n_a)/denominator
        pi=smooth.softmax(1)
        residual=F.interpolate(res_logits,size=(output_size,output_size),mode='bilinear',align_corners=False).sigmoid()
        pi_up=F.interpolate(pi,size=(output_size,output_size),mode='bilinear',align_corners=False)
        typed=pi_up[:,1:5]; generic=residual*pi_up[:,1:6].sum(1,keepdim=True)
        return {'residual':residual,'image_logits':image_logits,'pi':pi,'typed':typed,'generic':generic,'binary':torch.maximum(generic,typed.amax(1,keepdim=True)),'nuisance':pi_up[:,6:].sum(1,keepdim=True)}

def explanation_loss(pi, masks, dropout_probability=.25, bg_target=None):
    """Grouped cross-entropy on pi [B,n,h,w].

    bg_target=None  : loose background target -log(pi_normal + sum pi_nuisance)  (v0 behaviour; collapsed in practice,
                      see docs/results.md §2b.4).
    bg_target [B,h,w] long : per-cell anchor index for background cells (0 = normal, 6.. = a pseudo-labelled nuisance);
                      loss is the plain -log pi[bg_target].
    """
    target=F.adaptive_avg_pool2d(masks.float(),pi.shape[-2:])>=.25
    labels=target.float()
    if torch.rand((),device=pi.device)<dropout_probability:
        c=torch.randint(4,(),device=pi.device); dropped=labels[:,c].clone(); labels[:,c]=0
    else: dropped=torch.zeros_like(labels[:,0])
    defect=labels.sum(1); norm=(defect+dropped).clamp_min(1)
    loss=-(labels*pi[:,1:5].clamp_min(1e-8).log()).sum(1)/norm
    loss-=dropped*pi[:,5].clamp_min(1e-8).log()/norm
    background=(defect+dropped)==0
    if bg_target is None:
        # Without nuisance anchors (n_anchors=6) the loose target reduces to the normal anchor alone.
        loss[background]=-(pi[:,0]+pi[:,6:].sum(1))[background].clamp_min(1e-8).log()
    else:
        picked=pi.gather(1,bg_target.unsqueeze(1)).squeeze(1)
        loss[background]=-picked[background].clamp_min(1e-8).log()
    return loss.mean()


# ---------------------------------------------------------------------------------------------------------------------
# v2: residual-conditioned hierarchical decoupled gate (RC-HDG). See docs/results.md §2d.
# Anchor layout: 0 normal, 1-4 defect types, 5 generic defect, 6.. nuisances (graffiti removed -> 12 anchors by default).
# ---------------------------------------------------------------------------------------------------------------------
N_DEFECT_GROUP=5  # anchors 1..5

class NuisanceHeadV2(nn.Module):
    """Differences from NuisanceHead:
    * dual-path similarity: per-anchor learnable gate gamma mixes unsmoothed local similarity with the residual-weighted
      5x5 regional pooling (thin cracks keep local evidence, blobs keep regional context);
    * three-way competition read off the n-way softmax: nu = defect mass (anchors 1..5), mu = nuisance mass (6..);
    * four independent sigmoid type heads on local similarity (multi-label; overlap allowed), gated by nu;
    * image head pools residual features re-weighted by (0.5 + 0.5 nu) so high-residual nuisance regions are damped.
    """
    def __init__(self, token_dim=1024, text_dim=768, grid=37, hidden=128, temperature=.07, sigma=1.5, n_anchors=12, gamma_init=.5, nu_gate=True, gamma_fixed=None, use_residual=True):
        """nu_gate=False: ablation without nu gating (image head pools raw residual features; generic = residual; typed not gated).
        gamma_fixed in {0.,1.}: ablation with gamma frozen at pure regional (0) or pure local (1) similarity."""
        super().__init__()
        self.grid=grid; self.temperature=temperature; self.n_anchors=n_anchors; self.nu_gate=nu_gate; self.gamma_fixed=gamma_fixed; self.use_residual=use_residual   # use_residual=False: ablation, reference residual replaced by zeros (references unused)
        self.visual=nn.ModuleList([nn.Sequential(nn.Linear(token_dim,token_dim//4),nn.GELU(),nn.Linear(token_dim//4,token_dim)) for _ in range(4)])
        self.projections=nn.ModuleList([nn.Linear(token_dim,text_dim) for _ in range(4)])
        self.res_heads=nn.ModuleList([nn.Conv2d(2*token_dim,hidden,1) for _ in range(4)])
        self.seg=nn.Sequential(nn.Conv2d(hidden,hidden,3,padding=1),nn.ReLU(),nn.Conv2d(hidden,1,1))
        self.image=nn.Sequential(nn.Linear(hidden*8,hidden),nn.ReLU(),nn.Linear(hidden,2))
        g=torch.full((n_anchors,),float(torch.logit(torch.tensor(gamma_init))))
        if gamma_fixed is not None: g=torch.full((n_anchors,),12. if gamma_fixed>=.5 else -12.)
        self.gamma_logit=nn.Parameter(g,requires_grad=gamma_fixed is None)   # per-anchor local/regional mix
        self.type_scale=nn.Parameter(torch.ones(4)); self.type_bias=nn.Parameter(torch.zeros(4))   # sigmoid type heads
        y,x=torch.meshgrid(torch.arange(-2,3),torch.arange(-2,3),indexing='ij')
        kernel=torch.exp(-(x*x+y*y)/(2*sigma*sigma)).float().view(1,1,5,5)
        self.register_buffer('kernel',kernel)

    def forward(self,queries,references,text,output_size=518):
        if text.shape[0]!=self.n_anchors: raise ValueError('Unexpected anchor count')
        n_a=self.n_anchors
        z=[]; semantic=[]
        if references is None: references=[None]*len(queries)
        for i,(q,ref) in enumerate(zip(queries,references)):
            b,n,d=q.shape
            if n!=self.grid**2: raise ValueError('Unexpected patch grid')
            adapted=q+self.visual[i](q)
            if self.use_residual:
                bank=ref.reshape(b,-1,d)
                with torch.no_grad():
                    indices=torch.cat([torch.cdist(part,bank).argmin(-1) for part in q.split(256,dim=1)],dim=1)
                    nearest=bank.gather(1,indices.unsqueeze(-1).expand(-1,-1,d))
                resid=(adapted-nearest).abs()
            else: resid=torch.zeros_like(adapted)
            feat=torch.cat((adapted,resid),dim=-1).transpose(1,2).reshape(b,2*d,self.grid,self.grid)
            z.append(F.relu(self.res_heads[i](feat)))
            semantic.append(F.normalize(self.projections[i](adapted),dim=-1) @ F.normalize(text,dim=-1).T / self.temperature)
        combined=torch.stack(z).sum(0)
        res_logits=self.seg(combined)                                               # [B,1,g,g]
        weights=res_logits.sigmoid()
        local=torch.stack(semantic).mean(0).transpose(1,2).reshape(-1,n_a,self.grid,self.grid)   # unsmoothed
        denominator=F.conv2d(weights,self.kernel,padding=2).clamp_min(1e-8)
        region=F.conv2d(local*weights,self.kernel.expand(n_a,1,-1,-1),padding=2,groups=n_a)/denominator
        gamma=self.gamma_logit.sigmoid().view(1,n_a,1,1)
        mixed=gamma*local+(1-gamma)*region
        pi=mixed.softmax(1)                                                          # n-way, read as 3 groups
        nu=pi[:,1:1+N_DEFECT_GROUP].sum(1,keepdim=True); mu=pi[:,1+N_DEFECT_GROUP:].sum(1,keepdim=True)
        # multi-label type heads on the gamma-mixed similarity relative to the normal anchor (gamma learns per anchor
        # how much regional context each type wants; cracks can stay local, blobs can go regional)
        margin=(mixed[:,1:5]-mixed[:,:1])*self.temperature                           # back to cosine units
        p_type=(margin*self.type_scale.view(1,4,1,1)*(1/self.temperature)+self.type_bias.view(1,4,1,1)).sigmoid()
        # image head on nu-gated residual features
        gate=.5+.5*nu if self.nu_gate else torch.ones_like(nu)
        pooled=torch.cat([torch.cat([(a*gate).mean((2,3)),(a*gate).amax((2,3))],1) for a in z],1)
        image_logits=self.image(pooled)
        up=lambda t:F.interpolate(t,size=(output_size,output_size),mode='bilinear',align_corners=False)
        residual=up(res_logits).sigmoid(); nu_up=up(nu); mu_up=up(mu)
        typed=up(p_type)
        if self.nu_gate: typed_gated=typed*nu_up; generic=residual*nu_up
        else: typed_gated=typed; generic=residual
        # 'typed' is the ungated multi-label probability (same meaning as v0's typed = pi_c); 'typed_gated' = typed * nu is the
        # model's own output and feeds the binary map. Evaluation reports typed, typed*residual and typed*nu separately.
        return {'residual':residual,'image_logits':image_logits,'pi':pi,'nu':nu,'mu':mu,'p_type':p_type,'res_weights':weights,
                'typed':typed,'typed_gated':typed_gated,'nu_up':nu_up,'generic':generic,'binary':torch.maximum(generic,typed_gated.amax(1,keepdim=True)),'nuisance':mu_up}

def explanation_loss_v2(pi,masks,res_weights,zs_prob=None,tau_res=.25,tau_conf=.5,beta=.5,use_res=True,res_cap=.3,dropout_probability=.25):
    """Residual-conditioned stratified supervision on the n-way pi [B,n,g,g].
    defect cells (any class mask >= .25 of the cell): -log nu  +  within-group CE on pi[1..5]/nu with soft class targets
        (overlap shares mass; with prob dropout_probability one class is re-targeted to the generic anchor, as in v0), so the
        defect group cannot collapse onto one anchor and the generic anchor keeps its 'type-unknown defect' meaning
    background cells, low residual and no confident zero-shot nuisance: -log pi_normal
    background cells, high residual (sigmoid res > tau_res, detached) or confident zero-shot nuisance:
        beta * (-log mu) + (1-beta) * KL(q_zs || pi_nuis / mu)   where q_zs is the centered zero-shot distribution over nuisances.
    zs_prob: [B,k,g,g] with k = 1 + n_nuisance (normal first), or None (then only the residual condition is used and the KL term is dropped).
    Returns (loss, stats dict)."""
    B,n,g,_=pi.shape; n_nuis=n-1-N_DEFECT_GROUP
    target=F.adaptive_avg_pool2d(masks.float(),(g,g))>=.25
    defect=target.any(1)                                                             # [B,g,g]
    nu=pi[:,1:1+N_DEFECT_GROUP].sum(1); mu=pi[:,1+N_DEFECT_GROUP:].sum(1); p0=pi[:,0]
    r=res_weights.detach()[:,0]
    if use_res:
        # absolute threshold AND within the top res_cap fraction of background cells of the image (guards the untrained-head regime)
        bgvals=r[~defect]; cap=torch.quantile(bgvals,1-res_cap) if bgvals.numel() else r.new_tensor(float('inf'))
        high=(r>tau_res)&(r>=cap)
    else: high=torch.zeros_like(defect)
    if n_nuis==0:
        # no nuisance anchors (6-anchor ablation of v2): every background cell targets the normal anchor
        suspicious=torch.zeros_like(defect); zs_prob=None
    elif zs_prob is not None:
        q_nuis=zs_prob[:,1:]; conf=(q_nuis.max(1).values>=tau_conf)&(q_nuis.argmax(1)>=0)
        suspicious=(high|conf)&~defect
    else: suspicious=high&~defect
    clean=~defect&~suspicious
    loss=torch.zeros_like(p0)
    labels=target.float()                                                            # [B,4,g,g]
    if torch.rand((),device=pi.device)<dropout_probability:
        c=torch.randint(4,(),device=pi.device); dropped=labels[:,c].clone(); labels[:,c]=0
    else: dropped=torch.zeros_like(labels[:,0])
    pi_in=pi[:,1:1+N_DEFECT_GROUP]/nu.unsqueeze(1).clamp_min(1e-8)                    # within-defect-group distribution
    norm=(labels.sum(1)+dropped).clamp_min(1)
    ce_in=-(labels*pi_in[:,:4].clamp_min(1e-8).log()).sum(1)/norm-dropped*pi_in[:,4].clamp_min(1e-8).log()/norm
    loss[defect]=(-nu.clamp_min(1e-8).log()+ce_in)[defect]
    loss[clean]=-p0[clean].clamp_min(1e-8).log()
    if suspicious.any():
        l=-beta*mu.clamp_min(1e-8).log()
        if zs_prob is not None:
            pi_n=pi[:,1+N_DEFECT_GROUP:]/mu.unsqueeze(1).clamp_min(1e-8)
            q=q_nuis/q_nuis.sum(1,keepdim=True).clamp_min(1e-8)
            kl=(q*(q.clamp_min(1e-8).log()-pi_n.clamp_min(1e-8).log())).sum(1)
            l=l+(1-beta)*kl
        loss[suspicious]=l[suspicious]
    stats={'defect_cells':int(defect.sum()),'clean_cells':int(clean.sum()),'suspicious_cells':int(suspicious.sum())}
    return loss.mean(),stats

def ortho_loss(text,hand,start=1+N_DEFECT_GROUP):
    """Penalise nuisance anchors that grow more similar to each other than their hand prompts are."""
    t=F.normalize(text[start:],dim=-1); h=F.normalize(hand[start:],dim=-1)
    ct=t@t.T; ch=h@h.T; iu=torch.triu_indices(t.shape[0],t.shape[0],1,device=t.device)
    return F.relu(ct[iu[0],iu[1]]-ch[iu[0],iu[1]]).sum()
