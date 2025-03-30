---
type: basic
id: 0222
tags: [sample_size, ab_testing]
---

**Front:** What is the formula for calculating sample size per group in an A/B test?

**Back:** The formula is:
\[ n = \left( \frac{Z*{\alpha} + Z*{\beta}}{\Delta} \right)^2 \times \sigma^2 \]
Where:

- \( Z\_{\alpha} \) is the Z critical value for the significance level (alpha).
- \( Z\_{\beta} \) is the Z critical value for the statistical power (1 - beta).
- \( \Delta \) is the minimum detectable effect (MDE).
- \( \sigma^2 \) is the variance of the point estimation.
