#!/usr/bin/env python3
"""CreatorLang Compiler - Transform .create files into images, videos, and 3D models"""

import re
import sys
import os
from PIL import Image, ImageDraw, ImageFont
import json

class CreatorLangCompiler:
    def __init__(self, source_file):
        self.source_file = source_file
        self.output_dir = "output"
        self.assets = {}
        self.scenes = []
        self.animations = []
        
    def parse(self):
        """Parse the .create file"""
        with open(self.source_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract CREATE blocks
        create_blocks = re.findall(r'CREATE\s+(\w+)\s+AS\s+(\w+)\s*\{([^}]+)\}', content, re.DOTALL)
        for block_type, name, properties in create_blocks:
            self.assets[name] = {
                'type': block_type,
                'properties': self._parse_properties(properties)
            }
        
        # Extract SCENE blocks
        scene_blocks = re.findall(r'SCENE\s+(\w+)\s*\{([^}]+)\}', content, re.DOTALL)
        for name, properties in scene_blocks:
            self.scenes.append({
                'name': name,
                'properties': self._parse_properties(properties)
            })
        
        # Extract ANIMATE blocks  
        animate_blocks = re.findall(r'ANIMATE\s+(\w+)\s*\{([^}]+)\}', content, re.DOTALL)
        for target, keyframes in animate_blocks:
            self.animations.append({
                'target': target,
                'keyframes': self._parse_keyframes(keyframes)
            })
    
    def _parse_properties(self, prop_text):
        """Parse property assignments"""
        props = {}
        lines = prop_text.strip().split('\n')
        for line in lines:
            line = line.strip()
            if ':' in line:
                key, value = line.split(':', 1)
                props[key.strip()] = value.strip().strip(',"')
        return props
    
    def _parse_keyframes(self, keyframe_text):
        """Parse animation keyframes"""
        keyframes = []
        kf_blocks = re.findall(r'(\d+)%\s*\{([^}]+)\}', keyframe_text)
        for percent, properties in kf_blocks:
            keyframes.append({
                'percent': int(percent),
                'properties': self._parse_properties(properties)
            })
        return keyframes
    
    def compile(self):
        """Compile to visual output"""
        os.makedirs(self.output_dir, exist_ok=True)
        
        # For now, create a simple image representation
        img = Image.new('RGB', (800, 600), color='lightblue')
        draw = ImageDraw.Draw(img)
        
        # Draw assets
        y_pos = 50
        for name, asset in self.assets.items():
            text = f"{asset['type']}: {name}"
            draw.text((50, y_pos), text, fill='black')
            y_pos += 40
        
        # Save output
        output_path = os.path.join(self.output_dir, 'output.png')
        img.save(output_path)
        print(f"✓ Compiled to {output_path}")
        
        # Also save JSON representation
        json_path = os.path.join(self.output_dir, 'output.json')
        with open(json_path, 'w') as f:
            json.dump({
                'assets': self.assets,
                'scenes': self.scenes,
                'animations': self.animations
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
