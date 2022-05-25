import pickle
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import keras
from flask import Flask, render_template, request, session,jsonify
from keras.engine.saving import model_from_json

from DBConnection import Db
from hj import generate_summary
app = Flask(__name__)
app.secret_key='hiiii'


import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

from flask_mail import Mail, Message
app.config['MAIL_SERVER']= "smtp.gmail.com"
app.config['MAIL_PORT'] ='465'
app.config['MAIL_USERNAME'] = 'feedbacksystemusingrnn@gmail.com'
app.config['MAIL_PASSWORD'] = 'feedbacksystem@kmctcew'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail =  Mail(app)


@app.route('/')
def home():
    return render_template("login_index.html")

@app.route('/admin_home')
def admin_home():
    return render_template("admin/admin index.html")


# @app.route('/common')
# def common():
#     return render_template("common index.html")

# Sign Up

@app.route('/sign_up')
def sign_up():
    return render_template('common index.html')


# forget password

@app.route('/forget_password')
def forget_password():
    return render_template('reset password.html')


@app.route('/forget_post', methods=["post"])
def forget_post():
    email = request.form["textfield10"]
    db6 = Db()
    fgh = "SELECT * FROM login WHERE username='" + email + "'"
    res = db6.selectOne(fgh)
    x = res["psw"]

    if res is not None:
        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        s.login("feedbacksystemusingrnn@gmail.com", "feedbacksystem@kmctcew")
        msg = MIMEMultipart()  # create a message.........."
        message = "Messege from Feedback System"
        msg['From'] = "feedbacksystemusingrnn@gmail.com"
        msg['To'] = email
        msg['Subject'] = "Your Password for Feedback System"
        body = "Your Account has been verified by our team. You Can login using your password - " + str(x)
        msg.attach(MIMEText(body, 'plain'))
        s.send_message(msg)
        return '''<script>alert("send");window.location='/Login'</script>'''
    else:
        return '''<script>alert("Invalid");window.location='/forget_password'</script>'''
# Login page

@app.route('/Login')
def Login():
    return render_template('login_index.html')

@app.route('/Login_post',methods=["post"])
def Login_post():
    email= request.form["name"]
    psw= request.form["psw"]
    db=Db()

    qry="select * from login where username='"+email+"' and psw='"+psw+"'"
    res=db.selectOne(qry)
    if res!=None:
        session['lid']=res['lid']
        type=res['typ']

        if type=='admin':
            return '''<script>alert('success');window.location='/admin_home'</script>'''
        elif type=='teacher':
            qry = "SELECT `teacher`.regno,teacher.fname,teacher.lname,teacher.email,department.dname FROM `teacher` INNER JOIN `department` WHERE `teacher`.dept=department.did AND lid='"+str(res['lid'])+ "'"
            db = Db()
            rest = db.selectOne(qry)
            if rest is not None:
                session['name'] = rest["fname"] + " " + rest["lname"]
                session['regno'] = rest["regno"]
                session['email'] = rest["email"]
                session['dname'] = rest["dname"]

                return '''<script>alert('success');window.location='/Teacher_home'</script>'''
            else:
                 return '''<script>alert('invalid');window.location='/Login'</script>'''

        elif type=='student':
            qry="SELECT student.regno,student.fname,student.lname,student.email,student.sem, department.dname FROM `student` INNER JOIN `department` WHERE student.dept=department.did AND lid='"+str(res['lid'])+"'"
            db=Db()
            re=db.selectOne(qry)
            if res is not None:
                session['name']=re["fname"]+" "+re["lname"]
                session['regno']=re["regno"]
                session['email'] = re["email"]
                session['dname'] = re["dname"]
                session['sem'] = re["sem"]

                return '''<script>alert('success');window.location='/student_home'</script>'''
            else:
                return '''<script>alert('invalid');window.location='/Login'</script>'''
        else:
            return '''<script>alert('invalid');window.location='/Login'</script>'''
    else:
        return '''<script>alert('invalid');window.location='/Login'</script>'''

