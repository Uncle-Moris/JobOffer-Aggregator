import requests
from bs4 import BeautifulSoup
from lxml import etree

ALL_CATEGORIES = ["javascript",
                  "html",
                  "php",
                  "ruby",
                  "python",
                  "java",
                  "net",
                  "scala",
                  "c",
                  "mobile",
                  "testing",
                  "devops",
                  "admin",
                  "ux",
                  "pm",
                  "go",
                  "game",
                  "analytics",
                   "security", "data", "support", "erp", "other"]

def scrap_offers_links(category):
    # Define the XPath for the offers section
    offers_xpath = '/html/body/div[1]/div[2]/div[1]/div/div[2]/div/div/div[2]/div/div[2]'

    # Make a GET request to the webpage
    response = requests.get('https://justjoin.it/all-locations/'+ category)
    
    # Check if the request was successful
    if response.status_code != 200:
        print("Failed to retrieve the webpage.")
        return
    
    # Parse the webpage content with BeautifulSoup
    html_content = response.content
    soup = BeautifulSoup(html_content, 'lxml')
    
    # Convert BeautifulSoup object to lxml HTML
    dom = etree.HTML(str(soup))
    
    # Extract offer links using XPath
    offers_section = dom.xpath(offers_xpath)
    
    # Check if any offers section is found
    if not offers_section:
        print("No offers section found.")
        return
    
    # Extract links from the offers section
    links = []
    for offer in offers_section:
         
        link_elements = offer.xpath('.//a/@href')
        links.extend(link_elements)
    
    full_links = []
    for link in links:
        full_links.append('https://justjoin.it'+link) 
    return full_links

def scrap_offer(url):
    # Fetch HTML content from the URL
    response = requests.get(url)
    html_content = response.content

    # Parse HTML with BeautifulSoup using lxml parser
    soup = BeautifulSoup(html_content, 'lxml')
    dom = etree.HTML(str(soup))

    #TODO change xpath's to selectors to fix no data when is company profile element in body
    xpaths = {
        'title': '/html/body/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[2]/h1',
        'level': '/html/body/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]',
        'skills': '/html/body/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[3]/div/ul',
        'description': '/html/body/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[4]/div[2]',
        'company': '/html/body/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]/div[1]',
        'operating_mode': '/html/body/div[1]/div[2]/div[1]/div/div[2]/div[2]/div[2]/div[4]/div[2]/div[2]'
    }

    # Helper function to extract text using XPath
    def extract_text(xpath):
        elements = dom.xpath(xpath)
        if elements and elements[0] is not None:
            return ''.join(elements[0].xpath('.//text()')).strip()
        return "Not found"

    # Extract data using defined XPaths
    title = extract_text(xpaths['title'])
    level = extract_text(xpaths['level'])
    description = extract_text(xpaths['description'])
    company_name = extract_text(xpaths['company'])
    operating_mode = extract_text(xpaths['operating_mode'])

    # Extract skills with special handling
    skills_elements = dom.xpath(xpaths['skills'])
    skills_list = []
    if skills_elements:
        for div in skills_elements[0].xpath('.//div[@class="MuiBox-root css-jfr3nf"]'):
            skill_title = div.xpath('.//h4')
            if skill_title:
                skills_list.append(skill_title[0].text.strip())
    if not skills_list:
        skills_list.append("Skills not found")
    print(skills_list, description)
    return title, 

scrap_offer('https://justjoin.it/offers/benefit-systems-konsultant-ka-salesforce-warszawa-erp')