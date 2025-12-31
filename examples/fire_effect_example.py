#!/usr/bin/env python3
"""Fire Effect Example for CreatorLang

Demonstrates how to use the VFX engine to create a fire effect.
Run: python examples/fire_effect_example.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import cv2
from vfx_engine import VFXEngine, FireEffect


def create_fire_animation(duration_seconds=5, fps=30):
    """Create a fire effect animation"""
    
    # Initialize
    width, height = 1920, 1080
    vfx = VFXEngine()
    
    # Create fire particle system
    fire_config = FireEffect.create_fire_config(position=(width//2, height//2 + 200))
    fire_system = vfx.add_particle_system(fire_config)
    
    # Add glow effect
    vfx.add_effect('glow', {'intensity': 0.7, 'radius': 25})
    
    print(f"Creating fire animation: {duration_seconds}s at {fps} FPS")
    print(f"Resolution: {width}x{height}")
    
    # Setup video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('fire_animation.mp4', fourcc, fps, (width, height))
    
    total_frames = int(duration_seconds * fps)
    dt = 1.0 / fps
    
    for frame_num in range(total_frames):
        # Create base frame
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Update VFX
        vfx.update(dt)
        
        # Render VFX
        frame = vfx.render(frame)
        
        # Write frame
        out.write(frame)
        
        # Progress
        if (frame_num + 1) % 30 == 0:
            progress = (frame_num + 1) / total_frames * 100
            print(f"Progress: {progress:.1f}% ({frame_num + 1}/{total_frames} frames)")
    
    out.release()
    print("\n✅ Fire animation created: fire_animation.mp4")
    print(f"   Total particles rendered: {len(fire_system.particles)}")


if __name__ == '__main__':
    print("=" * 60)
    print("CreatorLang VFX Engine - Fire Effect Demo")
    print("=" * 60)
    print()
    
    create_fire_animation(duration_seconds=5, fps=30)
    
    print("\nDone! Open fire_animation.mp4 to see the result.")
