# ~/plotly_setup.py
import plotly.graph_objects as go
import plotly.io as pio
from IPython.display import HTML, display

display(HTML("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:ital,wght@0,400;0,700;1,400&display=swap');
</style>
"""))

# Define your theme
# 1. Define your custom theme colors and styles
theme_dark_1 = go.layout.Template(
    layout=go.Layout(
        # Font settings
        font=dict(
            family="JetBrains Mono, Monaco, Consolas, monospace",
            size=10,
            color="#E2E2E2"
        ),
        margin=dict(l=60, r=20, t=40, b=50),
        # Title adjustments
        title=dict(
            font=dict(size=12, color="#E2E2E2", weight="bold"),
            x=0.05, # Slightly inset from the left
        ),
        # Plot background and overall paper background
        paper_bgcolor="#121314",  # Light grey background
        plot_bgcolor="#181818",   # White plot area
        
        # Color palettes for data (Discrete and Continuous)
        colorway=["#9E9E9E", "#4A2AAA", "#0A6957", "#931629", "#3189B6"],
        colorscale=dict(
            sequential=[[0.0, "#EBF5FB"], [1.0, "#3E3E3E"]],
            diverging=[[0.0, "#740001"], [0.5, "#F8F9FA"], [1.0, "#1A5276"]]
        ),
        
        # Default Axis styling
        xaxis=dict(
            gridcolor="#4D4D4D",       # Subtle grid lines
            linecolor="#474747",       # Solid axis line
            showline=True,
            ticks="outside",
            tickcolor="#515151"
        ),
        yaxis=dict(
            gridcolor="#4D4D4D",
            linecolor="#474747",
            showline=True,
            ticks="outside",
            tickcolor="#515151",
            title_standoff=25
        ),
        
        # Legend positioning
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),

        hoverlabel=dict(
            bgcolor="#292929",              # Sleek dark background
            font_size=12,
            font_family="JetBrains Mono, monospace",
            font_color="#FFFFFF",           # High contrast white text
            bordercolor="#4B5563",          # Subtle border highlight
            align="left"
        ),
        hovermode="closest",
    )
)


theme_light_1 = go.layout.Template(
    layout=go.Layout(
        # Font settings - Darkened for readability on light backgrounds
        font=dict(
            family="JetBrains Mono, Monaco, Consolas, monospace",
            size=10,
            color="#1F2937"  # Deep charcoal
        ),
        # Updated margins to give the y-axis title more breathing room
        margin=dict(l=60, r=20, t=40, b=50),
        
        # Title adjustments
        title=dict(
            font=dict(size=12, color="#1F2937", weight="bold"),
            x=0.05,  # Slightly inset from the left
        ),
        
        # Plot background and overall paper background
        paper_bgcolor="#F9FAFB",  # Very light grey paper background
        plot_bgcolor="#FFFFFF",   # Pure white plot area
        
        # Color palettes for data (Discrete and Continuous)
        colorway=["#4A2AAA", "#0A6957", "#931629", "#3189B6", "#9E9E9E"],
        colorscale=dict(
            sequential=[[0.0, "#EBF5FB"], [1.0, "#1F2937"]],
            diverging=[[0.0, "#740001"], [0.5, "#F9FAFB"], [1.0, "#1A5276"]]
        ),
        
        # Default Axis styling
        xaxis=dict(
            gridcolor="#E5E7EB",       # Soft light grey grid lines
            linecolor="#9CA3AF",       # Medium grey solid axis line
            showline=True,
            ticks="outside",
            tickcolor="#9CA3AF"
        ),
        yaxis=dict(
            gridcolor="#E5E7EB",       # Soft light grey grid lines
            linecolor="#9CA3AF",       # Medium grey solid axis line
            showline=True,
            ticks="outside",
            tickcolor="#9CA3AF",
            # Added standoff distance between the tick labels and the axis title
            title_standoff=25
        ),
        
        # Legend positioning
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),

        # Hover label styled for clean pop on a light theme
        hoverlabel=dict(
            bgcolor="#FFFFFF",              # Crisp white background
            font_size=12,
            font_family="JetBrains Mono, monospace",
            font_color="#1F2937",           # Dark text
            bordercolor="#D1D5DB",          # Light grey border
            align="left"
        ),
        hovermode="closest",
    )
)

# 2. Register the template with Plotly
pio.templates["theme_dark_1"] = theme_dark_1
pio.templates["theme_light_1"] = theme_light_1


def show_available_templates():
    print("Available plotly templates:")
    for template in pio.templates:
        print(f"  -  {template}")