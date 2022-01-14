from flask import Flask, render_template, request,redirect,url_for
import mysql.connector
mydb = mysql.connector.connect(user='root', password='root123', host='127.0.0.1', database='ranidb')
import pyshorteners
import datetime
import socket

longurl=[]
shorturl=[]
app = Flask(__name__)
@app.route('/')
def enterurl():
    return render_template('index.html')

@app.route('/result', methods=['POST', 'GET'])
def result_app():
    if request.method == 'POST':
        a = request.form
        longurl = a['name']
        b=longurl
        s = pyshorteners.Shortener()
        result = s.tinyurl.short(longurl)
        ts = datetime.datetime.now()
        date_time = ts.strftime("%m/%d/%Y, %H:%M:%S")
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        mycursor = mydb.cursor()
        #mycursor.execute("CREATE TABLE Url_entry(id int NOT NULL AUTO_INCREMENT, longurl VARCHAR(255),shorturl VARCHAR(255),timestamp VARCHAR(255),ip_address VARCHAR(255),PRIMARY KEY (id))")
        mycursor.execute("INSERT INTO Url_entry(longurl,shorturl,timestamp,ip_address)values(%s,%s,%s,%s)",(b,result,date_time,IPAddr))
        mydb.commit()
        mycursor.execute("SELECT id,timestamp,ip_address,shorturl,longurl,count(longurl) as count FROM Url_entry GROUP BY longurl")
        count=mycursor.fetchall()

    return render_template('result.html',output=count)


if __name__ == '__main__':
    app.run(debug=True)
