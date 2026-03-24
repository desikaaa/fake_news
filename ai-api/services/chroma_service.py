import torch

def search_similar(collection, query_embedding, top_k=5):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    ids = results["ids"][0]
    distances = results["distances"][0]

    output = []
    for i in range(len(ids)):
        output.append({
            "id": ids[i],
            "score": distances[i]  # makin kecil = makin mirip
        })

    return output


def search_from_text(collection, model, query_text, top_k=5):
    query_embedding = model.encode(query_text).tolist()
    return search_similar(collection, query_embedding, top_k)
    
def insert_to_chroma(df, list_id, model, collection, batch_size=32):
    
    df['teks_vektor'] = df.get('klaim', df.get('penjelasan')).fillna("")
    list_teks = df['teks_vektor'].tolist()
    clean_ids = [str(i) for i in list_id]
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"🧠 Mulai membuat vektor menggunakan {device.upper()}...")
    
    list_vektor = model.encode(
        list_teks,
        show_progress_bar=True,
        batch_size=batch_size,
        device=device
    ).tolist()
    
    collection.add(
        ids=clean_ids,
        embeddings=list_vektor,
    )
    
    print("🎉 Semua proses selesai! Data tersinkronisasi di MySQL dan ChromaDB.")