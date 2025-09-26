# Opal C1 Controls

Working camera controls for the Opal C1 webcam on Linux using the depthai framework.

## Features

✅ **Manual Focus Control** - Disable auto focus for stable video calls  
✅ **Cross-Application** - Settings persist across Zoom, Teams, OBS, etc.  
✅ **Simple CLI** - Easy command-line interface  
🚧 **GUI Controls** - Coming soon  

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/opal-c1-controls
cd opal-c1-controls

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Usage

**Disable Auto Focus (for video calls):**
```bash
python set_manual_focus.py
```

**Set Custom Focus Distance:**
```bash
python set_manual_focus.py 150  # Focus value 0-255
```

**Test Camera:**
```bash
python test_camera.py
```

## Background

The Opal C1 is a high-quality webcam that uses the depthai framework internally. While it works as a standard UVC camera, advanced controls like manual focus require using the depthai API to send control commands to the camera hardware.

This project provides a working solution for Linux users who want professional camera control, especially for disabling the distracting auto focus during video calls.

## Requirements

- Linux (tested on Ubuntu)
- Python 3.8+
- Opal C1 camera connected via USB
- depthai framework
- OpenCV

## Contributing

Contributions welcome! Planned features:
- GUI application for real-time control
- Exposure and white balance controls
- Camera presets/profiles
- System tray integration

## License

MIT License - see LICENSE file for details.

## Acknowledgments

Based on research from the [open-opal](https://github.com/cansik/open-opal) project by cansik.
