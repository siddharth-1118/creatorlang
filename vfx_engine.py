"""CreatorLang VFX Engine

Visual Effects system for CreatorLang animation language.
Provides particle systems, lighting effects, post-processing, and more.

Author: Sai Siddharth
Date: December 31, 2025
"""

import numpy as np
import cv2
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict, Any
import random
import math


@dataclass
class Particle:
    """Represents a single particle in the system"""
    position: Tuple[float, float]
    velocity: Tuple[float, float]
    acceleration: Tuple[float, float]
    lifetime: float
    max_lifetime: float
    color: Tuple[int, int, int, int]  # RGBA
    size: float
    rotation: float = 0.0
    angular_velocity: float = 0.0


class ParticleSystem:
    """Manages particle emission, update, and rendering"""
    
    def __init__(self, config: Dict[str, Any]):
        self.particles: List[Particle] = []
        self.config = config
        self.emitter_pos = config.get('position', (0, 0))
        self.emission_rate = config.get('rate', 50)
        self.particle_config = config.get('particle', {})
        self.time_since_emit = 0.0
        
    def emit(self, count: int = 1):
        """Emit new particles"""
        for _ in range(count):
            particle = self._create_particle()
            self.particles.append(particle)
    
    def _create_particle(self) -> Particle:
        """Create a single particle with random properties"""
        pc = self.particle_config
        
        # Position with optional spread
        spread = pc.get('spread', 0)
        pos = (
            self.emitter_pos[0] + random.uniform(-spread, spread),
            self.emitter_pos[1] + random.uniform(-spread, spread)
        )
        
        # Velocity
        vel_base = pc.get('velocity', (0, -50))
        vel_random = pc.get('velocity_random', (0, 0))
        velocity = (
            vel_base[0] + random.uniform(-vel_random[0], vel_random[0]),
            vel_base[1] + random.uniform(-vel_random[1], vel_random[1])
        )
        
        # Acceleration (gravity, etc)
        acceleration = pc.get('acceleration', (0, 0))
        
        # Lifetime
        lifetime_base = pc.get('lifetime', 2.0)
        lifetime_random = pc.get('lifetime_random', 0.0)
        lifetime = lifetime_base + random.uniform(-lifetime_random, lifetime_random)
        
        # Color
        color = pc.get('color', (255, 255, 255, 255))
        
        # Size
        size_base = pc.get('size', 5)
        size_random = pc.get('size_random', 0)
        size = size_base + random.uniform(-size_random, size_random)
        
        # Rotation
        rotation = random.uniform(0, 360)
        angular_velocity = pc.get('angular_velocity', 0)
        
        return Particle(
            position=pos,
            velocity=velocity,
            acceleration=acceleration,
            lifetime=lifetime,
            max_lifetime=lifetime,
            color=color,
            size=size,
            rotation=rotation,
            angular_velocity=angular_velocity
        )
    
    def update(self, dt: float):
        """Update all particles"""
        # Update emission
        self.time_since_emit += dt
        if self.time_since_emit >= 1.0 / self.emission_rate:
            self.emit()
            self.time_since_emit = 0.0
        
        # Update each particle
        for particle in self.particles:
            # Update position
            particle.position = (
                particle.position[0] + particle.velocity[0] * dt,
                particle.position[1] + particle.velocity[1] * dt
            )
            
            # Update velocity
            particle.velocity = (
                particle.velocity[0] + particle.acceleration[0] * dt,
                particle.velocity[1] + particle.acceleration[1] * dt
            )
            
            # Update rotation
            particle.rotation += particle.angular_velocity * dt
            
            # Update lifetime
            particle.lifetime -= dt
        
        # Remove dead particles
        self.particles = [p for p in self.particles if p.lifetime > 0]
    
    def render(self, frame: np.ndarray):
        """Render all particles to frame"""
        for particle in self.particles:
            # Calculate opacity based on lifetime
            alpha = particle.lifetime / particle.max_lifetime
            color_with_alpha = (*particle.color[:3], int(particle.color[3] * alpha))
            
            # Draw particle
            pos = (int(particle.position[0]), int(particle.position[1]))
            if 0 <= pos[0] < frame.shape[1] and 0 <= pos[1] < frame.shape[0]:
                cv2.circle(frame, pos, int(particle.size), color_with_alpha[:3], -1)


