from traceback import print_tb

from flask import Flask, request, make_response, session, render_template, redirect
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_login import current_user
from data import db_session
from data.db_session import create_session
from data.users import User, Jobs
from forms.add_job_form import JobForm
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
    # user.email = 'admin@admin.com'
    # user.name = 'admin'
    # user.set_password('123')
    # db_sess.add(user)
    # db_sess.commit()
    app.run()


def get_users_name():
    db_sess = create_session()
    data = []
    for us in db_sess.query(User).all():
        data.append((us.id, us.name))
    return data


def get_jobs():
    db_session = create_session()
    data = []
    for i in db_session.query(Jobs).all():
        data.append([i.job, i.team_leader, i.work_size, i.collaborators, i.is_finished])
    return data

@app.route('/jobs', methods=['GET', 'POST'])
def show_jobs():
    form = JobForm()
    form.team_leader.choices = get_users_name()
    form.collaborators.choices = get_users_name()
    if form.validate_on_submit():
        job = Jobs()
        job.team_leader = form.team_leader.data
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        print(job.team_leader)
        print(job.job)
        print(job.collaborators)
    return render_template('show_jobs.html', form=form, jobs=get_jobs())


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