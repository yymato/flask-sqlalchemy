from traceback import print_tb

from flask import Flask, request, make_response, session, render_template, redirect, url_for, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_login import current_user
from data import db_session
from data.db_session import create_session
from data.users import User, Jobs, Hazard, Department
from forms.add_department import DepartmentForm, EditDepartmentForm
from forms.add_job_form import JobForm, EditJobForm
from forms.login_form import LoginForm
from forms.register import RegisterForm

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init('db/123.sqlite')
    # db_sess = db_session.create_session()
    get_jobs()
    app.run()

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')

@login_required
@app.route("/delete_job/<int:job_id>")
def delete_job(job_id):
    db_sess = create_session()
    db_sess.delete(db_sess.query(Jobs).filter(Jobs.id == job_id).first())
    db_sess.commit()

    return redirect('/jobs')

def get_users_name(collaborators=''):
    db_sess = create_session()
    data = []
    collaborators = str(collaborators).split(', ')
    for us in db_sess.query(User).all():
        if collaborators != ['']:
            if str(us.id) in collaborators:
                data.append((us.id, us.name))
        else:
            data.append((us.id, us.name))
    return data


def get_jobs():
    db_session = create_session()
    data = []
    for i in db_session.query(Jobs).all():
        data.append([i.id, i.job, i.team_leader, i.work_size, i.collaborators, i.is_finished, i.hazard[0].name])
        print(data)
    return data

def get_hazard():
    data = []
    db_session = create_session()
    for i in db_session.query(Hazard).all():
        data.append((i.id, i.name))
    return data

def get_departments():
    data = []
    db_session = create_session()
    for i in db_session.query(Department).all():
        data.append([i.chief, i.title, i.members, i.email])
    return data

@login_required
@app.route("/delete_department/<int:department_id>")
def delete_department(department_id):
    db_sess = create_session()
    department = db_sess.query(Department).filter(Department.id == department_id).first()
    if department:
        db_sess.delete(department)
        db_sess.commit()
    return redirect('/departments')


@login_required
@app.route('/departments', methods=['GET', 'POST'])
def show_departments():
    db_sess = create_session()
    form = DepartmentForm()
    form1 = EditDepartmentForm()

    # Choices для SelectField
    users = db_sess.query(User).all()
    user_choices = [(u.id, u.name) for u in users]
    form.chief.choices = user_choices
    form.members.choices = user_choices
    form1.chief.choices = user_choices
    form1.members.choices = user_choices

    if request.method == 'POST':
        if form.form_type.data == 'add' and form.validate_on_submit():
            department = Department()
            department.title = form.title.data
            department.chief = form.chief.data
            department.members = ', '.join(form.members.data)
            department.email = form.email.data
            db_sess.add(department)
            db_sess.commit()

        elif form1.form_type.data == 'edit' and form1.validate_on_submit():
            department = db_sess.query(Department).filter(Department.id == int(form1.department_id.data)).first()
            if department:
                department.title = form1.title.data
                department.chief = form1.chief.data
                department.members = ', '.join(form1.members.data)
                department.email = form1.email.data
                db_sess.commit()

        return redirect('/departments')

    # Получение всех департаментов
    return render_template('show_departments.html', form=form, form1=form1, departments=get_departments())


@login_required
@app.route("/get_department/<int:department_id>")
def get_department(department_id):
    db_session = create_session()
    department = db_session.query(Department).filter(Department.id == department_id).first()
    if not department:
        print('Нет департамента')
        return jsonify({"error": "department not found"}), 404

    print({
        "success": True,
        "id": department.id,
        "title": department.title,
        "chief": department.chief,
        "members": get_users_name(department.members),
        "email": department.email
    })
    return jsonify({
        "success": True,
        "id": department.id,
        "title": department.title,
        "chief": department.chief,
        "members": get_users_name(department.members),
        "email": department.email
    })


@login_required
@app.route("/get_job/<int:job_id>")
def get_job(job_id):
    db_session = create_session()
    job = db_session.query(Jobs).filter(Jobs.id == job_id).first()
    if not job:
        return jsonify({"error": "Job not found"}), 404

    return jsonify({
        'success': True,
        'id': job.id,
        'team_leader': get_users_name(job.team_leader),
        'job': job.job,
        'collaboration': get_users_name(job.collaborators),
        'worksize': job.work_size
    })


@app.route('/jobs', methods=['GET', 'POST'])
@login_required
def show_jobs():
    form = JobForm()
    form.team_leader.choices = get_users_name()
    form.collaborators.choices = get_users_name()
    form.hazard.choices = get_hazard()

    form1 = EditJobForm()
    form1.team_leader.choices = get_users_name()
    form1.collaborators.choices = get_users_name()
    form1.hazard.choices = get_hazard()

    if request.method == 'POST':
        db_sess = create_session()
        if form.form_type.data == 'add' and form.validate_on_submit():
            job = Jobs()
            job.team_leader = form.team_leader.data
            job.job = form.job.data
            job.work_size = form.work_size.data
            job.collaborators = ', '.join(form.collaborators.data)
            job.is_finished = form.is_finished.data
            job.hazard = [db_sess.query(Hazard).get(form.hazard.data)]

            db_sess.add(job)
            db_sess.commit()

        if form1.form_type.data == 'edit' and form1.validate_on_submit():
            job = db_sess.query(Jobs).filter(Jobs.id == form1.job_id.data).first()

            job.team_leader = form1.team_leader.data
            job.job = form1.job.data
            job.work_size = form1.work_size.data
            job.collaborators = ', '.join(form1.collaborators.data)
            job.hazard = [db_sess.query(Hazard).get(form1.hazard.data)]
            job.is_finished = form1.is_finished.data
            db_sess.commit()

        return redirect('/jobs')

    return render_template('show_jobs.html', form=form, form1=form1, jobs=get_jobs())


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
    if current_user.is_authenticated:
        return redirect('/login')

    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user:
            return render_template('register.html', message='Данная почта уже зарегистрирована. Попробуйте войти.',
                                   form=form)
        else:
            db_sess = create_session()
            user = User()
            user.name = form.name.data
            user.email = form.email.data
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            login_user(user)
            return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)




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