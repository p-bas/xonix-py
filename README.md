# xonix-py
Recreating a video game from the childhood memory

## Requirements
- Python 3.8+
- pygame >= 2.1

## Installation
1. Create a virtual environment:

	python -m venv .venv

2. Activate the environment and install dependencies:

	# Windows (PowerShell)
	.venv\Scripts\Activate.ps1
	pip install -r requirements.txt

	# macOS / Linux
	source .venv/bin/activate
	pip install -r requirements.txt

## Running
Run the game with:

```
python app.py
```

## Controls
- Arrow keys: move the player
- R: restart level when dead or to advance on win screen
- ESC: quit

## Notes
- Audio assets are in the `sounds/` folder. If a sound fails to load the game will continue but without that sound.
- Grid and game constants are defined in `app.py`; consider refactoring into modules for tests and maintainability.

## Development
- Consider adding unit tests for non-UI logic (`flood_fill`, `calculate_coverage`) and a CI workflow.
- See `copilot.log` for automated assistant actions performed during development.

## License
This repository is provided as-is.
