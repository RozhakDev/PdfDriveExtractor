# PdfDriveExtractor

PdfDriveExtractor is a minimal, CLI-first tool for extracting **clean and readable text** from **view-only Google Drive PDF files**.

This project is designed for situations where PDFs cannot be downloaded directly (e.g. locked lecture materials), but their textual content still needs to be analyzed, archived, or processed further.

## Features

* **Extracts text from view-only Google Drive PDFs** with automatic page scrolling
* **Cleans content** by removing UI elements, metadata, and noise
* **CLI-first and automation-friendly**, producing raw and cleaned text outputs

## Installation

This project uses **Poetry** for dependency management.

### Standard Installation (Recommended)

```bash
poetry install
```

### Workaround for Unstable Connections

If you experience network or DNS issues during `poetry install` (e.g. failing to download `mdurl`), you can use the following workaround:

```bash
poetry install --no-root
poetry run pip install -e .
```

This installs dependencies and registers the package locally for development.

## Usage

Run the tool via Poetry:

```bash
poetry run pdfdrive-extractor --url "https://drive.google.com/file/d/your-file-id/view"
```

This will generate:

* `materi_clean.txt` — cleaned, readable text
* `materi_raw.txt` — raw extracted text (for debugging)

### Custom Output Files

```bash
poetry run pdfdrive-extractor \
  --url "https://drive.google.com/file/d/your-file-id/view" \
  --output-clean clean.txt \
  --output-raw raw.txt
```

### Long Documents

For long PDFs, specify how many scroll iterations should be performed to ensure all pages are loaded:

```bash
# Example for ~150 pages
poetry run pdfdrive-extractor --pages 155 --url "https://drive.google.com/file/d/your-file-id/view"
```

### Help

```bash
poetry run pdfdrive-extractor --help
```

## Project Structure

```text
pdfdriveextractor/
├─ cli.py        # CLI entry point
├─ extractor.py  # Selenium-based PDF text extraction
├─ cleaner.py    # Text cleaning and filtering logic
├─ writer.py     # Output handling
├─ utils.py      # Helpers
```

## Disclaimer

This tool is intended for **educational and personal use only**.
Ensure you respect copyright and institutional policies when extracting content from restricted documents.

## License

MIT License