# admin home
@app.route('/Admin_home')
def Admin_home():
    return render_template('admin/Home.html')

# teacher home

@app.route('/Teacher_home')
def Teacher_home():
    db = Db()
    qry2 = "SELECT `teacher`.*,`department`.* FROM `teacher`" \
           " INNER JOIN `department` ON `teacher`.`dept`=`department`.`did` AND lid='" + str(session['lid']) + "'"
    rest = db.selectOne(qry2)

    qry3="SELECT `subject`.sem,`subject`.* FROM `subject`,`teacher`,`department`,`assign` WHERE" \
         "`assign`.`tid`=`teacher`.`lid` AND " \
         "`assign`.`subid`=`subject`.`subid` AND " \
         "`department`.`did`=`subject`.`dept` AND " \
         "`teacher`.lid='"+str(session['lid'])+"'"
    res=db.select(qry3)
    return render_template('teacher/teacher home.html',data=rest,data1=res)

# student home
@app.route('/student_home')
def student_home():
    db = Db()
    qry2 = "SELECT `student`.*,`department`.* FROM `student` INNER JOIN `department` ON `student`.`dept`=`department`.`did` where student.lid='" +str(session['lid'])+ "'"
    rest = db.selectOne(qry2)

    qry3="SELECT `teacher`.*,`subject`.* FROM `subject`,`teacher`,`department`,`student`,`assign` WHERE`assign`.`tid`=`teacher`.`lid` AND `assign`.`subid`=`subject`.`subid` AND `student`.`dept`=`department`.`did` AND `department`.`did`=`subject`.`dept` AND `student`.`sem`=`subject`.`sem` AND `student`.`dept`=`department`.`did` AND `student`.`lid`= '"+str(session['lid'])+"'"
    res=db.select(qry3)
    return render_template('student/student home.html',data=rest,data1=res)

#stud profile

@app.route('/stud_pofile')
def stud_pofile():
    return render_template("student/stud profile.html")

# edit profile

@app.route('/edit_stud_pofile')
def edit_stud_pofile():
    d = Db()
    qry3 = "SELECT * FROM `department`"
    res = d.select(qry3)
    qry = "SELECT * FROM `student` WHERE lid='"+str(session['lid'])+"'"
    res1 = d.selectOne(qry)
    return render_template("student/edit stud profile.html",data=res,data1=res1)

@app.route('/edit_stud_pofile_post', methods=['post'])
def edit_stud_pofile_post():
    lid=request.form["logid"]
    fname = request.form["fname"]
    lname = request.form["lname"]
    reg = request.form["reg"]
    dept = request.form["dept"]
    sem = request.form["sem"]
    email = request.form["email"]

    db=Db()
    qry="UPDATE student SET `regno`='"+reg+"',`fname`='"+fname+"',`lname`='"+lname+"',`dept`='"+dept+"',`sem`='"+sem+"',`email`='"+email+"' WHERE lid='"+lid+"'"
    db.update(qry)
    return '''<script>alert('success');window.location='/student_home'</script>'''


# Department add, delete,edit

@app.route('/admin_add_dept')
def admin_add_dept():
    return render_template('admin/AdminDept.html')

@app.route('/admin_add_dept_post',methods=["post"])
def admin_add_dept_post():
    depname=request.form["addDept"]
    qry="INSERT INTO department(dname)VALUES('"+depname+"')"
    db=Db()
    db.insert(qry)
    return '''<script>alert('success');window.location='/admin_add_dept'</script>'''

# View department
@app.route('/Dept_view')
def Dept_view():
    db=Db()
    res=db.select("SELECT * FROM `department`")
    return render_template('admin/Dept view.html',data=res)

@app.route('/dept_view_post',methods=['post'])
def dept_view_post():
    dept_view_var=request.form["search"]
    d=Db()
    qry= "SELECT * FROM `department` WHERE dname LIKE '%"+dept_view_var+"%'"
    res=d.select(qry)
    return render_template('admin/Dept view.html',data=res)

