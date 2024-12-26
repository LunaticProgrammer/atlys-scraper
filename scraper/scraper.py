import httpx
import asyncio
from bs4 import BeautifulSoup
from typing import List, Optional
from models import Product
from config import ScrapingConfig

class Scraper:
    def __init__(self, config: ScrapingConfig):
        self.config = config
        self.client = httpx.AsyncClient(proxy=self.config.proxy)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    async def _fetch_page(self, page_number: int) -> Optional[str]:
        headers = {'Authorization': f'Bearer {self.config.auth_token}'}

        for attempt in range(self.config.retry_attempts):
            try:
                if page_number==1:
                    url = f"{self.config.base_url}"
                else:
                    url = f"{self.config.base_url}/page/{page_number}"
                response = await self.client.get(url, headers=headers)
                print(response)
                response.raise_for_status()
                return response.text
            except httpx.HTTPError as e:
                print(e)
                if attempt == self.config.retry_attempts - 1:
                    raise e
                await asyncio.sleep(self.config.retry_delay)

    async def _parse_page(self, html: str) -> List[Product]:
        soup = BeautifulSoup(html, 'html.parser')
        products = []
        
        for product_elem in soup.find_all('div', class_='product-inner'):
            title = product_elem.find('h2').text.strip()
            price = float(product_elem.find('span', class_='amount').text.strip().replace('₹', ''))
            image_url = product_elem.find('img')["data-lazy-src"]
            
            products.append(Product(
                product_title=title,
                product_price=price,
                path_to_image=image_url
            ))
        
        return products

    async def scrape(self) -> List[Product]:
        all_products = []
        page = 1

        while True:
            if self.config.page_limit and page > self.config.page_limit:
                break

            try:
                html = await self._fetch_page(page)
                products = await self._parse_page(html)
                
                if not products:
                    break
                
                all_products.extend(products)
                page += 1
            except Exception as e:
                print(e)
                print(f"Error scraping page {page}: {str(e)}")
                page+=1
                continue

        return all_products

