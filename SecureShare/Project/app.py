from flask import Flask, request, redirect, url_for, flash, render_template, session, send_file
from pymongo import MongoClient
import user_details
import os
from werkzeug.utils import secure_filename
import crypto
import mail_sender
import threading
import threaded_functions as tf
from flask_socketio import SocketIO, emit

UPLOAD_FOLDER = os.getcwd() + "\\files"
UPLOAD_PASSWORDS = UPLOAD_FOLDER + "\\password"
DOWNLOAD_FOLDER = UPLOAD_FOLDER + "\\to_download"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx', 'pptx', 'mp4'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
mongodb_access = MongoClient("mongodb+srv://Afek:DHR9H03J@secureshare.tus0w.mongodb.net/"
                             "AfekDropBox?retryWrites=true&w=majority")
users_db = mongodb_access.AfekDropBox.users
app.secret_key = "afek"
sio = SocketIO(app, manage_session=False)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/download", methods=['GET', 'POST'])
def download_page():
    files = os.listdir(UPLOAD_FOLDER)
    files.remove("to_download")
    for file in files:
        if not os.path.isfile(f"{UPLOAD_FOLDER}\\{file}") or "." not in file:
            files.remove(file)
    return render_template("download.html", files=files)


@app.route("/password/<filename>", methods=['GET', 'POST'])
def check_pass(filename):
    if request.method == "GET":
        return render_template("password_check.html")
    else:
        password = request.form.get("password")
        with open(f"{UPLOAD_PASSWORDS}\\{filename}", "r") as f:
            real_password = crypto.decrypt_file(bytes(f.read(), 'utf-8')).decode('utf-8')
        if password == real_password:
            return download_file(filename)
        else:
            flash("Invalid Password.")
            return redirect(url_for("check_pass", filename=filename))


@app.route("/download_file/<filename>", methods=['GET', 'POST'])
def download_file(filename):
    if session.get("username"):
        with open(f"{DOWNLOAD_FOLDER}\\{filename}", "wb") as fIn:
            with open(f"{UPLOAD_FOLDER}\\{filename}", "rb") as fOut:
                fIn.write(crypto.decrypt_file(fOut.read()))
        path = f"{DOWNLOAD_FOLDER}\\{filename}"
        return send_file(path, as_attachment=True)
    else:
        flash("You must log in before downloading a file.")
        return redirect(url_for("login_page"))


@app.route("/insert_password/<filename>", methods=['GET', 'POST'])
def enter_pass(filename):
    if request.method == "GET":
        return render_template("password_insert.html")
    else:
        password = request.form.get("password")
        with open(f"{UPLOAD_PASSWORDS}\\{filename}", "wb") as f:
            f.write(crypto.encrypt_file(bytes(password, 'utf-8')))
        flash(f"{filename} uploaded.")
        return redirect(url_for("home_page"))


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part.')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file.')
            return redirect(request.url)
        if session.get("username"):
            if file and allowed_file(file.filename) and file.filename.split(".") is not None:
                filename = secure_filename(file.filename)
                file_data = file.read()
                encrypted_data = crypto.encrypt_file(file_data)
                with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), "wb") as f:
                    f.write(encrypted_data)
                return redirect(url_for("enter_pass", filename=filename))
            else:
                flash("Unfortunately, Can't upload this file.")
                return redirect(url_for("upload_file"))
        else:
            flash("You must log in before uploading a file.")
            return redirect(url_for("login_page"))
    else:
        return render_template("upload.html")


@app.route("/", methods=['POST', 'GET'])
def home_page():
    usersCounter = tf.count_users()
    filesCount = tf.count_files()
    return render_template("index.html", usersCounter=usersCounter, filesCounter=filesCount)


@sio.on("get_users_count")
def return_users_count():
    usersCounter = tf.count_users()
    emit("received_users_count", usersCounter)


@sio.on("get_files_count")
def return_files_count():
    filesCount = tf.count_files()
    emit("received_files_count", filesCount)


@app.route("/login", methods=['POST', 'GET'])
def login_page():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        for line in users_db.find():
            dec_password = crypto.decrypt_file(line["password"])
            if line["username"] == username and dec_password.decode('utf-8') == password:
                session["username"] = username
                flash(f"Logged in as {username}.")
                return redirect(url_for("home_page"))
        flash("Invalid username or password.")
        return redirect(url_for("login_page"))
    if request.method == "GET":
        return render_template("login.html")