# Edit Department
@app.route('/admin_edit_dept/<d_id>')
def admin_edit_dept(d_id):
    db=Db()
    qry="SELECT * FROM `department` WHERE did='"+str(d_id)+"'"
    res=db.selectOne(qry)
    return render_template('admin/edit dept.html',data=res)

@app.route('/admin_edit_dept_post',methods=["post"])
def admin_edit_dept_post():
    depname=request.form["editDept"]
    depid=request.form["dep_id"]
    d=Db()
    qry="UPDATE `department` SET `dname`='"+depname+"' WHERE did='"+depid+"'"
    d.update(qry)
    return '''<script>alert('success');window.location='/Dept_view'</script>'''

# Delete Department
@app.route('/delete_dept/<id>')
def delete_dept(id):
    db=Db()
    qry="DELETE FROM `department` WHERE `did`='"+str(id)+"'"
    res=db.delete(qry)
    return '''<script>alert('deleted');window.location='/Dept_view'</script>'''


# Subject add, view, delete, edit

@app.route('/add_subject')
def add_subject():
    d = Db()
    qry3 = "SELECT * FROM `department`"
    res = d.select(qry3)
    return render_template('admin/Add Subject.html', data=res)

@app.route('/add_subject_post',methods=["post"])
def add_subject_post():
    dept= request.form["dept"]
    sem = request.form["sem"]
    subname = request.form["sname"]
    subcode = request.form["scode"]
    d = Db()
    qry3="INSERT INTO `subject`(dept,sem,sname,scode)VALUES('"+dept+"','"+sem+"','"+subname+"','"+subcode+"')"
    res=d.insert(qry3)
    return '''<script>alert('success');window.location='/add_subject'</script>'''

# View Subject
@app.route('/sub_view')
def sub_view():
    db = Db()
    res = db.select("SELECT * FROM `department`")
    # res1 = db.select( "select * from subject")
    return render_template('admin/Subject view.html',data = res)

@app.route('/sub_view_post',methods=['post'])
def sub_view_post():
    view_dept = request.form["textfield3"]
    view_sem = request.form["Semester"]
    d = Db()
    qry="SELECT * FROM `subject` WHERE `dept` LIKE '"+view_dept+"' AND `sem` LIKE '"+view_sem+"'"
    res1 = d.select(qry)
    return render_template('admin/Subject view.html', data1=res1)

# Edit sub
@app.route('/admin_edit_sub/<sub_id>')
def admin_edit_sub(sub_id):
    db=Db()
    qry="SELECT * FROM `subject` WHERE subid='"+str(sub_id)+"'"
    res=db.selectOne(qry)
    return render_template('admin/edit sub.html',data=res)

@app.route('/admin_edit_sub_post',methods=["post"])
def admin_edit_sub_post():
    sname=request.form["editsub"]
    subid=request.form["sub_id"]
    d=Db()
    qry="UPDATE `subject` SET `sname`='"+sname+"' WHERE subid='"+subid+"'"
    d.update(qry)
    return '''<script>alert('success');window.location='/sub_view'</script>'''

# Delete  subject
@app.route('/delete_sub/<id>')
def delete_sub(id):
    db=Db()
    qry="DELETE FROM `subject` WHERE `subid`='"+str(id)+"'"
    res=db.delete(qry)
    return '''<script>alert('deleted');window.location='/sub_view'</script>'''


# Assign Subject to Staff


@app.route('/voicetyping')
def voicetyping():
    return render_template("student/voicetyping.html")



@app.route('/admin_assign_staff')
def admin_assign_staff():
    db = Db()
    res = db.select("SELECT * FROM `department`")
    return render_template('admin/assign staff to sub.html',data=res)

