# TypeAnchor: Text-Anchored Multi-Type Defect Segmentation on a Frozen Vision-Language Model for Concrete Bridge Inspection

This public repository contains the complete source code, documentation, LaTeX manuscript, and all 489 raw evaluation metric files for **TypeAnchor** (developed on Bridge512_balance_CODEBRIM, S2DS, and dacl10k).

---

## 1. Direct Links for Web AI Readers

### A. Paper & Documentation
- **Complete Experiment Results & Tables (docs/results.md)**:
  - Web: https://github.com/Skye412/TypeAnchor/blob/main/docs/results.md
  - Raw: https://raw.githubusercontent.com/Skye412/TypeAnchor/main/docs/results.md
- **Paper Storyline & Claim-Evidence Matrix (docs/paper-story.md)**:
  - Web: https://github.com/Skye412/TypeAnchor/blob/main/docs/paper-story.md
  - Raw: https://raw.githubusercontent.com/Skye412/TypeAnchor/main/docs/paper-story.md
- **Model Architecture Specification (docs/model-spec.md)**:
  - Web: https://github.com/Skye412/TypeAnchor/blob/main/docs/model-spec.md
  - Raw: https://raw.githubusercontent.com/Skye412/TypeAnchor/main/docs/model-spec.md
- **Research Idea Card & Hypotheses (docs/idea-card.md)**:
  - Web: https://github.com/Skye412/TypeAnchor/blob/main/docs/idea-card.md
  - Raw: https://raw.githubusercontent.com/Skye412/TypeAnchor/main/docs/idea-card.md
- **Audit & Experiment Protocol (docs/audit-design.md, docs/audit-execution.md, docs/experiment-protocol.md)**:
  - Raw (audit-design.md): https://raw.githubusercontent.com/Skye412/TypeAnchor/main/docs/audit-design.md
  - Raw (audit-execution.md): https://raw.githubusercontent.com/Skye412/TypeAnchor/main/docs/audit-execution.md
  - Raw (experiment-protocol.md): https://raw.githubusercontent.com/Skye412/TypeAnchor/main/docs/experiment-protocol.md
- **IEEEtran 6-Page LaTeX Manuscript (paper/main.tex & paper/refs.bib)**:
  - Web (main.tex): https://github.com/Skye412/TypeAnchor/blob/main/paper/main.tex
  - Raw (main.tex): https://raw.githubusercontent.com/Skye412/TypeAnchor/main/paper/main.tex
  - Raw (refs.bib): https://raw.githubusercontent.com/Skye412/TypeAnchor/main/paper/refs.bib

### B. Core Source Code
- **Model Definition (nuisance_model.py — NuisanceHeadV2, NuisanceHead, explanation_loss_v2)**:
  - Raw: https://raw.githubusercontent.com/Skye412/TypeAnchor/main/nuisance_model.py
- **Training Pipeline (train_nuisance.py — AnchorsV2, alternating optimization)**:
  - Raw: https://raw.githubusercontent.com/Skye412/TypeAnchor/main/train_nuisance.py
- **Inference & Map Saving (eval_nuisance.py, eval_tiled.py, eval_zeroshot.py)**:
  - Raw (eval_nuisance.py): https://raw.githubusercontent.com/Skye412/TypeAnchor/main/eval_nuisance.py
  - Raw (eval_tiled.py): https://raw.githubusercontent.com/Skye412/TypeAnchor/main/eval_tiled.py
  - Raw (eval_zeroshot.py): https://raw.githubusercontent.com/Skye412/TypeAnchor/main/eval_zeroshot.py
- **Unified Evaluation & Metrics (metrics_nuisance.py, metrics_multiclass.py, compare_fp.py, eval_filter.py)**:
  - Raw (metrics_nuisance.py): https://raw.githubusercontent.com/Skye412/TypeAnchor/main/metrics_nuisance.py
  - Raw (metrics_multiclass.py): https://raw.githubusercontent.com/Skye412/TypeAnchor/main/metrics_multiclass.py
  - Raw (compare_fp.py): https://raw.githubusercontent.com/Skye412/TypeAnchor/main/compare_fp.py
  - Raw (eval_filter.py): https://raw.githubusercontent.com/Skye412/TypeAnchor/main/eval_filter.py
  - Raw (eval_exclude_normals.txt): https://raw.githubusercontent.com/Skye412/TypeAnchor/main/eval_exclude_normals.txt
- **Compared Baselines Training & Evaluation (train_segformer.py, train_deeplab.py, multiads_bridge.py, eval_external_seg.py, eval_external_anomalyclip.py, eval_external_bayespfl.py)**:
  - Raw (train_segformer.py): https://raw.githubusercontent.com/Skye412/TypeAnchor/main/train_segformer.py
  - Raw (train_deeplab.py): https://raw.githubusercontent.com/Skye412/TypeAnchor/main/train_deeplab.py
  - Raw (multiads_bridge.py): https://raw.githubusercontent.com/Skye412/TypeAnchor/main/multiads_bridge.py
  - Raw (eval_external_seg.py): https://raw.githubusercontent.com/Skye412/TypeAnchor/main/eval_external_seg.py
  - Raw (eval_external_anomalyclip.py): https://raw.githubusercontent.com/Skye412/TypeAnchor/main/eval_external_anomalyclip.py
  - Raw (eval_external_bayespfl.py): https://raw.githubusercontent.com/Skye412/TypeAnchor/main/eval_external_bayespfl.py

### C. Raw Experiment Metric Files (runs_metrics/)
All 489 JSON, Markdown, and JSONL logs from runs/ are archived in runs_metrics/ (https://github.com/Skye412/TypeAnchor/tree/main/runs_metrics):
- **Matched-Recall False-Alarm Comparisons**:
  - CODEBRIM Test split (809 tiles): https://raw.githubusercontent.com/Skye412/TypeAnchor/main/runs_metrics/compare_fp_test.json
  - CODEBRIM Val split raw (400 tiles): https://raw.githubusercontent.com/Skye412/TypeAnchor/main/runs_metrics/compare_fp_fixed_raw.json
  - CODEBRIM Val split Cleaned-Val (379 tiles): https://raw.githubusercontent.com/Skye412/TypeAnchor/main/runs_metrics/compare_fp_fixed_clean.json
  - S2DS test (447 tiles): https://raw.githubusercontent.com/Skye412/TypeAnchor/main/runs_metrics/compare_fp_fixed_s2ds_test.json
  - dacl10k test (262 tiles): https://raw.githubusercontent.com/Skye412/TypeAnchor/main/runs_metrics/compare_fp_dacl10k.json
- **Summary Tables**:
  - 3-Seed Summary: https://raw.githubusercontent.com/Skye412/TypeAnchor/main/runs_metrics/summary_v2.md
  - Ablation Summary: https://raw.githubusercontent.com/Skye412/TypeAnchor/main/runs_metrics/summary_ablation.md
