"""Development server entry point.

Usage:
    python run.py
"""
from src import create_app


def main() -> None:
    """Boot the development server."""
    app = create_app()
    app.run(debug=True, host="127.0.0.1", port=5000)


app = create_app()

if __name__ == "__main__":
    main()