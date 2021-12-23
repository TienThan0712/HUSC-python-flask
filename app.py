from flask import Flask,render_template,g,request,flash,redirect,url_for,session,flash
import os
from functools import wraps
import sqlite3
import os
app = Flask(__name__)

# Kiểm tra đăng nhập
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap

# Kết nói CSDL
app.secret_key = os.urandom(24)
app.database='sample.db'
conn=sqlite3.connect('sample.db')
def connect_db():
 return sqlite3.connect(app.database)

# Trang chủ
@app.route('/home')
@login_required
def home():
 return render_template('home.html')

# Tìm kiếm sinh viên
@app.route('/sef')
@login_required
def sef():
 return render_template('search.html')

@app.route('/ser',methods=['POST'])
@login_required
def ser():
 g.db = connect_db()
 cur=g.db.execute( "select * from students where name like ? ", ["%"+request.form['search']+"%"] )
 row = cur.fetchall()
 return render_template("search.html",row=row)

# Sửa sinh viên
@app.route('/update',methods=['GET','POST'])
@login_required
def delt():
 g.db = connect_db()
 cur=g.db.execute( "select * from students where name = ? ",[request.args.get('name')])
 row=cur.fetchall()
 return render_template("update.html",row=row) 

@app.route('/upd', methods=['POST'])
@login_required
def upd():
 g.db=connect_db()
 g.db.execute('update students set name= ?, mark1=? ,mark2 =? ,total=? ,grade=?  where name=?',(request.form['name'],request.form['mark1'],request.form['mark2'],request.form['total'],request.form['grade'],request.form['name1']),)
 g.db.commit()
 return redirect(url_for('home'))

# Xóa sinh viên
@app.route('/delete',methods=['POST'])
@login_required
def delete():
 g.db = connect_db()
 g.db.execute( "delete from students where name = ? ", (request.form['delete'],) )
 g.db.commit()
 cur=g.db.execute( "select * from students ")
 row=cur.fetchall()
 return render_template("index.html",row=row) 

#Thêm sinh viên
@app.route('/stud', methods=['GET','POST'])
@login_required
def stud():
 return render_template('stud.html')

@app.route('/add', methods=['POST'])
@login_required
def add():
 g.db=connect_db()
 cur=g.db.execute( "select * from students where name = ? ",(request.form['name'],))
 row=cur.fetchall()
 if len(row)==0:
    g.db.execute('INSERT INTO students (name,mark1,mark2,total,grade) VALUES(?,?,?,?,?)',[request.form['name'],request.form['mark1'],request.form['mark2'],request.form['total'],request.form['grade']]);
    g.db.commit()
    flash('posted')
 else:
    flash('SV đã tồn tại')
    return render_template("stud.html",)
 return redirect(url_for('home'))

 # Đăng nhập 

@app.route('/', methods=['GET','POST'])
def login():
   error = None
   if request.method == 'POST':
    g.db=connect_db()
    cur=g.db.execute( "select * from admin where user = ? and pass = ? ",[request.form['username'],request.form['password'],])
    row=cur.fetchall()
    if len(row)==0:
            error = 'Invalid Credentials. Please try again.'
    else:
            session['logged_in']=True 
            return redirect(url_for('home'))
   return render_template('login2.html', error=error)

# Hiển thị sinh viên
@app.route('/rec')
@login_required
def rec(): 
 g.db = connect_db() 
 cur = g.db.execute('select name,mark1,mark2,total,grade from students')
 
 row = cur.fetchall()  
 return render_template('index.html',row=row)
 
# Đăng Xuất
@app.route('/logout')
@login_required
def logout():
 session.pop('logged_in',None)
 return redirect(url_for('login'))

# Thêm admin
@app.route('/addad', methods=['GET','POST'])
@login_required
def addad():
 return render_template('addadmin.html')

@app.route('/addadmin', methods=['POST'])
@login_required
def addadmin():
 g.db=connect_db()
 cur=g.db.execute( "select * from admin where user = ? ",(request.form['username'],))
 row=cur.fetchall()
 if len(row)==0:
    g.db.execute('INSERT INTO admin (user,pass) VALUES(?,?)',[request.form['username'],request.form['password'],]);
 else:
    flash('Admin đã tồn tại')
    return render_template("addadmin.html",)
 return redirect(url_for('home'))

# Hiển thị admin
@app.route('/recad')
@login_required
def recad(): 
 g.db = connect_db() 
 cur = g.db.execute('select user,pass from admin')
 
 row = cur.fetchall()  
 return render_template('index2.html',row=row)

# Xóa admin
@app.route('/deletead',methods=['POST'])
@login_required
def deletead():
 g.db = connect_db()
 g.db.execute( "delete from admin where user = ? ", (request.form['delete'],) )
 g.db.commit()
 cur=g.db.execute( "select * from admin ")
 row=cur.fetchall()
 return render_template("index2.html",row=row) 

if __name__ == '__main__':
 app.run(debug=True)
