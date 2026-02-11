from flask import Flask,redirect,url_for,render_template,request

app=Flask(__name__)

@app.route('/')
def welcome():
    return render_template('index.html')

@app.route('/success/<int:score>')
def success(score):
    res=""
    if score>=50:
        res="The Person has passed and the marks is "+ str(score)
    else:
        res="The Person has failed and the marks is "+ str(score)
    return render_template('result.html',result=res)

@app.route('/fail/<int:score>')
def fail(score):
    return "The Person has failed and the marks is "+ str(score)

@app.route('/results/<int:marks>')
def results(marks):
    result=""
    if marks<50:
        result='fail'
    else:
        result='success'
    return redirect(url_for(result,score=marks))

@app.route('/submit',methods=['POST', 'GET'])
def submit():
    total_score=0
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        country=request.form['country']
    
    res=""
    if total_score>=50:
        res="success"
    else:
      res="fail"
    return redirect(url_for(res,score=total_score))




if __name__=='__main__':
    app.run(debug=True)



#----------------------------------------------------------


from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "supersecretkey")  # Veiligere optie

DB_FILE = "Epstein_Files.db"
TABLE_NAME = "Epstein_Contributors"

# Functie om te checken of user bestaat
def check_user(username_to_check):
    if not os.path.exists(DB_FILE):
        return {"status": "error", "message": "Database does not exist yet."}

    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()

        # Check of tabel bestaat
        c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{TABLE_NAME}'")
        if not c.fetchone():
            return {"status": "error", "message": f"Table '{TABLE_NAME}' does not exist."}

        # Check of username bestaat
        c.execute(f"SELECT * FROM {TABLE_NAME} WHERE username = ?", (username_to_check,))
        user = c.fetchone()

        if user:
            return {"status": "found", "message": f"User '{username_to_check}' already exists.", "data": user}
        else:
            return {"status": "not_found", "message": f"User '{username_to_check}' does not exist."}

    except sqlite3.Error as e:
        return {"status": "error", "message": f"Database error: {e}"}

    finally:
        if 'conn' in locals():
            conn.close()

# Home page
@app.route("/")
def index():
    return render_template("index.html")

# Form submit
@app.route("/submit", methods=["POST"])
def submit():
    username = request.form.get("username")
    password = request.form.get("password")
    country = request.form.get("country")

    if not username or not password or not country:
        flash("I wish you luck")
        return redirect(url_for("index"))

    # Check of user al bestaat
    result = check_user(username)
    if result["status"] == "found":
        flash(result["message"])
        return redirect(url_for("index"))
    elif result["status"] == "error":
        flash(f"Error: {result['message']}")
        return redirect(url_for("index"))

    # Voeg user toe
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute(f"INSERT INTO Epstein_Contributors (username, password, country) VALUES (?, ?, ?)",
                  (username, password, country))
        conn.commit()
        flash(f"User '{username}' added successfully!")
    except sqlite3.IntegrityError:
        flash(f"User '{username}' already exists (IntegrityError).")
    except sqlite3.Error as e:
        flash(f"Database error: {e}")
    finally:
        conn.close()

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
