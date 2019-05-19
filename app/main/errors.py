from . import main
from flask import render_template, request, url_for
from .forms import ContactForm

@main.app_errorhandler(400)
@main.app_errorhandler(403)
@main.app_errorhandler(404)
@main.app_errorhandler(405)
@main.app_errorhandler(500)
def bad_request(e):
    form = ContactForm(request.form)
    form.next.data = url_for('main.index')
    return render_template('errors/error.html', form=form), 404
