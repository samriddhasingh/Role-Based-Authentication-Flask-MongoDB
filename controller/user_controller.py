from app import app
from flask import request,render_template,session,redirect,url_for
from model.user_model import user_model
from functools import wraps
obj=user_model()


def superuser_login_required(f):
    @wraps(f)
    def wrap():
        validuser = obj.verify_superuser_details(session['username'],session['password'])
        if validuser:
            return f()
        else:
            return redirect(url_for('home'))
    return wrap




@app.route('/superuser',methods=['GET', 'POST'])
def superuser():
    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')
        print(username,password)
        data=obj.superuser(username,password)
        print('controller')
        print(data)
        if data:
            for i in data:
                print(i)
                session['username']=i['username']
            session['role']='superuser'
            print(session['username'])
            return redirect(url_for('superuserdetails',role=session['role']))
        else:
            return render_template('login.html')
    else:
        
        return render_template('login.html')
    


@app.route('/details',methods=['GET', 'POST'])
def superuserdetails():
    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')
        role='admin'
        data=obj.admin(username,password)
        print('controller')
        print(data)
        if data:
            for i in data:
                print(i)
                session['username']=i['username']
            session['role']='superuser'
            print(session['username'])
            return redirect(url_for('details',role=session['role']))
        else:
            
            return render_template('login.html')
    else:
        data=obj.all_superuser_details()
        return render_template('dashboard.html',data=data)