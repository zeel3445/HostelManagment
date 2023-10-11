from flask import Flask, request, render_template
import mysql.connector
app = Flask(__name__)
db=mysql.connector.connect(host='localhost',user='root',passwd='',database='slogin')

@app.route('/') 
def someName():
    cur=db.cursor()
    #sql = "SELECT * FROM slogin"
    cur.execute("select * from login_detail")
   # cur.close()
    #db.commit()
    ans = cur.fetchall()
    return render_template('result.html',result=ans)
    
if __name__=='__main__':
    app.run()

