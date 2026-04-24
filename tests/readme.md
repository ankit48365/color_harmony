## tests layout

`test_color_harmony.py` verifies the refactored hue-bucket computation still classifies pixels correctly after the logic split into `src/*.py` modules.

`conftest.py` adds the `src/` directory to `sys.path` so tests can import the top-level modules directly.
