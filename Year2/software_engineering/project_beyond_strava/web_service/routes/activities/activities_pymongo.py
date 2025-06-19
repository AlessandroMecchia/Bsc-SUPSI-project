from flask import Blueprint, request, jsonify
from web_service.database import activities_collection

#activities_bp = Blueprint("activities", __name__, url_prefix="/activities")
activities_bp = Blueprint("activities", __name__)

# GET /activities – List all activities
@activities_bp.route("/", methods=["GET"])
def get_activities():
    activities = list(activities_collection.find({}, {"_id": 0}, {"streams": 0}))
    return jsonify(activities)


# GET /activities/<activity_id> – Get one activity
@activities_bp.route("/<int:activity_id>", methods=["GET"])
def get_activity(activity_id):
    activity = activities_collection.find_one({"id": activity_id}, {"_id": 0})
    if not activity:
        return jsonify({"error": "Activity not found"}), 404
    return jsonify(activity)

# POST /activities/<activity_id> – Get one activity
@activities_bp.route("/", methods=["POST"])
def create_activity():
    data = request.get_json()
    if not data or "id" not in data:
        return jsonify({"error": "Missing activity id"}), 400

    if activities_collection.find_one({"id": data["id"]}):
        return jsonify({"error": "Activity with this ID already exists"}), 409

    activities_collection.insert_one(data)
    return jsonify({"message": "Activity created successfully"}), 201


# PUT /activities/<activity_id> – Update an activity
@activities_bp.route("/<int:activity_id>", methods=["PUT"])
def update_activity(activity_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    result = activities_collection.update_one({"id": activity_id}, {"$set": data})
    if result.matched_count == 0:
        return jsonify({"error": "Activity not found"}), 404

    return jsonify({"message": "Activity updated successfully"})


# DELETE /activities/<activity_id> – Delete an activity
@activities_bp.route("/<int:activity_id>", methods=["DELETE"])
def delete_activity(activity_id):
    result = activities_collection.delete_one({"id": activity_id})
    if result.deleted_count == 0:
        return jsonify({"error": "Activity not found"}), 404

    return jsonify({"message": "Activity deleted successfully"})
