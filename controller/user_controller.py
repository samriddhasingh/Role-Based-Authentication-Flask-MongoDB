from app import app
from flask import request,render_template,session,redirect,url_for,flash
from model.user_model import user_model
from functools import wraps

obj=user_model()
ROLES = {
    'superuser': ['create_admin'],
    'admin': ['create_user'],
    'user': []
}

def role_required(roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            if 'username' in session:
                user=obj.verify_user(session['username'],session['role'])
                print(user)
                if user and session['role'] in ROLES:
                    return view_func(*args, **kwargs)
            return redirect(url_for('home'))
        return wrapper
    return decorator

@app.route('/user',methods=['GET', 'POST'])
def user():
    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')
        department=request.form.get('department')
        print(username,password,department)
        data,department_admin=obj.user(username,password,department)
        print(data)
        if data:
            session['username']=data['username']
            session['role']='user'
            session['department']=data['department']
            session['department_admin']=department_admin
            print(session['username'])
            return redirect(url_for('user_dashboard'))
        else:
            flash('Username or password incorrect please type correctly!!','error')
    return render_template('userlogin.html')
    

@app.route('/user_dashboard',methods=['GET', 'POST'])
@role_required(['user'])
def user_dashboard():
    username=session['username']
    department=session['department']
    department_admin=session['department_admin']
    return render_template('userdashboard.html',username=username,department=department,departmentadmin=department_admin)

