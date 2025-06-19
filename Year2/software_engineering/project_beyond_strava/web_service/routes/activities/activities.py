from flask import Blueprint, request, jsonify
from mongoengine.errors import ValidationError, NotUniqueError, DoesNotExist

from web_service.models.activity import Activity

# Define the blueprint without a URL prefix here
activities_bp = Blueprint('activities', __name__)


def _activity_to_dict(activity):
    """
    Convert a MongoEngine Activity document to a JSON-serializable dict,
    renaming the primary key `_id` back to `id`.
    """
    data = activity.to_mongo().to_dict()
    data['id'] = data.pop('_id')  # Convert ObjectId to string
    return data


# GET /activities – List all activities
@activities_bp.route('/', methods=['GET'])
def get_activities():
    activities = Activity.objects().exclude('streams')
    return jsonify([_activity_to_dict(a) for a in activities]), 200


# GET /activities/<activity_id> – Get one activity
@activities_bp.route('/<int:activity_id>', methods=['GET'])
def get_activity(activity_id):
    try:
        activity = Activity.objects.get(id=activity_id)
    except DoesNotExist:
        return jsonify({'error': 'Activity not found'}), 404
    return jsonify(_activity_to_dict(activity)), 200


# POST /activities – Create a new activity
@activities_bp.route('/', methods=['POST'])
def create_activity():
    data = request.get_json() or {}
    if 'id' not in data:
        return jsonify({'error': 'Missing activity id'}), 400
    if '_id' in data:
        data['id'] = data['_id']

    try:
        activity = Activity(**data)
        activity.save()
    except ValidationError as e:
        return jsonify({'error': f'Validation failed: {e}'}), 400
    except NotUniqueError:
        return jsonify({'error': 'Activity with this ID already exists'}), 409
    return jsonify({'message': 'Activity created successfully'}), 201


# PUT /activities/<activity_id> – Update an activity
@activities_bp.route('/<int:activity_id>', methods=['PUT'])
def update_activity(activity_id):
    data = request.get_json() or {}
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    try:
        activity = Activity.objects.get(id=activity_id)
    except DoesNotExist:
        return jsonify({'error': 'Activity not found'}), 404
    try:
        activity.update(**data)
    except ValidationError as e:
        return jsonify({'error': f'Validation failed: {e}'}), 400
    return jsonify({'message': 'Activity updated successfully'}), 200


# DELETE /activities/<activity_id> – Delete an activity
@activities_bp.route('/<int:activity_id>', methods=['DELETE'])
def delete_activity(activity_id):
    result = Activity.objects(id=activity_id).delete()
    if result == 0:
        return jsonify({'error': 'Activity not found'}), 404
    return jsonify({'message': 'Activity deleted successfully'}), 200
