from flask import Blueprint, request, jsonify
from web_service.models.athlete import Athlete
from web_service.services.summary_service import get_athlete_summary

analytics_bp = Blueprint("analytics", __name__, url_prefix="/analytics")
