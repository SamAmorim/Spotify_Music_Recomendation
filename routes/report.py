from flask import Blueprint, render_template

report_bp = Blueprint('report', __name__, url_prefix='/report')

@report_bp.route('/')
def main():
    return render_template('report.html')