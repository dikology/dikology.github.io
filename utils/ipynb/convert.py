import nbformat
import os
import glob


def convert_notebook_to_astro(notebook_path, output_dir=None, charts_dir=None, iframe_height=800):
    """
    Convert a Jupyter notebook to Astro-compatible Markdown with iframes for charts.
    
    Args:
        notebook_path (str): Path to the .ipynb file
        output_dir (str, optional): Directory to save the output file.
        charts_dir (str, optional): Base directory for charts in final URL.
        iframe_height (int): Height in pixels for the iframe elements.
    
    Returns:
        str: Path to the created markdown file
    """
    # Read the notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, as_version=4)
    
    # Get the notebook name without extension for output filename
    notebook_name = os.path.basename(notebook_path).split('.')[0]
    
    # Set output directory
    if output_dir is None:
        output_dir = os.path.dirname(notebook_path)
    
    # Set charts directory path for URLs
    if charts_dir is None:
        charts_dir = f"/charts/{notebook_name}"
    
    # Look for charts in the public directory
    public_charts_dir = os.path.join('public', charts_dir.lstrip('/'))
    
    # Check if the charts directory exists
    if not os.path.exists(public_charts_dir):
        print(f"Warning: Chart directory {public_charts_dir} not found.")
        print(f"Using empty chart list. Charts will need to be placed in {public_charts_dir}")
        chart_files = []
    else:
        # Find all HTML chart files in the public directory
        chart_files = sorted(glob.glob(os.path.join(public_charts_dir, 
                                                "chart_*.html")))
        print(f"Found {len(chart_files)} chart files in {public_charts_dir}")
    
    # Chart counter for automatic insertion
    chart_index = 0
    total_charts = len(chart_files)
    
    # Initialize markdown content with front matter
    md_content = f"""---
title: {notebook_name.replace('-', ' ').title()}
description: Converted from Jupyter notebook
layout: ../../../layouts/NotebookLayout.astro
---

"""
    
    # Store markdown cells and chart insertion points
    markdown_cells = []
    chart_indicators = [
        'create_plot', 'create_device_plot', 'create_time_series_plot', 
        'create_heatmap', 'show_spread', 'show_time_series', 'display_pivot',
        'show_time_series_amount', 'show_time_series_corrected', 'show_heatmap',
        'fig = px', '.plot(', 'plt.', 'fig.show(', 'fig.update_layout'
    ]
    
    # First pass: Extract all markdown cells
    for cell in notebook.cells:
        if cell.cell_type == 'markdown':
            markdown_cells.append(cell.source)
    
    # Connect markdown content
    connected_markdown = "\n\n".join(markdown_cells)
    
    # Second pass: Process cells in order and insert charts at appropriate places
    markdown_index = 0
    chart_sections = []
    
    for cell in notebook.cells:
        # Process markdown cells
        if cell.cell_type == 'markdown':
            chart_sections.append({"type": "markdown", "content": cell.source})
            markdown_index += 1
            
        # Process code cells for chart detection
        elif cell.cell_type == 'code' and chart_index < total_charts:
            # Check if this cell generates a chart
            is_chart_cell = any(indicator in cell.source for indicator in chart_indicators)
            
            if is_chart_cell:
                # Get chart file basename
                chart_basename = os.path.basename(chart_files[chart_index])
                # Use chart path for URL
                chart_path = f"{charts_dir}/{chart_basename}"
                
                # Create iframe HTML
                iframe_html = f"""
<div class="chart-container">
    <iframe src="{chart_path}" width="100%" height="{iframe_height}px" 
            frameborder="0"></iframe>
</div>
"""
                chart_sections.append({"type": "chart", "content": iframe_html})
                chart_index += 1
    
    # Build final markdown by interleaving markdown cells and charts
    for section in chart_sections:
        md_content += section["content"] + "\n\n"
    
    # Create output file path
    output_file = os.path.join(output_dir, f"{notebook_name}.md")
    
    # Write the markdown file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"Generated markdown file with {chart_index} chart references")
    return output_file


def convert_all_notebooks(notebooks_dir, output_dir=None, charts_dir=None, iframe_height=800):
    """
    Convert all notebooks in a directory to Astro-compatible markdown files.
    
    Args:
        notebooks_dir (str): Directory containing .ipynb files
        output_dir (str): Directory to save output files
        charts_dir (str): Base directory for chart URLs
        iframe_height (int): Height in pixels for the iframe elements
    
    Returns:
        list: Paths to created markdown files
    """
    if output_dir is None:
        output_dir = notebooks_dir
        
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Find all notebook files
    notebook_files = glob.glob(os.path.join(notebooks_dir, "*.ipynb"))
    
    # Convert each notebook
    converted_files = []
    for notebook_path in notebook_files:
        try:
            output_file = convert_notebook_to_astro(
                notebook_path, 
                output_dir, 
                charts_dir, 
                iframe_height
            )
            converted_files.append(output_file)
            print(f"Converted {notebook_path} to {output_file}")
        except Exception as e:
            print(f"Error converting {notebook_path}: {str(e)}")
    
    return converted_files


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Convert Jupyter notebooks to Astro-compatible markdown")
    parser.add_argument("--input", "-i", 
                    help="Input notebook file or directory", required=True)
    parser.add_argument("--output", "-o", help="Output directory (optional)")
    parser.add_argument("--charts", "-c", 
                    help="Base directory for chart URLs (default: /charts)")
    parser.add_argument("--height", "-t", type=int, default=800,
                    help="Height in pixels for chart iframes (default: 800)")
    
    args = parser.parse_args()
    
    if os.path.isdir(args.input):
        convert_all_notebooks(args.input, args.output, args.charts, args.height)
    else:
        convert_notebook_to_astro(args.input, args.output, args.charts, args.height) 