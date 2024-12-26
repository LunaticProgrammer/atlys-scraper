from fastapi import FastAPI, Depends, HTTPException, Header
from typing import Optional
from config import ScrapingConfig
from scraper.scraper import Scraper
from storage.json_storage import JsonStorage
from notifications.console_notifier import ConsoleNotifier
from cache.redis_cache import RedisCache

app = FastAPI()
redis_cache = RedisCache()

async def verify_token(authorization: str = Header(...)):
    token = authorization.split('Bearer ')[-1]
    if token != "your-static-token":
        raise HTTPException(status_code=401, detail="Invalid token")
    return token

@app.post("/scrape")
async def scrape_products(
    page_limit: Optional[int] = 5,
    proxy: Optional[str] = None,
    token: Optional[str] = None
):
    config = ScrapingConfig(
        base_url="https://dentalstall.com/shop",
        auth_token=token,
        page_limit=page_limit,
        proxy=proxy
    )

    storage = JsonStorage()
    notifier = ConsoleNotifier()
    
    try:
        async with Scraper(config) as scraper:
            products = await scraper.scrape()
        
        # Process products through cache
        updated_products = []
        for product in products:
            cached_price = redis_cache.get_price(product.product_title)
            if cached_price is None or cached_price != product.product_price:
                updated_products.append(product)
                redis_cache.set_price(product.product_title, product.product_price)
        
        # Save to storage
        await storage.save_products(updated_products)
        
        # Send notification
        message = f"Scraping completed. Total products scraped: {len(products)}. Updated products: {len(updated_products)}"
        await notifier.notify(message)
        
        return {"status": "success", "message": message}
    
    except Exception as e:
        print(e)
        error_message = f"Scraping failed: {str(e)}"
        await notifier.notify(error_message)
        raise HTTPException(status_code=500, detail=error_message)