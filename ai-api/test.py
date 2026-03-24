from config.chroma_config import get_chroma_collection

collection = get_chroma_collection()

print("Total data di Chroma:", collection.count())