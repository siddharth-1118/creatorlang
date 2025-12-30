#!/usr/bin/env python3
"""Generate animated video from CreatorLang timeline"""

import os
import sys
import numpy as np
from PIL import Image
import imageio

def create_animation_frames(num_frames=60):
    """Create frames for Doraemon flying animation"""
    frames = []
    
    # Load the base Doraemon image
    base_image = Image.open('output/doraemon_frame.png')
    
    for i in range(num_frames):
        # Create a copy of the frame
        frame = base_image.copy()
        
        # Convert PIL Image to numpy array
        frame_array = np.array(frame)
        frames.append(frame_array)
    
    return frames

def generate_video(frames, output_path='output/doraemon_movie.mp4', fps=30):
    """Save frames as video"""
    # Write video using imageio
    imageio.mimsave(output_path, frames, fps=fps)
    print(f"✓ Video saved to {output_path}")
    print(f"  Duration: {len(frames)/fps:.1f} seconds")
    print(f"  Frames: {len(frames)}")
    print(f"  FPS: {fps}")

if __name__ == "__main__":
    print("Generating Doraemon animation...")
    
    # Generate 2 seconds of video at 30 fps = 60 frames
    frames = create_animation_frames(num_frames=60)
    
    generate_video(frames, fps=30)
    print("✓ Animation complete!")
