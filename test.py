from flask import Flask
from data import db_session
from data.users import User
from data.jobs import Jobs
from flask import render_template
from forms.user import RegisterForm
from flask import redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/block.db")
    @app.route('/')
    @app.route('/index')
    def index():
        return render_template('base.html', title='Заготовка')

    @app.route('/register', methods=['GET', 'POST'])
    def reqister():
        form = RegisterForm()
        if form.validate_on_submit():
            if form.password.data != form.password_again.data:
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Пароли не совпадают")
            db_sess = db_session.create_session()
            if db_sess.query(User).filter(User.email == form.email.data).first():
                return render_template('register.html', title='Регистрация',
                                       form=form,
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
        return render_template('register.html', title='Регистрация', form=form)

    @app.route('/login')
    def login():
        return render_template('base.html', title='Заготовка')
    app.run()


if __name__ == '__main__':
    main()