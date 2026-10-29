# CODEBRIM baseline protocol

Source: official AdaptCLIP upstream revision 354d9e3332ec5348b3d8e4439111d34f8e94c0a9, imported without prior BridgeAdaptCLIP modifications.

This is supervised target-dataset adaptation on 2861 train images, not the paper cross-dataset zero-shot setting. All three official adapters are trained for 15 full epochs at 518 input, batch 8, Adam lr 0.001, seed 10. The CLIP backbone is frozen. Training prompts come exclusively from the 1944 train normals. Validation uses 400 images; test is withheld during development. Pixel masks are the exact union of the four CODEBRIM colors.

Necessary source repairs: train.py called encode_text with two arguments, but the implementation requires encode_text_learn for learned prompts; freeze unused backbone gradients; preserve batch dimension of final masks. No adapter architecture or loss change.

The supplied audit is a separate official-checkpoint, no-target-training experiment; do not substitute this supervised baseline for its audit maps. Nuisance-aware architecture is not specified in the supplied audit document. Human A-E annotations must remain unfilled until the user labels cards.

Run preparation: python scripts/prepare_codebrim.py --source /home/skye/data/Skye/databases/Bridge512_balance_CODEBRIM
Run training: bash scripts/train_baseline.sh (requires configured origin; pushes before training).
