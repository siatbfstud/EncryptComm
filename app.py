from flask import Flask , redirect , render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager , UserMixin , login_required ,login_user, logout_user
from werkzeug.utils import secure_filename


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.db'
app.config['SECRET_KEY']='abemad'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True

app.config["UPLOAD_FOLDER"] = "EncryptComm/static/pictures"

db = SQLAlchemy(app)




login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(200))
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))



@login_manager.user_loader
def get(id):
    return User.query.get(id)

@app.route('/',methods=['GET'])
@login_required
def get_home():
    return render_template('home.html')

@app.route('/login',methods=['GET'])
def get_login():
    return render_template('login.html')


@app.route('/signup',methods=['GET'])
def get_signup():
    return render_template('signup.html')

@app.route('/login',methods=['POST'])
def login_post():
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email).first()
    login_user(user)
    return redirect('/')

@app.route('/signup',methods=['POST'])
def signup_post():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    user = User(username=username,email=email,password=password)
    db.session.add(user)
    db.session.commit()
    user = User.query.filter_by(email=email).first()
    login_user(user)
    return redirect('/')

@app.route('/logout',methods=['GET'])
def logout():
    logout_user()
    return redirect('/login')

@app.route('/upload')
def upload_file():
   return render_template('login.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file2():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully'


if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True, debug=True)