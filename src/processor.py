import re
import logging
import pandas as pd


class DataProcessor:
    """پاک‌سازی، استانداردسازی و تحلیل داده‌های استخراج‌شده با Pandas"""

    RATING_MAP = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5,
    }

    def clean_data(self, raw_items: list[dict]) -> pd.DataFrame:
        if not raw_items:
            logging.warning("هیچ داده‌ای برای پردازش دریافت نشد.")
            return pd.DataFrame()

        df = pd.DataFrame(raw_items)

        # حذف ردیف‌های تکراری بر اساس لینک یا عنوان محصول
        df.drop_duplicates(subset=["url"], keep="first", inplace=True)

        # استخراج عدد خالص از قیمت متنی (مثلاً تبدیل £51.77 به 51.77)
        df["price_numeric"] = (
            df["raw_price"]
            .astype(str)
            .apply(lambda x: re.sub(r"[^\d.]", "", x))
        )
        df["price_numeric"] = pd.to_numeric(df["price_numeric"], errors="coerce").fillna(0.0)

        # استانداردسازی وضعیت موجودی
        df["in_stock"] = df["availability"].str.contains("In stock", case=False, na=False)

        # تبدیل امتیاز ستاره‌ها به عدد ۱ تا ۵
        df["rating_score"] = df["rating"].map(self.RATING_MAP).fillna(0).astype(int)

        # مرتب‌سازی بر اساس قیمت از ارزان‌ترین به گران‌ترین
        df.sort_values(by="price_numeric", ascending=True, inplace=True)
        df.reset_index(drop=True, inplace=True)

        # انتخاب و مرتب‌سازی ستون‌های نهایی
        final_columns = [
            "title",
            "price_numeric",
            "in_stock",
            "rating_score",
            "availability",
            "url",
        ]
        logging.info(f"تعداد {len(df)} رکورد تمیز و استاندارد آماده شد.")
        return df[final_columns]
