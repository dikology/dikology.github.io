---
id: 1
type: basic
tags:
  - data-analytics
  - retention
---

**Front:** 
What does the slope of a retention curve tell you, and how can you analyze it using derivative analysis?

**Back:** 
The slope of a retention curve represents the *rate of change* in user retention over time. A steep negative slope indicates rapid user drop-off, while a flatter slope indicates better user retention.  
**Derivative analysis** involves calculating the first derivative of the curve, which quantifies the slope at each point in time.  
Here’s how to approach it:  
1. **Calculate the first derivative**: Use numerical methods or existing libraries (like NumPy's `np.gradient()`) to compute how the curve changes from one time point to the next.  
2. **Identify inflection points**: Look for where the derivative shifts from negative to zero or becomes less negative. This can signal periods where retention stabilizes.  
3. **Analyze time intervals**: Check if specific cohorts have sharper drop-offs early on or if there are moments of stabilization.  

By focusing on where and how the slope changes, you can better understand user behavior, identify "aha moments," and target interventions at specific points in the user journey.
