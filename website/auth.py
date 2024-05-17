from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Owner, Car
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from datetime import date

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again!', category='error')
        else:
            flash('Email does not exits.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exits.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
            pass
        elif len(firstName) < 2:
            flash('First name must be greater than 1 character.',
                  category='error')
            pass
        elif password1 != password2:
            flash('Password don\'t match.', category='error')
            pass
        elif len(password1) < 7:
            flash('Password must be greater than 6 characters.',
                  category='error')
            pass
        else:
            new_user = User(email=email, first_name=firstName,
                            password=generate_password_hash(password1,
                                                            method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)


@auth.route('/add-owner', methods=['GET', 'POST'])
@login_required
def add_owner():
    if request.method == 'POST':
        ownerId = request.form.get('ownerId').upper()
        ownerName = request.form.get('ownerName')
        ownerEmail = request.form.get('ownerEmail')
        ownerPhone = request.form.get('ownerPhone')
        ownerBirth = request.form.get('ownerBirth')
        ownerOrigin = request.form.get('ownerOrigin')

        def name():
            tmp = [i.capitalize() for i in ownerName.split()]
            return " ".join(tmp)

        ownerName = name()

        def age():
            today = date.today()
            date1,time,year = [int(i) for i in ownerBirth.split('/')]
            ownerAge = today.year - year
            return ownerAge

        ownerAge = age()

        owner = Owner.query.filter_by(id=ownerId).first()

        if owner:
            flash('This owner already exists', category='error')
        elif len(ownerName) < 1:
            flash('Name must be greater than 1.', category='error')
            pass
        elif len(ownerEmail) < 1:
            flash('Email must be in (example@yourmail.com)', category='error')
        elif len(ownerPhone) != 10:
            flash('Phone number must be 10 number', category='error')
        elif ownerAge < 18:
            flash('Age must be greater than or equal to 18.', category='error')
            pass
        elif len(ownerBirth) != 10:
            flash('Birth must be in (dd/mm/yyyy)', category='error')
            pass
        elif len(ownerOrigin) < 1:
            flash('Origin error!', category='error')
            pass
        else:
            new_owner = Owner(id=ownerId, name=ownerName, age=ownerAge, birth=ownerBirth, place_of_origin=ownerOrigin, phone=ownerPhone, email=ownerEmail)
            db.session.add(new_owner)
            db.session.commit()
            flash('This owner added!', category='success')
            return redirect(url_for('auth.add_owner'))

    return render_template('add_owner.html', user=current_user)


@auth.route('/add-car', methods=['GET', 'POST'])
@login_required
def add_car():
    if request.method == 'POST':
        car_id = request.form.get('carId').upper()
        owner_id = request.form.get('ownerId').upper()

        owner = Owner.query.filter_by(id=owner_id).first()

        if owner:
            new_car = Car(id=car_id, owner_id=owner_id)
            db.session.add(new_car)
            db.session.commit()
            flash('This car added', category='success')
            return redirect(url_for('auth.add_car'))
        else:
            flash('There are no owner\'s information for this car!',
                  category='error')

    return render_template('add_car.html', user=current_user)