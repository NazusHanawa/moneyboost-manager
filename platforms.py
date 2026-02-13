import requests

from playwright.sync_api import sync_playwright
from ddgs import DDGS
from utils import calculate_similarity, get_last_url, get_normalized_name
    
class Platform:
    NAME = "platform_name"
    URL = "platform_url"
    STORES_URL = "platform_stores_url"
    
    @classmethod
    def get_partnership_url(cls, store_name):
        normalized_name = get_normalized_name(store_name)
        url = f"{cls.STORES_URL}/{normalized_name}"
        
        last_url = get_last_url(url)
        if not last_url:
            return cls._get_partnership_url_fallback(store_name)
        
        return last_url
    
    @classmethod
    def _get_partnership_url_fallback(cls, store_name):
        with DDGS() as ddgs:
            query = f"{store_name} site:{cls.URL}"
                
            results = ddgs.text(query, region='br-pt', max_results=10)
            if not results:
                return
            
            for result in results:
                url = result['href']
                if cls.STORES_URL in url:
                    last_url = get_last_url(url)
                    if not last_url:
                        break
                    
                    if len(cls.STORES_URL) < len(url):
                        similarity = calculate_similarity(store_name, url)
                        if similarity > 0.6:
                            return url              
        
        return None
    
    @classmethod
    def _normalized_name(cls, name):
        normalized_name = name.lower().replace(" ", "-").replace("!", "")
        
        return normalized_name

    
class Meliuz(Platform):
    NAME = "meliuz"
    URL = "https://www.meliuz.com.br"
    STORES_URL = f"{URL}/desconto"

class Cuponomia(Platform):
    NAME = "cuponomia"
    URL = "https://www.cuponomia.com.br"
    STORES_URL = f"{URL}/desconto"
        
class MyCashback(Platform):
    NAME = "mycashback"
    URL = "https://www.mycashback.com.br"
    STORES_URL = f"{URL}/retailer"
        
class InterShop(Platform):
    NAME = "inter shop"
    URL = "https://shopping.inter.co"
    STORES_URL = f"{URL}/site-parceiro/lojas"

class Zoom(Platform):
    NAME = "zoom"
    URL = "https://www.zoom.com.br"
    STORES_URL = f"{URL}/cupom-de-desconto"
    
    @classmethod
    def get_partnership_url(cls, store_name):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True) 
            context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
            page = context.new_page()
            
            try:
                page.goto("https://www.zoom.com.br/cupom-de-desconto/lojas", wait_until="load")
                
                search_input_xpath = "/html/body/main/div[1]/main/div/div[5]/div/div/input"
                page.wait_for_selector(f"xpath={search_input_xpath}")
                page.fill(f"xpath={search_input_xpath}", store_name)

                results_div_xpath = "/html/body/main/div[1]/main/div/div[8]"
                page.wait_for_selector(f"xpath={results_div_xpath}", state="attached", timeout=500)
                first_url_element = page.query_selector(f"xpath={results_div_xpath}//a")
                
                if first_url_element:
                    url = first_url_element.get_attribute("href")
                    if url and url.startswith("/"):
                        url = f"https://www.zoom.com.br{url}"
                    
                    return url
                else:
                    return None
            except Exception as e:
                print(f"ERRO: {e}")
                return None
            finally:
                browser.close()

class Opera(Platform):
    NAME = "opera"
    URL = "https://cashback.opera.com/br"
    STORES_URL = f"{URL}/shops"
    # TODO
    
class Letyshops(Platform):
    NAME = "letyshops"
    URL = "https://letyshops.com/br"
    STORES_URL = f"{URL}/shops"
    
class Megabonus(Platform):
    NAME = "megabonus"
    URL = "https://megabonus.com/br/pt"
    STORES_URL = f"{URL}/shop"
    
if __name__ == "__main__":
    print(Letyshops.get_partnership_url("magazine luiza"))
    