---
layout: page
title: Federated Heart Disease Prediction
description: Predicting heart disease from clinical biomarkers using federated learning.
img: assets/img/project/federated_heart_disease.jpg
importance: 4
category: biomedical/cv
---

**Links:** [GitHub repository](https://github.com/spearb0lt/Heart-Disease-Prediction-with-Biomarkers-using-Federated-Learning)

A federated learning study that predicts heart disease from clinical biomarkers without ever centralising patient records, so hospitals or clinics could collaborate on a shared model while keeping their data local.

## Details

- Trains on a dataset of **918 subjects with 11 clinical features**, including age, sex, chest pain type, resting blood pressure, cholesterol, fasting blood sugar, resting ECG, maximum heart rate, exercise-induced angina, oldpeak and ST slope, predicting the presence of heart disease.
- Uses a federated setup where each client trains locally and only model updates are shared and aggregated into a global model, preserving the privacy of sensitive medical data.
- Sits alongside my other federated-learning work as an exploration of privacy-preserving machine learning applied to healthcare biomarkers.
