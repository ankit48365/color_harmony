# Design Notes

## Refactor goal

The original implementation placed UI creation, image loading, hue analysis, and plotting inside one file: `src/color_harmony/app.py`.

The codebase now uses a flatter `src/` layout so each behavior is easier to read, test, and replace:

- `src/app.py` is the single launcher.
- `src/gradio_app.py` owns the Gradio view tree and event bindings.
- `src/load_image.py`, `src/refresh_histogram.py`, and `src/reset_app.py` are callback modules for UI state transitions.
- `src/compute_hue_statistics.py`, `src/build_histogram.py`, and `src/hue_label.py` are analysis and visualization helpers.

## Interface contract style

Each module now includes explicit type hints and a short docstring with:

- `Args`: the inputs expected by the public function.
- `Returns`: the exact object or tuple returned to callers.

That keeps callback boundaries clear, especially for Gradio functions that return multiple UI updates at once.