class EffectProcessor:
    """Post-processing effects for animations"""
    
    @staticmethod
    def apply_glow(frame: np.ndarray, intensity: float = 0.5, radius: int = 20) -> np.ndarray:
        """Apply glow effect using gaussian blur"""
        if radius % 2 == 0:
            radius += 1
        blurred = cv2.GaussianBlur(frame, (radius, radius), 0)
        return cv2.addWeighted(frame, 1.0, blurred, intensity, 0)
    
    @staticmethod
    def apply_motion_blur(frame: np.ndarray, prev_frame: np.ndarray, strength: float = 0.5) -> np.ndarray:
        """Apply motion blur by blending with previous frame"""
        return cv2.addWeighted(frame, 1 - strength, prev_frame, strength, 0)
    
    @staticmethod
    def apply_shake(frame: np.ndarray, intensity: int = 5) -> np.ndarray:
        """Apply camera shake effect"""
        h, w = frame.shape[:2]
        dx = random.randint(-intensity, intensity)
        dy = random.randint(-intensity, intensity)
        M = np.float32([[1, 0, dx], [0, 1, dy]])
        return cv2.warpAffine(frame, M, (w, h))
    
    @staticmethod
    def apply_glitch(frame: np.ndarray, intensity: float = 0.5) -> np.ndarray:
        """Apply glitch effect with RGB channel shift"""
        h, w = frame.shape[:2]
        result = frame.copy()
        
        # RGB channel shift
        shift = int(intensity * 10)
        if len(frame.shape) == 3:
            result[:,:,0] = np.roll(frame[:,:,0], shift, axis=1)
            result[:,:,2] = np.roll(frame[:,:,2], -shift, axis=1)
        
        # Random horizontal displacement
        if random.random() < intensity:
            y = random.randint(0, h - 50)
            height = random.randint(5, 50)
            shift_amount = random.randint(-20, 20)
            result[y:y+height] = np.roll(result[y:y+height], shift_amount, axis=1)
        
        return result
    
    @staticmethod
    def apply_radial_blur(frame: np.ndarray, center: Tuple[int, int], strength: float = 0.5) -> np.ndarray:
        """Apply radial blur (speed lines effect)"""
        h, w = frame.shape[:2]
        result = frame.copy()
        
        # Create radial gradient
        y, x = np.ogrid[:h, :w]
        dist = np.sqrt((x - center[0])**2 + (y - center[1])**2)
        dist = dist / np.max(dist)
        
        # Apply blur based on distance from center
        for i in range(int(strength * 10)):
            alpha = (i + 1) / (strength * 10)
            blurred = cv2.GaussianBlur(frame, (15, 15), 0)
            mask = (dist > 0.3).astype(float)
            result = cv2.addWeighted(result, 1 - alpha * 0.1, blurred, alpha * 0.1, 0)
        
        return result


class FireEffect:
    """Fire particle effect"""
    
    @staticmethod
    def create_fire_config(position: Tuple[int, int]) -> Dict:
        return {
            'position': position,
            'rate': 100,
            'particle': {
                'velocity': (0, -50),
                'velocity_random': (10, 10),
                'acceleration': (0, -20),
                'lifetime': 1.5,
                'lifetime_random': 0.5,
                'color': (255, 100, 0, 255),  # Orange
                'size': 10,
                'size_random': 5,
                'spread': 20
            }
        }


class ExplosionEffect:
    """Explosion particle burst"""
    
    @staticmethod
    def create_explosion_config(position: Tuple[int, int], particle_count: int = 200) -> Dict:
        return {
            'position': position,
            'rate': 0,  # Burst, not continuous
            'particle': {
                'velocity': (0, 0),  # Will be set radially
                'acceleration': (0, 100),  # Gravity
                'lifetime': 2.0,
                'lifetime_random': 0.5,
                'color': (255, 255, 0, 255),  # Yellow
                'size': 8,
                'size_random': 4
            }
        }
    
    @staticmethod
    def emit_radial_burst(system: ParticleSystem, count: int):
        """Emit particles in all directions"""
        for i in range(count):
            angle = (i / count) * 2 * math.pi
            speed = random.uniform(50, 200)
            
            particle = system._create_particle()
            particle.velocity = (
                math.cos(angle) * speed,
                math.sin(angle) * speed
            )
            system.particles.append(particle)


class VFXEngine:
    """Main VFX engine coordinating all effects"""
    
    def __init__(self):
        self.particle_systems: List[ParticleSystem] = []
        self.effect_processor = EffectProcessor()
        self.active_effects: List[Dict] = []
        self.prev_frame: Optional[np.ndarray] = None
    
    def add_particle_system(self, config: Dict) -> ParticleSystem:
        """Add a new particle system"""
        system = ParticleSystem(config)
        self.particle_systems.append(system)
        return system
    
    def add_effect(self, effect_type: str, params: Dict):
        """Add a post-processing effect"""
        self.active_effects.append({
            'type': effect_type,
            'params': params
        })
    
    def update(self, dt: float):
        """Update all particle systems"""
        for system in self.particle_systems:
            system.update(dt)
    
    def render(self, base_frame: np.ndarray) -> np.ndarray:
        """Render all effects to frame"""
        frame = base_frame.copy()
        
        # Render all particle systems
        for system in self.particle_systems:
            system.render(frame)
        
        # Apply post-processing effects
        for effect in self.active_effects:
            effect_type = effect['type']
            params = effect['params']
            
            if effect_type == 'glow':
                frame = self.effect_processor.apply_glow(
                    frame, 
                    params.get('intensity', 0.5),
                    params.get('radius', 20)
                )
            elif effect_type == 'motion_blur' and self.prev_frame is not None:
                frame = self.effect_processor.apply_motion_blur(
                    frame,
                    self.prev_frame,
                    params.get('strength', 0.5)
                )
            elif effect_type == 'shake':
                frame = self.effect_processor.apply_shake(
                    frame,
                    params.get('intensity', 5)
                )
            elif effect_type == 'glitch':
                frame = self.effect_processor.apply_glitch(
                    frame,
                    params.get('intensity', 0.5)
                )
            elif effect_type == 'radial_blur':
                frame = self.effect_processor.apply_radial_blur(
                    frame,
                    params.get('center', (frame.shape[1]//2, frame.shape[0]//2)),
                    params.get('strength', 0.5)
                )
        
        # Store for motion blur
        self.prev_frame = frame.copy()
        
        return frame
    
    def clear_effects(self):
        """Clear all active effects"""
        self.active_effects.clear()
    
    def clear_particles(self):
        """Clear all particle systems"""
        self.particle_systems.clear()


if __name__ == '__main__':
    # Test the VFX engine
    print("CreatorLang VFX Engine v1.0")
    print("Ready to add amazing visual effects to your animations!")
