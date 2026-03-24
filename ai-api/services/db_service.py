from config.db_config import get_connection
import pandas as pd
import json

def get_latest_title():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT judul FROM knowledge_base ORDER BY tanggal DESC LIMIT 1")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0].lower() if result else ""

def insert_to_mysql(df):
    db = get_connection()
    cursor = db.cursor()
    
    list_id_chroma = []
    
    df = df.where(pd.notnull(df), None)
    
    insert_query = """
        INSERT INTO knowledge_base (judul, link,kategori, hoax_text, fakta, link_counter) 
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    for _, row in df.iterrows():
        teks_hoaks = row.get('klaim') if row.get('klaim') else row.get('penjelasan')
        link_mentah = row.get('link_counter')
        link_json = json.dumps(link_mentah) if link_mentah else None
        
        cursor.execute(insert_query, (
            row.get('judul'),
            row.get('link'),
            row.get('kategori_hoaks'),
            teks_hoaks,
            row.get('fakta'),
            link_json
        ))
        
        inserted_id = cursor.lastrowid
        list_id_chroma.append(str(inserted_id))
    
    db.commit()
    cursor.close()
    db.close()
    
    print(f"✅ Berhasil menyimpan {len(list_id_chroma)} data ke MySQL.")
    return list_id_chroma