@app.route('/admin_assign_staff_post', methods=["post"])
def admin_assign_staff_post():
    # dep=request.form["dept"]
    db=Db()
    assign_staff = request.form["tchr"]
    assign_sub = request.form["sub"]
    qry = "INSERT INTO `assign` (subid,tid) VALUES('" + assign_sub + "','" + assign_staff + "')"
    res1 = db.insert(qry)
    return render_template('admin/assign staff to sub.html', data1=res1)

    # qry1 = "SELECT * FROM teacher WHERE dept= '" + str(dep) + "'"
    # dat = db.select(qry1)
    # qry2 = "SELECT * FROM subject WHERE dept= '" + str(dep) + "'"
    # dat2 = db.select(qry2)
    # print(qry)
    # print(dat2)
    # return jsonify(status="ok", teacher=dat, sub=dat2,data1=res1)

@app.route('/dep_wise_staff_post', methods=["post"])
def dep_wise_staff_post():

    dep=request.form['textfield3']
    db = Db()

    qry1 = "SELECT * FROM teacher WHERE dept= '" + str(dep) + "'"
    dat = db.select(qry1)
    qry2 = "SELECT * FROM subject WHERE dept= '" + str(dep) + "'"
    dat2 = db.select(qry2)

    print(qry1)
    print(dat2)
    return jsonify(status="ok", teacher=dat, sub=dat2)


# view allocated staff
@app.route('/view_allocated_staff')
def view_allocated_staff():
    db = Db()
    res = db.select("SELECT * FROM `department`")
    return render_template('admin/view allocated staff.html', data=res)


@app.route('/view_allocated_staff_post',methods=['post'])
def view_allocated_staff_post():
    dept_id=request.form["textfield3"]

    db=Db()
    qry="SELECT teacher.regno , teacher.fname , teacher.lname ,teacher.lid, subject.sname ,assign.aid FROM `teacher` ,`subject` , `assign`,`department` WHERE" \
        "`assign`.`tid`=`teacher`.`lid`AND " \
        "`assign`.`subid`=`subject`.`subid` AND " \
        "`department`.`did`=`subject`.`dept` AND " \
        "`teacher`.`dept`='"+str(dept_id)+"' "

    res1 = db.select(qry)

    res = db.select("SELECT * FROM `department`")
    return render_template('admin/view allocated staff.html',data1=res1, data=res)

# delete assigned staff

@app.route('/delete_staff/<id>')
def delete_staff(id):

    db=Db()
    qry="DELETE FROM `assign` WHERE `aid`='"+str(id)+"'"
    res=db.delete(qry)
    return '''<script>alert('deleted');window.location='/view_allocated_staff'</script>'''

#  edit assigned staff

# @app.route('/edit_assign/<id>')
# def edit_assign(id):
#     db=Db()
#     qry="SELECT * FROM assign WHERE subid='"+str(id)+"'"
#     res=db.selectOne(qry)
#     return render_template('admin/edit sub.html',data=res)
#
# @app.route('/admin_edit_sub_post',methods=["post"])
# def admin_edit_sub_post():
#     sname=request.form["editsub"]
#     subid=request.form["sub_id"]
#     d=Db()
#     qry="UPDATE `subject` SET `sname`='"+sname+"' WHERE subid='"+subid+"'"
#     d.update(qry)
#     return '''<script>alert('success');window.location='/sub_view'</script>'''
# Dsepartment wise staff

@app.route('/admin_dep_wise_staff')
def admin_dep_wise_staff():
    db=Db()
    res = db.select("SELECT * FROM `department`")
    return render_template('admin/dep wise staff.html',data=res)

@app.route('/admin_dep_wise_staff_post', methods=["post"])
def admin_dep_wise_staff_post():
    dep = request.form['textfield3']
    db = Db()
    qry = "SELECT * FROM teacher WHERE dept= '" +str(dep)+ "'"
    dat = db.select(qry)
    res = db.select("SELECT * FROM `department`")
    return render_template('admin/dep wise staff.html', data1=dat,data=res)




# Teacher register

