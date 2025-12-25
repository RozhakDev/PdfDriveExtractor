import logging
from rich.logging import RichHandler

def setup_logging():
    """
    Mengatur konfigurasi logging aplikasi dengan tampilan yang lebih informatif.
    Fungsi ini menggunakan `RichHandler` untuk memberikan output log yang rapi
    dan mudah dibaca selama pengembangan.
    """
    logging.basicConfig(
        level="INFO",
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, show_path=False)]
    )