# CreatorLang - Complete Language Specification

**Version 1.0.0** | **File Extension: `.create`**

CreatorLang is a unified creative programming language designed to generate:
- **Images** (PNG, JPG, SVG)
- **Videos** (MP4, GIF, WebM)
- **3D Models** (OBJ, GLTF, STL)

All from simple, intuitive text-based code.

---

## Table of Contents
1. [Quick Start](#quick-start)
2. [Image Generation](#image-generation)
3. [Video Generation](#video-generation)
4. [3D Model Generation](#3d-generation)
5. [Complete Examples](#examples)
6. [Syntax Reference](#syntax)

---

## Quick Start

### Installation
```bash
pip install creatorlang
```

### Hello Image
```creatorlang
# File: hello.create

image "HelloWorld":
    size 800x600
    background blue
    
    text "Hello, CreatorLang!":
        position center
        font Arial 48px
        color white
    
    export "hello.png"
```

### Run It
```bash
creatorlang hello.create
```

Output: `hello.png` created! 🎨

---

## 1. IMAGE GENERATION

### Basic Syntax

```creatorlang
image "MyImage":
    size WIDTH x HEIGHT
    background COLOR | gradient(COLOR1, COLOR2)
    
    # Add elements...
    
    export "filename.png"
```

### Complete Image Example

```creatorlang
image "BusinessCard":
    size 1000x600
    background gradient(#6366f1, #8b5cf6)
    
    # Logo
    circle:
        position (100, 100)
        radius 50
        color white
        border 3px #6366f1
    
    # Company Name
    text "TechCorp":
        position (200, 100)
        font "Helvetica Bold" 42px
        color white
    
    # Tagline
    text "Innovation Starts Here":
        position (200, 150)
        font "Helvetica" 18px
        color rgba(255,255,255,0.8)
    
    # Contact Box
    rectangle:
        position (50, 300)
        size 900x200
        color rgba(255,255,255,0.1)
        corner_radius 10px
    
    # Contact Info
    text "contact@techcorp.com | +1-555-0123":
        position center_bottom
        margin 50px
        font "Helvetica" 16px
        color white
    
    export "business_card.png"
```

### Image Elements

**Shapes:**
- `circle`, `rectangle`, `triangle`, `polygon`, `ellipse`
- `line`, `arrow`, `path`

**Properties:**
- `position`: `(x, y)`, `center`, `top_left`, `bottom_right`
- `color`: `red`, `#ff0000`, `rgb(255,0,0)`, `rgba(255,0,0,0.5)`
- `size`: `100x200`
- `rotation`: `45deg`
- `opacity`: `0.5`

---

## 2. VIDEO GENERATION

### Basic Syntax

```creatorlang
video "MyVideo":
    duration SECONDS
    fps 30
    size 1920x1080
    
    # Add scenes...
    
    export "video.mp4"
```

### Complete Video Example

```creatorlang
video "ProductDemo":
    duration 10 seconds
    fps 30
    size 1920x1080
    background black
    
    # Scene 1: Logo Reveal (0-3 seconds)
    scene "intro" from 0s to 3s:
        image "logo.png":
            position center
            scale 0 to 1
            animation fade_in
            duration 2s
        
        text "Welcome":
            position center_bottom
            margin 100px
            color white
            font Arial 36px
            animation slide_up
            delay 1s
    
    # Scene 2: Feature Showcase (3-7 seconds)
    scene "features" from 3s to 7s:
        transition fade 0.5s
        
        text "Amazing Features":
            position top_center
            margin 50px
            font "Arial Bold" 48px
            color white
        
        # Feature cards with animation
        for feature in ["Fast", "Secure", "Easy"]:
            rectangle:
                position auto_grid
                size 400x300
                color #333
                corner_radius 15px
                animation pop_in
                delay feature.index * 0.5s
            
            text feature:
                position inside_center
                font Arial 32px
                color white
    
    # Scene 3: Call to Action (7-10 seconds)
    scene "cta" from 7s to 10s:
        transition wipe_left 0.5s
        background gradient(#6366f1, #8b5cf6)
        
        text "Get Started Today!":
            position center
            font "Arial Bold" 64px
            color white
            animation pulse
        
        text "www.product.com":
            position center_bottom
            margin 100px
            font Arial 32px
            color white
    
    # Audio
    audio "background_music.mp3":
        volume 0.7
        fade_in 1s
        fade_out 1s
    
    export "product_demo.mp4"
```

### Video Features

**Animations:**
- `fade_in`, `fade_out`
- `slide_up`, `slide_down`, `slide_left`, `slide_right`
- `zoom_in`, `zoom_out`
- `rotate`, `spin`
- `bounce`, `pulse`, `shake`
- `pop_in`, `pop_out`

**Transitions:**
- `fade`, `dissolve`
- `wipe_left`, `wipe_right`, `wipe_up`, `wipe_down`
- `slide`, `push`
- `zoom`, `spin`

---

## 3. 3D MODEL GENERATION

### Basic Syntax

```creatorlang
model3d "MyModel":
    # Add 3D objects...
    
    export "model.obj"
```

### Complete 3D Model Example

```creatorlang
model3d "SimpleHouse":
    # Main house body
    cube "house_base":
        position (0, 0, 0)
        size (4, 3, 4)  # width, height, depth
        color brown
        material wood
    
    # Roof
    pyramid "roof":
        position (0, 3, 0)
        base 4x4
        height 2
        color red
        material tile
    
    # Door
    cube "door":
        position (0, 0, 2.1)
        size (1, 2, 0.1)
        color dark_brown
        material wood
    
    # Windows
    for x in [-1.5, 1.5]:
        cube "window":
            position (x, 1.5, 2.1)
            size (0.8, 0.8, 0.1)
            color light_blue
            material glass
            transparency 0.7
    
    # Chimney
    cylinder "chimney":
        position (1.5, 4, 1)
        radius 0.3
        height 1.5
        color gray
        material brick
    
    # Ground
    plane "ground":
        position (0, -0.1, 0)
        size 10x10
        color green
        material grass
    
    # Lighting
    light "sun":
        type directional
        position (5, 10, 5)
        intensity 1.0
        color white
    
    # Camera
    camera:
        position (10, 5, 10)
        look_at (0, 1, 0)
        fov 60
    
    export "house.obj"
    export_with_textures "house.gltf"
```

### 3D Primitives

- `cube`, `sphere`, `cylinder`, `cone`, `pyramid`
- `torus`, `plane`, `capsule`
- `custom_mesh` (load from file)

### 3D Properties

- `position (x, y, z)`
- `rotation (x, y, z)` in degrees
- `scale (x, y, z)`
- `color`
- `material`: `metal`, `plastic`, `wood`, `glass`, `stone`, `fabric`
- `texture`: load from image file
- `transparency`: `0.0` to `1.0`

### Materials & Textures

```creatorlang
material "custom_wood":
    type wood
    color #8B4513
    roughness 0.8
    metalness 0.0
    texture "wood_grain.jpg"

material "shiny_metal":
    type metal
    color silver
    roughness 0.1
    metalness 1.0
    reflection 0.9
```

---

## COMPLETE EXAMPLES

### Example 1: Social Media Post Generator

```creatorlang
image "InstagramPost":
    size 1080x1080
    background gradient(#ff6b6b, #4ecdc4)
    
    # Main content
    rectangle:
        position center
        size 900x900
        color white
        corner_radius 20px
        shadow 0 10px 40px rgba(0,0,0,0.2)
    
    # Quote
    text "The future\nbelongs to those\nwho believe":
        position (540, 400)
        align center
        font "Georgia Italic" 48px
        color #2d3436
        line_height 1.4
    
    # Author
    text "- Eleanor Roosevelt":
        position (540, 650)
        align center
        font "Georgia" 24px
        color #636e72
    
    # Branding
    text "@YourBrand":
        position (540, 950)
        font "Arial Bold" 20px
        color #6c5ce7
    
    export "instagram_quote.jpg" quality 95
```

### Example 2: Animated Logo Video

```creatorlang
video "LogoAnimation":
    duration 5 seconds
    fps 60
    size 1920x1080
    background white
    
    # Logo parts animate in sequence
    circle "logo_circle":
        position center
        radius 0 to 150
        color #6366f1
        animation grow
        duration 1s
        easing ease_out
    
    text "BRAND":
        position center
        font "Arial Black" 72px
        color white
        opacity 0 to 1
        animation fade_in
        delay 1s
        duration 0.5s
    
    text "Your Tagline Here":
        position center_bottom
        margin 200px
        font Arial 24px
        color #6366f1
        animation slide_up
        delay 1.5s
    
    # Camera zoom out effect
    camera:
        zoom 1.5 to 1.0
        duration 2s
        delay 3s
    
    export "logo_animation.mp4"
```

### Example 3: Product 3D Model

```creatorlang
model3d "CoffeeC
