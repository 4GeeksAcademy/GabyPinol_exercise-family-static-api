"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_get_all_members():
    # Obtenemos la lista directa y la devuelvo
    members = jackson_family.get_all_members()
    return jsonify(members), 200


@app.route('/member/<int:member_id>', methods=['GET'])
@app.route('/members/<int:member_id>', methods=['GET'])
def handle_get_single_member(member_id):
    member = jackson_family.get_member(member_id)
    
    # SI encontramos al miembro, lo devuelvo con un 200
    if member is not None:
        return jsonify(member), 200
    # SI NO, aviso que no existe con un 400
    else:
        return jsonify({"msg": "Member not found"}), 400


@app.route('/members', methods=['POST'])
def handle_add_member():
    body = request.get_json()
    
    # SI no mandan datos, o falta algún campo obligatorio...
    if not body or "first_name" not in body or "age" not in body or "lucky_numbers" not in body:
        return jsonify({"msg": "Missing required fields"}), 400
    # SI NO, todo está perfecto y lo agrego
    else:
        new_member = jackson_family.add_member(body)
        return jsonify(new_member), 200


@app.route('/member/<int:member_id>', methods=['DELETE'])
@app.route('/members/<int:member_id>', methods=['DELETE'])
def handle_delete_member(member_id):
    success = jackson_family.delete_member(member_id)
    
    # SI la eliminación fue exitosa...
    if success:
        return jsonify({"done": True}), 200
    # SI NO, es porque ese ID no existe
    else:
        return jsonify({"msg": "Member not found"}), 400


# Esto corre el servidor
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)