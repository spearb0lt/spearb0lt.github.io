---
layout: page
title: Privacy-Preserving Predictive Maintenance
description: A federated, differentially private framework for RUL prediction on the IDA 2024 SCANIA-X challenge.
img: assets/img/3.jpg
importance: 1
category: research
related_publications: true
---

**Links:** [GitHub](https://github.com/spearb0lt/Scania)

Built as part of my research at the VANET Lab, IIT Jodhpur, this project tackles the IDA 2024 Industrial Challenge: predicting the Remaining Useful Life (RUL) of components in the SCANIA-X dataset while keeping the training data private. The work is described in our paper {% cite dev2025dphybrid %}.

## What it does

- Preprocesses the SCANIA-X dataset and engineers a hybrid architecture that combines numerical and categorical features into transformer embeddings using a TabTransformer for minimal information loss.
- Implements several differential privacy (DP) algorithms, including Spectral-DP and DP-SGD, to protect training data.
- Designs a global model architecture that generalises to other predictive maintenance datasets involving numerical, categorical or multimodal features.
- Uses a federated training approach based on the `flwr` library, aggregating a global model across heterogeneous clients with different compute, parameters and hyperparameters, mirroring real industrial equipment.

## Results

- Currently the best RUL prediction model on the dataset with an MSE of 2725 while preserving training-data privacy.
- Developed an advanced Membership Inference Attack (MIA) that considers white-box, gray-box and black-box features along with time-series specific seasonality and trend features, achieving an MIA success rate (AUC) of 49.12% and MIA accuracy of 49.59%, confirming that the training data stays well protected.
