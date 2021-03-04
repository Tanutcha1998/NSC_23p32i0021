from flask import Flask, render_template, request, redirect, url_for
import requests
import json
import pandas as pd
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def showdata():
        DataFrame = pd.read_csv('Data.csv')
        rows = []
        for i in range(len(DataFrame)-1,-1,-1) :
                x = (i,DataFrame.at[i,'name'],DataFrame.at[i,'message'],DataFrame.at[i,'tag'],DataFrame.at[i,'time'])
                rows.append(x)
        rows = tuple(rows)
        return render_template('index.html', datas=rows)

@app.route('/question')
def showform():
        return render_template('addquestion.html')

@app.route('/delete/<string:id_data>',methods=['GET'])
def delete(id_data):
        id_data = int(id_data)
        DataFrame = pd.read_csv('Data.csv')
        DataFrame = DataFrame.drop(id_data).reset_index(drop=True)
        DataFrame.to_csv('Data.csv', index=False)
        return redirect(url_for('showdata'))

@app.route('/insert', methods=['POST'])
def insert():
    if request.method=="POST" :
        DataFrame = pd.read_csv('Data.csv')
        name = request.form['name']
        message = request.form['question']
        Tag = requests.post("http://45d293c7e1e5.ngrok.io/predict", data={'text': message})
        Tag = Tag.json()
        Tag = Tag['result']
        dict_tag = {'Violation':'กฎหมายการละเมิด(Personal Rights)', 'family':'กฎหมายครอบครัว(Family)', 'labor':'กฎหมายแรงงาน(Labor)', 'contract':'กฎหมายเอกเทศสัญญา(Contract)', 'criminal':'กฎหมายอาญา(Criminal)'}
        Tag = dict_tag[Tag]
        time = datetime.now()
        time = time.strftime("%d/%m/%Y %H:%M:%S")
        print(Tag)
        print(time)
        add = pd.DataFrame([[name,message,Tag,time]],columns=['name','message','tag','time'])
        DataFrame = DataFrame.append(add).reset_index(drop=True)
        DataFrame.to_csv('Data.csv', index=False)
        return redirect(url_for('showdata'))

@app.route('/update', methods=['POST'])
def update():
    if request.method=="POST" :
        id_update = int(request.form['id'])
        name = request.form['name']
        message = request.form['question']
        time = datetime.now()
        time = time.strftime("%d/%m/%Y %H:%M:%S")
        DataFrame = pd.read_csv('Data.csv')
        DataFrame.loc[id_update,'name'] = name
        DataFrame.loc[id_update,'message'] = message
        DataFrame.loc[id_update,'time'] = time
        DataFrame.sort_values(by=['time'], inplace=True, ascending=True)
        DataFrame = DataFrame.reset_index(drop=True)
        DataFrame.to_csv('Data.csv', index=False)
        return redirect(url_for('showdata'))

@app.route('/กฎหมายการละเมิด(Personal Rights)')
def tag1():
        DataFrame = pd.read_csv('Data.csv')
        DataFrame = DataFrame[DataFrame['tag'] == 'กฎหมายการละเมิด(Personal Rights)'].reset_index(drop=True)
        rows = []
        for i in range(len(DataFrame)-1,-1,-1) :
                x = (i,DataFrame.at[i,'name'],DataFrame.at[i,'message'],DataFrame.at[i,'tag'],DataFrame.at[i,'time'])
                rows.append(x)
        rows = tuple(rows)
        return render_template('select.html', datas=rows)

@app.route('/กฎหมายครอบครัว(Family)')
def tag2():
        DataFrame = pd.read_csv('Data.csv')
        DataFrame = DataFrame[DataFrame['tag'] == 'กฎหมายครอบครัว(Family)'].reset_index(drop=True)
        rows = []
        for i in range(len(DataFrame)-1,-1,-1) :
                x = (i,DataFrame.at[i,'name'],DataFrame.at[i,'message'],DataFrame.at[i,'tag'],DataFrame.at[i,'time'])
                rows.append(x)
        rows = tuple(rows)
        return render_template('select.html', datas=rows)

@app.route('/กฎหมายแรงงาน(Labor)')
def tag3():
        DataFrame = pd.read_csv('Data.csv')
        DataFrame = DataFrame[DataFrame['tag'] == 'กฎหมายแรงงาน(Labor)'].reset_index(drop=True)
        rows = []
        for i in range(len(DataFrame)-1,-1,-1) :
                x = (i,DataFrame.at[i,'name'],DataFrame.at[i,'message'],DataFrame.at[i,'tag'],DataFrame.at[i,'time'])
                rows.append(x)
        rows = tuple(rows)
        return render_template('select.html', datas=rows)

@app.route('/กฎหมายเอกเทศสัญญา(Contract)')
def tag4():
        DataFrame = pd.read_csv('Data.csv')
        DataFrame = DataFrame[DataFrame['tag'] == 'กฎหมายเอกเทศสัญญา(Contract)'].reset_index(drop=True)
        rows = []
        for i in range(len(DataFrame)-1,-1,-1) :
                x = (i,DataFrame.at[i,'name'],DataFrame.at[i,'message'],DataFrame.at[i,'tag'],DataFrame.at[i,'time'])
                rows.append(x)
        rows = tuple(rows)
        return render_template('select.html', datas=rows)

@app.route('/กฎหมายอาญา(Criminal)')
def tag5():
        DataFrame = pd.read_csv('Data.csv')
        DataFrame = DataFrame[DataFrame['tag'] == 'กฎหมายอาญา(Criminal)'].reset_index(drop=True)
        rows = []
        for i in range(len(DataFrame)-1,-1,-1) :
                x = (i,DataFrame.at[i,'name'],DataFrame.at[i,'message'],DataFrame.at[i,'tag'],DataFrame.at[i,'time'])
                rows.append(x)
        rows = tuple(rows)
        return render_template('select.html', datas=rows)

if __name__ == "__main__":
    app.run(debug=True)