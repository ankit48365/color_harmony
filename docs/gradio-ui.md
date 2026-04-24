# Gradio UI

This project exposes a small Gradio application that does the following:

1. Accepts a `.jpg` image upload.
2. Shows the uploaded image and a redo button.
3. Lets the user pick an integer `X` from 3 to 30.
4. Buckets every pixel into the nearest hue class and plots the counts as a colored histogram.

## Bucket behavior

- `X = 3` uses hue centers for red, green, and blue.
- Higher `X` values split the full 360 degree hue wheel into evenly sized classes.
- Low-saturation pixels still inherit the hue reported by HSV conversion, so they end up in the nearest hue bucket.

## Project layout

- `assets/` is a good place for sample JPG inputs or reference images.
- `src/app.py` launches the app.
- `src/gradio_app.py` defines the Blocks interface and event wiring.
- `src/load_image.py`, `src/refresh_histogram.py`, and `src/reset_app.py` hold the Gradio callback logic.
- `src/compute_hue_statistics.py`, `src/build_histogram.py`, and `src/hue_label.py` hold the hue analysis logic.
- `tests/` contains unit tests for hue-bucket classification.
