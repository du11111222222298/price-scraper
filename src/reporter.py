import os
import pandas as pd


class ExcelReporter:

  def __init__(self, df, output_dir="outputs"):
    self.df = df
    self.output_dir = output_dir
    # اطمینان از اینکه پوشه خروجی وجود دارد
    os.makedirs(self.output_dir, exist_ok=True)

  def generate_excel_report(self, filename="final_report.xlsx"):
    """ذخیره دیتافریم پانداس به صورت فایل اکسل در پوشه خروجی"""
    if self.df.empty:
      print("داده‌ای برای تولید گزارش اکسل وجود ندارد!")
      return

    file_path = os.path.join(self.output_dir, filename)

    try:
      # ذخیره در فایل اکسل بدون ایندکس اضافی
      self.df.to_excel(file_path, index=False, engine="openpyxl")
      print(f"گزارش اکسل با موفقیت در مسیر '{file_path}' ذخیره شد.")
    except Exception as e:
      print(f"خطا در ایجاد فایل اکسل: {e}")


if __name__ == "__main__":
  sample_df = pd.DataFrame([
      {"title": "Data Science Handbook", "price": 250, "category": "Books"},
      {"title": "Python Programming", "price": 150, "category": "Books"},
  ])
  reporter = ExcelReporter(sample_df)
  reporter.generate_excel_report()