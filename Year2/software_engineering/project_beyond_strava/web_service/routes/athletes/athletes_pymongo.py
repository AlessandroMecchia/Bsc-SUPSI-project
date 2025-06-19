from flask import Blueprint, request, jsonify
from web_service.database import athletes_collection
from web_service.services.summary_service import get_athlete_summary

#athletes_bp = Blueprint("athletes", __name__, url_prefix="/athletes")
athletes_bp = Blueprint("athletes", __name__)

# GET /athletes – Get a list of all athletes
@athletes_bp.route("/", methods=["GET"])
def get_athletes():
    athletes = list(athletes_collection.find({}, {'_id': 0}))
    return jsonify(athletes)


# GET /athletes/<athlete_id> – Get details of a specific athlete
@athletes_bp.route("/<int:athlete_id>", methods=["GET"])
def get_athlete(athlete_id):
    athlete = athletes_collection.find_one({'id': athlete_id}, {'_id': 0})
    if not athlete:
        return jsonify({'error': 'Athlete not found'}), 404
    return jsonify(athlete)


# POST /athletes – Create a new athlete
@athletes_bp.route("/", methods=["POST"])
def create_athlete():
    data = request.get_json()
    if not data or 'id' not in data:
        return jsonify({'error': 'Invalid athlete data'}), 400

    existing = athletes_collection.find_one({'id': data['id']})
    if existing:
        return jsonify({'error': 'Athlete with this ID already exists'}), 409

    athletes_collection.insert_one(data)
    return jsonify({'message': 'Athlete created successfully'}), 201


# PUT /athletes/<athlete_id> – Update an existing athlete
@athletes_bp.route("/<int:athlete_id>", methods=["PUT"])
def update_athlete(athlete_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid update data'}), 400

    result = athletes_collection.update_one({'id': athlete_id}, {'$set': data})
    if result.matched_count == 0:
        return jsonify({'error': 'Athlete not found'}), 404

    return jsonify({'message': 'Athlete updated successfully'})


# DELETE /athletes/<athlete_id> – Delete an athlete
@athletes_bp.route("/<int:athlete_id>", methods=["DELETE"])
def delete_athlete(athlete_id):
    result = athletes_collection.delete_one({'id': athlete_id})
    if result.deleted_count == 0:
        return jsonify({'error': 'Athlete not found'}), 404

    return jsonify({'message': 'Athlete deleted successfully'})


# GET /athletes/<athlete_id>/summary – Summary of an athlete
@athletes_bp.route("/<int:athlete_id>/summary", methods=["GET"])
def get_summary_of_athlete(athlete_id):
    summary = get_athlete_summary(athlete_id)
    if not summary:
        return jsonify({'error': 'Athlete not found'}), 404
    return jsonify(summary)

