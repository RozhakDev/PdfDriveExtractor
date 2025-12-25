import logging
from pathlib import Path
from rich.console import Console

log = logging.getLogger(__name__)

def save_text_to_file(content: str, filename: str, console: Console):
    """
    Menyimpan teks ke file dengan penanganan error dan notifikasi melalui console.

    Fungsi ini menulis string `content` ke file yang ditentukan oleh `filename`,
    menggunakan encoding UTF-8. Jika operasi berhasil, pesan sukses ditampilkan
    melalui objek `console`. Jika terjadi kesalahan I/O, error tersebut dicatat
    ke logger dengan level error.

    Args:
        content (str): Teks yang akan disimpan ke file.
        filename (str): Nama atau path file tujuan penyimpanan.
        console (Console): Objek Rich Console untuk menampilkan pesan ke pengguna.
    """
    try:
        output_path = Path(filename)
        output_path.write_text(content, encoding="utf-8")
        console.print(f"Successfully saved content to [bold green]{filename}[/bold green]")
    except IOError as e:
        log.error(f"Failed to write to file {filename}: {e}")