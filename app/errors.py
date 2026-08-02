from flask import render_template, request, url_for
from app import app, db

@app.errorhandler(404)
def not_found(error):
    back_url = url_for('index')
    return render_template('404.html', back_url=back_url), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    back_url = request.referrer or url_for('index')
    return render_template('500.html', back_url=back_url), 500