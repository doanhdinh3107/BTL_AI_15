from flask import Blueprint, render_template, flash, request
from flask_login import login_required, current_user
from .models import Owner, Car
import os
from werkzeug.utils import secure_filename
from .test1 import get_result
from .test2 import get_image

views = Blueprint('views', __name__)

ALLOWED_EXTENSIONS = set(['jpg','png'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


def get_infor(car_id_list, video_name):
    infor_list = list()
    for i in car_id_list:
        if i[1] == '0':
            image = i[0]
            infor_list.append((image,'0'))
        else:
            image = i[0]
            car_id = i[1]
            car = Car.query.filter_by(id = car_id).first()
            if car:
                owner = Owner.query.filter_by(id = car.owner_id).first()
                infor_list.append((image, car_id, owner))
            else:
                flash("There are no info of this car owner (Car id: " + car_id + " )")
                infor_list.append((image, car_id))
    return render_template("home.html", user=current_user, infor_list = infor_list, video=video_name)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if 'file' not in request.files:
        flash('No file part')
    else:
        vid = request.files['file']
        if vid.filename == '':
            flash('No video selected for uploading')
        elif vid and allowed_file(vid.filename):
            video_name = secure_filename(vid.filename)
            vid.save(os.path.join('website/static/video', video_name))
            flash('Image successfully uploaded and displayed below')
            image = get_image(video_name)
            if image:
                car_id_list = get_result(image)
                if car_id_list:
                    return get_infor(car_id_list, video_name)
            return render_template("home.html", user=current_user,
                                   video=video_name)
        else:
            flash('Allowed image type .jpg, .png')

    return render_template("home.html", user=current_user)
