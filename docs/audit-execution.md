# Audit execution

Frozen protocol: docs/audit-design.md. CODEBRIM validation 277 normal and 123 anomaly images; training normals as reference. Seed 10, no replacement for 4 references. 518 model input, bilinear 512 map output, sigma 4. Official AdaptCLIP prediction fusion is unchanged. Audit outputs stay under runs/audit/.

Existing MVTec checkpoint was found at /home/skye/data/Skye/AdaptCLIP/adaptclip_checkpoints/12_4_128_train_on_mvtec_3adapters_batch8/epoch_15.pth, SHA256 90b95703879af490b6ce841e141625516db63d23fdaef4cf86731b3d7bb3b1bb. Official origin is not yet verified. Treat maps as provisional until provenance matches official release.

AnomalyDINO source b9d1c2648e3a5247437d4d953d907a8f3d994457; 16 random training normals without replacement, seed 10; DINOv2-B/14, 518 input, cosine distance on normalized patch features, bilinear resize to 512, Gaussian sigma 4, no masking. Wrapper implements the prescribed patch nearest-neighbor configuration.
