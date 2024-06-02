import asyncio
from requests_html import AsyncHTMLSession

async def scrape_product_data_amazon(url):
    session = AsyncHTMLSession()
    response = await session.get(url)

    if response.status_code == 200:
        # Render JavaScript to get dynamic content
        await response.html.arender(sleep=1)  # Adjust sleep time as needed

        # Extract product title
        title_element = response.html.find('#productTitle', first=True)
        title = title_element.text.strip() if title_element else "Title not found"

        # Extract price
        price_element = response.html.find('span.priceBlockBuyingPriceString', first=True)
        price = price_element.text.strip() if price_element else "Price not found"

        # Extract features
        features_elements = response.html.find('ul.feature-list li')
        features = [li.text.strip() for li in features_elements]

        # Extract reviews
        reviews = []
        for review_element in response.html.find('div.review'):
            rating = review_element.find('span.a-icon-alt', first=True).text.strip()
            comment = review_element.find('span.review-text', first=True).text.strip()
            reviews.append({'rating': rating, 'comment': comment})

        # Return scraped data
        return {
            'title': title,
            'price': price,
            'features': features,
            'reviews': reviews
        }
    else:
        raise Exception(f"Failed to scrape data from {url}. Error code: {response.status_code}")

# Example usage
product_url = 'https://www.amazon.com/dp/B07V5KS95Y'
product_data = await scrape_product_data_amazon(product_url)
print(product_data)

