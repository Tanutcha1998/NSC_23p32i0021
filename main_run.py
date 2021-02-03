from flask import Flask, render_template, request, redirect, url_for
import requests
import pymysql
import random
import json

app = Flask(__name__)
conn = pymysql.connect('localhost','root','1234','post')

@app.route('/')
def showdata():
        cur = conn.cursor()
        cur.execute("SELECT * FROM `message` ORDER BY id desc ")
        rows = cur.fetchall()
        return render_template('index.html', datas=rows)

@app.route('/question')
def showform():
        return render_template('addquestion.html')

@app.route('/delete/<string:id_data>',methods=['GET'])
def delete(id_data):
        cur = conn.cursor()
        cur.execute("delete from message where id=%s",(id_data))
        conn.commit()
        return redirect(url_for('showdata'))

@app.route('/insert', methods=['POST'])
def insert():
    if request.method=="POST" :
        name = request.form['name']
        message = request.form['question']
        Tag = requests.post("http://50c92d9a5b44.ngrok.io/predict", data={'text': message})
        Tag = Tag.json()
        Tag = Tag['result']
        dict_tag = {'Violation':'กฎหมายการละเมิด(Violation)', 'family':'กฎหมายครอบครัว(Family)', 'labor':'กฎหมายแรงงาน(Labor)', 'contract':'กฎหมายเอกเทศสัญญา(Contract)', 'criminal':'กฎหมายอาญา(Criminal)'}
        Tag = dict_tag[Tag]
        print(Tag)
        with conn.cursor() as cursor :
            sql = "Insert into `message` (`name`,`message`,`Tag`) values(%s,%s,%s)"
            cursor.execute(sql,(name,message,Tag))
            conn.commit()
        return redirect(url_for('showdata'))

@app.route('/update', methods=['POST'])
def update():
    if request.method=="POST" :
        id_update = request.form['id']
        name = request.form['name']
        message = request.form['question']
        with conn.cursor() as cursor :
            sql = "update message set name=%s, message=%s where message.id=%s"
            cursor.execute(sql,(name,message,id_update))
            conn.commit()
        return redirect(url_for('showdata'))

@app.route('/กฎหมายการละเมิด(Violation)')
def tag1():
        cur = conn.cursor()
        sql = "SELECT * FROM `message` WHERE `tag`='กฎหมายการละเมิด(Violation)' ORDER BY `id` DESC"
        sql = sql.encode('utf-8')
        cur.execute(sql)
        rows = cur.fetchall()
        return render_template('select.html', datas=rows)

@app.route('/กฎหมายครอบครัว(Family)')
def tag2():
        cur = conn.cursor()
        sql = "SELECT * FROM `message` WHERE `tag`='กฎหมายครอบครัว(Family)' ORDER BY `id` DESC"
        sql = sql.encode('utf-8')
        cur.execute(sql)
        rows = cur.fetchall()
        return render_template('select.html', datas=rows)

@app.route('/กฎหมายแรงงาน(Labor)')
def tag3():
        cur = conn.cursor()
        sql = "SELECT * FROM `message` WHERE `tag`='กฎหมายแรงงาน(Labor)' ORDER BY `id` DESC"
        sql = sql.encode('utf-8')
        cur.execute(sql)
        rows = cur.fetchall()
        return render_template('select.html', datas=rows)

@app.route('/กฎหมายเอกเทศสัญญา(Contract)')
def tag4():
        cur = conn.cursor()
        sql = "SELECT * FROM `message` WHERE `tag`='กฎหมายเอกเทศสัญญา(Contract)' ORDER BY `id` DESC"
        sql = sql.encode('utf-8')
        cur.execute(sql)
        rows = cur.fetchall()
        return render_template('select.html', datas=rows)

@app.route('/กฎหมายอาญา(Criminal)')
def tag5():
        cur = conn.cursor()
        sql = "SELECT * FROM `message` WHERE `tag`='กฎหมายอาญา(Criminal)' ORDER BY `id` DESC"
        sql = sql.encode('utf-8')
        cur.execute(sql)
        rows = cur.fetchall()
        return render_template('select.html', datas=rows)

conn.close

if __name__ == "__main__":
    app.run(debug=True)