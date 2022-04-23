from flask import Flask, redirect, render_template, request, session, url_for
from database import create_table, insert_data, login_user

app = Flask(__name__)
app.secret_key = "anytext"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"


@app.route("/")
def homepage():
    if not session.get("email"):
        return render_template("index.html")
    else:
        return render_template("index.html",logout=True)

@app.route("/account")
def account():
    if not session.get("email"):
        return render_template("account.html")
    else:
        return redirect("/")


@app.route("/cart")
def cart():
    return render_template("cart.html")

@app.route("/ebooks")
def ebooks():
    return render_template("ebooks.html")

@app.route("/book_detail")
def book_detail():
    return render_template("book-detail.html")

@app.route("/signup", methods=['POST', 'GET'])
def signup_user():
    if request.method == 'POST':
        email = request.form['signup-email']
        passwd = request.form['signup-password']
        print(email, passwd)
        sign_up(email, passwd)
        return render_template("account.html",msg = "Sign up Successfully")
    else:
        return render_template("account.html", msg="Please Try Again")


@app.route("/login", methods=['POST', 'GET'])
def loginusers():
    if request.method == 'POST':
        email = request.form['login-email']
        passwd = request.form['login-password']
        res = loginUser(email, passwd)
        # if true then go
        if res:
            # store email in session for remember login
            session["email"] = email
            return redirect("/")
        else:
            return "Password or Username is Incorrect"
    else:
        return render_template("account.html")


@app.route("/logout")
def logout():
    session["email"] = None
    return redirect("/")


def sign_up(email, passwd):
    # if table not exist then first create table
    create_table("User", ['username', 'password'])
    # Storing email and password
    insert_data("User", ['username', 'password'], [email, passwd])


def loginUser(email, passwd):
    data = login_user("User", email)
    # Checking user password
    if len(data) > 0:
        if passwd == str(data[0][-1]):
            return True
        else:
            return False
    else:
        return False


if __name__ == "__main__":
    app.run()