@app.route('/Teacher_Register')
def Teacher_Register():
    d = Db()

    qry = "SELECT * FROM `department`"
    res = d.select(qry)
    return render_template('teacher registration.html',data=res)

@app.route('/Teacher_Register_post',methods=["post"])
def Teacher_Register_post():
    teacher_fname=request.form["textfield1"]
    teacher_lname = request.form["textfield2"]
    teacher_dep = request.form["textfield3"]
    teacher_email = request.form["textfield4"]
    teacher_psw= request.form["textfield5"]
    teacher_reg = request.form["textfield6"]
    d = Db()
    q= "INSERT INTO login(username,psw,typ)VALUES('"+teacher_email+"','"+teacher_psw+"','teacher')"
    lid=d.insert(q)
    qry1 = "INSERT INTO teacher(regno,fname,lname,dept,email,psw,lid)VALUES('"+teacher_reg+"','"+teacher_fname+"','"+teacher_lname+"','"+teacher_dep+"','"+teacher_email+"','"+teacher_psw+ "','"+str(lid)+ "')"

    res=d.insert(qry1)
    return '''<script>alert('success');window.location='/Login'</script>'''


# Student register

@app.route('/Student_Register')
def Student_Register():
    d = Db()
    qry2 = "SELECT * FROM `department`"
    rest = d.select(qry2)
    return render_template('student registration.html',data=rest)

@app.route('/Student_Register_post',methods=["post"])
def Student_Register_post():
    student_reg=request.form["sreg"]
    student_fname= request.form["sfname"]
    student_lname= request.form["slname"]
    student_dep= request.form["sdep"]
    student_sem= request.form["ssem"]
    student_email= request.form["semail"]
    student_psw= request.form["spsw"]

    d = Db()
    p= "INSERT INTO login(username,psw,typ)VALUES('"+student_email+"','"+student_psw+"','student')"
    lid=d.insert(p)
    qry2 = "INSERT INTO student(regno,fname,lname,dept,sem,email,lid)VALUES('"+student_reg+"','"+student_fname+"','"+student_lname+"','"+student_dep+"','"+student_sem+"','"+student_email+"','"+str(lid)+ "')"
    rest=d.insert(qry2)

    # session['dept'] = rest['dept']
    # session['sem'] = rest['sem']
    return '''<script>alert('success');window.location='/Login'</script>'''

@app.route('/upload_feedback/<id>/<sub>')
def upload_feedback(id,sub):
    db=Db()
    qry="SELECT * FROM `teacher` WHERE `lid`='"+str(id)+"'"
    qry2= "SELECT * FROM subject WHERE subid= '"+str(sub)+"'"
    res=db.selectOne(qry)
    res2=db.selectOne(qry2)
    return render_template('student/feedback.html',data=res,data2=res2)

@app.route('/upload_feedback_post',methods=["post"])
def upload_feedback_post():
    teacher_id=request.form['teacher_id']
    subject=request.form['subid']
    stud_feedback = request.form['feedback']

    print("feedback from student",stud_feedback)

    from EmotionChecking import emotions
    em = emotions()
    resemotion=em.pred(stud_feedback)

    ####lstmbased
    keras.backend.clear_session()
    msg=stud_feedback

    path1="D:\\feedbacksm\\feedbacksystem\\feedbacksystem\\model.h5"
    path2="D:\\feedbacksm\\feedbacksystem\\feedbacksystem\\model.json"
    path3="D:\\feedbacksm\\feedbacksystem\\feedbacksystem\\tokenizer.pickle"

    with open(path3,"rb") as h:
        tokenizer=pickle.load(h)

    jhandle=open(path2,'r')

    jsoncontent=jhandle.read()
    print(jsoncontent)
    jhandle.close()

    loadedmodel=model_from_json(jsoncontent)
    loadedmodel.load_weights(path1)
    lst=[msg]
    from keras.preprocessing.sequence import pad_sequences
    f = tokenizer.texts_to_sequences(lst)
    trainFeatures = pad_sequences(f, 100, padding='post')
    loadedmodel.compile(optimizer='Adam',loss='binary_crossentropy',metrics=['accuracy'])
    p=loadedmodel.predict(trainFeatures)
    print(round(p[0][0]),"likhil..........................")
    if round(p[0][0])==0:
        result='Neutral'

    elif round(p[0][0])==1:
        result='negative'

    else:
        result='positive'


    db = Db()
    print("helllooooooooooooooooooooooooooooooo")
    print(resemotion)
    qry="INSERT INTO `feedback_table`(studid,tid,feedback,DATE,subid,emotion) VALUES ('"+str(session['lid'])+"','"+str(teacher_id)+"','"+stud_feedback+"',curdate(),'"+str(subject)+"','"+result+"')"
    res=db.insert(qry)

    return '''<script>alert('Feedback Uploaded');window.location='/student_home'</script>'''

