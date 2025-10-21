from flask import Blueprint, jsonify, request, render_template, flash, redirect, url_for
from flask_jwt_extended import jwt_required

from App.controllers import student as studentController

student_views = Blueprint('student_views', __name__)

@student_views.route('/students', methods=['GET'])
def students_page():
    return render_template('students.html')


@student_views.route('/api/student', methods=['POST'])
def create_student_api():
    data = request.json
    result = studentController.create_student(
        data.get('name'), 
        data.get('email'), 
        data.get('password'), 
        data.get('programme')
    )
    return jsonify(result)


@student_views.route('/api/student/add_record', methods=['POST'])
def add_student_record_api():
    data = request.json
    result = studentController.add_student_record(
        data.get('student_id'), 
        data.get('hours')
    )
    return jsonify(result)


@student_views.route('/api/student/leaderboard', methods=['GET'])
def view_leaderboard_api():
    num = request.args.get('num', default=3, type=int)
    result = studentController.view_leaderboard(num)
    return jsonify(result)


@student_views.route('/api/student/my_position/<int:student_id>', methods=['GET'])
def view_my_position_api(student_id):
    result = studentController.view_my_position(student_id)
    return jsonify(result)


@student_views.route('/api/student/my_accolades/<int:student_id>', methods=['GET'])
def my_accolades_api(student_id):
    result = studentController.get_my_accolades(student_id)
    return jsonify(result)
