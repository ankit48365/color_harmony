# color_harmony

![coverage](https://img.shields.io/badge/coverage-67.00%25-blue)
![pylint](https://img.shields.io/badge/pylint-7.44-green)

Small Gradio app for uploading a JPG, choosing `X` hue classes, and viewing a pixel-count histogram for the closest color buckets.

## Run

```powershell
uv sync
uv run color-harmony
```

## Test

```powershell
uv run pytest
```

## Source layout

- `src/app.py` launches the Gradio experience.
- `src/gradio_app.py` builds the interface and wires event callbacks.
- `src/compute_hue_statistics.py`, `src/build_histogram.py`, and `src/hue_label.py` hold the color-analysis logic.
- `src/load_image.py`, `src/refresh_histogram.py`, and `src/reset_app.py` handle UI callback behavior.

More detail lives in `docs/gradio-ui.md` and `docs/design.md`.
