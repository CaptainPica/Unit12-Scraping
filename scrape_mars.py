from splinter import Browser
from bs4 import BeautifulSoup

import pandas as pd

def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    #Article Info
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    heads = soup.find("div", class_="content_title").text
    abouts = soup.find("div", class_="article_teaser_body").text

    #Featured image
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    featured_image_url = "https://www.jpl.nasa.gov"
    im = soup.find("article", class_="carousel_item")
    featured_image_url = featured_image_url + im.a["data-fancybox-href"]

    #Weather Info
    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_weather = soup.find_all("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    for weather in mars_weather:
        if weather.text[0:7] == "InSight":
            out_weather = weather.text.split("pic.twit")[0]
            break
    
    #Mars Facts
    scraped_table = pd.read_html("https://space-facts.com/mars/")[0]
    out_table = scraped_table.to_html(header=False,index=False,escape=True)

    #Mars Hemispheres
    hemisphere_image_urls = []
    repeat_dict = {"title":"","img_url":""}
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    title_list = soup.select("div.description > a > h3")
    title_list = [title.text.rsplit(" ",1)[0] for title in title_list]

    #This will only run from the initial page defined in this section
    for i in range(len(title_list)):
        browser.find_by_css("div.description > a")[i].click()
        #mechanical_soup has a get_current_page_function which returns the equivalent of soup here
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        #     img_link = soup.select("div.downloads > img.wide-image")[0]["src"]
        img_link = soup.find_all("img",class_="wide-image")[0]["src"]
        img_link = "https://astrogeology.usgs.gov" + img_link
        repeat_dict["title"] = title_list[i]
        repeat_dict["img_url"] = img_link
        hemisphere_image_urls.append(repeat_dict.copy())
        browser.back()

    browser.quit()
    out_dict = {"news_title":heads,"news_p":abouts,"featured_image_url":featured_image_url,"mars_weather":out_weather,"con_table":out_table,"hemisphere_image_urls":hemisphere_image_urls}
    return out_dict