---
layout: ../../layouts/MarkdownPostLayout.astro
title: Turning a Metabase Dashboard into a Figma Prototyping Tool
description: Figma, with its flexible design tools, seemed like the perfect platform to build a dashboard prototyping tool. I envisioned a library of components, complete with filters, charts, and grids, all ready to be adapted for any data story.
date: 2025-01-01
image:
  src: https://cdn.midjourney.com/bff41755-cc0d-4a63-948e-09b0a7708cb6/0_0.png
  alt: Metabase Dashboard
featured: false
draft: true
category: tech
---
## The Problem

It all started with a challenge: how to align on dashboard definitions with stakeholders before jumping into Metabase, ensuring everyone agrees on the desired outcome. As a data analyst myself, I was working with Metabase dashboards daily. I thought, “What if I could replicate these dashboards in a way that anyone could prototype them quickly?” That’s when I turned to Figma.

Figma, with its flexible design tools, seemed like the perfect platform to build a dashboard prototyping tool. I envisioned a library of components, complete with filters, charts, and grids, all ready to be adapted for any data story.

## Reverse-Engineering the Metabase Dashboard

The first step was to analyze the Metabase dashboard I used daily. I broke it down into its core elements:

1. **Filters**: Dropdowns, date pickers, and multi-selects.
2. **Charts**: Line graphs, bar charts, stacked bar charts, and pie charts.
3. **Sections and Headings**: Clearly separated areas with consistent typography.
4. **Grids**: A layout system to keep everything organized.

To speed things up, I used a browser extension to convert the HTML of existing dashboards into Figma designs. While this required some cleanup—removing unnecessary divs and aligning elements—it was still much faster than recreating components from scratch. Afterward, I refined each piece, focusing on modularity and adaptability.

## Building the Components

### Filters

Filters are essential in dashboards, so I began by designing dropdown menus, date pickers, etc. Using Figma’s **Auto Layout** feature, I ensured they could resize dynamically while maintaining proper alignment. I also created variants, leveraging **Component Properties** to make filters more flexible, allowing for quick adjustments to size, text, or type based on project needs.

### Charts

Next came the charts. I wanted them to be as realistic as possible while staying editable.

### Typography and Headings

Metabase dashboards rely on clear headings and labels. I set up text styles in Figma to match the fonts and sizes commonly used in dashboards. This made it easy to maintain consistency across designs.

### The Grid System

To replicate the structured layout of Metabase, I set up a **grid system** in Figma. I used a 12-column grid with equal gutters, ensuring flexibility for various chart and filter placements.

## Packaging the Tool

With all the components ready, I grouped them into a library in Figma. Each component was labeled clearly, and I added usage notes for anyone unfamiliar with the tool. The library included:

- Filters (with variants)
- Charts
- Text styles for headings and labels
- Layout grids and containers

This library was then shared as a team project, making it easy for others to copy and customize.

## Real-World Application

The first time I used this prototyping tool, it was for a dashboard project. I mocked up the design in Figma in just 30 minutes. Stakeholders could see the proposed layout and provide feedback before any development began.

What’s more, this tool became a go-to resource for other analysts on my team. They could now prototype dashboards without needing advanced design skills.

## Lessons Learned

Creating this tool taught me a few valuable lessons:

1. **Modularity is Key**: Breaking down a dashboard into reusable components makes prototyping faster and more consistent.
2. **Collaboration Matters**: Sharing the library with the team opened up opportunities for feedback and improvement.
3. **Iterate and Improve**: The first version of the tool wasn’t perfect. Over time, I added new components and refined existing ones based on team needs.

## How You Can Do It Too

If you’re inspired to create your own dashboard prototyping tool, here’s a quick guide:

1. Analyze your existing dashboards and identify common elements.
2. Recreate those elements in Figma, focusing on flexibility and reusability.
3. Use Auto Layout and variants to make components dynamic.
4. Set up a grid system to organize your layouts.
5. Package everything into a library and share it with your team.

Whether you’re working with Metabase, Tableau, or any other BI tool, this approach can save you time and make your dashboard design process more collaborative and creative.

---

Designing dashboards doesn’t have to be daunting. With a little effort upfront, you can build tools that empower your team and make your data stories shine. Happy prototyping!

[[Work]]
