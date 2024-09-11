#!/usr/bin/python3

from api.blueprint import app_views, auth
# from models.v1.report import Report
from models import storage, Report
from flask import jsonify, request
# import requests
from api.blueprint.Mailing.controller import runner

api = "https://unikribmailer.onrender.com"

@app_views.route('/reports', strict_slashes=False)
@auth.login_required(role="admin")
def all_reports():
    """This returns a list of all reports"""
    reports = []

    for key, obj in storage.all(Report).items():
        reports.append(obj.to_dict())

    return jsonify(reports)

@app_views.route('/reports/<report_id>', strict_slashes=False)
@auth.login_required(role="admin")
def get_report(report_id):
    """This returns a report based on id"""
    report = storage.get('Report', report_id)
    if report is None:
        return jsonify({"error": "Report not found"}), 404
    return jsonify(report.to_dict())

@app_views.route('/users/<user_id>/reports', strict_slashes=False)
@auth.login_required(role="admin")
def get_user_reports(user_id):
    """This returns a list of all the reports filed against a user"""
    reports = storage.search(Report, reported=user_id)
    if reports is None:
        return jsonify({"error":'No reports for this user'}), 404
    report = []
    for obj in reports:
        report.append(obj.to_dict())
    return jsonify(report)

@app_views.route('/reports', methods=['POST'], strict_slashes=False)
@auth.login_required
def create_report():
    if not request.json:
        return jsonify("Not a valid json"), 400
    report_dict = request.get_json()

    if "topic" not in report_dict or report_dict['topic'] == "":
        return jsonify({"error":"Please include a topic"}), 400
    if "reporter" not in report_dict or report_dict['reporter'] == "":
        user = auth.current_user()
        report_dict['reporter'] = user.id
    if "reported" not in report_dict or report_dict['reported'] == "":
        return jsonify({"error": "Please include the reported"}), 400

    reported = report_dict['reported']

    if user.id == reported:
        return jsonify("You can not leave a report for yourself"), 400

    report = Report(**report_dict)
    report.save()
    res = runner.newReport(topic=report.topic, reporter=report.reporter,
                    reported=report.reported, description=report.description)
    if res['status_code'] != 200:
        return jsonify("Report not added"), 404
    return jsonify(report.to_dict())

