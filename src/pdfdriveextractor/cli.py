import typer
from typing_extensions import Annotated
import logging
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

from pdfdriveextractor.utils import setup_logging
from pdfdriveextractor.extractor import extract_text_from_url
from pdfdriveextractor.cleaner import clean_text
from pdfdriveextractor.writer import save_text_to_file

console = Console()
log = logging.getLogger(__name__)

app = typer.Typer(
    name="PdfDriveExtractor",
    help="Extract clean text from a view-only Google Drive file.",
    add_completion=False,
    no_args_is_help=True,
)

def version_callback(value: bool):
    """
    Menampilkan versi aplikasi dan keluar jika opsi --version digunakan.
    Fungsi ini dipanggil secara otomatis oleh Typer saat pengguna memberikan
    argumen versi di CLI.
    """
    if value:
        console.print("[bold green]PdfDriveExtractor[/bold green] version: [cyan]1.0.0[/cyan]")
        raise typer.Exit()
    
@app.command()
def extract(
    url: Annotated[str, typer.Argument(
        help="The full URL of the view-only Google Drive file."
    )],
    pages: Annotated[int, typer.Option(
        "--pages", "-p",
        help="Set the number of pages/scrolls to perform. Increase for longer documents."
    )] = 25,
    output_clean: Annotated[str, typer.Option(
        "--output-clean", "-o",
        help="Filename for the cleaned text output."
    )] = "materi_clean.txt",
    output_raw: Annotated[str, typer.Option(
        "--output-raw", "-r",
        help="Filename for the raw text output for comparison."
    )] = "materi_raw.txt",
    version: Annotated[bool, typer.Option(
        "--version", "-v",
        callback=version_callback,
        is_eager=True,
        help="Show the application version and exit."
    )] = False,
):
    """
    Antarmuka CLI utama untuk PdfDriveExtractor — alat ekstraksi teks dari dokumen
    Google Drive yang hanya bisa dilihat (view-only).

    Fungsi `extract` menyediakan antarmuka berbasis perintah untuk:
    - Mengekstraksi teks mentah dari URL Google Drive,
    - Membersihkannya dari artefak UI dan metadata,
    - Menyimpan hasil dalam dua format: mentah dan bersih.

    Argumen dan opsi dikonfigurasi menggunakan Typer dengan dukungan Rich untuk
    tampilan terminal yang informatif dan interaktif.

    Args:
        url (str): URL lengkap dokumen Google Drive yang bersifat view-only.
        pages (int): Jumlah scroll halaman untuk memastikan seluruh konten dimuat.
        output_clean (str): Nama file output untuk teks yang telah dibersihkan.
        output_raw (str): Nama file output untuk teks mentah hasil ekstraksi.
        version (bool): Menampilkan versi aplikasi dan keluar jika diaktifkan.
    """
    setup_logging()

    console.print(Panel(
        "[bold green]PdfDriveExtractor[/bold green] | [cyan]Text Extraction Tool[/cyan]",
        title="Welcome",
        border_style="blue"
    ))
    log.info(f"Starting extraction for URL: {url}")
    console.print(f"Set to scroll for [bold cyan]{pages}[/bold cyan] pages. Adjust with --pages if needed.")

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            transient=True,
        ) as progress:
            raw_text = extract_text_from_url(url, pages, progress)

            if not raw_text:
                log.error("Extraction failed. No text was retrieved.")
                raise typer.Exit(code=1)
            
            save_text_to_file(raw_text, output_raw, console)

            cleaned_text = clean_text(raw_text)

            if cleaned_text:
                save_text_to_file(cleaned_text, output_clean, console)
                console.print(f"Process complete. Check '[bold green]{output_clean}[/bold green]' and '[bold yellow]{output_raw}[/bold yellow]'.")
            else:
                log.warning("Cleaning process resulted in empty text. Only raw file was saved.")
    except Exception as e:
        log.error(f"A critical error occurred: {e}", exc_info=True)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()