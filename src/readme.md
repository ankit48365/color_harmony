## src layout

The application code now lives as small top-level modules inside `src/` instead of one package directory.

- `app.py` is the runtime entrypoint and launches the Gradio app.
- `gradio_app.py` defines the Blocks UI, CSS, and callback wiring.
- `app_config.py` keeps shared configuration such as `DEFAULT_BUCKETS`.
- `hue_label.py` maps hue centers to readable labels.
- `compute_hue_statistics.py` converts RGB pixels into bucket counts, labels, and display colors.
- `build_histogram.py` renders the Matplotlib histogram figure.
- `load_image.py` loads uploads and returns the initial UI state updates.
- `refresh_histogram.py` rebuilds the plot when the slider changes.
- `reset_app.py` clears the interface back to its initial state.

Each module exposes a narrow function surface and uses type hints plus docstrings to state its expected inputs and outputs.
