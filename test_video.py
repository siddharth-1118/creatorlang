#!/usr/bin/env python3
"""
CreatorLang - Simple Test Video
This creates a basic animated video to test your setup.
No API keys needed!
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

def create_test_video():
    print("\n🎬 Creating CreatorLang Test Video...")
    print("-" * 50)
    
    # Video settings
    width, height = 1280, 720
    fps = 30
    duration = 5  # seconds
    
    # Create video writer
    output_file = 'creatorlang_test.mp4'
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
    
    total_frames = fps * duration
    print(f"\nGenerating {total_frames} frames at {fps} FPS...")
    
    # Generate frames
    for frame_num in range(total_frames):
        # Create gradient background
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)
        
        # Animated gradient background
        for y in range(height):
            color_value = int(50 + 50 * np.sin((y + frame_num * 5) / 50))
            draw.rectangle([0, y, width, y+1], fill=(20, color_value, 80))
        
        # Moving circle
        circle_x = int((width / 2) + (width / 3) * np.sin(frame_num / 20))
        circle_y = height // 2
        circle_radius = 50
        draw.ellipse(
            [circle_x - circle_radius, circle_y - circle_radius,
             circle_x + circle_radius, circle_y + circle_radius],
            fill=(255, 200, 0)
        )
        
        # Text - "CreatorLang Works!"
        text_x = width // 2 - 200
        text_y = height // 2 + 100
        draw.text((text_x, text_y), "CreatorLang Works!", 
                 fill=(255, 255, 255))
        
        # Frame counter
        draw.text((width - 150, 30), f"Frame {frame_num + 1}/{total_frames}",
                 fill=(200, 200, 200))
        
        # Convert PIL image to OpenCV format
        frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        out.write(frame)
        
        # Progress indicator
        if (frame_num + 1) % 30 == 0:
            progress = ((frame_num + 1) / total_frames) * 100
            print(f"Progress: {progress:.0f}% [{frame_num + 1}/{total_frames} frames]")
    
    # Release video writer
    out.release()
    
    print("\n" + "="*50)
    print("✅ SUCCESS! Video created successfully!")
    print("="*50)
    print(f"\n🎬 Output file: {output_file}")
    print(f"📊 Size: {os.path.getsize(output_file) / 1024:.2f} KB")
    print(f"⏱️  Duration: {duration} seconds")
    print(f"🎥 Resolution: {width}x{height}")
    print(f"📽️ FPS: {fps}")
    print("\n▶️  Open the file to view your video!")
    print("\n🚀 Next steps:")
    print("   1. Run: git pull")
    print("   2. Try: python examples/photorealistic_ai_video.create")
    print("   3. Create your own stories!")
    print()

if __name__ == "__main__":
    try:
        create_test_video()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have installed: pip install opencv-python numpy pillow")
