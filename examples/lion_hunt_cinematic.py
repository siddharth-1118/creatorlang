#!/usr/bin/env python3
"""Lion Hunt Cinematic - Lion King Style Chase Scene

Creates a realistic, cinematic lion chase sequence with:
- Fast-running lion with motion blur
- Dust particle effects
- Camera shake and dynamic movement  
- Radial blur for speed
- Atmospheric effects
- Cinematic color grading

Inspired by The Lion King (Simba movie)
Run: python examples/lion_hunt_cinematic.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import cv2
from vfx_engine import VFXEngine, ParticleSystem, EffectProcessor
import random
import math


class LionHuntScene:
    """Epic lion hunt cinematic scene"""
    
    def __init__(self, width=1920, height=1080, fps=60):
        self.width = width
        self.height = height
        self.fps = fps
        self.vfx = VFXEngine()
        
        # Create dust particle systems for running
        self.create_dust_effects()
        
    def create_dust_effects(self):
        """Create realistic dust clouds from running"""
        # Main dust trail
        dust_config = {
            'position': (self.width // 2, self.height - 200),
            'rate': 150,
            'particle': {
                'velocity': (-80, -40),
                'velocity_random': (60, 30),
                'acceleration': (0, 20),  # Settle down
                'lifetime': 1.8,
                'lifetime_random': 0.6,
                'color': (180, 160, 140, 120),  # Sandy dust
                'size': 25,
                'size_random': 15,
                'spread': 40
            }
        }
        self.dust_system = self.vfx.add_particle_system(dust_config)
        
        # Ground impact dust
        impact_config = {
            'position': (self.width // 2 - 50, self.height - 180),
            'rate': 80,
            'particle': {
                'velocity': (-100, -60),
                'velocity_random': (50, 20),
                'acceleration': (0, 40),
                'lifetime': 1.2,
                'lifetime_random': 0.4,
                'color': (200, 180, 150, 150),
                'size': 18,
                'size_random': 8,
                'spread': 30
            }
        }
        self.impact_system = self.vfx.add_particle_system(impact_config)
    
    def create_base_frame(self, frame_num, total_frames):
        """Create savanna landscape background"""
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        
        # Sky gradient (golden hour)
        for y in range(self.height // 2):
            progress = y / (self.height // 2)
            # Golden sky
            r = int(255 * (1 - progress * 0.3))
            g = int(200 * (1 - progress * 0.4))
            b = int(100 * (1 - progress * 0.6))
            frame[y, :] = [b, g, r]
        
        # Ground gradient (savanna)
        for y in range(self.height // 2, self.height):
            progress = (y - self.height // 2) / (self.height // 2)
            # Sandy/grassland
            r = int(140 + progress * 40)
            g = int(120 + progress * 30)
            b = int(70 + progress * 20)
            frame[y, :] = [b, g, r]
        
        # Add some grass texture
        noise = np.random.randint(-15, 15, (self.height, self.width, 3), dtype=np.int16)
        frame = np.clip(frame.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        
        return frame
    
    def draw_lion(self, frame, position, size=200):
        """Draw simplified lion silhouette"""
        x, y = position
        
        # Lion body (oval)
        cv2.ellipse(frame, (x, y), (size, size//2), 0, 0, 360, 
                   (80, 100, 140), -1)  # Golden-brown
        
        # Lion head
        head_x = x + size - 40
        cv2.circle(frame, (head_x, y - 20), size//3, (100, 120, 160), -1)
        
        # Mane
        cv2.circle(frame, (head_x, y - 20), size//2, (120, 100, 80), -1)
        cv2.circle(frame, (head_x, y - 20), size//3, (100, 120, 160), -1)
        
        # Legs (running pose)
        leg_offset = int(math.sin(position[0] * 0.1) * 20)
        # Front leg
        cv2.line(frame, (x + 40, y + size//2), 
                (x + 40 + leg_offset, y + size//2 + 60), (90, 110, 150), 15)
        # Back leg  
        cv2.line(frame, (x - 40, y + size//2),
                (x - 40 - leg_offset, y + size//2 + 60), (90, 110, 150), 15)
        
        # Tail
        tail_x = x - size + 20
        tail_y = y - 10
        cv2.line(frame, (x - size//2, y), (tail_x, tail_y), (100, 120, 140), 12)
        
        return frame
    
    def draw_gazelle(self, frame, position, size=120):
        """Draw running gazelle (prey)"""
        x, y = position
        
        # Body
        cv2.ellipse(frame, (x, y), (size//2, size//3), 0, 0, 360,
                   (90, 140, 160), -1)  # Light brown
        
        # Head
        cv2.circle(frame, (x + size//2, y - 15), size//4, (100, 150, 170), -1)
        
        # Legs
        leg_offset = int(math.sin(position[0] * 0.15) * 15)
        cv2.line(frame, (x + 20, y + size//3), 
                (x + 20 + leg_offset, y + size//3 + 40), (100, 140, 160), 8)
        cv2.line(frame, (x - 20, y + size//3),
                (x - 20 - leg_offset, y + size//3 + 40), (100, 140, 160), 8)
        
        return frame
    
    def render_scene(self, duration_seconds=10):
        """Render the complete cinematic scene"""
        print("🦁 Creating Lion Hunt Cinematic Scene - Lion King Style")
        print(f"Resolution: {self.width}x{self.height} @ {self.fps}FPS")
        print(f"Duration: {duration_seconds}s")
        print()
        
        # Setup video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter('lion_hunt_cinematic.mp4', fourcc, self.fps, 
                             (self.width, self.height))
        
        total_frames = int(duration_seconds * self.fps)
        dt = 1.0 / self.fps
        
        # Lion starts at left, prey at right
        lion_start_x = 200
        prey_start_x = self.width - 300
        
        for frame_num in range(total_frames):
            progress = frame_num / total_frames
            
            # Create base landscape
            frame = self.create_base_frame(frame_num, total_frames)
            
            # Calculate positions (lion chasing, getting closer)
            lion_speed = 400  # pixels per second
            prey_speed = 320
            
            lion_x = int(lion_start_x + lion_speed * frame_num / self.fps)
            prey_x = int(prey_start_x + prey_speed * frame_num / self.fps)
            
            lion_y = self.height - 300
            prey_y = self.height - 320
            
            # Draw gazelle (prey)
            if prey_x < self.width + 200:
                frame = self.draw_gazelle(frame, (prey_x, prey_y))
            
            # Draw lion
            if lion_x < self.width + 300:
                frame = self.draw_lion(frame, (lion_x, lion_y))
            
            # Update dust particle positions
            self.dust_system.emitter_pos = (lion_x, lion_y + 100)
            self.impact_system.emitter_pos = (lion_x - 50, lion_y + 90)
            
            # Update VFX
            self.vfx.update(dt)
            
            # Add dynamic effects based on speed
            # Motion blur when running fast
            if frame_num > 60 and frame_num % 3 == 0:
                self.vfx.add_effect('motion_blur', {'strength': 0.4})
            
            # Camera shake during intense moments
            if progress > 0.6 and random.random() < 0.3:
                self.vfx.add_effect('shake', {'intensity': 3})
            
            # Radial blur for speed effect (centered on lion)
            if progress > 0.7:
                self.vfx.add_effect('radial_blur', {
                    'center': (lion_x, lion_y),
                    'strength': 0.3
                })
            
            # Render all VFX
            frame = self.vfx.render(frame)
            
            # Clear one-time effects
            if frame_num % 3 == 0:
                self.vfx.clear_effects()
            
            # Cinematic color grading
            frame = self.apply_cinematic_grade(frame)
            
            # Write frame
            out.write(frame)
            
            # Progress
            if (frame_num + 1) % 60 == 0:
                percent = (frame_num + 1) / total_frames * 100
                particles = len(self.dust_system.particles) + len(self.impact_system.particles)
                print(f"Progress: {percent:.1f}% | Frame {frame_num + 1}/{total_frames} | Particles: {particles}")
        
        out.release()
        print()
        print("✅ Lion Hunt Cinematic Complete!")
        print("   Output: lion_hunt_cinematic.mp4")
        print(f"   Total Frames: {total_frames}")
        print(f"   File Size: ~{total_frames * 0.1:.1f}MB (estimated)")
    
    def apply_cinematic_grade(self, frame):
        """Apply Lion King-style color grading"""
        # Warm golden tones
        frame = frame.astype(np.float32)
        
        # Increase warmth (more red/yellow)
        frame[:,:,2] = np.clip(frame[:,:,2] * 1.15, 0, 255)  # More red
        frame[:,:,1] = np.clip(frame[:,:,1] * 1.08, 0, 255)  # More green
        frame[:,:,0] = np.clip(frame[:,:,0] * 0.92, 0, 255)  # Less blue
        
        # Increase contrast
        frame = np.clip((frame - 128) * 1.2 + 128, 0, 255)
        
        # Slight vignette
        h, w = frame.shape[:2]
        y, x = np.ogrid[:h, :w]
        center_y, center_x = h // 2, w // 2
        dist = np.sqrt((x - center_x)**2 + (y - center_y)**2)
        max_dist = np.sqrt(center_x**2 + center_y**2)
        vignette = 1 - (dist / max_dist) * 0.4
        frame = frame * vignette[:,:,np.newaxis]
        
        return np.clip(frame, 0, 255).astype(np.uint8)


if __name__ == '__main__':
    print("=" * 70)
    print("  CREATORLANG CINEMATIC: THE LION KING - HUNT SCENE")
    print("  Realistic lion chase with VFX")
    print("=" * 70)
    print()
    
    scene = LionHuntScene(width=1920, height=1080, fps=60)
    scene.render_scene(duration_seconds=10)
    
    print()
    print("🎬 Scene complete! Open lion_hunt_cinematic.mp4 to watch!")
    print("   This epic chase scene features:")
    print("   - Realistic dust particle effects")
    print("   - Motion blur for speed")
    print("   - Camera shake for intensity")
    print("   - Radial blur for dramatic effect")
    print("   - Cinematic color grading (golden hour)")
    print()
    print("   Just like The Lion King! 🦁👑")
