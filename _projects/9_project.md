---
layout: page
title: Federated Cervical Cancer Detection
description: Cervical cancer detection on Pap smear images, comparing three federated learning strategies.
img: assets/img/proj_9.jpg
importance: 3
category: research
---

**Links:** [GitHub repository](https://github.com/spearb0lt/Cervical-Cancer-Detection-implementing-FL-using-Pap-Smear-Dataset)

A deep learning study on detecting cervical cancer from a Pap smear dataset while training in a federated, privacy-preserving setting, where patient data never leaves the client. The project implements and compares three influential federated learning strategies on the same task:

- **FedDrop (Federated Dropout):** tackles the communication and computation bottlenecks of federated learning on resource-constrained devices by generating dropout-based subnets of the global model, adapting the dropout rate per device so each client trains a smaller network matched to its capacity, then aggregating the subnets back into the global model (based on arXiv:2109.15258).
- **FedAvg:** the foundational strategy that performs several rounds of local SGD on each client and averages the resulting model updates at the server, communicating only model weights rather than raw data (based on arXiv:1602.05629).
- **HeteroFL:** allows each client to train a model of different complexity based on its own compute and communication budget while still contributing to one global model, using shrunken model variants, a masking trick and static batch normalisation to keep updates stable across heterogeneous, non-IID clients (based on arXiv:2010.01264).

Comparing the three side by side on Pap smear data highlights the trade-offs between communication cost, per-device compute and accuracy in realistic federated deployments.
