import os
import sys

# Ensure project root is on sys.path when running `python app/main.py`
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.ui import build_ui


def main() -> None:
    """Entry point script for launching the SortSmart application."""
    demo = build_ui()
    demo.launch(server_name="127.0.0.1", server_port=7860)


if __name__ == "__main__":
    main()