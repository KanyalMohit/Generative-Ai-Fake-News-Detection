# Truth Lens Desktop GUI

This folder contains a more premium desktop interface for the fake news detection backend.

## Highlights

- Native desktop-style GUI using **PySide6**
- Modern dark visual design with:
  - visual mode cards
  - result hero section
  - metric chips
  - activity panel
  - stronger verdict color states
- Modes for:
  - Text
  - URL
  - Image
  - Video
- Connects to the backend gateway at:
  - `http://127.0.0.1:8000`

## Setup

Open a terminal in `desktopgui/` and run:

```bash
pip install -r requirements.txt
python main.py
```

## Important

The backend gateway/content/video services must already be running.
This GUI talks to the API rather than embedding backend logic directly.

Default API target:

- `http://127.0.0.1:8000`

Optional override:

```bash
set TRUTH_LENS_API=http://127.0.0.1:8000
python main.py
```
