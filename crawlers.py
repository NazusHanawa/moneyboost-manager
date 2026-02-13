from platforms import *

class PartnershipCrawler:
    PLATFORMS = {
        "meliuz": Meliuz,
        "cuponomia": Cuponomia,
        "mycashback": MyCashback,
        "inter shop": InterShop,
        "zoom": Zoom,
        "opera": Opera,
        "letyshops": Letyshops,
        "megabonus": Megabonus
    }
    
    @classmethod
    def get_partnership_url(self, platform_name, store_name):
        
        platform = self.PLATFORMS.get(platform_name.lower(), None)
        if not platform:
            raise Exception(f"Platform not found: {platform_name}")
        
        return platform.get_partnership_url(store_name)

if __name__ == "__main__":
    print(PartnershipCrawler().PLATFORMS)
    
    
    
    


