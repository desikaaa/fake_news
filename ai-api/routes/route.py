from flask import Blueprint
from controllers.search_controller import search_controller
from flask import Blueprint, jsonify
from controllers.scraper_controller import run_scraper_pipeline
search_bp = Blueprint("search", __name__)

def init_search_routes(collection, model):
    @search_bp.route("/search", methods=["POST"])
    def search():
        return search_controller(collection, model)

    return search_bp

def init_scrape_routes(collection, model):
    scrape_bp = Blueprint("scrape", __name__)

    @scrape_bp.route("/scrape", methods=["POST"])
    def scrape():
        try:
            run_scraper_pipeline(model, collection, batch_size=32)

            return jsonify({
                "status": "success",
                "message": "Scraping dan insert ke DB & Chroma selesai."
            }), 200

        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500

    return scrape_bp