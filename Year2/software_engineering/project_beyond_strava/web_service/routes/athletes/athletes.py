from flask import Blueprint, request, jsonify
from mongoengine.errors import ValidationError, NotUniqueError, DoesNotExist

from web_service.models.athlete import Athlete
from web_service.services.summary_service import get_athlete_summary

athletes_bp = Blueprint("athletes", __name__)


def _athlete_to_dict(athlete):
    data = athlete.to_mongo().to_dict()
    data['_id'] = str(data['_id'])  # Converti ObjectId in stringa per JSON
    # 'id' è già presente come intero nel documento
    return data


# GET /athletes – Get a list of all athletes
@athletes_bp.route('/', methods=['GET'])
def get_athletes():
    athletes = Athlete.objects()
    return jsonify([_athlete_to_dict(a) for a in athletes]), 200


# GET /athletes/<athlete_id> – Get details of a specific athlete
@athletes_bp.route('/<int:athlete_id>', methods=['GET'])
def get_athlete(athlete_id):
    try:
        athlete = Athlete.objects.get(athlete_id=athlete_id)
    except DoesNotExist:
        return jsonify({'error': 'Athlete not found'}), 404
    return jsonify(_athlete_to_dict(athlete)), 200


# POST /athletes – Create a new athlete
@athletes_bp.route('/', methods=['POST'])
def create_athlete():
    data = request.get_json() or {}
    if 'athlete_id' not in data:
        return jsonify({'error': 'Invalid athlete data: missing id'}), 400
    try:
        athlete = Athlete(**data)
        athlete.save()
    except ValidationError as e:
        return jsonify({'error': f'Validation failed: {e}'}), 400
    except NotUniqueError:
        return jsonify({'error': 'Athlete with this ID or username already exists'}), 409

    return jsonify({'message': 'Athlete created successfully'}), 201


# PUT /athletes/<athlete_id> – Update an existing athlete
@athletes_bp.route('/<int:athlete_id>', methods=['PUT'])
def update_athlete(athlete_id):
    data = request.get_json() or {}
    if not data:
        return jsonify({'error': 'Invalid update data'}), 400

    try:
        athlete = Athlete.objects.get(athlete_id=athlete_id)
    except DoesNotExist:
        return jsonify({'error': 'Athlete not found'}), 404

    data.pop('_id', None)
    # Perform the update
    try:
        athlete.update(**data)
    except ValidationError as e:
        return jsonify({'error': f'Validation failed: {e}'}), 400

    return jsonify({'message': 'Athlete updated successfully'}), 200


# DELETE /athletes/<athlete_id> – Delete an athlete
@athletes_bp.route('/<int:athlete_id>', methods=['DELETE'])
def delete_athlete(athlete_id):
    result = Athlete.objects(athlete_id=athlete_id).delete()
    if result == 0:
        return jsonify({'error': 'Athlete not found'}), 404
    return jsonify({'message': 'Athlete deleted successfully'}), 200


# GET /athletes/<athlete_id>/summary – Summary of an athlete
@athletes_bp.route('/<int:athlete_id>/summary', methods=['GET'])
def get_summary_of_athlete(athlete_id):
    summary = get_athlete_summary(athlete_id)
    if not summary:
        return jsonify({'error': 'Athlete not found'}), 404
    return jsonify(summary), 200


######
@athletes_bp.route('/athlete-ids', methods=['GET'])
def get_athlete_ids():
    try:
        ids = [a.athlete_id for a in Athlete.objects.only('athlete_id')]
        return jsonify(ids), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500