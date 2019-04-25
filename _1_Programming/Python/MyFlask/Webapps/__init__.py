from flask import Flask,render_template,request,session,redirect,url_for,flash
# 引入Bootstrap库
from flask_bootstrap import Bootstrap
# 引入时间处理库
from flask_moment import Moment
from datetime import datetime
# 引入WTF处理表单
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired

# 当test调用 __init__.py 时，将构造函数的 name 参数传给 Flask 程序，Flask 用这个参数决定程序的根目录
# __name__ = (str) 'Webapps'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'call me root'
bootstrap = Bootstrap(app)
moment = Moment(app)


# 定义表单类
class NameForm(FlaskForm):
    name = StringField('What is your name?',validators=[DataRequired()])
    submit = SubmitField('submit')

# 路由： URL到函数的映射关系
# 用修饰器把函数注册为事件的处理程序
@app.route('/',methods=['GET','POST'])
# 视图函数
# 使用/POST/重定向/GET模式 避免出现再次提交表单警告
# 需要使用session保存用户会话
def index():
    form = NameForm()
    if form.validate_on_submit():
        # 数据变化后，使用flush刷新
        old_name = session.get('name')
        if old_name is not None and old_name!= form.name.data:
            flash('You have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html',form=form,name=session.get('name'),current_time=datetime.utcnow())

# Flask把动态部分作为参数传入函数
@app.route('/user/<username>/')
def get_index_username(username):
    return ("Hello, "+username)

# 支持int float 和 path（把 / 作为动态片段的一部分）
@app.route('/user/<int:userid>/')
def get_index_userid(userid):
    return ("Hello, you're the NO."+str(userid)+" visitor")

@app.route('/user/<path:userpath>/')
def get_index_userpath(userpath):
    return ("Hello, this is your path:"+str(userpath))



# Flask从客户端收到请求时，要让视图函数能访问一些对象，才能处理请求
# 请求对象封装了客户端发送的HTTP请求
# 将请求对象作为参数传入视图函数会导致每个视图函数都在增加参数
# 使用上下文可以临时把某些对象变成全局可访问
# 实际上多线程中处理的request对象不同，Flask使用上下文让特定变量在一个线程中全局访问（创建线程池），而不干扰其他线程
@app.route('/request/agent/',methods=['GET'])
def get_request_agent():
    user_agent = request.headers.get('User-Agent')
    return ('Your browser is '+user_agent)

# 视图函数的两个作用：业务逻辑 and 表现逻辑
# 把表现逻辑移到模板中可以提升程序的可维护性
# 模板中动态部分用占位变量表示，在请求上下文中获取到真实值替换占位变量的过程称为渲染
# Flask把模板保存在程序文件夹的templates子文件夹
@app.route('/login/',methods=['GET'])
def get_login():
    return render_template('Login_Index.html') #第一个参数是模板名，随后的都是键值对

@app.route('/login/',methods=['POST'])
def post_login():
    username = request.form['username']
    password = request.form['password']
    if username =='admin' and password == 'password':
        return render_template('Login_Success.html',username=username)
    return render_template('Login_Index.html',message='Invalid User or Password',username=username)
    #左边的username表示参数名，就是模板中使用的占位符，右边的username是当前作用域下的变量


# 自定义错误界面
@app.errorhandler(404)
def error_page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def error_internal_server_error(e):
    return render_template('500.html'),500


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=31942)