@app.route("/logout", methods=['POST', 'GET'])
def logout_page():
    if request.method == "POST":
        if session.get("username"):
            session["username"] = None
            flash("You logged out successfully.")
            return redirect(url_for("home_page"))
        else:
            flash("You can't logout if you are not logged in.")
            return redirect(url_for("home_page"))
    if request.method == "GET":
        return render_template("logout.html")


@app.route('/register', methods=['POST', 'GET'])  # registration
def register_page():
    if request.method == "POST":
        new_user = user_details.User(request.form.get("username"), request.form.get("password"),
                                     request.form.get("email"))
        errors = new_user.register()
        for line in users_db.find():
            if line["username"] == new_user.getusername():
                errors.append("Username already used.")
                break
            if line["email"] == new_user.getemail():
                errors.append("Email already used.")
                break
        if errors:
            for error in errors:
                flash(error)
            return redirect(url_for("register_page"))
        else:
            enc_password = crypto.encrypt_file(bytes(new_user.getpassword(), 'utf-8'))
            users_db.insert_one({"username":  new_user.getusername(),
                                 "password": enc_password, "email": new_user.getemail()})
            mail_sender.send_register_mail(new_user.getemail(), new_user.getusername(), new_user.getpassword())
            flash("Success! Please Login.")
            return redirect(url_for("login_page"))
    else:
        return render_template("register.html")


@app.route("/forgotpassword", methods=['POST', 'GET'])
def forgot_password():
    if request.method == 'GET':
        return render_template("forgot_password.html")
    else:
        email = request.form.get("email")
        for line in users_db.find():
            if line["email"] == email:
                password = line["password"]
                username = line["username"]
                email = line["email"]
                dec_password = crypto.decrypt_file(password).decode('utf-8')
                mail_sender.send_password_mail(email, username, dec_password)
                flash('A mail sent to you.')
                return redirect(url_for("login_page"))
        flash('There is no account with this mail.')
        return redirect(url_for("forgot_password"))


@app.route("/changepassword", methods=['GET', 'POST'])
def change_password():
    if request.method == 'GET':
        return render_template("change_password.html")
    else:
        email = request.form.get("email")
        current_password = request.form.get("currentpassword")
        mail_flag = False
        password_flag = False
        for line in users_db.find():
            if email == line["email"]:
                mail_flag = True
                dec_password = crypto.decrypt_file(line["password"]).decode('utf-8')
                if dec_password == current_password:
                    password_flag = True
                    break
        if not mail_flag:
            flash('There is no account with this mail.')
            return redirect(url_for("register_page"))
        elif mail_flag and not password_flag:
            flash('Invalid password.')
            return redirect(url_for("change_password"))
        else:  # Mail and password are correct
            new_password = request.form.get("newpassword")
            new_password_confirm = request.form.get("newpasswordconfirm")
            if new_password == new_password_confirm:
                for line in users_db.find():
                    if line["email"] == email:
                        username = line["username"]
                        enc_password = crypto.encrypt_file(bytes(new_password, 'utf-8'))
                        users_db.delete_one(line)
                        users_db.insert_one({"username":  username, "password": enc_password, "email": email})
                        break
                mail_sender.send_new_password_mail(email, username, new_password)
                flash('Password Changed.')
                return redirect(url_for("login_page"))
            else:
                flash('Two different password are given.')
                return redirect(url_for("change_password"))


@app.errorhandler(404)
def page_not_found(error):
    return render_template("page_not_found.html"), 404


@app.errorhandler(500)
def bug_in_loading(error):
    return render_template("loading_error.html"), 500


def run_flask():
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)


if __name__ == "__main__":
    remover_no_password = threading.Thread(target=tf.uploaded_without_password, args=())
    remover_decrypted = threading.Thread(target=tf.remove_decrypted_files, args=())
    flask_runner = threading.Thread(target=run_flask, args=())
    remover_no_password.start()
    remover_decrypted.start()
    flask_runner.start()
    remover_no_password.join()
    remover_decrypted.join()
    flask_runner.join()
