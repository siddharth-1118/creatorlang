#!/usr/bin/env python3
"""CreatorLang Compiler v2 - Parse Doraemon syntax and render shapes"""

import re
import sys
import os
from PIL import Image, ImageDraw, ImageFont
import json

class CreatorLangCompiler:
    def __init__(self, source_file):
        self.source_file = source_file
        self.output_dir = "output"
        self.video_config = {}
        self.shapes = []
        self.groups = []
        
    def parse(self):
        """Parse the .create file with Doraemon syntax"""
        with open(self.source_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove comments
        content = re.sub(r'#.*$', '', content, flags=re.MULTILINE)
        
        # Extract video configuration
        video_match = re.search(r'video\s+"([^"]+)":', content)
        if video_match:
            self.video_config['name'] = video_match.group(1)
        
        # Extract basic video properties
        duration_match = re.search(r'duration\s+(\d+)\s+seconds', content)
        if duration_match:
            self.video_config['duration'] = int(duration_match.group(1))
        
        size_match = re.search(r'size\s+(\d+)x(\d+)', content)
        if size_match:
            self.video_config['width'] = int(size_match.group(1))
            self.video_config['height'] = int(size_match.group(2))
        else:
            self.video_config['width'] = 1920
            self.video_config['height'] = 1080
        
        # Extract background
        bg_match = re.search(r'background\s+gradient\(([^)]+)\)', content)
        if bg_match:
            colors = bg_match.group(1).split(',')
            self.video_config['background'] = [c.strip() for c in colors]
        
        # Parse shapes (circle, ellipse, rectangle, line)
        self._parse_shapes(content)
        
        print(f"Parsed {len(self.shapes)} shapes from {self.source_file}")
    
    def _parse_shapes(self, content):
        """Extract all shapes from content"""
        # Parse circles
        circle_pattern = r'circle\s+"([^"]+)":\s*position\s*\(([^)]+)\)\s*radius\s+(\d+)\s*color\s+([#\w]+)'
        for match in re.finditer(circle_pattern, content, re.DOTALL):
            name = match.group(1)
            pos = match.group(2).split(',')
            x, y = int(pos[0].strip()), int(pos[1].strip())
            radius = int(match.group(3))
            color = match.group(4).strip()
            self.shapes.append({
                'type': 'circle',
                'name': name,
                'x': x,
                'y': y,
                'radius': radius,
                'color': color
            })
        
        # Parse ellipses
        ellipse_pattern = r'ellipse\s+"([^"]+)":\s*position\s*\(([^)]+)\)\s*size\s*\(([^)]+)\)\s*color\s+([#\w]+)'
        for match in re.finditer(ellipse_pattern, content, re.DOTALL):
            name = match.group(1)
            pos = match.group(2).split(',')
            x, y = int(pos[0].strip()), int(pos[1].strip())
            size = match.group(3).split(',')
            width, height = int(size[0].strip()), int(size[1].strip())
            color = match.group(4).strip()
            self.shapes.append({
                'type': 'ellipse',
                'name': name,
                'x': x,
                'y': y,
                'width': width,
                'height': height,
                'color': color
            })
    
    def _parse_color(self, color_str):
        """Convert color string to RGB tuple"""
        color_map = {
            'white': '#FFFFFF',
            'black': '#000000',
            'red': '#FF0000',
            'blue': '#0000FF',
        }
        
        color = color_map.get(color_str.lower(), color_str)
        
        if color.startswith('#'):
            color = color.lstrip('#')
            if len(color) == 6:
                return tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        
        return (255, 255, 255)  # Default white
    
    def compile(self):
        """Compile to visual output with actual rendering"""
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Create image with background
        width = self.video_config.get('width', 1920)
        height = self.video_config.get('height', 1080)
        
        # Create gradient background
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)
        
        # Simple gradient (top to bottom)
        if 'background' in self.video_config and len(self.video_config['background']) >= 2:
            start_color = self._parse_color(self.video_config['background'][0])
            end_color = self._parse_color(self.video_config['background'][1])
            
            for y in range(height):
                ratio = y / height
                r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
                g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
                b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
                draw.line([(0, y), (width, y)], fill=(r, g, b))
        else:
            draw.rectangle([0, 0, width, height], fill=(135, 206, 235))  # Sky blue
        
        # Draw all shapes
        for shape in self.shapes:
            if shape['type'] == 'circle':
                x, y = shape['x'], shape['y']
                r = shape['radius']
                color = self._parse_color(shape['color'])
                draw.ellipse([x-r, y-r, x+r, y+r], fill=color)
            
            elif shape['type'] == 'ellipse':
                x, y = shape['x'], shape['y']
                w, h = shape['width']//2, shape['height']//2
                color = self._parse_color(shape['color'])
                draw.ellipse([x-w, y-h, x+w, y+h], fill=color)
        
        # Save output
        output_path = os.path.join(self.output_dir, 'doraemon_frame.png')
        img.save(output_path)
        print(f"✓ Rendered image to {output_path}")
        
        # Save JSON data
        json_path = os.path.join(self.output_dir, 'output.json')
        with open(json_path, 'w') as f:
            json.dump({
                'video_config': self.video_config,
                'shapes': self.shapes,
                'total_shapes': len(self.shapes)
            }, f, indent=2)
        print(f"✓ Saved structure to {json_path}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python compiler.py <file.create>")
        sys.exit(1)
    
    source_file = sys.argv[1]
    if not os.path.exists(source_file):
        print(f"Error: File '{source_file}' not found")
        sys.exit(1)
    
    compiler = CreatorLangCompiler(source_file)
    print(f"Compiling {source_file}...")
    compiler.parse()
    compiler.compile()
    print("✓ Compilation complete!")

if __name__ == "__main__":
    main()
