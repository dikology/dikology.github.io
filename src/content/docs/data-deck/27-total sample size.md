---
type: basic
id: 0227
title: Total Sample Size
description: How do you calculate the total sample size for an A/B test with two groups?
tags:
  - ab-testing
created: January 03
modified: May 03
---
**Front:** How do you calculate the total sample size for an A/B test with two groups?

**Back:** First, calculate the sample size per group using the formula:
\[ n = \left( \frac{Z*{\alpha} + Z*{\beta}}{\Delta} \right)^2 \times \sigma^2 \]
Then, multiply the result by 2 to get the total sample size for both the control and treatment groups.

---
[[Data Analytics]]