---
id: 0209
type: basic
title: Export Args
description: How to export args
tags:
  - tech
---

**Front:**
test

**Back:**
export $(grep -v '^#' .env | xargs)

[[Tech]]
