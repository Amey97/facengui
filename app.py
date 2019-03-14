from flask import Flask, json, Response, request, render_template
from werkzeug.utils import secure_filename
from os import path, getcwd
import time
from db import Database
from face import Face
import db as dbHandler
from md5 import test
import sqlite3

import json
app = Flask(__name__)

#1.configuration settings
app.config['file_allowed'] = ['image/png', 'image/jpeg']
app.config['storage'] = path.join(getcwd(), 'storage')
app.db = Database()
app.face = Face(app)


def success_handle(output, status=200, mimetype='application/json'):
    return Response(output, status=status, mimetype=mimetype)


def error_handle(error_message, status=500, mimetype='application/json'):
    return Response(json.dumps({"error": {"message": error_message}}), status=status, mimetype=mimetype)

#default page
@app.route('/')
def index():
    return render_template('home.html')

#login page
@app.route('/login', methods=['POST','GET'])
def login():
   if request.method == 'POST':
      username = request.form['username']
      password = request.form['password']
      demo = test(str(password))
      print (demo)
      print (password)
      #password.encode("ascii")
      #demo = [input(password).encode("ascii")]
      #print (demo)
      #for message in demo:
      #  result = md5_to_hex(md5(message))
      #print (password)
      #print (result)
      con = sqlite3.connect("database.db")
      con.row_factory = sqlite3.Row
      cur = con.cursor()
      cur.execute("SELECT * from login WHERE username=? AND password=?", (username, demo))
      results = cur.fetchall()
      for row in results:
         type = row[2]
      if type == "admin":
         return admin_home()
      elif type == "police":
          return police_home()
      elif type == "company":
         return company_home()
   else:
      print("error")
      return render_template('home.html')

#2 police_db
@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        name_of_police_stn = request.form['name_of_police_stn']
        police_stn_no = request.form['police_stn_no']
        region1 = request.form['region1']
        address_ps = request.form['address_ps']
        ps_phone1 = request.form['ps_phone1']
        head_officer = request.form['head_officer']
        head_id = request.form['head_id']
        head_aadhar = request.form['head_aadhar']
        head_pan = request.form['head_pan']
        head_email = request.form['head_email']
        head_mob_no = request.form['head_mob_no']
        head_user_id1 = request.form['head_user_id1']
        head_pass1 = request.form['head_pass1']
        head_pass21 = request.form['head_pass21']
        pass_police = test(str(head_pass1))
        print (pass_police)
        #print (head_pan)
        app.db.insertUser(name_of_police_stn, police_stn_no, region1, address_ps, ps_phone1, head_officer, head_id, head_aadhar, head_pan, head_email, head_mob_no, head_user_id1, pass_police, head_pass21)

        return render_template('home.html')
    else:
        return render_template('home.html')


@app.route('/admin_user2det')
def show():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("select * from police_reg")

    rows = cur.fetchall();
    return render_template("admin_user2det.html", rows=rows)

#3,com

@app.route('/addrec1', methods=['POST', 'GET'])
def addrec1():
    if request.method == 'POST':
        name_of_comp = request.form['name_of_comp']
        reg_no = request.form['unique_reg_no']
        region= request.form['region']
        address_comp = request.form['address_comp']
        ps_phone = request.form['ps_phone']
        hr_name = request.form['hr_name']
        emp_id = request.form['emp_id']
        hr_aadhar = request.form['hr_aadhar']
        hr_pan = request.form['hr_pan']
        hr_email = request.form['hr_email']
        hr_mob_no = request.form['hr_mob_no']
        head_user_id = request.form['head_user_id']
        head_pass = request.form['head_pass']
        head_pass2 = request.form['head_pass2']
        pass_comp = test(str(head_pass))
        print (pass_comp)
        app.db.insertUser1('INSERT INTO company_reg (name_of_comp, reg_no, region, address_comp,ps_phone, hr_name, emp_id, hr_aadhar, hr_pan, hr_email, hr_mob_no, head_user_id, head_pass, head_pass2) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)',name_of_comp, reg_no, region, address_comp, ps_phone, hr_name, emp_id, hr_aadhar, hr_pan, hr_email, hr_mob_no, head_user_id, pass_comp, head_pass2)
        #app.db.insertUser(name_of_comp, reg_no, region, address_comp, ps_phone, hr_name, emp_id, hr_aadhar, hr_pan, hr_email, hr_mob_no, head_user_id, head_pass, head_pass2)
        return render_template('home.html')
    else:
        return render_template('home.html')


