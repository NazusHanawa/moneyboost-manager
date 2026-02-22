import os

from dotenv import load_dotenv
from config import STORES, PLATFORMS, DEBUG
from database import DB
from crawlers import PartnershipCrawler

load_dotenv()

db = DB(os.environ.get("DATABASE_URL"), os.environ.get("AUTH_TOKEN"))
# db.clear()
# db.load_schema()

old_stores = db.get_stores()

db.add_platforms(PLATFORMS)
db.add_stores(STORES)

# CREATE PARTNERSHIPS
platforms = db.get_platforms()
stores = db.get_stores()

print(old_stores)
print()
print(stores)
print()

new_stores = []
for store in stores:
    if store not in old_stores:
        new_stores.append(store)
        
print(new_stores)

partnerships = []
for platform in platforms:
    for store in new_stores:
        partnership_url = PartnershipCrawler.get_partnership_url(platform["name"], store["name"])
        
        if DEBUG:
            print(f"{store['name']} - {partnership_url}")
        
        partnership = {
            "store_id": store["id"],
            "platform_id": platform["id"],
            "url": partnership_url
        }
        partnerships.append(partnership)

db.add_partnerships(partnerships)
