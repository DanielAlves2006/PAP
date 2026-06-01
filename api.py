import sqlite3
import requests

def seed():
    conn = sqlite3.connect('oficina_do_pombo.db')
    cursor = conn.cursor()
    
  
    cursor.execute("SELECT id FROM lojas WHERE id = 1")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO lojas (id, nome, localizacao, contacto) VALUES (?, ?, ?, ?)",
                       (1, 'Oficina Principal', 'Lisboa', '210000000'))
        print("Default store inserted.")
    
    print("Fetching products from API...")
    try:
        response = requests.get(" https://api.bestbuy.com/v1/products")
        response.raise_for_status()
        data = response.json()
        products = data.get('products', [])
    except Exception as e:
        print(f"Error fetching products: {e}")
        conn.close()
        return

    print(f"Fetched {len(products)} products.")

   
    categories = set(p['category'] for p in products)
    category_map = {}
    for cat_name in categories:
        cursor.execute("SELECT id FROM categorias WHERE nome = ?", (cat_name,))
        row = cursor.fetchone()
        if row:
            category_map[cat_name] = row[0]
        else:
            cursor.execute("INSERT INTO categorias (nome) VALUES (?)", (cat_name,))
            category_map[cat_name] = cursor.lastrowid
    print("Categories mapped.")

   
    inserted_count = 0
    for p in products:
        
        cursor.execute("SELECT id FROM produtos WHERE nome = ?", (p['title'],))
        row = cursor.fetchone()
        if not row:
            cursor.execute("""
                INSERT INTO produtos (nome, descricao, preco, categoria_id, imagem)
                VALUES (?, ?, ?, ?, ?)
            """, (p['title'], p['description'], p['price'], category_map[p['category']], p['thumbnail']))
            product_id = cursor.lastrowid
            
            
            cursor.execute("""
                INSERT INTO stock (produto_id, loja_id, quantidade)
                VALUES (?, ?, ?)
            """, (product_id, 1, 10)) 
            
            inserted_count += 1

    conn.commit()
    conn.close()
    print(f"Seeded successfully. Inserted {inserted_count} new products.")

if __name__ == '__main__':
    seed()
