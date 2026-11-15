from src.processor import DataProcessor
from src.reporter import ExcelReporter
from src.scraper import DataScraper


def main():
  print("--- شروع فرآیند اتوماسیون داده ---")

  # ۱. استخراج داده‌ها
  target_url = "https://example.com"
  scraper = DataScraper(target_url)
  raw_data = scraper.fetch_data()

  if not raw_data:
    print("هیچ داده‌ای دریافت نشد. عملیات متوقف شد.")
    return

  # ۲. پردازش و تمیزکاری داده‌ها
  processor = DataProcessor(raw_data)
  processed_df = processor.clean_and_process()

  # ۳. تولید گزارش نهایی اکسل
  reporter = ExcelReporter(processed_df)
  reporter.generate_excel_report("products_report.xlsx")

  print("--- اتوماسیون با موفقیت به پایان رسید ---")


if __name__ == "__main__":
  main()