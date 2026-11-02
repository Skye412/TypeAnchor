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