@app.route('/admin_user3det')
def list():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("select * from company_reg")

    rows = cur.fetchall();
    return render_template("admin_user3det.html", rows=rows)

@app.route('/admin_home')
def admin_home():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from company_reg where status='false' ")
    row1 = cur.fetchall()
    cur.execute("select * from police_reg where status='false' ")
    row2 = cur.fetchall()
    return render_template("admin_home.html", row1=row1, row2=row2)

@app.route('/police_home')
def police_home():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("select * from users ORDER BY id DESC")

    rows = cur.fetchall();

    return render_template("police_home.html", rows=rows)

#4.face wala db
def get_user_by_id(user_id):
    user = {}
    results = app.db.select(
        'SELECT users.id, users.name, users.created, faces.id, faces.user_id, faces.filename,faces.created FROM users LEFT JOIN faces ON faces.user_id = users.id WHERE users.id = ?',
        [user_id])

    index = 0
    for row in results:
        # print(row)
        face = {
            "id": row[3],
            "user_id": row[4],
            "filename": row[5],
            "created": row[6],
        }
        if index == 0:
            user = {
                "id": row[0],
                "name": row[1],
                "created": row[2],
                "faces": [],
            }
        if row[3]:
            user["faces"].append(face)
        index = index + 1

    if 'id' in user:
        return user
    return None

@app.route('/delete_user_by_id', methods=['POST', 'GET'])
def delete_user_by_id():
    if request.method == 'POST':
        user_id = request.form['user_id']
        app.db.delete('DELETE FROM users WHERE users.id = ?', [user_id])
    # also delete all faces with user id
        app.db.delete('DELETE FROM faces WHERE faces.user_id = ?', [user_id])
        return render_template('layout_police.html')
    else:
        return render_template('layout_police.html')

#5. Actual working part


@app.route('/api', methods=['GET'])
def homepage():
    output = json.dumps({"api": '1.0'})
    return success_handle(output)


@app.route('/api/train', methods=['POST'])
def train():
    output = json.dumps({"success": True})

    if 'file' not in request.files:

        print ("Face image is required")
        return error_handle("Face image is required.")
    else:

        print("File request", request.files)
        file = request.files['file']

        if file.mimetype not in app.config['file_allowed']:

            print("File extension is not allowed")

            return error_handle("We are only allow upload file with *.png , *.jpg")
        else:

            # get name in form data
            name = request.form['name']
            contact = request.form['contact']
            address = request.form['address']
            aadhar = request.form['aadhar']
            crime = request.form['crime']
            act = request.form['act']
            gender = request.form['gender']
            dob = request.form['dob']


            #print("Information of that face", dob)

            print("File is allowed and will be saved in ", app.config['storage'])
            filename = secure_filename(file.filename)
            trained_storage = path.join(app.config['storage'], 'trained')
            file.save(path.join(trained_storage, filename))
            # let start save file to our storage

            # save to our sqlite database.db
            created = int(time.time())
            user_id = app.db.insert('INSERT INTO users(name, contact,address,aadhar,crime,act,gender,dob, created) values(?,?,?,?,?,?,?,?,?)', [name, contact, address,aadhar,crime,act,gender,dob, created])

            if user_id:

                print("User saved in data", name, user_id)
                # user has been save with user_id and now we need save faces table as well

                face_id = app.db.insert('INSERT INTO faces(user_id, filename, created) values(?,?,?)',
                                        [user_id, filename, created])

                if face_id:

                    print("cool face has been saved")
                    face_data = {"id": face_id, "filename": filename, "created": created}
                    return_output = json.dumps({"id": user_id, "name": name, "face": [face_data]})
                    return success_handle(return_output)
                else:

                    print("An error saving face image.")

                    return error_handle("n error saving face image.")

            else:
                print("Something happend")
                return error_handle("An error inserting new user")

        print("Request is contain image")
    return success_handle(output)

