import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from rich.progress import Progress

log = logging.getLogger(__name__)

def extract_text_from_url(url: str, pages: int, progress: Progress) -> str:
    """
    Mengekstraksi teks dari dokumen PDF yang di-host di Google Drive menggunakan Selenium.

    Fungsi ini membuka URL yang diberikan, mencari iframe viewer PDF, melakukan scrolling
    otomatis sesuai jumlah halaman yang ditentukan, lalu mengekstrak seluruh teks dari halaman.
    Kemajuan proses ditampilkan melalui objek `Progress` dari Rich.

    Args:
        url (str): URL dokumen Google Drive yang berisi PDF.
        pages (int): Jumlah halaman untuk diskroll guna memuat konten.
        progress (Progress): Objek Rich Progress untuk menampilkan status eksekusi.

    Returns:
        str: Teks mentah yang diekstraksi dari halaman web.
    """
    task_id = progress.add_task("[cyan]Initializing WebDriver...", total=None)

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-plugins")
    options.add_argument("--disable-extensions")
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    raw_text = ""

    try:
        progress.update(task_id, description="[cyan]Opening Google Drive URL...")
        driver.get(url)
        time.sleep(10)

        progress.update(task_id, description="[cyan]Searching for PDF viewer iframe...")
        log.info("Looking for PDF viewer iframe...")

        iframe_selectors = [
            "iframe[src*='drive.google.com/uc?export']",
            "iframe[src*='drive.google.com/viewer']",
            "iframe[src*='/viewer']",
            "iframe[src*='pdf']",
            "iframe"
        ]

        pdf_iframe = None
        for selector in iframe_selectors:
            try:
                pdf_iframe = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                log.info(f"Found iframe with selector: {selector}")
                break
            except TimeoutException:
                log.warning(f"Selector '{selector}' not found, trying next.")
                continue

        if pdf_iframe:
            driver.switch_to.frame(pdf_iframe)
            log.info("Switched to PDF viewer iframe.")
            time.sleep(8)

            progress.update(task_id, description="[cyan]Scrolling to load all pages...")
            log.info(f"Scrolling based on user input for {pages} pages...")

            actions = ActionChains(driver)

            scroll_task = progress.add_task("Scrolling...", total=pages)
            for i in range(pages):
                actions.send_keys(Keys.PAGE_DOWN).perform()
                time.sleep(1.5)
                progress.update(scroll_task, advance=1, description=f"[cyan]Scroll {i + 1}/{pages}")
            progress.remove_task(scroll_task)
        else:
            log.warning("Could not find PDF viewer iframe, will try to extract from main document.")
            driver.switch_to.default_content()

        time.sleep(5)

        driver.switch_to.default_content()

        progress.update(task_id, description="[cyan]Extracting text content...")
        body_element = driver.find_element(By.TAG_NAME, "body")
        raw_text = body_element.get_attribute("textContent")
        log.info(f"Successfully extracted {len(raw_text)} raw characters.")
    except Exception as e:
        log.error(f"An error occurred during extraction: {e}", exc_info=True)

    finally:
        progress.update(task_id, description="[green]Finalizing...", total=1, completed=1)
        driver.quit()
        log.info("WebDriver has been closed.")

    return raw_text