---
layout: page
title: Face Liveliness Detection
description: A lightweight, fast anti-spoofing model that tells real faces from fake images and videos.
img: assets/img/11.jpg
importance: 5
category: research
---

**Links:** [GitHub](https://github.com/spearb0lt/Face-Liveliness-Detection-Using-DL)

A deep learning model for face liveliness detection that differentiates between real and fake (spoofed) images and videos, intended to harden security systems against presentation attacks.

## Highlights

- Lightweight and fast, with a detection speed of about 30ms, making it suitable for real-time security use cases.
- Includes a full pipeline: extracting face crops from video streams to build a dataset, training the liveness model, and running live detection.
- Uses an OpenCV face detector (Caffe model) for face localisation before the liveness classification step.
