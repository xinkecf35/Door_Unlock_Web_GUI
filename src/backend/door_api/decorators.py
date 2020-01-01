from Flask import Blueprint
import json
from werkzeug.exceptions import HTTPException

bp = Blueprint(__name__)


@bp.errorhandler(HTTPException)
def handle_exception(e):
    return e.get_response()
