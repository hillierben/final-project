import words
import requests
from flask import Flask, render_template, request, session, redirect
from flask_session import Session
import random
import times_tables
from helpers import error, login_required
import helpers
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

tablesDict = {}
spellingDict = {}

@app.route("/")
def index():
    if request.method == "GET":
        return render_template("index.html")

@app.route("/stickers", methods=["GET", "POST"])
@login_required
def stickers():
    
    #if request.method == "GET":
    with sqlite3.connect("tracker.db") as con:
        con.row_factory = sqlite3.Row
        id = int(session["user_id"])
        userPoints = con.execute("SELECT * FROM timestables WHERE user_id = ?", (id,))
        points = userPoints.fetchall()

        # print total timestables points on stickers page
        totalTimestablesPoints = con.execute("SELECT SUM(twoXPoints + threeXPoints + fourXPoints + fiveXPoints + sixXPoints + sevenXPoints + eightXPoints + nineXPoints + tenXPoints + elevenXPoints + twelveXPoints) AS total FROM timestables WHERE user_id = ?", (id,))
        timestablesPoints = totalTimestablesPoints.fetchone()
        print(timestablesPoints)

        # print total spelling points on stickers page
        totalSpellingPoints = con.execute("SELECT SUM(threeLettPoints + fourLettPoints + fiveLettPoints + sixLettPoints + sevenLettPoints + eightLettPoints + nineLettPoints + tenLettPoints) AS total FROM spelling WHERE user_id = ?", (id,))
        spellingPoints = totalSpellingPoints.fetchone()

        # Dict of all points
        tablesDict = {
            "twoXPoints": points[0]["twoXPoints"],
            "threeXPoints": points[0]["threeXPoints"],
            "fourXPoints": points[0]["fourXPoints"],
            "fiveXPoints": points[0]["fiveXPoints"],
            "sixXPoints": points[0]["sixXPoints"],
            "sevenXPoints": points[0]["sevenXPoints"],
            "eightXPoints": points[0]["eightXPoints"],
            "nineXPoints": points[0]["nineXPoints"],
            "tenXPoints": points[0]["tenXPoints"],
            "elevenXPoints": points[0]["elevenXPoints"],
            "twelveXPoints": points[0]["twelveXPoints"]
        }

        spellPoints = con.execute("SELECT * FROM spelling WHERE user_id = ?", (id,))
        points = spellPoints.fetchall()

        spellingDict = {
            "threeLettPoints": points[0]["threeLettPoints"],
            "fourLettPoints": points[0]["fourLettPoints"],
            "fiveLettPoints": points[0]["fiveLettPoints"],
            "sixLettPoints": points[0]["sixLettPoints"],
            "sevenLettPoints": points[0]["sevenLettPoints"],
            "eightLettPoints": points[0]["eightLettPoints"],
            "nineLettPoints": points[0]["nineLettPoints"],
            "tenLettPoints": points[0]["tenLettPoints"]
        }




        # Decide if stickers will be shown            
        image = []
        for row in tablesDict:
            s = str(row)
            sqlPoint = con.execute(f"SELECT {s} FROM timestables WHERE user_id = ?", (id,))
            point = sqlPoint.fetchone()[0]
            print(point)
            
            if point >= 12:
                image.append("images")
            elif point < 12:
                image.append("black_images")

        for row in spellingDict:
            s = str(row)
            sqlPoint = con.execute(f"SELECT {s} FROM spelling WHERE user_id = ?", (id,))
            point = sqlPoint.fetchone()[0]
            print(point)
            
            if point >= 12:
                image.append("images")
            elif point < 12:
                image.append("black_images")

        return render_template("stickers.html", timestables=tablesDict, spelling=spellingDict, spellingPoints=spellingPoints['total'], timestablesPoints=timestablesPoints['total'], image=image, tDict=tablesDict, sDict=spellingDict)


