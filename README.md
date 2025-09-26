# Opal C1 Linux Controls

Working camera controls for the Opal C1 webcam on Linux using the depthai framework.

> **Note**: This project is specifically for Linux. The Opal C1 works differently on Windows/macOS.

## Features

✅ **Manual Focus Control** - Disable auto focus for stable video calls  
✅ **Cross-Application** - Settings persist across Zoom, Teams, OBS, etc.  
✅ **Simple CLI** - Easy command-line interface  
✅ **GUI Interface** - User-friendly graphical controls  
🚧 **Advanced Controls** - Exposure and white balance coming soon  

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/opal-c1-linux-controls
cd opal-c1-linux-controls

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Usage

**GUI Interface (Recommended):**
```bash
python opal_gui.py
```

**Disable Auto Focus (CLI):**
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

- **Linux** (tested on Ubuntu 24.04)
- Python 3.8+
- Opal C1 camera connected via USB
- depthai framework
- OpenCV

## Platform Notes

This solution is Linux-specific because:
- Uses V4L2/UVC interface for video streaming
- Requires depthai framework for camera controls
- Linux-specific USB device handling

For Windows users, the official Opal software may provide similar controls.

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
