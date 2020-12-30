from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import pymongo
from pprint import pprint

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_dict ={}

    url = 'https://mars.nasa.gov/news/'

    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")

    # Retrieve the latest element that contains news title and news paragraph
    news_title = soup.find_all('div', class_='content_title')[1].text
    news_p = soup.find_all('div', class_='article_teaser_body')[0].text

    # Print scrapped data 
    print("Title: ",news_title)
    print("--------------------------------------------------------------------")
    print("Paragraph: ",news_p)

    # Scrape Mars Image
    base_url = 'https://www.jpl.nasa.gov'
    images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(images_url)
    html = browser.html
    image_soup = bs(html, 'html.parser')

    relative_image_path = '/spaceimages/images/wallpaper/PIA18048-1920x1200.jpg'
    featured_image_url = base_url + relative_image_path
    print(featured_image_url)

    # Mars Facts
    url = 'https://space-facts.com/mars/'

    # Create table from url
    table = pd.read_html(url)
    mars_facts = table[1]
    mars_facts


    # Convert table into html 
    facts_df = table[0]
    facts_df.columns = ['Fact', 'Data']
    facts_df['Fact'] = facts_df['Fact'].str.replace(':', '')
    facts_df
    facts_html = facts_df.to_html()

    print(facts_html)

    # Mars Hemispheres
    # Scrape USGS webpage for hemispehere images
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, "html.parser")

    # Create dictionary to store titles & links to images
    hemisphere_image_urls = []

    # Retrieve all elements that contain image information
    results = soup.find("div", class_ = "result-list" )
    hemispheres = results.find_all("div", class_="item")

    # Iterate through each image
    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup = bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_image_urls.append({"title": title, "img_url": image_url})
    # Print image title and url
    print(hemisphere_image_urls)

    # Store data in a dictionary
    mars_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_facts": mars_facts,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_dict
    