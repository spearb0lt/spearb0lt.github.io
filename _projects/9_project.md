---
layout: page
title: Federated Cervical Cancer Detection
description: Cervical cancer detection on Pap smear images using federated learning with federated dropout.
img: assets/img/9.jpg
importance: 3
category: research
---

**Links:** [GitHub](https://github.com/spearb0lt/Cervical-Cancer-Detection-implementing-FL-using-Pap-Smear-Dataset)

A deep learning study on detecting cervical cancer from a Pap smear dataset while training in a federated, privacy-preserving setting.

## Highlights

- Implements Federated Dropout (Fed-Drop), following the paper "Federated Dropout: A Simple Approach for Enabling Federated Learning on Resource Constrained Devices".
- Addresses the two main federated-learning bottlenecks: the communication cost of high-dimensional model updates, and the computation cost on resource-constrained devices.
- Generates dropout-based subnets from a global model so each client trains a smaller network, then aggregates the subnets back into the global model, with dropout rates adapted to each client's communication and compute budget.
