---
layout: ../../layouts/MarkdownPostLayout.astro
title: Anki cards about retention
description: Setting up a structure for some Anki cards
date: 2024-12-09
image:
  src: https://cdn.midjourney.com/f1f1d54a-8740-4594-a9bb-a1c9f4c49478/0_0.png
  alt: Anki cards about retention
featured: false
draft: true
category: tech
---

I've decided to write this as a separate article to be able to chat about bits of it with ChatGPT.
If I start with ipynb, those pieces would be hard to copypaste here and there. Let there be a place to hold the whole picture.

## The project

I want to make one or several Anki cards about retention. This will test the flow of [[Automating Anki Deck Generation and Updates with GitHub Actions & GitHub Releases]]. I don't want this to be "what is retention" type of cards, so I decided to use concepts that I found recently. It's analysing the slope of retention curve with some points of interest.
The card should also have a good visual — a graph of retention. Perfect if with good data visualisation techniques, but it's fine for MVP to put what I already can create.
I have an access to a real database, so I'll use ipynb file to get data and create a plotly graph. While on it, I need to consider storing variables and other stuff.

## ipynb

We'll start by recreating an ipynb file from my work project, but adapting it to needs of this project. Later, we can thin about how to [[convert ipynb for astro]], with the layout for it.

### managing dependencies with poetry and running ipynb in VSCode

I chose poetry for managing dependencies in this project, and I was afraid that VSCode won't be able to pick that up. But it seems this part will have no problems:
![[Pasted image 20241209213845.png]]

### creating a database connection

I am using this sqlalchemy code in ipynb file to create a database connection:

```python
engine_dws = create_engine("postgresql://{}:{}@{}:{}/dws".format(
	os.environ.get("DWS_USER"),
	os.environ.get("DWS_PWD"),
	os.environ.get("DWS_HOST"),
	os.environ.get("DWS_PORT")
))
```

I store these variables in `.env` file.

## points of interest

Finding the **bend point** (inflection point) in a retention curve can help identify the moment when the rate of user activation or retention stabilizes or drastically changes. This is crucial for identifying the **"aha moment"**—the point by which users should ideally be activated to maximize retention.

### Steps to Identify the Bend Point:

---

#### **1. First Derivative Analysis (Rate of Change)**

The **first derivative** (or slope) of the retention curve shows how retention is changing over time. A significant drop in the slope indicates a bend point.

- **Method**: Calculate the rate of change of retention over time:
  ```python
  filtered_data['slope'] = filtered_data['retention_rate'].diff() / filtered_data['days_since_cohort'].diff()
  ```
- **Identify the Bend Point**: Find where the slope reaches its **lowest value** or stabilizes:
  ```python
  bend_point = filtered_data.loc[filtered_data['slope'].idxmin()]
  print(f"Bend Point: {bend_point['days_since_cohort']} days")
  ```

---

#### **2. Second Derivative Analysis (Acceleration/Deceleration)**

The **second derivative** measures the rate of change of the slope. The inflection point occurs where the second derivative equals zero, meaning the curve transitions from steep to flat.

- **Method**: Calculate the second derivative:
  ```python
  filtered_data['curvature'] = filtered_data['slope'].diff()
  ```
- **Find the Inflection Point**: Locate where `curvature` approaches 0:
  ```python
  inflection_point = filtered_data.loc[(filtered_data['curvature'] > -0.01) & (filtered_data['curvature'] < 0.01)].iloc[0]
  print(f"Inflection Point: {inflection_point['days_since_cohort']} days")
  ```

---

#### **3. Find the Retention Plateau**

After the bend point, retention typically stabilizes, forming a plateau. Look for the point where the retention rate decreases minimally (e.g., < 1% change over several days).

- **Method**: Identify when retention stabilizes:
  ```python
  plateau_point = filtered_data.query("retention_rate.diff().abs() < 1").iloc[0]
  print(f"Plateau Point: {plateau_point['days_since_cohort']} days")
  ```

---

#### **4. Visualize the Bend Point**

Overlay the bend point and inflection point on your retention curve for clarity:

