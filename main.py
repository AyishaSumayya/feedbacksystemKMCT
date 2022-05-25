from flask import Flask,render_template,request,redirect,url_for,session
from DBConnection import  Db
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
app = Flask(__name__)
app.secret_key="jfdkfjd"
static_path="C:\\Users\\HP\\OneDrive\\Desktop\\Excercise Recommendation\\Excercise Recommendation\\static\\"
@app.route('/')
def hello_world():
    return render_template("login_index.html")
@app.route('/login_post',methods=['post'])
def login_post():

    uname=request.form['textfield']
    paswd=request.form['textfield2']
    s="SELECT * FROM `login` WHERE `username`='"+uname+"' AND `password`='"+paswd+"'"
    db=Db()
    res=db.selectOne(s)
    if res is not None:
        session["lid"]=res["log_id"]
        if res['type']=="admin":
            
            return render_template("admin/admin_home.html")
        
        else:
            return render_template("user/user_home.html")
    else:
        return '''<script>alert('Invalid Username or password');window.location='/'</script>'''
@app.route('/ad_home')
def ad_home():
    session["page"] = "Admin home"
    return render_template("admin/admin_home.html")

@app.route('/student_signup')
def student_signup():
    return render_template('Sign-up.html')

@app.route('/student_signup_post',methods=['post'])
def student_signup_post():
    name=request.form['textfield']
    age=request.form["age"]
    gen=request.form["gen"]
    place=request.form['textfield2']
    post=request.form['textfield3']
    pin=request.form['textfield4']
    qual=request.form['textfield5']

    logo=request.files['fileField']

    logo.save(static_path+"business_logo\\"+logo.filename)
    url="/static/business_logo/"+logo.filename





    phno=request.form['textfield7']
    email=request.form['textfield8']
    password = request.form['pswrd1']

    c=Db()

    qry1 = "INSERT INTO login(username,password,type) VALUES('"+email+"', '"+password+"','student')"
    res1 = c.insert(qry1)
    qry="INSERT INTO `students`(`uname`,`uage`,`usex`,`uplace`,`upost`,`upin`,`uqual`,`uemail`,`ucontact`,`uphoto`,`ulid`)values('"+name+"','"+age+"','"+gen+"','"+place+"','"+post+"','"+pin+"','"+qual+"','"+email+"','"+phno+"','"+url+"','"+str(res1)+"')"
    res=c.insert(qry)
    return '''<script>alert('Success');window.location='/'</script>'''


@app.route('/ad_view_approved_users')
def ad_view_approved_users():
    # session["page"] = "Admin View Approved users"
    qry="select * from students "
    db=Db()
    res=db.select(qry)
    return render_template("admin/view approved users.html",res=res)

@app.route('/admin_add_test')
def admin_add_test():

    return render_template('admin/Add Exam.html')

@app.route('/admin_add_mock_test_post',methods=['post'])
def admin_add_mock_test_post():
    text=request.form['textfield']

    c=Db()
    qry="insert into exam (exam) values ('"+text+"')"
    c.insert(qry)
    return render_template('admin/Add Exam.html')



@app.route('/admin_view_mock_test')
def admin_view_mock_test():

    c=Db()
    qry="select * from exam"
    res = c.select(qry)
    return render_template('admin/View ExaM.html',data=res)


@app.route('/admin_delete_exam/<id>')
def admin_delete_exam(id):
    c=Db()
    qry="delete from exam where ex_id='"+id+"'"
    res = c.delete(qry)
    return '''<script>alert('success');window.location='/admin_view_mock_test'</script>'''
@app.route('/admin_add_questions/<tid>')
def admin_add_questions(tid):
    d = Db()
    qry1=d.selectOne("select * from exam where ex_id='"+tid+"'")
    qry = "select * from question  where ex_id='"+tid+"'"
    res = d.select(qry)
    return render_template('admin/addquestion.html',data=res,data1=qry1)

