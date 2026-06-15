import uuid
from tqdm.notebook import tqdm
from IPython.display import display, HTML

class ProgressBar:
    def __init__(self, iterable=None, total=None, desc="Loading", bar_color=None, bg_color=None, font_color=None, font_family="sans-serif"):
        """
        Base progress bar class that handles tqdm logic and injects 
        advanced CSS targeting parent wrappers to eliminate outer white spaces.
        """
        if iterable is None and total is not None:
            iterable = range(total)
            
        self.pbar = tqdm(iterable, total=total, desc=desc, colour=bar_color)
        
        # Explicitly force the widget layout to take maximum width
        self.pbar.container.layout.width = '100%'
        
        # Generate a unique CSS class name for this progress bar instance
        self.uid = f"tqdm-style-{uuid.uuid4().hex[:8]}"
        self.pbar.container.add_class(self.uid)
        
        css_rules = []
        
        if bg_color:
            # 1. Target the Jupyter/VS Code outer output area containing this specific widget
            # Stripping its padding and matching its background fixes the white gap.
            css_rules.append(f"""
                .cell-output-wrapper:has(.{self.uid}),
                .output_subarea:has(.{self.uid}),
                .jp-OutputArea-output:has(.{self.uid}),
                div:has(> .{self.uid}) {{
                    background-color: {bg_color} !important;
                    background: {bg_color} !important;
                    padding: 0 !important;
                }}
                
                # 2. Style our widget container to fit flush edge-to-edge
                .{self.uid} {{
                    width: 100% !important;
                    background-color: {bg_color} !important;
                    background: {bg_color} !important;
                    padding: 14px 18px !important;
                    border-radius: 8px !important;
                    border: none !important;
                    margin: 0 !important;
                    box-sizing: border-box !important;
                }}
                
                # 3. Fix the unfilled progress track background color
                .{self.uid} progress,
                .{self.uid} .progress,
                .{self.uid} .widget-progress {{
                    background-color: #3a414c !important;
                    background: #3a414c !important;
                    border: none !important;
                    border-radius: 4px !important;
                }}
                .{self.uid} progress::-webkit-progress-bar {{
                    background-color: #3a414c !important;
                    border-radius: 4px !important;
                }}
            """)
            
        if bar_color:
            css_rules.append(f"""
                .{self.uid} progress::-webkit-progress-value {{
                    background-color: {bar_color} !important;
                }}
                .{self.uid} progress::-moz-progress-bar {{
                    background-color: {bar_color} !important;
                }}
            """)
            
        if font_color or font_family:
            font_style = f"font-family: {font_family} !important;" if font_family else ""
            color_style = f"color: {font_color} !important;" if font_color else ""
            
            css_rules.append(f"""
                .{self.uid} div, .{self.uid} span, .{self.uid} p, .{self.uid} .widget-html {{
                    {font_style}
                    {color_style}
                }}
            """)
            
        if css_rules:
            display(HTML(f"<style>{''.join(css_rules)}</style>"))

    def __iter__(self):
        return self.pbar.__iter__()

    def update(self, n=1):
        self.pbar.update(n)

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pbar.close()


class ProgressBarDark(ProgressBar):
    def __init__(self, iterable=None, total=None, desc="Processing (Dark)"):
        """
        A specialized Progress Bar tailored for Dark UI themes.
        """
        super().__init__(
            iterable=iterable,
            total=total,
            desc=desc,
            bar_color="#8b00b5",                 # Deep purple filled bar
            bg_color="#121314",                  # Sleek dark charcoal background
            font_color="#eeeeee",                # Readable off-white text
            font_family="'JetBrains Mono', monospace"
        )