```python
fig.add_trace(
    go.Scatter(
        x=[bend_point['days_since_cohort']],
        y=[bend_point['retention_rate']],
        mode='markers+text',
        marker=dict(size=10, color='red'),
        text=['Bend Point'],
        textposition='top center',
        name='Bend Point'
    )
)

fig.add_trace(
    go.Scatter(
        x=[inflection_point['days_since_cohort']],
        y=[inflection_point['retention_rate']],
        mode='markers+text',
        marker=dict(size=10, color='blue'),
        text=['Inflection Point'],
        textposition='top center',
        name='Inflection Point'
    )
)

fig.show()
```

---

### 5. Interpret the Bend Point

Once you have the bend point:

- **If the bend occurs early (e.g., Day 1-7)**:
  - Focus on improving onboarding and first-use experience.
  - Reinforce the "aha moment" that retains users early.
- **If the bend occurs later (e.g., Day 15-30)**:
  - Ensure sustained engagement through reminders, follow-ups, and feature discovery.
  - Identify features or actions users perform before this point.

---

### Final Thoughts:

The bend point typically aligns with when a user transitions from **trying out the product** to becoming a **habitual user**. Use this analysis to design experiments aimed at driving engagement earlier and pushing users toward their "aha moment." 🚀 Let me know if you'd like to automate this further!

## Here's what I stopped at now:

```python
# Create Plotly line plot
fig = go.Figure()

# **1. Retention Curve**
fig.add_trace(
    go.Scatter(
        x=filtered_data['days_since_cohort'],
        y=filtered_data['retention_rate'],
        mode='lines+markers',
        name='Average Retention Rate',
        line=dict(color='royalblue', width=3),  # Thicker line, clear focus
        marker=dict(size=6, color='royalblue')  # Consistent color for markers
    )
)

# **2. Inflection Point**
fig.add_trace(
    go.Scatter(
        x=[inflection_point['days_since_cohort']],
        y=[inflection_point['retention_rate']],
        mode='markers+text',
        marker=dict(size=12, color='blue', symbol='circle'),
        text=['Inflection Point'],
        textposition='top center',
        name='Inflection Point'
    )
)

# **3. Bend Point**
fig.add_trace(
    go.Scatter(
        x=[bend_point['days_since_cohort']],
        y=[bend_point['retention_rate']],
        mode='markers+text',
        marker=dict(size=12, color='red', symbol='x'),
        text=['Bend Point'],
        textposition='top center',
        name='Bend Point'
    )
)

# **4. Critical Vertical Line (Day 7)**
fig.add_vline(
    x=7,
    line_width=2,
    line_dash="dash",
    line_color="crimson",
    annotation_text="Day 7: Critical point",  # Shortened for clarity
    annotation_position="top right",
    annotation_font=dict(size=12, color="crimson")  # Consistent with the line color
)

# **5. Layout Customization**
fig.update_layout(
    title=dict(
        text='Retention Curve: Early Drop Followed by Stability After Day 7',
        font=dict(size=20, color='black')
    ),
    xaxis_title='Days Since Cohort Start',
    yaxis_title='Retention Rate (%)',
    xaxis=dict(
        range=[0, 100],  # Set x-axis range
        showgrid=False,  # No x-axis gridlines (less clutter)
        tickmode='linear',
        dtick=5,  # Tick every 10 days instead of every 1
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        range=[0, 100],  # Set y-axis range
        showgrid=True,
        gridcolor="LightGray",
        tickmode='linear',
        dtick=10,  # Tick every 10 days instead of every 1
        tickfont=dict(size=12)
    ),
    template='plotly_white',
    margin=dict(l=50, r=50, t=50, b=50),  # Compact margins
    showlegend=True,
    legend=dict(
        orientation="h",  # Horizontal legend at the bottom
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5
    )
)

# **6. Line and Marker Colors (Gradient)**
colors = np.linspace(0, 1, len(filtered_data))  # Gradient
fig.update_traces(
    selector=dict(mode='lines+markers'),
    marker=dict(
        color=colors,
        colorscale='Blues',  # Sequential color scale
        showscale=False
    )
)

# **7. Improved Hover Tooltips**
fig.update_traces(
    hovertemplate="Day %{x}: %{y:.2f}% retention<extra></extra>"
)

# Show the figure
fig.show(renderer='notebook')
```