@app.route('/admin_add_questions_post',methods=['post'])
def business_add_questions_post():
    q=request.form['textfield']
    oa=request.form['textfield2']
    ob=request.form['textfield3']
    oc=request.form['textfield4']
    od=request.form['textfield5']
    ca=request.form['select']
    type=request.form["select2"]
    tid=request.form['tid']
    c=Db()
    qry="INSERT INTO `question`(`Question`,`Answer`,`Type`,`Option1`,`Option2`,`Option3`,`Option4`,`ex_id`)VALUES('"+q+"','"+ca+"','"+type+"','"+oa+"','"+ob+"','"+oc+"','"+od+"','"+tid+"')"
    res=c.insert(qry)
    return '''<script>alert('Added');window.location='/admin_view_mock_test'</script>'''

@app.route('/admin_delete_question/<id>')
def admin_delete_question(id):
    c=Db()
    qry="delete from question where Q_id='"+id+"'"
    res=c.delete(qry)
    return '''<script>alert('deleted');window.location='/admin_view_mock_test'</script>'''



@app.route('/admin_add_recc')
def admin_add_recc():
    data1=[]
    return render_template('admin/Add Rececommentation.html',data1=data1)

@app.route('/admin__expost',methods=['post'])
def admin__expost():
    q = request.form['textfield']
    oa = request.form['textfield2']
    ob = request.form['textfield3']
    oc = request.form['textfield4']
    od = request.form['textfield5']
    ca = request.form['select']
    type = request.form["select2"]

    c = Db()
    qry = "INSERT INTO `excersice`(`Question`,`Answer`,`Type`,`Option1`,`Option2`,`Option3`,`Option4`)VALUES('" + q + "','" + ca + "','" + type + "','" + oa + "','" + ob + "','" + oc + "','" + od + "')"
    res = c.insert(qry)
    return '''<script>alert('Added');window.location='/admin_add_recc'</script>'''


@app.route('/admin_view_rec')
def admin_view_rec():

    c=Db()
    qry="select * from excersice"
    res = c.select(qry)
    return render_template('admin/View recommendation.html',data=res)


@app.route('/admin_delete_ex/<id>')
def admin_delete_ex(id):
    c=Db()
    qry="delete from excersice where ecrid='"+id+"'"
    res = c.delete(qry)
    return '''<script>alert('success');window.location='/admin_view_rec'</script>'''




#

@app.route("/view_profile")
def  viewprofile():
    c = Db()
    qry = "select * from students where ulid='" + str(session["lid"]) + "'"
    res = c.selectOne(qry)
    return render_template("user/signupview.html",data=res)


@app.route('/user_view_mock_test')
def user_view_mock_test():

    c=Db()
    qry="select * from exam"
    res = c.select(qry)
    return render_template('user/View ExaM.html',data=res)


@app.route("/apply/<examid>")
def apply(examid):
    session["examid"]=examid
    session["qid"]="0"
    session["mark"]="0"
    session["wordslist"]=[]
    session["Logical Reasoning"]=0
    session["Verbal Reasoning"] = 0
    session["Analytical Reasoning"] = 0
    session["General Knowledge"]=0
    session["History"]=0


    qry="SELECT `question`.* FROM `question` WHERE ex_id='"+examid+"' AND Q_id > 0 ORDER BY Q_id asc "
    db=Db()
    res=db.select(qry)
    if len(res)>0:
        i=res[0]
        session["qid"]=i['Q_id']
        return render_template("/user/attendexam.html",i=res[0])
    else:

        return "<script>alert('Exam Finished');window.location='/user_view_mock_test'</script>"


