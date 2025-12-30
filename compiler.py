#!/usr/bin/env python3
"""CreatorLang Compiler v4 - Multi-line Animation Parser"""

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
        self.current_shape = None
        self.current_indent = 0
        
    def parse(self):
        """Parse CreatorLang file with multi-line support"""
        with open(self.source_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        i = 0
        while i < len(lines):
            line = lines[i]
            original_line = line
            line = line.rstrip()
            
            # Skip comments and empty lines
            if not line.strip() or line.strip().startswith('#'):
                i += 1
                continue
            
            # Get indentation level
            indent = len(line) - len(line.lstrip())
            line = line.strip()
            
            # Parse video config
            if line.startswith('video '):
                match = re.search(r'"([^"]+)"', line)
                if match:
                    self.video_config['name'] = match.group(1)
            
            elif line.startswith('size '):
                match = re.search(r'(\d+)x(\d+)', line)
                if match:
                    self.video_config['width'] = int(match.group(1))
                    self.video_config['height'] = int(match.group(2))
            
            elif line.startswith('background gradient'):
                match = re.search(r'gradient\(([^)]+)\)', line)
                if match:
                    colors = [c.strip() for c in match.group(1).split(',')]
                    self.video_config['background'] = colors
            
            # Parse shape declarations (colon at end indicates multi-line)
            elif line.startswith(('circle ', 'ellipse ', 'rectangle ', 'line ')):
                if line.endswith(':'):
                    # Multi-line format: collect properties from following lines
                    shape_type = line.split()[0]
                    name_match = re.search(r'"([^"]+)"', line)
                    if name_match:
                        shape_name = name_match.group(1)
                        shape_data = {'type': shape_type, 'name': shape_name}
                        
                        # Read properties from indented lines
                        i += 1
                        while i < len(lines):
                            next_line = lines[i].rstrip()
                            if not next_line.strip() or next_line.strip().startswith('#'):
                                i += 1
                                continue
                            
                            next_indent = len(next_line) - len(next_line.lstrip())
                            if next_indent <= indent:
                                i -= 1  # Back up one line
                                break
                            
                            prop_line = next_line.strip()
                            self._parse_property(prop_line, shape_data)
                            i += 1
                        
                        self._finalize_shape(shape_data)
                else:
                    # Single-line format (legacy support)
                    self._parse_single_line_shape(line)
            
            i += 1
        
        # Set defaults
        if 'width' not in self.video_config:
            self.video_config['width'] = 1920
        if 'height' not in self.video_config:
            self.video_config['height'] = 1080
        
        print(f"✓ Parsed {len(self.shapes)} shapes from {self.source_file}")
    
    def _parse_property(self, line, shape_data):
        """Parse individual property lines"""
        if line.startswith('position '):
            match = re.search(r'\((-?\d+),\s*(-?\d+)\)', line)
            if match:
                shape_data['x'] = int(match.group(1))
                shape_data['y'] = int(match.group(2))
        
        elif line.startswith('radius '):
            match = re.search(r'radius\s+(\d+)', line)
            if match:
                shape_data['radius'] = int(match.group(1))
        
        elif line.startswith('size '):
            match = re.search(r'\((\d+),\s*(\d+)\)', line)
            if match:
                shape_data['width'] = int(match.group(1))
                shape_data['height'] = int(match.group(2))
        
        elif line.startswith('color '):
            color = line.split('color ', 1)[1].strip()
            shape_data['color'] = color
        
        elif line.startswith('from '):
            match = re.search(r'from\s+\((-?\d+),\s*(-?\d+)\)\s+to\s+\((-?\d+),\s*(-?\d+)\)', line)
            if match:
                shape_data['x1'] = int(match.group(1))
                shape_data['y1'] = int(match.group(2))
                shape_data['x2'] = int(match.group(3))
                shape_data['y2'] = int(match.group(4))
    
    def _finalize_shape(self, shape_data):
        """Add completed shape to shapes list"""
        if shape_data['type'] in ['circle', 'ellipse', 'rectangle', 'line']:
            self.shapes.append(shape_data)
    
    def _parse_single_line_shape(self, line):
        """Parse legacy single-line shape format"""
        parts = line.split()
        try:
            shape_type = parts[0]
            name = parts[1].strip('":')
            
            if shape_type == 'circle':
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
            
            elif shape_type in ['ellipse', 'rectangle']:
                pos_idx = parts.index('position')
                x = int(parts[pos_idx + 1].strip('(,'))
                y = int(parts[pos_idx + 2].strip('),'))
                size_idx = parts.index('size')
                width = int(parts[size_idx + 1].strip('(,'))
                height = int(parts[size_idx + 2].strip('),'))
                color_idx = parts.index('color')
                color = parts[color_idx + 1] if color_idx + 1 < len(parts) else 'white'
                
                self.shapes.append({
                    'type': shape_type,
                    'name': name,
                    'x': x,
                    'y': y,
                    'width': width,
                    'height': height,
                    'color': color
                })
            
            elif shape_type == 'line':
                from_idx = parts.index('from')
                x1 = int(parts[from_idx + 1].strip('(,'))
                y1 = int(parts[from_idx + 2].strip('),'))
                to_idx = parts.index('to')
                x2 = int(parts[to_idx + 1].strip('(,'))
                y2 = int(parts[to_idx + 2].strip('),'))
                color_idx = parts.index('color')
                color = parts[color_idx + 1] if color_idx + 1 < len(parts) else 'black'
                
                self.shapes.append({
                    'type': 'line',
                    'name': name,
                    'x1': x1,
                    'y1': y1,
                    'x2': x2,
                    'y2': y2,
                    'color': color
                })
        except (ValueError, IndexError) as e:
            print(f"Warning: Could not parse line: {line}")
    
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
            color = self._parse_color(shape.get('color', 'white'))
            
            if shape['type'] == 'circle':
                x, y, r = shape['x'], shape['y'], shape['radius']
                draw.ellipse([x-r, y-r, x+r, y+r], fill=color)
            
            elif shape['type'] == 'ellipse':
                x, y = shape['x'], shape['y']
                w, h = shape.get('width', 50)//2, shape.get('height', 50)//2
                draw.ellipse([x-w, y-h, x+w, y+h], fill=color)
            
            elif shape['type'] == 'line':
                x1, y1 = shape.get('x1', 0), shape.get('y1', 0)
                x2, y2 = shape.get('x2', 0), shape.get('y2', 0)
                draw.line([(x1, y1), (x2, y2)], fill=color, width=2)
            
            elif shape['type'] == 'rectangle':
                x, y = shape['x'], shape['y']
                w, h = shape.get('width', 50), shape.get('height', 50)
                draw.rectangle([x, y, x+w, y+h], fill=color)
        
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