@app.route('/view_feedback/<sid>')
def view_feedback(sid):
    db=Db()
    qry="SELECT `feedback_table`.*, `student`.`fname`,`student`.`lname` FROM `student` INNER JOIN `feedback_table` ON `feedback_table`.`studid`=`student`.`lid` WHERE feedback_table.`subid`='"+sid+"' AND feedback_table.tid='"+str(session['lid'])+"'"
    res=db.select(qry)
    ls=[]
    from sd import extractkeywords
    for i in res:
        ss=extractkeywords(i['feedback'])
        a={ 'fname' : i["fname"], 'lname' :i["lname"],'words' : ss,'fid': i["fid"] }
        ls.append(a)
    emotion = []
    r = {}
    if len(res) > 0:
        for i in res:
            print(i["emotion"])
            emotion.append(i["emotion"])
            print(emotion)
        count_positive = emotion.count("positive")
        print("count positive=", count_positive)
        count_neutral = emotion.count("neutral")
        print("count neutral=", count_neutral)
        count_negative = emotion.count("negative")
        print("count negative=", count_negative)
        total_count = len(emotion)
        print("total count=", total_count)
        per_positive = (float(count_positive) / float(total_count)) * 100
        print("percentage positive=", per_positive)
        per_neutral = (float(count_neutral) / float(total_count)) * 100
        print("percentage neutral=", per_neutral)
        per_negative = (float(count_negative) / float(total_count)) * 100
        print("percentage negative=", per_negative)
        if len(res) > 0:
            # r['status'] = "1"
            # r['Angry'] = per_anger
            # r['Disgusted'] = per_disgus
            # r['Fearful'] = per_fear
            # r['Happy'] = per_joy
            # r['Neutral'] = per_neutral
            # r['Sad'] = per_sad
            # r['Surprised'] = per_surp
            # print(gco,hc1)
            labels = ["Positive", "Neutral", "Negative"]
            values = [per_positive, per_neutral, per_negative]

            print(labels)
            print(values)



            return render_template('teacher/viewfeedback.html',data1=ls,labels=labels,values=values)
        else:
            return "No data"


# admin view feedback
@app.route('/adm_view_feedback')
def adm_view_feedback():
    db=Db()
    qry="select * from department"
    res=db.select(qry)
    return render_template('admin/admin view feeddback.html',data=res)
@app.route('/adm_view_feedback_post',methods=['post'])
def adm_view_feedback_post():
    dept_id=request.form["textfield3"]

    db=Db()
    qry="SELECT teacher.regno , teacher.* , subject.* FROM `teacher` ,`subject` , `assign`,`department` WHERE" \
        "`assign`.`tid`=`teacher`.`lid`AND " \
        "`assign`.`subid`=`subject`.`subid` AND " \
        "`department`.`did`=`subject`.`dept` AND " \
        "`teacher`.`dept`='"+str(dept_id)+"' "

    # qry="SELECT teacher.regno , teacher.fname,teacher.lname, subject.sname FROM `teacher` ,`subject` , `assign`,`department` WHERE `assign`.`tid`=`teacher`.`lid` AND `assign`.`subid`=`subject`.`subid` AND `department`.`did`=`subject`.`dept` AND teacher.`dept`='"+str(dept_id)+"'"
    res1 = db.select(qry)
    res = db.select("SELECT * FROM `department`")
    return render_template('admin/admin view feeddback.html',data1=res1, data=res)

