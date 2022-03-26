# Dependencies
import os
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pandas as pd
import time


def scrape():
    # Import Splinter and set the chromedriver path
    executable_path = {"executable_path": "/Users/halabi93/Desktop/Data Science Boot Camp/web-scraping-challenge/Missions_to_Mars/chromedriver"}
    browser = Browser("chrome", **executable_path, headless = False)    

    # Create a empty dictionary to store the data
    scraped_data = {}

    url_redplanet = "https://redplanetscience.com"
    browser.visit(url_redplanet)
    time.sleep(5)
    html_redplanet = browser.html
    soup = BeautifulSoup(html_redplanet, 'html.parser')

    # Search for the div where the title is located
    results = soup.find_all('div', class_="content_title")
    news_title = results[1].text
    
    # Search for the div where the paragraph news is located
    results = soup.find_all('div', class_="article_teaser_body")
    p = results[0].text

    # Save the scraped data to an entry of the dictionary
    scraped_data["Title"] = news_title
    scraped_data["Paragraph"] = p

    url_spaceimage = "https://spaceimages-mars.com"
    browser.visit(url_spaceimage)
    html_spaceimage = browser.html
    soup = BeautifulSoup(html_spaceimage, 'html.parser')
    html_spaceimage = browser.html
    soup = BeautifulSoup(html_spaceimage, 'html.parser')

    # Featured image is in the div class="carousel_container"
    result = soup.find('img', class_ = "headerimage fade-in").get("src")

    featured_image_url = f"{url_spaceimage}/{result}"

    # Save the scraped data to an entry of the dictionary
    scraped_data["ImageURL"] = featured_image_url

    url_galaxyfacts = "https://galaxyfacts-mars.com"

    tables = pd.read_html(url_galaxyfacts)
    table = tables[0]
    table = table.rename(columns={0:"Description", 1:"Mars", 2:"Earth"})
    table = table.set_index("Description")
    scraped_data["TableHTML"] = table.to_html()

    url_marshemispheres = "https://marshemispheres.com"

    browser.visit(url_marshemispheres)
    html_marshemispheres  = browser.html
    soup = BeautifulSoup(html_marshemispheres, 'html.parser')  

    # By analyzing the page we can find that the images are in a div class='description'
    results = soup.find_all('div',class_='description') 

    # Create a list with the name of the hemispheres
    list_hemispheres = []
    for i in range(len(results)):
        list_hemispheres.append(results[i].a.h3.text)
    
    hemisphere_image_urls = []

    # Create a list of dictionaries for each hemisphere
    for i in range(len(list_hemispheres)):

        browser.click_link_by_partial_text(list_hemispheres[i])
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        results_new = soup.find_all('li')
        for n in range(len(results_new)):
            if results_new[n].a.text == 'Sample':
                hemisphere_image_urls.append({"title": list_hemispheres[i].replace("Hemisphere Enhanced", 'Hemisphere'), "img_url": results_new[0].a["href"]})
        browser.visit(url_marshemispheres)
    
    scraped_data["ListImages"] = hemisphere_image_urls
    browser.quit()




    return scraped_data