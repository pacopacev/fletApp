

query_radios = {
    "all_radios_favorites": """SELECT name,url,favorite, favicon_url, COUNT(*) as count FROM flet_radios
                WHERE favorite = True
                GROUP BY name, url, favorite, favicon_url, created_at
                ORDER BY created_at DESC
                LIMIT 666;""",
    "all_radios_last_visited": """SELECT name,url,favorite, favicon_url, COUNT(*) as count FROM flet_radios
                GROUP BY name, url, favorite, favicon_url, created_at
                ORDER BY created_at DESC
                LIMIT 666;""",
    "favorite_radios": """SELECT name,url,favorite, favicon_url, COUNT(*) as count FROM flet_radios
                WHERE favorite = True
                GROUP BY name, url, favorite, favicon_url
                ORDER BY count DESC
                LIMIT 666;""",    
    "check_radio_exists": """SELECT * FROM flet_radios WHERE uuid = %s;""",
    "insert_radio": """INSERT INTO flet_radios (name, url, favicon_url, uuid,created_at) VALUES (%s, %s, %s, %s, %s);""",
}

