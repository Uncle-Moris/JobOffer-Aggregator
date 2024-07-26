import requests
from bs4 import BeautifulSoup


job_title_selector = 'div.MuiBox-root.css-s52zl1 h1'
skills_list_selector = 'div.MuiBox-root.css-qal8sw ul h4'
description_selector = 'div.MuiBox-root.css-7nl6k4'
company_name_selector = 'div.MuiBox-root.css-1730po7'
level_selector = '.MuiBox-root.css-6ffpw7:nth-of-type(2) .MuiBox-root.css-snbmy4'
operating_mode_selector = '.MuiBox-root.css-6ffpw7:nth-of-type(4) .MuiBox-root.css-snbmy4'
salary_selector = 'div.MuiBox-root.css-ntm2tb span'

def scrap_offer(url):
    # Pobranie treści strony
    response = requests.get(url)
    html_doc = response.text
    soup = BeautifulSoup(html_doc, 'lxml')

    def simple_extractor(selector):
        element = soup.select_one(selector)
        value = element.text.strip() if element else None
        return value

    job_title = simple_extractor(job_title_selector)
    company_name = simple_extractor((company_name_selector))
    skills = [skill.text.strip() for skill in soup.select(skills_list_selector)]
    description=simple_extractor(description_selector)
    level = simple_extractor(level_selector)
    mode = simple_extractor(operating_mode_selector)
    salary = simple_extractor(salary_selector)

    print(f"Title: {job_title}\nCompany: {company_name}\nSkills: {skills}\nDescription: {description}\nLevel: {level}\nMode: {mode}, S{salary}")


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
