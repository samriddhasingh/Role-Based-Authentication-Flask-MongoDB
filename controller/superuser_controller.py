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




@app.route('/superuser',methods=['GET', 'POST'])
def superuser():
    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')
        data=obj.superuser(username,password)
        print(data)
        if data:
            session['username']=data['username']
            session['role']='superuser'
            print(session['username'])
            return redirect(url_for('superuser_dashboard'))
        else:
            flash('Username or password incorrect please type correctly!!','error')
    return render_template('login.html')
    

@app.route('/superuser_dashboard',methods=['GET', 'POST'])
@role_required(['superuser'])
def superuser_dashboard():
    
    admindata,userdata=obj.superuserdetails()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        department=request.form.get('department')


        msg=obj.createadmin(username,password,department)


        flash(msg,'success')
        return render_template('dashboard.html',admindata=admindata,userdata=userdata)
    return render_template('dashboard.html',admindata=admindata,userdata=userdata)




    