import logging
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from src.fetcher import WebFetcher


class ProductScraper:
    """موتور استخراج اطلاعات محصولات و پیمایش خودکار صفحات (Pagination)"""

    BASE_URL = "https://books.toscrape.com/"

    def __init__(self, fetcher: WebFetcher | None = None):
        self.fetcher = fetcher or WebFetcher()

    def parse_products(self, html: str, page_url: str) -> list[dict]:
        soup = BeautifulSoup(html, "html.parser")
        products = []

        for item in soup.select("article.product_pod"):
            title_tag = item.select_one("h3 a")
            price_tag = item.select_one("p.price_color")
            stock_tag = item.select_one("p.instock.availability")
            rating_tag = item.select_one("p.star-rating")

            title = title_tag["title"].strip() if title_tag and title_tag.has_attr("title") else "N/A"
            relative_link = title_tag["href"] if title_tag and title_tag.has_attr("href") else ""
            full_link = urljoin(page_url, relative_link)
            raw_price = price_tag.get_text(strip=True) if price_tag else "0"
            availability = stock_tag.get_text(strip=True) if stock_tag else "Unknown"

            rating = "N/A"
            if rating_tag and rating_tag.has_attr("class"):
                classes = [c for c in rating_tag["class"] if c != "star-rating"]
                rating = classes[0] if classes else "N/A"

            products.append({
                "title": title,
                "raw_price": raw_price,
                "availability": availability,
                "rating": rating,
                "url": full_link,
            })

        return products

    def get_next_page_url(self, html: str, current_url: str) -> str | None:
        soup = BeautifulSoup(html, "html.parser")
        next_button = soup.select_one("li.next a")
        if next_button and next_button.has_attr("href"):
            return urljoin(current_url, next_button["href"])
        return None

    def scrape_pages(self, start_url: str = BASE_URL, max_pages: int = 3) -> list[dict]:
        all_products = []
        current_url = start_url
        page_count = 0

        while current_url and page_count < max_pages:
            page_count += 1
            logging.info(f"در حال پردازش صفحه {page_count} از حداکثر {max_pages}...")
            html = self.fetcher.get_page(current_url)
            if not html:
                break

            page_items = self.parse_products(html, current_url)
            all_products.extend(page_items)
            logging.info(f"{len(page_items)} محصول از صفحه {page_count} استخراج شد.")

            current_url = self.get_next_page_url(html, current_url)

        logging.info(f"استخراج به پایان رسید. مجموع محصولات: {len(all_products)}")
        return all_products
