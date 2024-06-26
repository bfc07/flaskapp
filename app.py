import identity.web
import requests
from flask import Flask, redirect, render_template, request, session, url_for, flash, session
from flask_session import Session
from datetime import datetime

import app_config

# connection to database
from models import db, Input
from sqlalchemy.exc import IntegrityError



app = Flask(__name__)
app.config.from_object(app_config)
assert app.config["REDIRECT_PATH"] != "/", "REDIRECT_PATH must not be /"
Session(app)

db.init_app(app)
with app.app_context():
    db.create_all()


# This section is needed for url_for("foo", _external=True) to automatically
# generate http scheme when this sample is running on localhost,
# and to generate https scheme when it is deployed behind reversed proxy.
# See also https://flask.palletsprojects.com/en/2.2.x/deploying/proxy_fix/
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

app.jinja_env.globals.update(Auth=identity.web.Auth)  # Useful in template for B2C
auth = identity.web.Auth(
    session=session,
    authority=app.config["AUTHORITY"],
    client_id=app.config["CLIENT_ID"],
    client_credential=app.config["CLIENT_SECRET"],
)


@app.route("/login")
def login():
    return render_template("login.html", **auth.log_in(
        scopes=app_config.SCOPE, # Have user consent to scopes during log-in
        redirect_uri=url_for("auth_response", _external=True), # Optional. If present, this absolute URL must match your app's redirect_uri registered in Azure Portal
        prompt="select_account",  # Optional. More values defined in  https://openid.net/specs/openid-connect-core-1_0.html#AuthRequest
    ))


@app.route(app_config.REDIRECT_PATH)
def auth_response():
    result = auth.complete_log_in(request.args)
    if "error" in result:
        return render_template("auth_error.html", result=result)
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    return redirect(auth.log_out(url_for("index", _external=True)))


@app.route("/")
def index():
    if not (app.config["CLIENT_ID"] and app.config["CLIENT_SECRET"]):
        # This check is not strictly necessary.
        # You can remove this check from your production code.
        return render_template('config_error.html')
    if not auth.get_user():
        return redirect(url_for("login"))
    return render_template('index.html', user=auth.get_user())


@app.route("/submit", methods=['POST'])
def handle_submit():
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    hosts = session.get('inputs', [])

    data = request.get_json()
    inputs = data.get('inputs', [])
    print(inputs)


        # host = Input(
        #     username=host_data['username'],
        #     host=host_data['host'],
        #     category=host_data['category'],
        #     time=time
        # )

        # try:
        #     db.session.add(host)
        #     db.session.commit()
        #     flash("Submitted", "success")
        # except IntegrityError:
        #     db.session.rollback()  # Rollback the session in case of IntegrityError
        #     flash("Host already exists.", "error")
    
    return redirect(url_for("index"))



if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)