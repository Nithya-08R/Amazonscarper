from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def scrape_amazon(search_query, max_pages=1, headless=True):
    """
    Simple Amazon Scraper: Extracts product name, price, rating, reviews, availability, and image URL.
    
    Parameters:
        search_query (str): The product search term to query on Amazon.
        max_pages (int): Number of pages to scrape (pagination).
        headless (bool): If True, run in headless mode; otherwise, show browser.

    Returns:
        list: A list of dictionaries containing product details (name, price, rating, reviews, availability, image URL).
    """
    # Set up Selenium
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    products = []

    for page in range(1, max_pages + 1):
        url = f'https://www.amazon.com/s?k={search_query}&page={page}'
        driver.get(url)
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        for item in soup.find_all('div', {'data-component-type': 's-search-result'}):
            # Extract name, price, rating, reviews, availability, and image URL
            name = item.h2.text.strip()
            price = item.find('span', 'a-price-whole').text.strip() if item.find('span', 'a-price-whole') else 'N/A'
            rating = item.find('span', 'a-icon-alt').text if item.find('span', 'a-icon-alt') else 'N/A'
            reviews = item.find('span', {'class': 'a-size-base'}).text.strip() if item.find('span', {'class': 'a-size-base'}) else 'N/A'
            
            # Amazon search results usually don't show availability in the listing, so we'll default to 'Check Product Page'
            availability = 'Check Product Page'
            
            image_url = item.find('img', class_='s-image')['src'] if item.find('img', class_='s-image') else 'N/A'
            
            products.append({
                'name': name,
                'price': price,
                'rating': rating,
                'reviews': reviews,
                'availability': availability,  # Default since availability info is often not in search results
                'image_url': image_url
            })

    driver.quit()
    return products

if __name__ == "__main__":
    search_query = 'laptop'
    max_pages = 2  # Number of pages to scrape

    # Scrape data
    products = scrape_amazon(search_query, max_pages=max_pages, headless=True)

    # Save to CSV
    df = pd.DataFrame(products)
    df.to_csv('amazon_products_corrected.csv', index=False)

    print('Data saved to amazon_products_corrected.csv')




