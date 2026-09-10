---
layout: cv
permalink: /cv/
title: CV
nav: true
nav_order: 3
# cv_pdf: /assets/pdf/Shubhro_Dev_Resume.pdf # you can also use external links 
# cv_pdf: https://drive.google.com/file/d/1GiQo5uSdp-kXcbHb6Fi5XJ081OUrJDEv/view?usp=sharing # you can also use external links here

cv_format: rendercv # options: rendercv, jsonresume
description: The curriculum vitae of Shubhro Dev. Use the button above to view a PDF copy.

# How the download control in the page header looks and behaves.
# Markup: _includes/cv/render.liquid | styles: assets/css/main.scss | behaviour: assets/js/cv-downloads.js
#
#   single         one PDF icon, exactly what the theme ships (the default)
#   icons          two glyphs side by side, a caption under each
#   menu           one glyph, the choice opens on click
#   menu-caret     the same, plus a small caret hinting that a menu is there
#   split          the glyph opens the short file, the caret opens the choice
#   split-divided  the same, with a hairline between the two halves
#
# Every style except `single` needs BOTH urls below. Leave either one blank and the
# page falls back to `single`, so a half-finished config never ships broken.
# Either url can be a site path or an external link; a Google Drive link works.
cv_downloads:
  style: menu
  rows: labels # labels | notes | sizes . How each menu row reads (menu and split styles).
  captions: muted # muted | caps | boxed . How the words look (icons style only).
  short:
    url: "https://drive.google.com/file/d/1GiQo5uSdp-kXcbHb6Fi5XJ081OUrJDEv/view?usp=sharing" # the 1-page version. e.g. /assets/pdf/..._1pg.pdf or a Drive link
    label: 1 pager
    note: quick read # shown only when rows: notes
    size: "" # shown only when rows: sizes
  full:
    url: "https://drive.google.com/file/d/1JtO0wd2pwmw4YJ13o_wTLkvuiba63Z6k/view?usp=drive_link" # blank means: use the cv_pdf link above
    label: detailed
    note: ""
    size: ""
toc:
  sidebar: left
---
