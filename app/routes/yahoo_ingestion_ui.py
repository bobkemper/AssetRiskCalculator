from flask import Blueprint, render_template

bp = Blueprint("yahoo_ingestion_ui", __name__)

@bp.get("/yahoo-ingest")
def yahoo_ingest_page():
    return render_template("pages/yahoo_ingest.html")
