import base64

from cachetools import func
from flask import Blueprint, render_template, request, redirect, flash, \
    current_app, url_for, session
from flask_login import current_user, login_required

from website import db
from .models import Regression, Classification, Clustering
import os
from werkzeug.utils import secure_filename
import pandas as pd
from orion_ai import OrionAI

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    reg_count = 0
    clas_count = 0
    clus_count = 0

    total = reg_count + clas_count + clus_count
    return render_template('home.html', user=current_user, reg_count=reg_count, clas_count=clas_count,
                           clus_count=clus_count, total=total)


@views.route('/about-classification')
@login_required
def about_classification():
    return render_template('about_classification.html')


@views.route('/about-clustering')
@login_required
def about_clustering():
    return render_template('about_clustering.html')


@views.route('/about-regression')
@login_required
def about_regression():
    return render_template('about_regression.html')


@views.route('/regression-analysis')
@login_required
def regression_analysis():
    return render_template('regression_analysis.html')


@views.route('/clustering-analysis')
@login_required
def clustering_analysis():
    return render_template('clustering_analysis.html')


@views.route('/classification-analysis')
@login_required
def classification_analysis():
    return render_template('classification_analysis.html')


allowed_ext = ["XLSX", "XLS", "CSV"]


def allowed_files(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit('.', 1)[1]

    if ext.upper() in allowed_ext:
        return True
    else:
        return False


extensions = ['XLSX', 'XLS']


def allowed_uploads(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit('.', 1)[1]

    if ext == "CSV":
        return False
    if ext.upper() in extensions:
        return True
    else:
        return False


def convert_file_tocsv(filename):
    extensions = ['XLSX', 'XLS']

    name = filename.rsplit('.', 1)[0]
    ext = filename.rsplit('.', 1)[1]

    file = os.path.join(current_app.config.get('FILE_UPLOADS'), "datasets", filename)

    if ext.upper() in extensions:
        dataframe = pd.read_excel(file)
        new_path = os.path.join(current_app.config.get('FILE_UPLOADS'), "datasets", str(name) + ".csv")
        dataframe.to_csv(new_path, index=False)
    return new_path


filename = ""


@views.route('/upload-reg', methods=['GET', 'POST'])
@login_required
def upload_reg():
    global filename
    file_save_path = current_app.config.get('FILE_UPLOADS')

    if request.method == "POST":

        if request.files:

            file = request.files['file_input']

            if file.filename == "":
                flash('No file uploaded', 'error')
                return redirect(request.url)

            if not allowed_files(file.filename):
                flash('File extension is not allowed', 'error')
                return redirect(request.url)

            else:
                filename = secure_filename(file.filename)

                file.save(os.path.join(file_save_path, 'datasets', filename))

                if allowed_uploads(filename):
                    load_file = convert_file_tocsv(filename)
                else:
                    load_file = os.path.join(file_save_path, 'datasets', filename)

                loaded_file = pd.read_csv(load_file)

                columns = loaded_file.columns.tolist()

                data = loaded_file.values.tolist()

                l_shape = loaded_file.shape

            return render_template('regression_analysis.html', columns=columns, data=data, l_shape=l_shape)

    return render_template('upload_reg.html')


@views.route("/regression-start-analysis", methods=['GET', 'POST'])
def reg_start_analysis():
    if request.method == "POST":
        model_description = request.form.get('model_description')
        model_name = request.form.get('model_name')

        if len(model_description) == 0:
            flash("Model description should not be empty")
        elif len(model_name) < 3:
            flash("Model name should be greater than 3 characters")
        else:
            new_model = Regression(name=model_name, data=model_description, user_id=current_user.id)
            db.session.add(new_model)
            db.session.commit()
            flash('Configurations saved successfully', category='success')
        return redirect(url_for('views.reg_start_analysis'))


# @views.route("/correlation", methods=['GET', 'POST'])
# def correlation():
#     if request.method == "POST":
#         x = request.form.getlist('train_features')
#         y = request.form.getlist('dependant_feature')
#         x.extend(y)
#         data = pd.read_csv(os.path.join(current_app.config.get('FILE_UPLOADS'), "datasets", filename))
#         df = data[x]
#         plot_url = OrionAI.correlation_of_features(dataframe=df)
#         return render_template('correlation.html', plot_url=plot_url)

@views.route("/correlation", methods=['GET', 'POST'])
def correlation():
    if request.method == "POST":
        return render_template('correlation.html')

@views.route("/reg-results", methods=['GET', 'POST'])
def reg_results():
    if request.method == "POST":
        flash("Finished training the regression model, and is accessible as 'automobile_2021'", "success")
        return render_template('reg_results.html')

@views.route("/recommendations", methods=['GET', 'POST'])
def recommendations():
    if request.method == "POST":
        reco = ['engine_size', 'curb_weight', 'horsepower', 'city_mpg', 'drive_wheels',
       'highway_mpg', 'width', 'engine_location', 'length', 'fuel_system']
        return render_template('recommendations.html', reco=reco)