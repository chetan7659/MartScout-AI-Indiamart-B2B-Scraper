import requests
import logging
from bs4 import BeautifulSoup
from Products.product import ScrapedProduct
from Helpers.utils import get_scrapeops_url

logger= logging.getLogger(__name__)

def search_products(product_name: str, page_number: int=1, location:str="us", retries: int=2, data_pipeline=None):
    scraped_products= []
    attempts =0
    success = False

    # Indiamart URL structure
    # Standard: https://dir.indiamart.com/search.mp?ss=laptop
    # With City: https://dir.indiamart.com/search.mp?ss=laptop&cq=Delhi
    
    # We map 'location' properly. If 'us', we ignore it (default). If mapped to a city, we use it.
    # For now, let's keep it simple.
    
    base_url = f"https://dir.indiamart.com/search.mp?ss={product_name}"
    if location and location.lower() != "us":
        base_url += f"&cq={location}"
        
    # Indiamart doesn't strictly follow page numbers in the URL like Amazon (page=2).
    # It uses 'start' parameter sometimes or just pagination links. 
    # For MVP we scrape the first page.

    while attempts < retries and not success:
        try: 
            search_url = get_scrapeops_url(base_url, location="in") # Use 'in' (India) for ScrapeOps
            logger.info ( f" Fetching: {search_url}")
            
            response= requests.get(search_url)
            if response.status_code!=200:
                raise Exception (f"Status code: { response.status_code}. Response: {response.text}")
            
            logger.info( "Successfull fetched page")
            soup= BeautifulSoup( response.text, "html.parser")
            
            # Indiamart Card Selector (Tailwind classes)
            # finding divs that look like cards
            def is_card(class_val):
                return class_val and "bg-white" in class_val and "rounded-lg" in class_val and "shadow-sm" in class_val and "border" in class_val
            
            product_cards = soup.find_all("div", class_=is_card)
            
            if not product_cards:
                 # Fallback for list view or different layout
                 product_cards = soup.find_all("div", class_=lambda x: x and "m-p" in x)

            for card in product_cards:
                try:
                    # Title
                    # Look for anchor with /products/ in href
                    title_anchor = card.find("a", href=lambda x: x and "/products/" in x)
                    if not title_anchor: continue
                    
                    product_title = title_anchor.text.strip()
                    product_url = "https://dir.indiamart.com" + title_anchor.get("href") if title_anchor.get("href").startswith("/") else title_anchor.get("href")
                    
                    # ID
                    # Extract from params if possible or generic
                    name = "unknown"
                    if "id=" in product_url:
                        import re
                        match = re.search(r"id=(\d+)", product_url)
                        if match: name = match.group(1)

                    # Price
                    # Look for element with currency symbol or price class
                    current_price = 0.0
                    currency = "₹"
                    price_element = card.find(lambda tag: tag.name in ["p", "span"] and "₹" in tag.text)
                    
                    if price_element:
                        price_text = price_element.text.strip()
                        # Clean price: "₹ 28,000" -> 28000.0
                        clean_price = price_text.replace("₹", "").replace(",", "").replace("Rs", "").strip()
                        try:
                            current_price = float(clean_price)
                        except:
                            current_price = 0.0
                            
                    # Company
                    # Look for anchor with /company/
                    company_anchor = card.find("a", href=lambda x: x and "/company/" in x)
                    company_name = company_anchor.text.strip() if company_anchor else "Unknown Company"
                    
                    # Rating
                    rating = 0.0
                    # Look for a bold number usually 3.x to 5.x
                    # or the star span
                    # class_ can be a list in bs4
                    def is_rating_span(tag):
                        if tag.name != "span": return False
                        classes = tag.get("class", [])
                        if "font-bold" in classes:
                            text = tag.text.strip()
                            return len(text) <= 4 and ("." in text)
                        return False

                    rating_span = card.find(is_rating_span)
                    if rating_span:
                        try:
                             val = float(rating_span.text.strip())
                             if 0 < val <= 5: rating = val
                        except:
                            rating = 0.0
                            
                    is_sponsored = False 

                    product = ScrapedProduct(
                        name=name, 
                        product_title=product_title,
                        product_url=product_url,
                        current_price=current_price,
                        original_price=current_price, 
                        currency=currency,
                        rating=rating,
                        is_sponsored=is_sponsored,
                        company_name=company_name
                    )
                    data_pipeline.add_data(product)
                    
                except Exception as e:
                    logger.warning(f"Error parsing card: {e}")
                    continue
            
            success = True

        except Exception as e: 
            logger.warning(f"Attempts {attempts +1 } failed: {e}")
            attempts+=1
    
    if not success:
        logger.error(" scraping failed")
    

    return scraped_products