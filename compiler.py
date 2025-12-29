#!/usr/bin/env python3
"""CreatorLang Compiler v3 - Fixed line-by-line parser"""

import re
import sys
import os
from PIL import Image, ImageDraw
import json

class CreatorLangCompiler:
    def __init__(self, source_file):
        self.source_file = source_file
        self.output_dir = "output"
        self.video_config = {}
        self.shapes = []
        
    def parse(self):
        """Parse using line-by-line approach"""
        with open(self.source_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            
            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue
            
            # Parse video config
            if line.startswith('video'):
                match = re.search(r'"([^"]+)"', line)
                if match:
                    self.video_config['name'] = match.group(1)
            
            elif line.startswith('size'):
                match = re.search(r'(\d+)x(\d+)', line)
                if match:
                    self.video_config['width'] = int(match.group(1))
                    self.video_config['height'] = int(match.group(2))
            
            elif line.startswith('background gradient'):
                match = re.search(r'gradient\(([^)]+)\)', line)
                if match:
                    colors = [c.strip() for c in match.group(1).split(',')]
                    self.video_config['background'] = colors
            
            # Parse circles: circle "name": position (x, y) radius R color COLOR
            elif line.startswith('circle'):
                parts = line.split()
                try:
                    name = parts[1].strip('":')  
                    pos_idx = parts.index('position')
                    x = int(parts[pos_idx + 1].strip('(,'))
                    y = int(parts[pos_idx + 2].strip('),'))
                    radius_idx = parts.index('radius')
                    radius = int(parts[radius_idx + 1])
                    color_idx = parts.index('color')
                    color = parts[color_idx + 1] if color_idx + 1 < len(parts) else 'white'
                    
                    self.shapes.append({
                        'type': 'circle',
                        'name': name,
                        'x': x,
                        'y': y,
                        'radius': radius,
                        'color': color
                    })
                except (ValueError, IndexError) as e:
                    print(f"Warning: Could not parse circle line: {line}")
            
            # Parse ellipses: ellipse "name": position (x, y) size (w, h) color COLOR
            elif line.startswith('ellipse'):
                parts = line.split()
                try:
                    name = parts[1].strip('":')  
                    pos_idx = parts.index('position')
                    x = int(parts[pos_idx + 1].strip('(,'))
                    y = int(parts[pos_idx + 2].strip('),'))
                    size_idx = parts.index('size')
                    width = int(parts[size_idx + 1].strip('(,'))
                    height = int(parts[size_idx + 2].strip('),'))
                    color_idx = parts.index('color')
                    color = parts[color_idx + 1] if color_idx + 1 < len(parts) else 'white'
                    
                    self.shapes.append({
                        'type': 'ellipse',
                        'name': name,
                        'x': x,
                        'y': y,
                        'width': width,
                        'height': height,
                        'color': color
                    })
                except (ValueError, IndexError) as e:
                    print(f"Warning: Could not parse ellipse line: {line}")
        
        # Set defaults if not specified
        if 'width' not in self.video_config:
            self.video_config['width'] = 800
        if 'height' not in self.video_config:
            self.video_config['height'] = 600
        
        print(f"Parsed {len(self.shapes)} shapes from {self.source_file}")
    
    def _parse_color(self, color_str):
        """Convert color string to RGB tuple"""
        color_map = {
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            'red': (255, 0, 0),
            'blue': (0, 0, 255),
        }
        
        if color_str.lower() in color_map:
            return color_map[color_str.lower()]
        
        # Parse hex color
        if color_str.startswith('#'):
            color = color_str.lstrip('#')
            if len(color) == 6:
                return tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        
        return (255, 255, 255)  # Default white
    
    def compile(self):
        """Compile and render shapes"""
        os.makedirs(self.output_dir, exist_ok=True)
        
        width = self.video_config['width']
        height = self.video_config['height']
        
        # Create image with gradient background
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)
        
        # Draw gradient background
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
            color = self._parse_color(shape['color'])
            
            if shape['type'] == 'circle':
                x, y, r = shape['x'], shape['y'], shape['radius']
                draw.ellipse([x-r, y-r, x+r, y+r], fill=color)
            
            elif shape['type'] == 'ellipse':
                x, y = shape['x'], shape['y']
                w, h = shape['width']//2, shape['height']//2
                draw.ellipse([x-w, y-h, x+w, y+h], fill=color)
        
        # Save output
        output_path = os.path.join(self.output_dir, 'doraemon_frame.png')
        img.save(output_path)
        print(f"✓ Rendered image to {output_path}")
        
        # Save JSON
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
