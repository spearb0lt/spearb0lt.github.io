---
layout: page
title: Privacy-Preserving Predictive Maintenance
description: A federated, differentially private framework for RUL prediction on the IDA 2024 SCANIA-X challenge.
img: assets/img/proj_1.jpg
importance: 1
category: research
related_publications: true
---

**Links:** [GitHub repository](https://github.com/spearb0lt/Scania)

Developed during my research at the VANET Lab, IIT Jodhpur, this project is an end-to-end privacy-preserving Predictive Maintenance (PdM) framework built for the **IDA 2024 Industrial Challenge** on the SCANIA-X truck telemetry dataset. The goal is to predict the Remaining Useful Life (RUL) of components accurately while guaranteeing that the sensitive training data cannot be reconstructed or inferred. The methodology is described in our paper {% cite dev2025dphybrid %}.

The framework is deliberately architected to be **cross-industry applicable**: any dataset that combines numerical time-series with categorical metadata can plug into the same pipeline with minimal configuration changes.

## Hybrid TabTransformer architecture

A two-stage model designed for multimodal industrial telemetry:

- A `TimeSeriesEmbedder` (a two-layer Transformer encoder) turns sliding windows of raw sensor data into a compact fixed-size embedding, capturing temporal dependencies across 70 time steps of 105 sensor features.
- A `CombinedRULModel` then feeds that time-series embedding, together with 8 ordinal-encoded vehicle-specification features, into a TabTransformer for the final RUL regression.
- The design minimises information loss across both modalities: last-step pooling preserves the causal state, while the TabTransformer's categorical embeddings avoid the information loss of one-hot encoding.

## Custom differential privacy

Two differential privacy mechanisms were implemented from scratch, without relying on third-party DP libraries for the core gradient manipulation:

- **Spectral-DP**, a gradient perturbation method that operates in the SVD (spectral) domain: singular values are clipped and perturbed instead of the raw gradients, giving more information-theoretically compact noise injection.
- **DP-SGD** with per-sample gradient clipping and Gaussian noise, and a custom Renyi Differential Privacy (Moments) accountant to track the (epsilon, delta) budget across training.

## Federated learning and privacy audit

- Federated training is built on the Flower (`flwr`) library, including a heterogeneous strategy where each client receives a different per-round configuration (local epochs, batch size, learning rate, optimizer, model depth and DP settings), mirroring real industrial deployments with varied hardware and privacy requirements.
- The framework is the current **best RUL prediction model on the dataset with an MSE of 2725** while preserving training-data privacy.
- A comprehensive Membership Inference Attack (white-box, gray-box and black-box, plus time-series specific seasonality and trend features) achieves an AUC of 49.12% and accuracy of 49.59%, both near random, confirming that the training data stays well protected.
