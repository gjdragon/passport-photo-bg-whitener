# Passport Photo Editor
A desktop application to enhance and edit photos for passport, visa, and official documents with real-time preview and preset configurations.

---
## Screenshot
![Screenshot](res/screenshot.png)

---
## Features
- Real-time image preview with live adjustments
- 4 adjustment sliders: Brightness, Contrast, Saturation, Sharpness
- 4 preset profiles: Passport, Visa, Bright, Neutral
- Support for JPG, PNG, BMP, and GIF formats
- High-quality output (95% quality)
- Simple and intuitive UI

---
## Installation

### 1. Create and activate a virtual environment
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

### 2. Install dependencies
```bash
python.exe -m pip install --upgrade pip
pip install pillow
```

### 3. Run the application
```bash
python src/main.py
```

### 4. Package the application (optional)
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=res/icon.ico src/main.py
```

---
## Usage
1. Click **Open Image** to load a photo
2. Adjust sliders for Brightness, Contrast, Saturation, and Sharpness
3. Use preset buttons for quick enhancements (Passport, Visa, Bright, Neutral)
4. Preview changes in real-time on the left panel
5. Click **Save Image** to export your edited photo
6. Use **Reset** to return to default settings

---
## License
MIT