@app.route("/login", methods=["GET", "POST"])
def login():

    # clear current saved login details (logout)
    session.clear()

    if request.method == "POST":
        # check username/password not empty
        if not request.form.get("username"):
            return error("Please enter Username")
        if not request.form.get("password"):
            return error("Please enter Password")

        username = request.form.get("username")

        # check username in SQL
        with sqlite3.connect("tracker.db") as con:
            con.row_factory = sqlite3.Row
            rows = con.execute("SELECT * FROM users WHERE username = ?", [request.form.get("username")])
            row = rows.fetchone()
            print(row)
            rose = rows.fetchall()
            
            if row == None:
                return error("invalid username and/or password", 403)

            if not check_password_hash(row['hash'], request.form.get("password")):
                return error("invalid username and/or password", 403)
 
        session["user_id"] = row["id"]
        name = (request.form.get("username"))
        "".join(name)
        print(name)
        session["username"] = name

        return redirect("/stickers")

    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/registration", methods=["GET", "POST"])
def registration():

    if request.method == "POST":
        if request.form.get("username") == "":
            return error("Please enter Username")
        if request.form.get("age") == "not":
            return error("Please select Age")
        if request.form.get("password") == "":
            return error("Please enter password")
        if request.form.get("confirmation") != request.form.get("password"):
            return error("Passwords do not match")
        
        username = request.form.get("username")
        age = request.form.get("age")
        password = request.form.get("password")
        hash = generate_password_hash(password, method="pbkdf2:sha256", salt_length=8)
        
        con = sqlite3.connect("tracker.db")
        con.row_factory = sqlite3.Row
        # if username already exists
        check_exists = con.execute("SELECT username FROM users WHERE username= ?", [username])
        # convert table object to tuple
        try:
            checked = list(check_exists)[0]
            print(checked)
            listypoo = list(checked)
            if username in listypoo:
                return error("Username already exists")
        except:
            pass

        with sqlite3.connect("tracker.db") as con:
            con.row_factory = sqlite3.Row
            con.execute("INSERT INTO users(username, age, hash) VALUES(?, ?, ?)", (username, age, hash))
            userId = con.execute("SELECT id FROM users WHERE username = ?", [username])
            id = userId.fetchone()
            con.execute("INSERT INTO spelling(user_id, threeLettPoints, fourLettPoints, fiveLettPoints, sixLettPoints, sevenLettPoints, eightLettPoints, nineLettPoints, tenLettPoints) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (id["id"], '0', '0', '0', '0', '0', '0', '0', '0'))
            con.execute("INSERT INTO timestables(user_id, twoXPoints, threeXPoints, fourXPoints, fiveXPoints, sixXPoints, sevenXPoints, eightXPoints, nineXPoints, tenXPoints, elevenXPoints, twelveXPoints) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (id["id"], '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'))

            return render_template("login.html")

    return render_template("registration.html")


@app.route("/timestables", methods=["GET", "POST"])
@login_required
def timestables():
    global TEST
    global TIMESTABLE
    if request.method == "POST":
        if request.form.get("button") == "2x":
            TEST = times_tables.twoTimesTable
            TIMESTABLE = 'twoXPoints' 
            key = random.choice(list(times_tables.twoTimesTable))
            with open("tempTables.txt", "w") as file:
                file.write(key)
        if request.form.get("button") == "3x":
            TEST = times_tables.threeTimesTable
            TIMESTABLE = 'threeXPoints' 
            key = random.choice(list(times_tables.threeTimesTable))
            with open("tempTables.txt", "w") as file:
                file.write(key)
        if request.form.get("button") == "4x":
            TEST = times_tables.fourTimesTable
            TIMESTABLE = 'fourXPoints' 
            key = random.choice(list(times_tables.fourTimesTable))
            with open("tempTables.txt", "w") as file:
                file.write(key)
        if request.form.get("button") == "5x":
            TEST = times_tables.fiveTimesTable
            TIMESTABLE = 'fiveXPoints' 
            key = random.choice(list(times_tables.fiveTimesTable))
            with open("tempTables.txt", "w") as file:
                file.write(key)
        if request.form.get("button") == "6x":
            TEST = times_tables.sixTimesTable
            TIMESTABLE = 'sixXPoints' 
            key = random.choice(list(times_tables.sixTimesTable))
            with open("tempTables.txt", "w") as file:
                file.write(key)
        if request.form.get("button") == "7x":
            TEST = times_tables.sevenTimesTable
            TIMESTABLE = 'sevenXPoints' 
            key = random.choice(list(times_tables.sevenTimesTable))
            with open("tempTables.txt", "w") as file:
                file.write(key)
        if request.form.get("button") == "8x":
            TEST = times_tables.eightTimesTable
            TIMESTABLE = 'eightXPoints' 
            key = random.choice(list(times_tables.eightTimesTable))
            with open("tempTables.txt", "w") as file:
                file.write(key)
        if request.form.get("button") == "9x":
            TEST = times_tables.nineTimesTable
            TIMESTABLE = 'nineXPoints' 
            key = random.choice(list(times_tables.nineTimesTable))
            with open("tempTables.txt", "w") as file:
                file.write(key)
        if request.form.get("button") == "10x":
            TEST = times_tables.tenTimesTable
            TIMESTABLE = 'tenXPoints' 
            key = random.choice(list(times_tables.tenTimesTable))
            with open("tempTables.txt", "w") as file:
                file.write(key)
        if request.form.get("button") == "11x":
            TEST = times_tables.elevenTimesTable
            TIMESTABLE = 'elevenXPoints' 
            key = random.choice(list(times_tables.elevenTimesTable))
            with open("tempTables.txt", "w") as file:
                file.write(key)
        if request.form.get("button") == "12x":
            TEST = times_tables.twelveTimesTable
            TIMESTABLE = 'twelveXPoints' 
            key = random.choice(list(times_tables.twelveTimesTable))
            with open("tempTables.txt", "w") as file:
                file.write(key)

        check = ""
        with open("tempTables.txt", "r") as file:
            key = file.readlines()
        if request.method == "POST" and request.form.get("submit") == "yes":
            if request.form.get("answer") == times_tables.allTimesTables[key[0]]:
                print("Fuck Yea!")
                check = "correct"
                key = random.choice(list(TEST))
                print(key)
                with open("tempTables.txt", "w") as file:
                    file.write(key)

                
                # update user points
                with sqlite3.connect("tracker.db") as con:
                    con.row_factory = sqlite3.Row
                    con.execute(f"UPDATE timestables SET {TIMESTABLE} = {TIMESTABLE} + 1")


                return render_template("timestables.html", key=key, check=check)
            else:
                print("Balls")
                check = "wrong"
        return render_template("timestables.html", key=key[0], check=check)
    else:
        pick = ""
        return render_template("timestables.html", key=pick)


@app.route("/spelling", methods=["GET", "POST"])
@login_required
def spelling():

    definition = None 
    audio = None 
    word_input = None
    check = ""
    global SPELT
    global LENGTH

    if request.method == "POST" and request.form.get("spell") != None:
        answer = request.form.get("spell")
        with open("temp.txt", "r") as file:
            compare = file.readline()

        if answer == compare:
            check = "correct"
            print(check)
            word_input = random.sample(SPELT, k=1)[0]
            print(word_input)
            api = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word_input}"
            word_request = requests.get(api)
            spelling = word_request.json()
            word = spelling[0]["word"]
            definition = spelling[0]["meanings"][0]["definitions"][0]["definition"]
            audio = spelling[0]["phonetics"][0]["audio"]

            with open("temp.txt", "w") as file:
                file.write(word_input)

            # update user points
            with sqlite3.connect("tracker.db") as con:
                con.row_factory = sqlite3.Row
                print(session["user_id"])
                con.execute(f"UPDATE spelling SET {LENGTH} = {LENGTH} + 1 WHERE user_id = ?",[session["user_id"]])

        else:
            check = "wrong"
            api = f"https://api.dictionaryapi.dev/api/v2/entries/en/{compare}"
            word_request = requests.get(api)
            spelling = word_request.json()
            word = spelling[0]["word"]
            definition = spelling[0]["meanings"][0]["definitions"][0]["definition"]
            audio = spelling[0]["phonetics"][0]["audio"]


        return render_template("spelling.html", check=check, definition=definition, audio=audio, word=word_input)
    
    if request.method == "POST":
        # Randomly choose word from LIST - Depends on length of word button
        if request.form.get("submit") == "three":
            SPELT = words.threeLetters
            LENGTH = 'threeLettPoints'
            word_input = random.sample(words.threeLetters, k=1)[0]
            print(word_input)
        if request.form.get("submit") == "four":
            SPELT = words.fourLetters
            LENGTH = 'fourLettPoints'
            word_input = random.sample(words.fourLetters, k=1)[0]
            print(word_input)
        if request.form.get("submit") == "five":
            SPELT = words.fiveLetters
            LENGTH = 'fiveLettPoints'
            word_input = random.sample(words.fiveLetters, k=1)[0]
            print(word_input)
        if request.form.get("submit") == "six":
            SPELT = words.sixLetters
            LENGTH = 'sixLettPoints'
            word_input = random.sample(words.sixLetters, k=1)[0]
            print(word_input)
        if request.form.get("submit") == "seven":
            SPELT = words.sevenLetters
            LENGTH = 'sevenLettPoints'
            word_input = random.sample(words.sevenLetters, k=1)[0]
            print(word_input)
        if request.form.get("submit") == "eight":
            SPELT = words.eightLetters
            LENGTH = 'eightLettPoints'
            word_input = random.sample(words.eightLetters, k=1)[0]
            print(word_input)
        if request.form.get("submit") == "nine":
            SPELT = words.nineLetters
            LENGTH = 'nineLettPoints'
            word_input = random.sample(words.nineLetters, k=1)[0]
            print(word_input)
        if request.form.get("submit") == "ten":
            SPELT = words.tenLetters
            LENGTH = 'tenLettPoints'
            word_input = random.sample(words.tenLetters, k=1)[0]
            print(word_input)

        # Retieve Word from Dictionary - word, definition, audio example
        api = f"https://www.dictionaryapi.com/api/v3/references/learners/json/{word_input}?key=085a4ba8-dbd2-4e41-8df1-abff8d8aefcb"
        word_request = requests.get(api)
        print(word_request)
        spelling = word_request.json()
        print(spelling)
        word = word_input
        definition = spelling[0]["shortdef"][0]
        print(definition)
        audio = words.audioDict[word_input]

        print(word_input)
        with open("temp.txt", "w") as file:
            file.write(word_input)
    
        return render_template("spelling.html", definition=definition, audio=audio, check=check, word=word_input)
    else:
        pick = ""
        return render_template("spelling.html", definition=pick)
    

@app.route("/welcome")
@login_required
def welcome():

    #if request.method == "GET":
    with sqlite3.connect("tracker.db") as con:
        con.row_factory = sqlite3.Row
        id = int(session["user_id"])
        userPoints = con.execute("SELECT * FROM timestables WHERE user_id = ?", (id,))
        points = userPoints.fetchall()

        # print total timestables points on stickers page
        totalTimestablesPoints = con.execute("SELECT SUM(twoXPoints + threeXPoints + fourXPoints + fiveXPoints + sixXPoints + sevenXPoints + eightXPoints + nineXPoints + tenXPoints + elevenXPoints + twelveXPoints) AS total FROM timestables WHERE user_id = ?", (id,))
        timestablesPoints = totalTimestablesPoints.fetchone()
        print(timestablesPoints)

        # print total spelling points on stickers page
        totalSpellingPoints = con.execute("SELECT SUM(threeLettPoints + fourLettPoints + fiveLettPoints + sixLettPoints + sevenLettPoints + eightLettPoints + nineLettPoints + tenLettPoints) AS total FROM spelling WHERE user_id = ?", (id,))
        spellingPoints = totalSpellingPoints.fetchone()

    # Redirect user to login form
    return redirect("/stickers")
