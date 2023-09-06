from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///application_database.db'
db = SQLAlchemy(app)


class UserChatter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    author = db.Column(db.String(30), nullable=False)
    message = db.Column(db.String(1000), nullable=False)


@app.route("/")
def default():
    return redirect(url_for("login_controller"))


@app.route("/login/", methods=["GET", "POST"])
def login_controller():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = UserChatter.query.filter_by(username=username, password=password).first()

        if user:
            return redirect(url_for("profile", username=username))
        else:
            return "Invalid username or password. Please try again."

    return render_template("login.html")


@app.route("/register/", methods=["GET", "POST"])
def register_controller():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        add_user_info = UserChatter(username=username, email=email, password=password)

        try:
            db.session.add(add_user_info)
            db.session.commit()
            return redirect(url_for("profile", username=username))
        except:
            return "There was an issue adding your information to the database"

    return render_template("register.html")


@app.route("/profile/<username>")
def profile(username=None):
    user = UserChatter.query.filter_by(username=username).first()
    if not user:
        return redirect(url_for("login_controller"))

    return render_template("chat_page.html", username=username)


@app.route("/new_message/", methods=["POST"])
def new_message():
    if request.method == "POST":
        author = request.form.get("username")
        message = request.form.get("message")

        new_chat = Chat(author=author, message=message)
        db.session.add(new_chat)
        db.session.commit()

    return redirect(url_for("profile", username=author))


@app.route("/messages/")
def messages():
    chats = Chat.query.all()
    chats_as_json_objects = [{"author": chat.author, "message": chat.message} for chat in chats]
    return jsonify(chats_as_json_objects)

@app.route("/logout/")
def logout():
    # You can clear any user session data here if needed
    # For example, if using Flask-Login, you can use `logout_user()` to clear the user session
    # Alternatively, you can handle any cleanup or logging out processes here

    # For now, we will simply redirect the user back to the login page after clicking the logout button
    return redirect(url_for("login_controller"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
