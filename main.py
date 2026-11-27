import logging
from src.scraper import ProductScraper
from src.processor import DataProcessor
from src.reporter import ReportGenerator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def run_pipeline(max_pages: int = 3) -> None:
    logging.info("شروع فرآیند جامع استخراج و پردازش داده‌ها...")

    scraper = ProductScraper()
    processor = DataProcessor()
    reporter = ReportGenerator(output_dir="outputs")

    # ۱. استخراج داده‌ها از صفحات وب
    raw_products = scraper.scrape_pages(max_pages=max_pages)
    if not raw_products:
        logging.error("هیچ محصولی استخراج نشد؛ فرآیند متوقف شد.")
        return

    # ۲. پاک‌سازی و استانداردسازی داده‌ها
    cleaned_df = processor.clean_data(raw_products)

    # ۳. تولید گزارش‌های Excel و CSV
    exported_files = reporter.export(cleaned_df, prefix="market_prices")
    logging.info(f"فرآیند با موفقیت کامل شد. فایل‌های خروجی: {exported_files}")


if __name__ == "__main__":
    run_pipeline(max_pages=3)
