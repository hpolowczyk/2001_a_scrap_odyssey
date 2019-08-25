from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser


def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    ### NASA Mars News
    mars_news = 'https://mars.nasa.gov/news/'
    browser.visit(mars_news)
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    # Use select_one to find the first tag that matches the defined selector
    latest = soup.select_one("ul.item_list li.slide")
    # Collect and store latest news title
    latest_title = latest.find(class_='content_title').get_text()
    # Collect and store latest news description
    latest_blurb = latest.find(class_='rollover_description_inner').get_text()

    
    ### Mars Featured Image
    mars_image = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(mars_image)
    # Click the 'Full Image' button on the main page
    browser.click_link_by_partial_text('FULL IMAGE')
    # Allow 3 seconds so that page can load before next click
    time.sleep(3)
    # Click the 'Full Image' button on the main page
    browser.click_link_by_partial_text('more info')
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')
    # Use find() to navigate and retrieve the image url
    image_url = soup.find(class_='lede').find('a')['href']
    # Save image URL
    featured_image_url = 'https://www.jpl.nasa.gov' + image_url


    ### Mars Weather
    mars_weather = 'https://twitter.com/marswxreport?lang=en'
    # Retrieve page with the requests module
    response = requests.get(mars_weather)
    # Create BeautifulSoup object; parse with 'lxml'
    soup = bs(response.text, 'lxml')
    # Collect and store latest tweet
    latest_tweet = soup.find(class_='js-tweet-text-container').find("p").text


    ### Mars Facts Table
    # URL of page to be scraped
    mars_facts = 'https://space-facts.com/mars/'
    # Use read_html to parse the URL for tables
    table_list = pd.read_html(mars_facts)
    # Select the desired table from the list
    mars_facts_table = table_list[1]
    # Rename the columns accordingly
    mars_facts_table.columns = ['Planet Profile',' ']
    # Reset the index
    mars_facts_table.set_index('Planet Profile',inplace=True)
    # Convert the data to a HTML table string
    html_table = mars_facts_table.to_html()


    ### Mars Hemispheres
    mars_hemispheres = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_hemispheres)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')
    # Retrieve all elements that contain hemisphere information
    desc_list = soup.find_all(class_='description')
    # Use a list comprehension to extract the name of each hemisphere
    hemisphere_names = [desc.find('h3').text.replace(' Enhanced','') for desc in desc_list]
    
    # Create an empty list to contain all hemisphere dictionaries
    hemisphere_image_urls  = []
    # Create a for-loop that retrieves each hemisphere name and its corresponding image and inserts them into a dictionary
    for name in hemisphere_names:
        # URL of the page to be scraped
        mars_hemispheres = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(mars_hemispheres)
        # Click on the name of each hemisphere to retrieve the full image
        browser.click_link_by_partial_text(f'{name} Enhanced')
        # HTML object
        html = browser.html
        # Parse HTML with Beautiful Soup
        soup = bs(html, 'html.parser')
        # Use find() to locate the class where the image is located
        image_class = soup.find(class_='downloads')
        # Use find() to navigate and retrieve the image url
        image_url = image_class.find('li').find('a')['href']
        # Create a dictionary containing the title and image url for each hemisphere and append to the empty list 
        hemisphere_image_urls.append({'title':name, 'img_url':image_url})


    ### Mars Data Dictionary
    # Store data in a dictionary
    mars_data = {
        'news_title': latest_title,
        'news_desc': latest_blurb,
        'feat_image': featured_image_url,
        'weather': latest_tweet,
        'fact_table': html_table,
        'hemispheres': hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
