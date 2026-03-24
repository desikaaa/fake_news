import pandas as pd
from services.scraper_service import *
import torch
import pandas as pd
from services.db_service import insert_to_mysql, get_latest_title
from services.chroma_service import insert_to_chroma

def run_scraper_pipeline(model, collection, batch_size=32):
    print("🚀 Memulai proses scraping data hoaks...")
    latest_title = get_latest_title()
    print(f"📌 Judul terbaru di database: '{latest_title}'")
    df = scrape_new_hoaxes(latest_title)
    df = scrape_all(df)
    df = retry_scrape_nan(df)
    df = clean_dataframe(df)
    
    if df is None or df.empty:
        print("✅ Tidak ada data hoaks baru untuk diproses hari ini.")
        return None

    list_id = insert_to_mysql(df)
    insert_to_chroma(df, list_id, model, collection, batch_size)
    

def clean_dataframe(df):
    print(df['judul'])
    df['kategori_hoaks'] = df['judul'].apply(lambda x: re.search(r'\[(.*?)\]', x).group(1).strip() 
                                             if re.search(r'\[(.*?)\]', x) else None)
    print(df['kategori_hoaks'])
    # Hapus teks dalam bracket dari judul
    df['judul'] = df['judul'].apply(lambda x: re.sub(r'\s*\[.*?\]\s*', ' ', x).strip())

    # Bersihkan tanggal
    df['tanggal'] = df['tanggal'].str.replace(r'[^0-9A-Za-z ]', '', regex=True).str.strip()
    bulan_dict = {
        'Januari':'01','Februari':'02','Maret':'03','April':'04','Mei':'05',
        'Juni':'06','Juli':'07','Agustus':'08','September':'09','Oktober':'10',
        'November':'11','Desember':'12'
    }
    def ubah_tanggal_manual(tgl_str):
        for bulan, angka in bulan_dict.items():
            if bulan in tgl_str:
                tgl_str = tgl_str.replace(bulan, angka)
        return tgl_str
    df['tanggal'] = df['tanggal'].apply(ubah_tanggal_manual)
    df['tanggal'] = pd.to_datetime(df['tanggal'], dayfirst=True, errors='coerce')
    df = df.dropna(subset=['tanggal']).sort_values(by='tanggal', ascending=False).reset_index(drop=True)

    # Hapus duplikat judul
    df = df.drop_duplicates(subset=['judul'])

    return df