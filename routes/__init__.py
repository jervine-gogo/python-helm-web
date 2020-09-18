from flask import Blueprint
routes = Blueprint('routes', __name__)

from .kube_helm_routes import *