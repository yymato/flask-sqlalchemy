from flask import Flask, request, make_response, session, render_template, redirect
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_login import current_user
from data import db_session
from data.db_session import create_session
from data.users import User, Jobs
from forms.login_form import LoginForm
from forms.register import RegisterForm

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init('123.sqlite')
    # db_sess = create_session()
    # user = User()
    # user.email = '070913a@gmail.com'
    # user.name = 'sv'
    # user.set_password('123')
    # db_sess.add(user)
    # db_sess.commit()
    app.run()

def get_jobs():
    db_session = create_session()
    data = []
    for i in db_session.query(Jobs).all():
        data.append([i.job, i.team_leader, i.work_size, i.collaborators, i.is_finished])
    return data

@app.route('/jobs')
def show_jobs():
    return render_template('show_jobs.html', jobs=get_jobs())


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/jobs')
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/jobs")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        pass
    return render_template('register.html', form=form)

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect('/jobs')
    else:
        return redirect('/register')

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)

if __name__ == '__main__':
    main()






