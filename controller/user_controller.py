from app import app
from flask import request,render_template,session,redirect,url_for
from model.user_model import user_model

from functools import wraps



obj=user_model()

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
            return redirect(url_for('details',role=session['role']))
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/details/<role>',methods=['GET'])
def details(role):
    print(session['username'])
    print(session['role'])
    data=obj.details(session['username'],session['role'])
    print(data)
    return render_template('dashboard.html',data=data)