---
layout: page
title: Lung Cancer Detection with Soft Attention
description: A soft-attention deep transfer learning model for lung cancer identification from CT scans and histopathology.
img: assets/img/project/lung_cancer_dl.jpg
importance: 2
category: biomedical/cv
related_publications: true
---

**Links:** [GitHub repository](https://github.com/spearb0lt/Lung-Cancer-Detection-Using-DL) and [paper (DOI)](https://doi.org/10.1109/ISACC65211.2025.10969319)

Research from my time at the CMATER Lab, Jadavpur University, on identifying lung cancer from medical images. The work was published at IEEE ISACC 2025, and the full method and results are described in our paper {% cite dev2025lungcancer %}.

## What it does

- Builds a custom architecture based on transfer learning and a soft-attention mechanism that detects and classifies lung cancer from both CT scans and histopathological images.
- Uses the attention module to let the network focus on the diagnostically relevant regions of an image rather than the whole frame, which is important when lesions are small or localised.
- Experiments with attention, PCA, colour-channel splitting analysis and image partitioning to squeeze the most signal out of relatively small medical-imaging datasets.

## Datasets and evaluation

The system was trained and evaluated on three publicly available datasets that are deliberately small and challenging for deep models, including IQ-OTH/NCCD (1190 CT scan images across normal, benign and malignant cases) and the LC25000 histopathology dataset. Training across these multi-source datasets shows that the proposed method generalises across images captured under different conditions, a common and difficult requirement in medical imaging.