# route for user profile
@app.route('/api/users/<int:user_id>', methods=['GET', 'DELETE'])
def user_profile(user_id):
    if request.method == 'GET':
        user = get_user_by_id(user_id)
        if user:
            return success_handle(json.dumps(user), 200)
        else:
            return error_handle("User not found", 404)
    if request.method == 'DELETE':
        delete_user_by_id(user_id)
        return success_handle(json.dumps({"deleted": True}))


#criminal profile
@app.route('/view/<id>', methods=['POST', 'GET'])
def view(id):
    print (id)
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * from users WHERE id=?", [id])
    results = cur.fetchall()
    con.commit()
    return render_template('criminal_profile.html', rows=results)


def get_users_data(user_id):
    results = app.db.select('SELECT * from users WHERE id=?',[user_id])

    for row in results:
         print(row)
    return results

# router for recognize a unknown face
@app.route('/api/recognize', methods=['POST','GET'])
def recognize():
    if 'file' not in request.files:
        return error_handle("Image is required")
    else:
        file = request.files['file']
        # file extension valiate
        if file.mimetype not in app.config['file_allowed']:
            return error_handle("File extension is not allowed")
        else:

            filename = secure_filename(file.filename)
            unknown_storage = path.join(app.config["storage"], 'unknown')
            file_path = path.join(unknown_storage, filename)
            file.save(file_path)

            user_id = app.face.recognize(filename)
            get_users_data(user_id)
            #result = app.db.select('SELECT * from users WHERE id=?',[user_id])
            #print (result)
            if user_id:
                user = get_user_by_id(user_id)
                print(user)
                print(type(user))
                message = {"message": "yach nav".format(user["name"]),
                           "user": user}

                #print (user)
                #message = {"message": "Hey we found {0} matched with your face image",
                #           "user": user}
                #view(user_id)
                return success_handle(json.dumps(message))
            else:

                return error_handle("Sorry we can not found any people matched with your face image, try another image")

@app.route('/logout')
def logout():
    return render_template('home.html')


@app.route('/home')
def home():
    return render_template('home.html')

# admin window
#@app.route('/admin_home')
#def admin_home():
#    return render_template('admin_home.html')
@app.route('/admin_user2det')
def admin_user2det():
    return render_template('admin_user2det.html')
@app.route('/admin_user3det')
def admin_user3det():
    return render_template('admin_user3det.html')

@app.route('/notification')
def notification():
   return render_template('notification.html')

# police user window
@app.route('/police_add')
def police_add():
    return render_template('police_add.html')
@app.route('/police_delete')
def police_delete():
    return render_template('police_delete.html')
@app.route('/police_update')
def police_update():
    return render_template('police_update.html')

# company user window
@app.route('/company_home', methods=['GET','POST'])
def company_home():
    return render_template('company_home.html')

# registration details
@app.route('/reg2')
def reg2():
    return render_template('reg2.html')
@app.route('/reg1')
def reg1():
    return render_template('reg1.html')

