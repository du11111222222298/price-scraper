import os
import logging
from datetime import datetime
import pandas as pd


class ReportGenerator:
    """تولید گزارش‌های خروجی در قالب Excel (.xlsx) و CSV"""

    def __init__(self, output_dir: str = "outputs"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def export(self, df: pd.DataFrame, prefix: str = "market_prices") -> dict[str, str]:
        if df.empty:
            logging.warning("جدول داده‌ها خالی است؛ فایلی ذخیره نشد.")
            return {}

        timestamp = datetime.now().strftime("%Y-%m-%d")
        csv_path = os.path.join(self.output_dir, f"{prefix}_{timestamp}.csv")
        excel_path = os.path.join(self.output_dir, f"{prefix}_{timestamp}.xlsx")

        # ذخیره نسخه CSV با پشتیبانی کامل از کاراکترهای UTF-8
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")

        # ذخیره نسخه Excel با تنظیم خودکار عرض ستون‌ها
        with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Prices")
            worksheet = writer.sheets["Prices"]
            for column_cells in worksheet.columns:
                max_length = max(len(str(cell.value or "")) for cell in column_cells)
                adjusted_width = min(max_length + 4, 60)
                worksheet.column_dimensions[column_cells[0].column_letter].width = adjusted_width

        logging.info(f"گزارش‌ها با موفقیت ذخیره شدند: {excel_path} و {csv_path}")
        return {"csv": csv_path, "excel": excel_path}
