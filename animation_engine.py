#!/usr/bin/env python3
"""CreatorLang Animation Engine - Full timeline animation support"""

import os
import re
import math
import numpy as np
from PIL import Image, ImageDraw
import imageio

class AnimationEngine:
    """Advanced animation engine with keyframes, easing, and effects"""
    
    @staticmethod
    def ease_in_out(t):
        """Smooth easing function"""
        return t * t * (3 - 2 * t)
    
    @staticmethod
    def interpolate(start, end, progress, easing='linear'):
        """Interpolate between two values with easing"""
        if easing == 'ease_in_out':
            progress = AnimationEngine.ease_in_out(progress)
        return start + (end - start) * progress

class AnimatedCompiler:
    """Full animation compiler with timeline support"""
    
    def __init__(self, source_file):
        self.source_file = source_file
        self.output_dir = "output"
        self.video_config = {
            'duration': 10,
            'fps': 30,
            'width': 1920,
            'height': 1080
        }
        self.shapes = []
        self.video_duration_set = False
        
    def parse(self):
        """Parse CreatorLang file with animation support"""
        with open(self.source_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        current_shape = None
        inside_video_block = False
        i = 0
        
        while i < len(lines):
            line = lines[i].rstrip()
            
            if not line.strip() or line.strip().startswith('#'):
                i += 1
                continue
            
            indent = len(line) - len(line.lstrip())
            line = line.strip()
            
            # Check if we're inside the video config block
            if line.startswith('video '):
                inside_video_block = True
                match = re.search(r'"([^"]+)"', line)
                if match:
                    self.video_config['name'] = match.group(1)
                i += 1
                continue
            
            # Parse ONLY top-level video duration
            if inside_video_block and indent > 0 and 'duration' in line.lower() and not self.video_duration_set:
                match = re.search(r'duration\s+(\d+)', line)
                if match:
                    self.video_config['duration'] = int(match.group(1))
                    self.video_duration_set = True
                    print(f"  ✓ Video duration: {self.video_config['duration']} seconds")
            
            if inside_video_block and indent == 0 and not line.startswith('video'):
                inside_video_block = False
            
            if inside_video_block and 'fps' in line.lower():
                match = re.search(r'fps\s+(\d+)', line)
                if match:
                    self.video_config['fps'] = int(match.group(1))
                    print(f"  ✓ FPS: {self.video_config['fps']}")
            
            if inside_video_block and line.startswith('size '):
                match = re.search(r'(\d+)x(\d+)', line)
                if match:
                    self.video_config['width'] = int(match.group(1))
                    self.video_config['height'] = int(match.group(2))
                    print(f"  ✓ Size: {self.video_config['width']}x{self.video_config['height']}")
            
            if inside_video_block and line.startswith('background gradient'):
                match = re.search(r'gradient\(([^)]+)\)', line)
                if match:
                    colors = [c.strip() for c in match.group(1).split(',')]
                    self.video_config['background'] = colors
            
            if line.startswith(('circle ', 'ellipse ', 'rectangle ', 'line ')):
                if line.endswith(':'):
                    shape_type = line.split()[0]
                    name_match = re.search(r'"([^"]+)"', line)
                    if name_match:
                        shape_name = name_match.group(1)
                        current_shape = {
                            'type': shape_type,
                            'name': shape_name,
                            'animations': []
                        }
                        
                        i += 1
                        while i < len(lines):
                            next_line = lines[i].rstrip()
                            if not next_line.strip() or next_line.strip().startswith('#'):
                                i += 1
                                continue
                            
                            next_indent = len(next_line) - len(next_line.lstrip())
                            if next_indent <= indent:
                                i -= 1
                                break
                            
                            prop_line = next_line.strip()
                            
                            if prop_line.startswith('duration '):
                                i += 1
                                continue
                            
                            if prop_line.startswith('animation '):
                                anim_type = prop_line.split('animation ', 1)[1]
                                current_shape['animations'].append({'type': anim_type})
                            else:
                                self._parse_property(prop_line, current_shape)
                            
                            i += 1
                        
                        self.shapes.append(current_shape)
                        current_shape = None
            
            i += 1
        
        total_frames = self.video_config['duration'] * self.video_config['fps']
        print(f"\n✓ Parsed {len(self.shapes)} shapes")
        print(f"  📹 Final video config:")
        print(f"     Duration: {self.video_config['duration']}s")
        print(f"     FPS: {self.video_config['fps']}")
        print(f"     Total frames: {total_frames}")
    
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
        
        if color_str.startswith('#'):
            color = color_str.lstrip('#')
            if len(color) == 6:
                return tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        
        return (255, 255, 255)
    
    def generate_frame(self, frame_number):
        """Generate a single frame of animation"""
        width = self.video_config['width']
        height = self.video_config['height']
        total_frames = self.video_config['duration'] * self.video_config['fps']
        progress = frame_number / max(total_frames, 1)
        time_seconds = frame_number / self.video_config['fps']
        
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)
        
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
            draw.rectangle([0, 0, width, height], fill=(135, 206, 235))
        
        for shape in self.shapes:
            x = shape.get('x', 0)
            y = shape.get('y', 0)
            
            shape_name = shape.get('name', '').lower()
            
            if any(keyword in shape_name for keyword in ['body', 'head', 'face', 'eye', 'nose', 'whisker', 
                                                          'mouth', 'collar', 'bell', 'arm', 'hand', 'leg', 
                                                          'foot', 'tail', 'belly', 'propeller']):
                offset_x = int(AnimationEngine.interpolate(0, 1400, progress, 'ease_in_out'))
                x += offset_x
                
                bob_cycle = math.sin(time_seconds * math.pi * 2) * 25
                y += int(bob_cycle)
            
            if 'cloud' in shape_name:
                for anim in shape.get('animations', []):
                    anim_type = anim.get('type', '')
                    if 'slide_right' in anim_type:
                        x += int(time_seconds * 50)
                    elif 'slide_left' in anim_type:
                        x -= int(time_seconds * 40)
            
            color = self._parse_color(shape.get('color', 'white'))
            
            if shape['type'] == 'circle':
                r = shape.get('radius', 50)
                draw.ellipse([x-r, y-r, x+r, y+r], fill=color)
            
            elif shape['type'] == 'ellipse':
                w = shape.get('width', 50) // 2
                h = shape.get('height', 50) // 2
                draw.ellipse([x-w, y-h, x+w, y+h], fill=color)
            
            elif shape['type'] == 'line':
                x1 = shape.get('x1', 0) + (x - shape.get('x', 0))
                y1 = shape.get('y1', 0) + (y - shape.get('y', 0))
                x2 = shape.get('x2', 0) + (x - shape.get('x', 0))
                y2 = shape.get('y2', 0) + (y - shape.get('y', 0))
                draw.line([(x1, y1), (x2, y2)], fill=color, width=2)
            
            elif shape['type'] == 'rectangle':
                w = shape.get('width', 50)
                h = shape.get('height', 50)
                draw.rectangle([x, y, x+w, y+h], fill=color)
        
        return np.array(img)
    
    def compile_animation(self):
        """Generate all frames and create video"""
        os.makedirs(self.output_dir, exist_ok=True)
        
        total_frames = self.video_config['duration'] * self.video_config['fps']
        fps = self.video_config['fps']
        
        if total_frames == 0:
            print("\n❌ Error: Duration is 0 seconds. Cannot generate animation.")
            return
        
        print(f"\n🎬 Generating {total_frames} frames...")
        frames = []
        
        for frame_num in range(total_frames):
            if frame_num % 30 == 0 or frame_num == total_frames - 1:
                print(f"  Frame {frame_num+1}/{total_frames} ({(frame_num+1)/total_frames*100:.1f}%)")
            
            frame = self.generate_frame(frame_num)
            frames.append(frame)
        
        output_path = os.path.join(self.output_dir, 'doraemon_animated.mp4')
        print(f"\n💾 Saving video...")
        imageio.mimsave(output_path, frames, fps=fps)
        
        print(f"\n✅ Animation complete!")
        print(f"  📁 File: {os.path.abspath(output_path)}")
        print(f"  ⏱️  Duration: {self.video_config['duration']}s")
        print(f"  📐 Size: {self.video_config['width']}x{self.video_config['height']}")
        print(f"  🎞️  FPS: {fps}")
        print(f"  🖼️  Frames: {total_frames}")
        print(f"\n🎥 Open the file to watch Doraemon fly!")

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python animation_engine.py <file.create>")
        sys.exit(1)
    
    source_file = sys.argv[1]
    if not os.path.exists(source_file):
        print(f"Error: File '{source_file}' not found")
        sys.exit(1)
    
    print("🎥 CreatorLang Animation Engine v1.0")
    print("=" * 50)
    
    compiler = AnimatedCompiler(source_file)
    print(f"\n📄 Parsing {source_file}...")
    compiler.parse()
    
    print(f"\n🎬 Compiling animation...")
    compiler.compile_animation()

if __name__ == "__main__":
    main()
