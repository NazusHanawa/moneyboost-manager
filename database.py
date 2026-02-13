import libsql

from utils import timer

class DB:
    def __init__(self, database_url, auth_token):
        self.database_url = database_url
        self.auth_token = auth_token
        self.connection = libsql.connect(database=database_url, auth_token=auth_token)
        self.cursor = self.connection.cursor()

    def commit(self):
        self.connection.commit()
        
    @timer
    def remove_tables(self):
        query = ""
        
        tables = ["stores", "cashbacks", "partnerships", "platforms"]
        for table in tables:
            query_table = f"DROP TABLE IF EXISTS {table};"
            query += query_table
        
        self.cursor.executescript(query)
        self.commit()

    @timer
    def create_tables(self):
        with open("schema.sql", "r") as file:
            self.cursor.executescript(file.read())
        self.commit()
        
    @timer
    def get_platforms(self):
        rows = self.cursor.execute("SELECT * FROM platforms").fetchall()
        
        stores = [
            {"id": row[0], "name": row[1], "url": row[2]} 
            for row in rows
        ]
        
        return stores
    
    @timer
    def add_platforms(self, platforms):
        base_query = "INSERT OR IGNORE INTO platforms (name, url) VALUES "
        placeholders = ", ".join(["(?, ?)"] * len(platforms))
        full_query = base_query + placeholders
        
        flattened_values = []
        for store in platforms:
            flattened_values.extend([store["name"], store["url"]])
        
        self.cursor.execute(full_query, flattened_values)
        self.commit()
    
    @timer
    def get_stores(self):
        rows = self.cursor.execute("SELECT * FROM stores").fetchall()
        
        stores = [
            {"id": row[0], "name": row[1], "url": row[2]} 
            for row in rows
        ]
        
        return stores
    
    @timer
    def add_stores(self, stores):
        base_query = "INSERT OR IGNORE INTO stores (name, url) VALUES "
        placeholders = ", ".join(["(?, ?)"] * len(stores))
        full_query = base_query + placeholders
        
        flattened_values = []
        for store in stores:
            flattened_values.extend([store["name"], store["url"]])
        
        self.cursor.execute(full_query, flattened_values)
        self.commit()
    
    @timer
    def add_partnerships(self, partnerships):
        base_query = "INSERT OR IGNORE INTO partnerships (store_id, platform_id, url) VALUES "
        placeholders = ", ".join(["(?, ?, ?)"] * len(partnerships))
        full_query = base_query + placeholders
        
        flattened_values = []
        for partnership in partnerships:
            flattened_values.extend(
                [partnership["store_id"], partnership["platform_id"], partnership["url"]]
            )
        
        self.cursor.execute(full_query, flattened_values)
        self.commit()
    
    