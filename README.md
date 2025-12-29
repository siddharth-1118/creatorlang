# creatorlang
A unified creative language to generate images, videos, and 3D models using simple, intuitive syntax. One language for all your creative content.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/siddharth-1118/creatorlang.git
cd creatorlang
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Run the compiler:

```bash
python compiler.py examples/simple_test.create
```

This will:
- Parse your .create file
- Generate output images/videos
- Save results to the `output/` folder

### Try the Doraemon animation:

```bash
python compiler.py examples/doraemon_animation.create
```

## Example

Here's a simple CreatorLang program:

```creatorlang
CREATE SHAPE AS circle {
  type: "circle",
  radius: 50,
  color: "blue"
}

SCENE main {
  background: "white",
  width: 800,
  height: 600
}

RENDER main
```

## Features

- 🎨 Create images with simple syntax
- 🎬 Generate animated videos
- 🎯 Build 3D models
- 📝 Intuitive, readable code

For detailed syntax and more examples, see [CREATORLANG_SPEC.md](CREATORLANG_SPEC.md)
