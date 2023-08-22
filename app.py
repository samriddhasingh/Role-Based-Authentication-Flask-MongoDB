from flask import Flask, request,render_template,session,redirect,url_for,flash
import secrets


app=Flask(__name__)

app.secret_key = secrets.token_hex(16) 

@app.route('/')
def home():
    return "This is homepage"



if __name__=='__main__':
    app.run(debug=True)


from controller import *