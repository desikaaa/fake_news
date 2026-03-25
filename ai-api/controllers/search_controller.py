from flask import Blueprint, request, jsonify
from services.chroma_service import search_from_text
from services.nli_service import run_nli  
from services.db_service import get_row_by_id

search_bp = Blueprint("search", __name__)

def search_controller(collection, transformer, nli, top_k=5, gap_threshold=5.0):
    data = request.get_json()
    if not data or "query" not in data:
        return jsonify({"error": "Query tidak ditemukan"}), 400

    query = data["query"]

    results = search_from_text(collection, transformer, query, top_k=top_k)

    if not results:
        return jsonify({"query": query, "results": []})

    first_score = results[0]["score"]
    filtered = [
        r for r in results
        if abs(r["score"] - first_score) <= gap_threshold
    ]

    if not filtered:
        return jsonify({"query": query, "results": []})

    candidate_rows = [get_row_by_id(r["id"]) for r in filtered]

    pairs = [(query, row.get("judul", "")) for row in candidate_rows]

    nli_scores = run_nli(nli, pairs) 

    for r, nli in zip(filtered, nli_scores):
        r["nli_label"] = nli["label"]
        r["nli_score"] = nli["score"]
        r["hoax_text"] = candidate_rows[filtered.index(r)].get("hoax_text", "")
        r["fakta"] = candidate_rows[filtered.index(r)].get("fakta", "")
        r["kategori"] = candidate_rows[filtered.index(r)].get("kategori", "")
        r["link"] = candidate_rows[filtered.index(r)].get("link", "")
        r["link_counter"] = candidate_rows[filtered.index(r)].get("link_counter", "")

    return jsonify({
        "query": query,
        "top_k": top_k,
        "results": filtered
    })


def init_search_routes(collection, transformer, nli):
    @search_bp.route("/search", methods=["POST"])
    def search():
        return search_controller(collection, transformer, nli)

    return search_bp