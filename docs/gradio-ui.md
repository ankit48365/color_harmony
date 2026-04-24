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
- `src/color_harmony/` contains the Gradio application package.
- `tests/` contains unit tests for hue-bucket classification.
