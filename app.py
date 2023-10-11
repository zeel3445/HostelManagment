from email import message
from flask import Flask
from flask import render_template,request,flash
import mysql.connector
app = Flask(__name__)
db=mysql.connector.connect(host='localhost',user='root',passwd='',database='hostel_management')

#used to insert value in relations of database

@app.route("/akshay")
def insert():
    for i in range(6,25):
        if(i<10):
            usn=f"1bm20is00{i}"
        else:
            usn=f"1bm20is0{i}"
        cur=db.cursor()
        cur.execute(f"insert into slogin values('{usn}','bmsce123',0)")
    db.commit()
    return "sucess"
@app.route("/room")
def room():
    cur=db.cursor()
    for i in range(1,6):
        cur.execute(f"insert into room(room_id,occupancy,hostel_id)values('%s','%s','%s')"%(f'GH2{i}','vacat','GH2'))
    db.commit()
    return "success"
    

#backend routing begins

@app.route("/")
def home():
    return render_template('main_hostel_login.html')

@app.route("/about")
def about():
    return render_template('about.html')
@app.route("/student_login")
def slogin():
    return render_template('student_login.html')
@app.route("/admin_page")
def alogin():
    return render_template('admin_page.html')
@app.route("/admin_front")
def admin_front():
    return render_template('admin_front.html')
@app.route("/result", methods=['GET', 'POST'])
def results():
    if 1:
       # getting input with name = fname in HTML form
        user = request.form.get('stud')
       # getting input with name = lname in HTML form
        pas = request.form.get('pass')
        cur=db.cursor()
        cur.execute("select user from slogin")
   # cur.close()
    #db.commit()
        ans = cur.fetchall()
        for i in ans:
            c=0
            if(i[0]==user):
                sql=f"select status from slogin where user='{user}'"
                cur.execute(sql)
                ans=cur.fetchall()
                if(ans[0][0]==0):
                    return render_template('Student_Form.html')
                else:
                    return  render_template('student_front.html',result="you have already filled please wait for approval")
        
        mess="Invalid Credential"
        return render_template("student_login.html",mess=mess)
                
    #return render_template("form.html")
@app.route("/student_form", methods=['GET', 'POST'])
def student_form():
    name=request.form.get('name')
    usn=request.form.get('usn')
    fathername=request.form.get('fname')
    mothername=request.form.get('Mname')
    email=request.form.get('email')
    aadhar=request.form.get('aadhaar')
    gender=request.form.get('Gender')
    year=request.form.get('Year')
    dob=request.form.get('DOB')
    phone=request.form.get('ph1')
    gphone=request.form.get('ph2')
    nationality=request.form.get('nationality')
    country=request.form.get('Country')
    city=request.form.get('City')
    pincode=request.form.get('pin')

    cur=db.cursor()
    sql=f"insert into student(name,usn,DOB,nationality,email,gender,phone_num,fathers_name,mothers_name,aadhaar_num,guardian_no,city,pincode,country) VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(name,usn,dob,nationality,email,gender,phone,fathername,mothername,aadhar,gphone,city,pincode,country)
    cur.execute(sql)
    cur.execute(f"update slogin set status=1 where user='{usn}'")
    db.commit()
    return render_template('student_front.html',result="you have filled please wait for approval")

    
    #return '{name}','{usn}','{dob}','{nationality}','{email}','{gender}','{phone}','{fathername}','{mothername}','{aadhar}','{gphone}','{city}',{pincode},'{country}'
@app.route("/pending_app")
def pending_app():
    cur=db.cursor()
    cur.execute("select name,email,usn,gender from student where hostel_id is NULL")
    ans=cur.fetchall()
    print(ans)
    return render_template('result.html',result=ans)
    
@app.route("/allotment", methods=['GET', 'POST'])
def allotment():
    l=[]
    cur=db.cursor()
    cur.execute("select name,email,usn,gender from student where hostel_id is NULL")
    ans=cur.fetchall()
    for i in ans:
        print(f'{i[2]}')
        hostel=request.form.get(f'{i[2]}')
        cur.execute(f"update student set hostel_id='{hostel}' where usn='{i[2]}'")
        if(i[3]=='male'):
            cur.execute(f"update student set mess_id='Bmess' where usn='{i[2]}'")
        else:
            cur.execute(f"update student set mess_id='Gmess' where usn='{i[2]}'")
    db.commit()
    return render_template('admin_front.html')

