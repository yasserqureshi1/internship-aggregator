from app import create_app
from flask import render_template

app = create_app()
app.app_context().push()


@app.errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(405)
def error_405(error):
    return render_template('errors/405.html'), 405


@app.errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500


if __name__ == '__main__':
    app.run(use_reloader=False)     # Change this