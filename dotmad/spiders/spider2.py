import scrapy
from .. items import DotmadItem
import os
from urllib.parse import urljoin
import requests
from scrapy import Selector
from selenium import webdriver
from .. settings import ChormeDriver

#----------Class for scraping----------

class DotMad1Spider(scrapy.Spider):
    name = "dotmad1"
    handle_httpstatus_all = True
    # start_urls = [
    #         'https://www.dotmed.com/equipment/7/10/all/'
    #     ]
    count = 0

    def __init__(self, *args, **kwargs): 
        super(DotMad1Spider, self).__init__(*args, **kwargs) 
        self.start_urls = [kwargs.get('start_url')] 


    def start_requests(self):        
        for url in self.start_urls:
            yield scrapy.Request(url=url,callback=self.FetchCatg,dont_filter = True)
        

    def FetchCatg(self,response):
        catg_listing = response.css("body > div.container > div.card > div.card-body > div a::attr(href)").extract()
        for catg_list in catg_listing:
            url = urljoin(response.url, catg_list)
            yield scrapy.Request(url = url, callback=self.ListingTargetUrl,meta={'handle_httpstatus_list': [301]},dont_filter = True) 


    def ListingTargetUrl(self,response):
        if response.status in [301, 302]:
            redirecturl = "https://www.dotmed.com"+response.css("a::attr(href)").extract()[0]
        else:
            redirecturl = response.url
        yield scrapy.Request(url = redirecturl, callback=self.FetchType,dont_filter = True) 

    def FetchType(self,response):
        catg_type = response.css("body > div.container > div.card > div.card-body > div a::attr(href)").extract()
        if catg_type:
            for catg_type in catg_type:
                url = urljoin(response.url, catg_type)
                yield scrapy.Request(url = url, callback=self.FetchListing,meta={'handle_httpstatus_list': [301]},dont_filter = True) 
        else:
            yield scrapy.Request(url = response.url, callback=self.FetchListing,meta={'handle_httpstatus_list': [301]},dont_filter = True)
        

    def FetchListing(self,response):
        s = 0
        for i in range(0,100):
            Url = response.url+"offset/"+str(s)
            s = s + 15
            yield scrapy.Request(url = Url, callback=self.FetchDataLinks,dont_filter = True)


    def FetchDataLinks(self,response):
        datalinks = response.css(".listing-info h4 a::attr(href)").extract()
        if datalinks:
            for dataobj in datalinks:
                Url = urljoin(response.url, dataobj)
                yield scrapy.Request(url = Url, callback=self.ScrapData, dont_filter = True)



    def ScrapData(self,response):

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(ChormeDriver,chrome_options=chrome_options)
        driver.get(response.url)
        
        selenium_response_text = driver.page_source
        new_selector = Selector(text=selenium_response_text)
        items = DotmadItem()

        LineData = new_selector.css(".visit_menu_link li span::text").extract()
        if LineData:
            Line = '->'.join(LineData)
        else:
            Line = None
        Category = new_selector.css(".visit_menu_link li span::text").extract()[1].strip() if new_selector.css(".visit_menu_link li span::text").extract() else None
        SubCategory = new_selector.css(".visit_menu_link li span::text").extract()[2].strip() if new_selector.css(".visit_menu_link li span::text").extract() else None
        ListingTitle = new_selector.css(".listing_title_info h3::text").extract()[0].strip() if new_selector.css(".listing_title_info h3::text").extract() else None
        ListingNumber = new_selector.css(".listing_id::text").extract()[0].strip() if new_selector.css(".listing_id::text").extract() else None
        ListingLink = response.url
        AskingPrice = new_selector.css(".price::text").extract()[0].strip() if new_selector.css(".price::text").extract() else None
        Condition = new_selector.css(".item_description_list ul li::text").extract()[0].replace(u'\xa0', u' ').strip() if new_selector.css(".item_description_list ul li::text").extract() else None
        QtyAvailable = new_selector.css(".listing_info li::text").extract()[-3].strip() if new_selector.css(".listing_info li::text").extract() else None
        InStock = new_selector.css(".active::text").extract()[0].strip() if new_selector.css(".active::text").extract() else None
        Date = new_selector.css(".listing_info li::text").extract()[-1].strip() if new_selector.css(".listing_info li::text").extract() else None
        Company = new_selector.css(".ratting:nth-child(1) .seller_name::text").extract()[0].strip() if new_selector.css(".ratting:nth-child(1) .seller_name::text").extract() else None
        RepName = new_selector.css(".seller_name a::text").extract()[0].strip() if new_selector.css(".seller_name a::text").extract() else None
        RepLink = urljoin(response.url, new_selector.css(".seller_name a::attr(href)").extract()[0].strip()) if new_selector.css(".seller_name a::attr(href)").extract() else None
        Reviews = new_selector.css(".d-flex+ a::text").extract()[0].replace(u'(', u'').replace(u')', u'').strip() if new_selector.css(".d-flex+ a::text").extract() else None
        Location = new_selector.css(".personal_info li:nth-child(1)::text").extract()[0].strip() if new_selector.css(".personal_info li:nth-child(1)::text").extract() else None
        Phone = new_selector.css(".personal_info li+ li a::text").extract()[0].strip() if new_selector.css(".personal_info li+ li a::text").extract() else None
        Brand = new_selector.css(".item_description_list ul li::text").extract()[1].replace(u'\xa0', u' ').strip() if new_selector.css(".item_description_list ul li::text").extract() else None
        Type = new_selector.css(".item_description_list ul li::text").extract()[2].replace(u'\xa0', u' ').strip() if new_selector.css(".item_description_list ul li::text").extract() else None
        Model = new_selector.css(".item_description_list ul li::text").extract()[3].replace(u'\xa0', u' ').strip() if new_selector.css(".item_description_list ul li::text").extract() else None
        # DescriptionData = new_selector.css(".additional_info::text").extract()
        # if DescriptionData:
        #     Description = ' '.join(DescriptionData)
        # else:
        #     Description = None

        items['Line']=Line
        items['ListingTitle']=ListingTitle
        items['ListingNumber']=ListingNumber
        items['ListingLink']=ListingLink
        items['AskingPrice']=AskingPrice
        items['Condition']=Condition
        items['QtyAvailable']=QtyAvailable
        items['InStock']=InStock
        items['Date']=Date
        items['Company']=Company
        items['RepName']=RepName
        items['RepLink']=RepLink
        items['Reviews']=Reviews
        items['Location']=Location
        items['Phone']=Phone
        items['Brand']=Brand
        items['Type']=Type
        items['Model']=Model
        items['Category']=Category
        items['SubCategory']=SubCategory

        #items['Description']=Description
        yield items  

