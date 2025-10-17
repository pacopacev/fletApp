

query_radios = {
    "all_radios": """SELECT name,url,favorite, favicon_url, COUNT(*) as count FROM flet_radios
                GROUP BY name, url, favorite, favicon_url
                ORDER BY count DESC
                LIMIT 666;""",
    "favorite_radios": """SELECT name,url,favorite, favicon_url, COUNT(*) as count FROM flet_radios
                WHERE favorite = True
                GROUP BY name, url, favorite, favicon_url
                ORDER BY count DESC
                LIMIT 666;""",    
}