@app.route("/hostel_data")
def hostel_data():
    cur=db.cursor()
    cur.execute("select * from queries")
    queries=cur.fetchall()
    return render_template('query.html',queries=queries)
@app.route("/query1", methods=['GET', 'POST'])
def query1():
    student=request.form.getlist('student')
    mess=request.form.getlist('Mess')
    room=request.form.getlist('Room')
    hostel=request.form.getlist('hostel')
    warden=request.form.getlist('Warden')
    cur=db.cursor()
    
    cur.execute("select * from queries")
    queries=cur.fetchall()

    student_str=",".join(student)
    mess_str=",".join(mess)
    room_str=",".join(room)
    hostel_str=",".join(hostel)
    warden_str=",".join(warden)
    if(len(student)==0 and len(mess)==0 and len(room)==0 and len(hostel)==0 and len(warden)!=0):
        cur.execute(f"select {warden_str} from warden")
        ans=cur.fetchall()
    elif(len(student)==0 and len(mess)==0 and len(room)==0 and len(hostel)!=0 and len(warden)==0):
        cur.execute(f"select {hostel_str} from hostel")
        ans=cur.fetchall()
    elif(len(student)==0 and len(mess)==0 and len(room)!=0 and len(hostel)==0 and len(warden)==0):
        cur.execute(f"select {room_str} from room")
        ans=cur.fetchall()
    elif(len(student)==0 and len(mess)!=0 and len(room)==0 and len(hostel)==0 and len(warden)==0):
        cur.execute(f"select {mess_str} from mess")
        ans=cur.fetchall()
    elif(len(student)!=0 and len(mess)==0 and len(room)==0 and len(hostel)==0 and len(warden)==0):
        cur.execute(f"select {student_str} from student")
        ans=cur.fetchall()
    elif(len(student)==0 and len(mess)==0 and len(room)==0 and len(hostel)!=0 and len(warden)!=0):
        cur.execute(f"select {hostel_str},{warden_str} from hostel,student where warden.warden_id=hostel.warden_id")
        ans=cur.fetchall()
    elif(len(student)==0 and len(mess)==0 and len(room)!=0 and len(hostel)!=0 and len(warden)==0):
        cur.execute(f"select {hostel_str},{room_str} from hostel,room where hostel.hostel_id=room.hostel_id")
        ans=cur.fetchall()
    else:
        flist=[student_str,mess_str,room_str,hostel_str,warden_str]
        final_str=""
        for j in flist:
            if(j==""):
                continue
            else:
                final_str=final_str+j+","
        final_str=final_str[:len(final_str)-1]
    
        sql=f"select distinct {final_str} from student,hostel,mess,warden,room where student.hostel_id=hostel.hostel_id and student.mess_id=mess.mess_id and student.room_id=room.room_id and hostel.warden_id=warden.warden_id "
        print(sql)
        cur=db.cursor()
        cur.execute(sql)
        ans=cur.fetchall()
    return render_template('query.html',result=ans,queries=queries)
    # for i in range(len(student)):
    #     if(i==len(student)-1):
    #         sql=sql+student[i]
    #     else:
    #         sql=sql+student[i]+','
    # sql=sql+" from student"
    # cur=db.cursor()
    # cur.execute(sql)
    # ans=cur.fetchall()
@app.route("/query2", methods=['GET', 'POST'])
def query2():
    query_id=request.form.get('sql')
    sql=f"select query from queries where query_id={query_id}"
    print(sql)
    cur=db.cursor()
    cur.execute(sql)
    ans=cur.fetchall()
    print(ans[0][0])
    cur=db.cursor()
    cur.execute(ans[0][0])
    a=cur.fetchall()
    cur.execute("select * from queries")
    queries=cur.fetchall()
    return render_template('query.html',result=a,queries=queries)



@app.route("/query3", methods=['GET', 'POST'])
def query3():
    sql=request.form.get('sql')
    remark=request.form.get('remark')
    cur=db.cursor()
    cur.execute(f"insert into queries(remark,query) values('%s','%s')"%(remark,sql))
    db.commit()
    cur.execute(sql)
    ans=cur.fetchall()
    
    cur.execute("select * from queries")
    queries=cur.fetchall()
    print(sql,remark)
    return render_template('query.html',result=ans,queries=queries)  
