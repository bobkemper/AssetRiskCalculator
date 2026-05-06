from flask import Blueprint, render_template
from ..constants_securities import SECURITY_TYPE_LIST, PRICE_SOURCE_LIST

bp = Blueprint("securities_ui", __name__)

@bp.get("/securities")
def securities_master():
    return render_template(
        "pages/securities.html",
        security_type_list=SECURITY_TYPE_LIST,
        price_source_list=PRICE_SOURCE_LIST,
    )