@app.route("/nextquestions")
def nextquestions():



    qry="SELECT `question`.* FROM `question` WHERE ex_id='"+str(session['examid'])+"' AND Q_id > "+str(session['qid'])+" ORDER BY Q_id ASC"
    db=Db()
    res=db.select(qry)
    if len(res)>0:
        i=res[0]
        session["qid"]=i['Q_id']
        return render_template("/user/attendexam.html",i=res[0])
    else:
        lr=int(session["Logical Reasoning"])*2

        vr=int(session["Verbal Reasoning"]) *2
        ar=int(session["Analytical Reasoning"])*2
        gk=int(session["General Knowledge"])*2
        hs=int(session["History"])*2
        qry="INSERT INTO `exammarks` (`examid`,`mark`,`slid`,type,date) VALUES ('"+str(session['examid'])+"','"+str(lr)+"','"+str(session["lid"])+"','Logical Reasoning',curdate())"
        db=Db()
        db.insert(qry)

        qry = "INSERT INTO `exammarks` (`examid`,`mark`,`slid`,type,date) VALUES ('" + str(session['examid']) + "','" + str(
            vr) + "','" + str(session["lid"]) + "','Verbal Reasoning',curdate())"
        db = Db()
        db.insert(qry)

        qry = "INSERT INTO `exammarks` (`examid`,`mark`,`slid`,type,date) VALUES ('" + str(session['examid']) + "','" + str(
            ar) + "','" + str(session["lid"]) + "','Analytical Reasoning',curdate())"
        db = Db()
        db.insert(qry)

        qry = "INSERT INTO `exammarks` (`examid`,`mark`,`slid`,type,date) VALUES ('" + str(session['examid']) + "','" + str(
            gk) + "','" + str(session["lid"]) + "','Verbal Reasoning',curdate())"
        db = Db()
        db.insert(qry)

        qry = "INSERT INTO `exammarks` (`examid`,`mark`,`slid`,type,date) VALUES ('" + str(session['examid']) + "','" + str(
            hs) + "','" + str(session["lid"]) + "','History',curdate())"
        db = Db()
        db.insert(qry)
        aa=list(session["wordslist"])
        lp=["1","2","3","4","5","6","7","8","9","10",",",".","`","'"]
        for i in aa:
            if i in lp:
                aa.remove(i)
        return render_template("user/viewmarks.html",lr=lr,vr=vr,ar=ar,hs=hs,gk=gk,tot=(lr+vr+ar+hs+gk),words=aa)



@app.route("/answer",methods=['post'])
def ans():
    answer= request.form["radio"]
    print(answer)
    db=Db()
    qry="SELECT * FROM `question` WHERE `Q_id`='"+str(session['qid'])+"'"
    res=db.selectOne(qry)
    if res is not None:
        question=res["Question"]
        type = res["Type"]
        correctanswer=""
        if res['Answer']=="1":
            correctanswer=res['Option1']
        elif res['Answer']=="2":
            correctanswer=res['Option2']
        elif res['Answer']=="3":
            correctanswer=res['Option3']
        elif res['Answer']=="4":
            correctanswer=res['Option4']
        print(correctanswer)
        if correctanswer== answer:
            print(answer)
            m=int(session["mark"])
            m=m+1
            session["mark"]=str(m)
            if type=="Logical Reasoning":
                m = int(session["Logical Reasoning"])
                m=m+1
                session["Logical Reasoning"] = m
            elif type=="Verbal Reasoning":
                m = int(session["Verbal Reasoning"])
                m = m + 1
                session["Verbal Reasoning"] = m
            elif type == "Analytical Reasoning":
                m = int(session["Analytical Reasoning"])
                m = m + 1
                session["Analytical Reasoning"] = m
            elif type == "General Knowledge":
                m = int(session["General Knowledge"])
                m = m + 1
                session["General Knowledge"] = m
            elif type=="History":
                m = int(session["History"])
                m = m + 1
                session["History"] = m
            question.replace(",","").replace(".","").replace("0","").replace("1","").replace("2","").replace("3","").replace("4","").replace("5","").replace("6","").replace("7","").replace("8","").replace("0","").replace("!","").replace("@","")
            ss=word_tokenize(question)
            print(ss)
            filtered_sentence = []

            for w in ss:
                if w not in stop_words:
                    filtered_sentence.append(w)

            print(ss)
            print(filtered_sentence)
            aa=list(session["wordslist"])
            print(aa)

            for i in filtered_sentence:
                aa.append(i)
            session["wordslist"]=aa

    return redirect('/nextquestions')


@app.route("/studentviewmarks")
def studentviewmarks():
    db=Db()
    qry="SELECT `exam`.*,`course`.*,`exammarks`.* FROM `exammarks` INNER JOIN `exam` ON `exam`.`examid`=`exammarks`.`examid` INNER JOIN `course` ON `course`.`course_id`=`exam`.`cid` WHERE `exammarks`.`slid`='"+str(session['lid'])+"'"
    res=db.select(qry)
    return render_template("user/viewmarks.html",d=res)


if __name__ == '__main__':
    app.run(debug=True)
