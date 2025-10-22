from flask import Blueprint, jsonify, request, render_template
from flask_jwt_extended import jwt_required

from App.controllers import staff as staffController
from App.controllers import studentrecord as studentrecordController

staff_views = Blueprint('staff_views', __name__)

@staff_views.route('/staff', methods=['GET'])
def staff_page():
    return render_template('admin/index.html')


@staff_views.route('/api/staff', methods=['POST'])
def create_staff_api():
    data = request.json
    result = staffController.create_staff(
        data.get('name'), 
        data.get('email'), 
        data.get('password'), 
        data.get('department')
    )
    return jsonify(result)


@staff_views.route('/api/staff/list_pending', methods=['GET'])
def list_pending_records_api():
    result = staffController.list_pending_records()
    return jsonify(result)


@staff_views.route('/api/staff/list_all', methods=['GET'])
def list_all_records_api():
    result = studentrecordController.get_all_records()
    return jsonify(result)


@staff_views.route('/api/staff/confirm/<int:record_id>', methods=['PUT'])
def confirm_record_api(record_id):
    result = staffController.confirm_record(record_id)
    return jsonify(result)


@staff_views.route('/api/staff/reject/<int:record_id>', methods=['PUT'])
def reject_record_api(record_id):
    result = staffController.reject_record(record_id)
    return jsonify(result)


@staff_views.route('/api/staff/give_award', methods=['POST'])
def give_award_api():
    data = request.json
    result = staffController.give_award(
        data.get('student_id'), 
        data.get('accolade_tier')
    )
    return jsonify(result)
