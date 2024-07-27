import requests
from bs4 import BeautifulSoup

ALL_CATEGORIES = [
    "javascript", "html", "php", "ruby", "python", "java", "net",
    "scala", "c", "mobile", "testing", "devops", "admin", "ux", "pm", "go",
    "game", "analytics", "security", "data", "support", "erp", "other"
    ]



def scrap_offer(url):

    response = requests.get(url)
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'lxml')

    def simple_extractor(selector):
        element = soup.select_one(selector)
        value = element.text.strip() if element else None
        return value

    job_title = simple_extractor('div.MuiBox-root.css-s52zl1 h1')
    company_name = simple_extractor('div.MuiBox-root.css-1730po7')
    skills = [skill.text.strip() for skill in soup.select('div.MuiBox-root.css-qal8sw ul h4')]
    description=simple_extractor('div.MuiBox-root.css-7nl6k4')
    level = simple_extractor('.MuiBox-root.css-6ffpw7:nth-of-type(2) .MuiBox-root.css-snbmy4')
    operating_mode = simple_extractor('.MuiBox-root.css-6ffpw7:nth-of-type(4) .MuiBox-root.css-snbmy4')
    salary = simple_extractor('div.MuiBox-root.css-ntm2tb span')

    print(f"Title: {job_title}\nCompany: {company_name}\nSkills: {skills}\nDescription: {description}\nLevel: {level}\nMode: {operating_mode}, S{salary}")


def scrap_offers_links(category):

    offers_xpath = 'a'

    response = requests.get('https://justjoin.it/all-locations/'+ category)
    
    if response.status_code != 200:
        print("Failed to retrieve the webpage.")
        return
    
    html_content = response.content
    soup = BeautifulSoup(html_content, 'lxml')

    dom = etree.HTML(str(soup))

    offers_section = dom.xpath(offers_xpath)
    
    if not offers_section:
        print("No offers section found.")
        return
    
    links = []
    for offer in offers_section:
         
        link_elements = offer.xpath('.//a/@href')
        links.extend(link_elements)
    
    full_links = []
    for link in links:
        full_links.append('https://justjoin.it'+link) 
    return full_links


if __name__ == "__main__":
    url = 'https://justjoin.it/offers/future-processing-java-solutions-architect-gliwice-java'
    scrap_offer(url)
