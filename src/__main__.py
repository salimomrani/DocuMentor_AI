"""Main CLI for DocuMentor AI."""

import sys


def main() -> None:
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python -m src <command>")
        print("Commands:")
        print("  scrape    - Scrape Angular documentation")
        print("  index     - Index documents into vector store")
        print("  run       - Run the Streamlit app")
        sys.exit(1)

    command = sys.argv[1]

    if command == "scrape":
        from src.scraper.angular_scraper import main as scraper_main

        scraper_main()

    elif command == "index":
        from src.rag.indexer import index_documents

        index_documents()

    elif command == "run":
        import subprocess

        subprocess.run([".venv/bin/streamlit", "run", "src/ui/app.py"])

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
