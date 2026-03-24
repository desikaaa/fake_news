from flask import Flask
from routes.route import init_search_routes, init_scrape_routes
from config.chroma_config import get_chroma_collection
from config.model_config import get_model
from config.config import Config

app = Flask(__name__)
app.config.from_object(Config)

print(f"Running in {Config.ENV} mode, DEBUG={Config.DEBUG}")

# Init dependency
collection = get_chroma_collection()
model = get_model()

# Register routes
search_bp = init_search_routes(collection, model)
scrape_bp = init_scrape_routes(collection, model)

app.register_blueprint(search_bp)
app.register_blueprint(scrape_bp)

if __name__ == "__main__":
    app.run(debug=True)