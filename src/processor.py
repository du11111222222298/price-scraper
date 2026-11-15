import pandas as pd


class DataProcessor:

  def __init__(self, raw_data):
    self.df = pd.DataFrame(raw_data)

  def clean_and_process(self):
    """پردازش و تمیزکاری داده‌ها، حذف مقادیر تکراری و محاسبات آماری"""
    if self.df.empty:
      print("داده‌ای برای پردازش وجود ندارد!")
      return self.df

    # حذف رکوردهای تکراری احتمالی
    self.df.drop_duplicates(inplace=True)

    # مرتب‌سازی بر اساس قیمت (از زیاد به کم)
    if "price" in self.df.columns:
      self.df.sort_values(by="price", ascending=False, inplace=True)

    print("داده‌ها با موفقیت پردازش و تمیزسازی شدند.")
    return self.df


if __name__ == "__main__":
  sample = [
      {"title": "Python Programming", "price": 150, "category": "Books"},
      {"title": "Data Science Handbook", "price": 250, "category": "Books"},
  ]
  processor = DataProcessor(sample)
  print(processor.clean_and_process())