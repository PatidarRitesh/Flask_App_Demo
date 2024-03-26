from flask import Flask, redirect, url_for, request, Response, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = '10.7.35.113'
app.config['MYSQL_USER'] = 'test'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'imdb'

mysql = MySQL(app)

@app.route('/', methods = ["POST", "GET"])
def main_page():
    return render_template("index.html")

@app.route('/a_1', methods = ["POST", "GET"])
def a_1():
    if request.method == "POST":
        print("HI")
        print(request.method)
        print(request.form["box"])  

        print("TEST")

        cursor = mysql.connection.cursor()
        cursor.execute("select * from genre where movie_id like (select id from movie where title like %s)", (request.form["box"],))

        data = cursor.fetchone()

        cursor.close()

    return render_template("index.html", a_1_data = data) 


@app.route('/a_2', methods = ["POST", "GET"])
def a_2():
    if request.method == "POST":
        cursor = mysql.connection.cursor()
        cursor.execute("select title from movie join genre on movie.id = genre.movie_id where genre = %s limit 10", (request.form["box"],))

        data = cursor.fetchall()

        cursor.close()
    print("HELL")
    return render_template("index.html", a_2_data = data) 


@app.route('/a_3', methods = ["POST", "GET"])
def a_3():
    if request.method == "POST":
        cursor = mysql.connection.cursor()
        cursor.execute("select title from movie where id in (select movie_id from director_mapping where name_id in (select id from `names` where `name` like %s)) limit 5;", (request.form["box"],))

        data = cursor.fetchall()

        cursor.close()
    
    if len(data) == 0:
        return render_template("index.html", a_3_data = [["Ritesh is hero."]]) 

    return render_template("index.html", a_3_data = data) 

@app.route('/a_4', methods = ["POST", "GET"])
def a_4():
    if request.method == "POST":
        cursor = mysql.connection.cursor()
        cursor.execute("select `name` from `names` where id in (select name_id from director_mapping where movie_id = (select id from movie where title like %s)) LIMIT 1", (request.form["box"],))

        data = cursor.fetchall()

        cursor.close()
    
    if len(data) == 0:
        return render_template("index.html", a_4_data = [["Ritesh is hero."]]) 

    return render_template("index.html", a_4_data = data)

if __name__ == '__main__':
   app.run(host="0.0.0.0", port="80", debug = True) 