#police delete
@app.route('/pro', methods=['POST','GET'])
def pro():
    if request.method == 'POST':
        id = request.form['id']
        print (id)
        con = sqlite3.connect("database.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        print ("conn")
        cur.execute("SELECT * from users WHERE id=?", [id])
        print ("query")
        results = cur.fetchall()
        return render_template('police_delete.html', rows=results)
    else:
        print("error")
        return render_template('police_home.html')

@app.route('/delete/<id>')
def base1(id):
    print(id)
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("DELETE from users WHERE id=?", [id])
    con.commit()
    return police_home()

#update police
@app.route('/pro1', methods=['POST','GET'])
def pro1():
    if request.method == 'POST':
        id = request.form['id']
        con = sqlite3.connect("database.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * from users WHERE id=?", [id])
        results = cur.fetchall()
        return render_template('police_update.html', rows=results)
    else:
        print("error")
        return render_template('police_home.html')

@app.route('/update1/<id>')
def update1(id):
    print(id)
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * from users WHERE id=?", [id])
    results = cur.fetchall()
    con.commit()
    print("done")
    return render_template('update.html', rows=results)

#update form
@app.route('/upd', methods=['POST','GET'])
def upd():
    print ("...")
    if request.method == 'POST':
        print ("a")
        con = sqlite3.connect("database.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        id = request.form['id']
        print (id)
        name = request.form['name']
        dob = request.form['dob']
        print (name)
        gender = request.form['gender']
        contact = request.form['contact']
        address = request.form['address']
        aadhar = request.form['aadhar']
        crime = request.form['crime']
        act = request.form['act']
        print ("b")
        cur.execute("UPDATE users set name=?, dob=?  WHERE id=?", [name, dob, id])
        print ("k")
        con.commit()
        return police_home()
    else:
        return police_home()


#accept reject logic for company user
@app.route('/accept/<head_user_id>', methods=['POST','GET'])
def accept(head_user_id):
    print (head_user_id)
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("UPDATE company_reg set status='true' where head_user_id=?", [head_user_id])
    print ("up")
    #con.commit()
    #cur = con.cursor()
    cur.execute("SELECT * from company_reg where head_user_id=?", [head_user_id])
    results = cur.fetchall()
    print ("one")
    for row in results:
        password = row[12]
        type = row[15]
    #con.commit()
    print (type)
    print (password)
    #cur = con.cursor()
    cur.execute("INSERT INTO login (username,password,type) values(?,?,?)", [head_user_id, password, type])
    con.commit()
    return admin_home()


@app.route('/reject/<head_user_id>', methods=['POST', 'GET'])
def reject(head_user_id):
    print(head_user_id)
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("DELETE from company_reg WHERE head_user_id=?", [head_user_id])
    print ("delete succ")
    con.commit()
    return admin_home()


#accept reject logic for police user
@app.route('/acc/<head_user_id1>', methods=['POST', 'GET'])
def paccept(head_user_id1):
    print (head_user_id1)
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("UPDATE police_reg set status='true' where head_user_id1=?", [head_user_id1])
    print ("up")
    #con.commit()
    #cur = con.cursor()
    cur.execute("SELECT * from police_reg where head_user_id1=?", [head_user_id1])
    results = cur.fetchall()
    print ("one")
    for row in results:
        password = row[12]
        type = row[14]
    #con.commit()
    print (type)
    print (password)
    #cur = con.cursor()
    cur.execute("INSERT INTO login (username,password,type) values(?,?,?)", [head_user_id1, password, type])
    con.commit()
    return admin_home()

@app.route('/rej/<head_user_id1>', methods=['POST', 'GET'])
def pr(head_user_id1):
    print(head_user_id1)
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("DELETE from police_reg WHERE head_user_id1=?", [head_user_id1])
    print ("delete succ")
    con.commit()
    return admin_home()


#company home criminal profile
@ app.route('/crimesearch', methods=['POST', 'GET'])
def crimesearch():
        if request.method == 'POST':
            name = request.form['name']
            print (name)
            con = sqlite3.connect("database.db")
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            print ("conn")
            cur.execute("SELECT * from users WHERE name=?", [name])
            print ("query")
            results = cur.fetchall()
            return render_template('criminal_profile.html', rows=results)
        else:
            print("error")
            return render_template('police_home.html')


#@app.route('/cripro', methods=['POST', 'GET'])
#def cripro():

# Run the app
app.run()
