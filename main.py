from flask import Flask, render_template, redirect
from regex import F

from forms.user import RegisterForm, LoginForm
from data.users import User
from data import db_session


app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY'

name = ''


def main():
    db_session.global_init("db/blogs.db")
    app.run()


@app.route('/')
@app.route('/2')
def main1():
    global name
    name = ''
    return render_template('index1.html', img='static/img/str1')

@app.route('/1')
def main2():      
    return render_template('index3.html', img='static/img/str1', name=name.name)

@app.route('/main')
def main3():
    return render_template('index2.html', img='static/img/str2', name=name.name)


@app.route('/register/', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form, img='static/img/str2')


@app.route('/login', methods=['GET', 'POST'])
def login():
    global name
    form = LoginForm()
    if form.email.data and form.password.data:
        db_sess = db_session.create_session()
        name = db_sess.query(User).filter(User.email == form.email.data).first()
        if name and name.check_password(form.password.data):
            return redirect('/1')
        elif name and not name.check_password(form.password.data):
            return render_template('login.html', form=form,
                                    message="Неверный пароль!")
        else:
            return render_template('login.html', form=form,
                                    message="Пользователя не существует")
    return render_template("login.html", form=form)


if __name__ == '__main__':
    main()