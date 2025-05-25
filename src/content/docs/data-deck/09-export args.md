---
id: 0209
type: basic
title: Export Args
description: How to export args
tags:
  - tech
created: March 30
modified: May 21
---

**Front:**
How to load environment variables from `.env` file

**Back:**
export $(grep -v '^#' .env | xargs)

[[Tech]]
