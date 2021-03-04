from flask import Flask, render_template, request, session, url_for
from werkzeug.utils import redirect
import pymysql

#在本地可以连接到MySQL server,放到docker上就不行了，查下怎么设置，参数，环境等等
db = pymysql.connect(host='localhost',user='root',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

cur = db.cursor()
cur.execute("create database IF NOT EXISTS zhong")
cur.execute("use zhong")
cur.execute("create table IF NOT EXISTS user(username varchar(20), password varchar(20));")
#cur.execute("insert into user values(\"zhongai\",\"abc\")")
db.commit()

print("database and table created: success")

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "hello, world!"

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST','GET'])
def loging():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        print("username: " + username)
        print("password: " + password)
        #一些判断语句验证，1：用户名是否存在 2：密码是否正确
        sql = "select * from user where username = (%s)"
        cur.execute(sql,(username))
        name = cur.fetchone()
        if name is None:
            return "no exist this username!"
        print("login name:" + name['username'])

        print(name)
        if name['password'] == password:
            return "成功登入，欢迎回来： " + username
        else:
            return "登入失败, 用户："+username+" 密码错误"

    return render_template('login.html')


@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_check = request.form['pcheck']
        print("username: " + username)
        print("password: " + password)
        print("password_check: " + password_check)

        #一些判断语句，比如输入空白提示，2次密码不同提示，用户名重复提示等等
        sql = "select * from user where username = (%s)"
        cur.execute(sql, (username))
        name = cur.fetchone()
        ex = 0;
        if name is None:
            ex = 1;
        if password != password_check:
            return "注册失败，two passwords don't match."
        elif ex == 0:
            return "注册失败，username \""+username+ "\" existed."

        #新用户添加到database
        sql = "insert into user values (%s,%s)"
        cur.execute(sql,(username,password))
        db.commit()
        return "注册成功，欢迎新用户: "+username
        #return render_template('register.html', rep=username,title="欢迎登入")
        #rep和title是html里面{{}}里的变量
    return render_template('register.html')

@app.route('/a')
def index2():
   if 'username' in session:
        username = session['username']
        return 'Logged in as ' + username + '<br>' + "<b><a href = '/logout'>click here to log out</a></b>"
   return "You are not logged in <br><a href = '/login'>" + "click here to log in</a>"


if __name__=="__main__":
    app.run(host='0.0.0.0',port=8000)