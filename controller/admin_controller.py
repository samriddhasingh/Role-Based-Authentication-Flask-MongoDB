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

@app.route('/admin',methods=['GET', 'POST'])

def admin():
    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')
        data=obj.admin(username,password)
        if data:
            session['username']=data['username']
            session['role']='admin'
            session['department']=data['department']
            return redirect(url_for('admindashboard'))
        else:
            flash('Username or password incorrect please type correctly!!','error')
    return render_template('adminlogin.html')


@app.route('/admindashboard',methods=['GET', 'POST'])
@role_required(['admin'])
def admindashboard():
    department=session['department']
    userdata=obj.userdetails(session['department'])
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        department=session['department']

        msg=obj.createuser(username,password,department)


        flash(msg,'success')
        return render_template('admindashboard.html',userdata=userdata,department=department,username=session['username'])
    return render_template('admindashboard.html',userdata=userdata,department=department,username=session['username'])