# admin detailed feedback
@app.route('/admin_view_dfeedback/<sid>/<lid>')
def admin_view_dfeedback(sid,lid):

    totalstatements=""





    db=Db()
    qry="SELECT `feedback_table`.*, `student`.`fname`,`student`.`lname` FROM `student` INNER JOIN `feedback_table` ON `feedback_table`.`studid`=`student`.`lid` WHERE feedback_table.`subid`='"+sid+"' AND feedback_table.tid='"+lid+"'"
    res=db.select(qry)
    msw=[]

    from  sd import  extractkeywords
    for i in res:
        fname=i['fname']
        feedback=extractkeywords(i['feedback'])
        msw.append({'fname':fname,'feedback':feedback,'fid':i['fid']})
        totalstatements=totalstatements+ feedback +" "
        # print(res)

    finalreview= extractkeywords(totalstatements,20)

    emotion = []
    r = {}
    if len(res) > 0:
        for i in res:
            print(i["emotion"])
            emotion.append(i["emotion"])
            print(emotion)
        count_positive = emotion.count("positive")
        print("count positive=", count_positive)
        count_neutral = emotion.count("neutral")
        print("count neutral=", count_neutral)
        count_negative = emotion.count("negative")
        print("count negative=", count_negative)
        total_count = len(emotion)
        print("total count=", total_count)
        per_positive = (float(count_positive) / float(total_count)) * 100
        print("percentage positive=", per_positive)
        per_neutral = (float(count_neutral) / float(total_count)) * 100
        print("percentage neutral=", per_neutral)
        per_negative = (float(count_negative) / float(total_count)) * 100
        print("percentage negative=", per_negative)
        if len(res) > 0:
            # r['status'] = "1"
            # r['Angry'] = per_anger
            # r['Disgusted'] = per_disgus
            # r['Fearful'] = per_fear
            # r['Happy'] = per_joy
            # r['Neutral'] = per_neutral
            # r['Sad'] = per_sad
            # r['Surprised'] = per_surp
            # print(gco,hc1)
            labels = ["Positive", "Neutral", "Negative"]
            values = [per_positive, per_neutral, per_negative]

            print(labels)
            print(values)

    return render_template('admin/detailfeedback.html',data1=msw,finalreview=finalreview,labels=labels,values=values)

# teacher view student list


@app.route("/detailedfdbk/<id>")
def detailedfdbk(id):
    db=Db()
    res=db.selectOne("SELECT * FROM `feedback_table` WHERE fid='"+id+"'")
    return render_template("admin/feedbackmore.html",res=res)


@app.route("/tdetailedfdbk/<id>")
def tdetailedfdbk(id):
    db=Db()
    res=db.selectOne("SELECT * FROM `feedback_table` WHERE fid='"+id+"'")
    return render_template("teacher/feedbackmore.html",res=res)



@app.route('/stud_list_view')
def stud_list_view():
    return render_template("teacher/student profile.html")

@app.route('/stud_list_view_post',methods=['post'])
def stud_list_view_post():
    sem=request.form["Sem"]
    db=Db()
    # qry="SELECT regno,fname,lname,email FROM student WHERE student.dept= AND student.sem='"+sem+"'"

    qry="SELECT student.regno,student.fname,student.lname,student.email FROM student, teacher WHERE student.dept= teacher.dept AND student.sem='"+sem+"' AND teacher.lid='"+str(session['lid'])+"'"
    res=db.select(qry)
    return render_template("teacher/student profile.html",data=res)

if __name__ == '__main__':
    app.run(debug=True, port=5000)