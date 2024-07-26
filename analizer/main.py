import json
import scraper
from db import add_offer

with open('jobs.json', 'r+', encoding="utf-8") as file:
    data = json.load(file)

#TODO Add link to offer insted of source, source shoud be a site
class Offer:
    def __init__(self, title, level: str, source: str, skills: list,
            description: str, company_name: str, operating_mode: str) -> None:
        
        self.title = title
        self.level = level
        self.source = source
        self.skills = skills
        self.description = description
        self.company_name = company_name
        self.operating_mode = operating_mode 

    def add_job(self):
        add_offer(
            title=self.title,
            level=self.level,
            source=self.source,
            skills=self.skills,
            description=self.description,
            company_name=self.company_name,
            operating_mode=self.operating_mode  
        )

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

for category in ALL_CATEGORIES:
    for offer_link in scraper.scrap_offers_links(category):
        title, skills_list, description, company_name, level, operating_mode = scraper.scrap_offer(offer_link)
        offer = Offer(title=title,
                    level=level,
                    source=offer_link,
                    skills=skills_list,
                    description=description,
                    operating_mode=operating_mode,
                    company_name=company_name
                    )
        offer.add_job()