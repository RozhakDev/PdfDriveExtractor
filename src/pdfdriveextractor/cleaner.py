import re
import logging

log = logging.getLogger(__name__)

def clean_text(text: str) -> str:
    """
    Membersihkan teks dari elemen non-esensial seperti metadata, UI, atau artefak ekstraksi.
    Fungsi ini menyaring baris berdasarkan panjang, pola teks, dan konten umum Google Drive,
    lalu menghapus struktur JSON-like dan baris kosong berlebih.

    Args:
        text (str): Teks mentah yang akan dibersihkan.

    Returns:
        str: Teks bersih yang siap digunakan.
    """
    if not text:
        return ""
    
    log.info("Starting text cleaning process...")

    lines = text.split('\n')

    filtered_lines = []
    for line in lines:
        line = re.sub(r'\s+', ' ', line).strip()

        if (len(line) > 15 and
            line.count(' ') >= 2 and
            not re.match(r'^[A-Z][a-z]+$', line) and
            not re.match(r'^[A-Z]{2,}\s+[A-Z]{2,}$', line) and
            not re.match(r'^\d+\s+dari\s+\d+$', line) and
            not re.search(r'gstatic|google\.com|_DRIVE|og\.asy|_initStaticViewer|AA2YrT|CONFIG|\{.*?\}|= \[.*\]', line, re.IGNORECASE) and
            not re.search(r'Pencetakan|Zoom|Sembunyikan|Tampilkan panel|Lihat Detail|Minta peninjauan', line) and
            not re.search(r'Simple View|Fit to Width|Full Screen|Actual Size', line, re.IGNORECASE) and
            not line.isupper()
        ):
            filtered_lines.append(line)

    cleaned_text = '\n'.join(filtered_lines)

    cleaned_text = re.sub(r'\{.*?"id".*?"mimeType".*?\}', '', cleaned_text)

    patterns_to_remove = [
        r'\[.*\];Halaman \d+ dari \d+',
        r'= \[.*\];',
        r'\w+\[.*?\]=.*?;',
        r'Sheet samping.*?Tutup',
    ]

    for pattern in patterns_to_remove:
        cleaned_text = re.sub(pattern, '', cleaned_text, flags=re.MULTILINE | re.IGNORECASE)

    cleaned_text = re.sub(r'\n\s*\n\s*\n', '\n\n', cleaned_text)

    log.info(f"Text cleaning finished. Original length: {len(text)}, Cleaned length: {len(cleaned_text.strip())}")

    return cleaned_text.strip()