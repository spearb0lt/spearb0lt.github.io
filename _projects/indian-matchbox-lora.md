---
layout: page
title: Indian Matchbox Art Style Generator
description: Two LoRA fine-tunes that generate vintage Indian matchbox labels from a text prompt, trained on the same 197 labels with two different model families and objectives.
img: assets/img/project/indian-matchbox-lora.jpg
importance: 1
category: finetuning
tags: [finetuning, lora, diffusion, flow-matching, text-to-image, image-generation, diffusers, huggingface, open-weights]
---

{% assign pt = site.data.project_tags %}{% assign all_families = 'domain,method,stack,meta' | split: ',' %}{% assign fams = pt.families_on.project_pages | default: all_families %}{% if pt.enabled and pt.show_on.project_pages and page.tags %}<div class="proj-tags proj-tags-page pt-style-{{ pt.style.project_pages | default: 'soft' }}">{% for t in page.tags %}{% assign fam = pt.map[t] | default: pt.default_family %}{% if fams contains fam %}<span class="proj-tag pt-{{ fam }} pt-tag-{{ t | slugify }}">{{ t }}</span>{% endif %}{% endfor %}</div>{% endif %}

**Links:** [GitHub repository](https://github.com/spearb0lt/Indian-Matchbox-Art-Style-Text-to-Image-Generator), [weights and model card on Hugging Face](https://huggingface.co/spearb0lt/Indian-Matchbox-Art-Style-Text-to-Image-Generator) and [the training dataset](https://huggingface.co/datasets/spearb0lt/Indian-Matchbox-Labels)

Two LoRA fine-tunes generate new vintage Indian matchbox labels from a text prompt. Both were trained on the same 197 labels, but on different model families with different training objectives, which makes the pair a controlled look at what the choice of base model actually buys you. The trigger word is `phlmx`, from _phillumeny_, the hobby of collecting matchbox labels.

## The two models

|                | SDXL LoRA                                      | SD3.5-medium LoRA                                              |
| -------------- | ---------------------------------------------- | -------------------------------------------------------------- |
| base model     | Stable Diffusion XL 1.0 (U-Net)                | Stable Diffusion 3.5-medium (MMDiT transformer)                |
| objective      | noise prediction (DDPM), min-SNR-5 weighting   | flow matching (velocity prediction), logit-normal timesteps    |
| text encoders  | CLIP-L + OpenCLIP-bigG                         | CLIP-L + OpenCLIP-bigG + T5-XXL                                |
| LoRA placement | U-Net attention, 560 layers, 23.2 M parameters | both streams of joint attention, 243 layers, 11.9 M parameters |
| training run   | 5,670 steps, 124 min on an L4                  | 1,418 steps of 4 images, 74 min on an L4                       |

## What the comparison shows

**Lettering is where they separate.** The SD3.5-medium LoRA spells the headline correctly in all five side-by-side pairs; its smaller secondary text is still often garbled. The SDXL LoRA gets some headlines right and misspells others ("LOVE BRRDS", "JJUMBO", "MAY UR"), and fills the rest of the label with invented pseudo-text.

Three causes, ordered by how confident I am in each. First, the text encoder: T5-XXL keeps the individual letters and words of the prompt, where CLIP encoders were trained to match images to captions and are known to be weak at spelling, and in SD3.5 those text tokens take part in every attention block. Second, the captions: notebook 69 trained on captions that spell out each label's headline, while 77% of notebook 55's auto-captions ran past SDXL's 77-token limit, cutting off exactly the ending where Florence-2 quotes the label's text. Third, the base models themselves, which a strength grid at LoRA scale 0.0 shows are roughly equal at short headlines, so the gap appears with fine-tuning rather than before it.

**Neither is simply better.** SD3.5-medium produces flat, saturated colour fields with clean outlines, like a crisp reprint. SDXL produces a muted palette with ink-on-paper texture, misregistration and engraved line work, more like a worn original, and its kohya-format file loads in AUTOMATIC1111 and ComfyUI. The two notebooks' CLIP scores are not comparable with each other, because they were measured on different evaluation prompts, so this judgement is explicitly a visual one.

## The data

197 vintage Indian matchbox labels, one per image, each with a hand-written English caption describing the content and the printed text rather than the style. 131 came from Wikimedia Commons, 46 from the Internet Archive and 20 from elsewhere, with every source recorded in `sources.csv`. Most originals are small scans, so 186 were upscaled 2x or 4x with a super-resolution model. Both models hold out the same split: 189 for training, 8 for evaluation.

## How each notebook is built

**Notebook 55 puts curation first.** It removes exact and near-duplicates with SHA-256, a perceptual hash and DINO embeddings, surfaces the least typical images for review, buckets by aspect ratio, auto-captions with Florence-2, then runs a caption ablation of four strategies in otherwise identical short runs and trains the main run with the winner. Checkpoints are selected on held-out CLIP style score, prompt adherence and a DINO memorisation check, and the diffusers and kohya exports are verified to load to identical weights.

**Notebook 69 puts the objective first.** Part one trains a small network on a 2-D toy under both objectives, verifies the flow-matching convention against the diffusers source, compares sampling from 1 to 64 steps, straightens paths with reflow and works through timestep sampling and the resolution shift. Part two caches the three text encoders and frees them to fit a 16 GB GPU, trains the LoRA with the flow-matching loss, tracks held-out velocity error at fixed noise levels, and reloads the saved file into a fresh pipeline to prove it reproduces the model.

The published SDXL run moved held-out CLIP style score from 0.583 to 0.672 with zero generations copying a training image; the SD3.5-medium run moved it from 0.580 to 0.592 and lowered held-out velocity error against the base model at all five fixed noise levels.
