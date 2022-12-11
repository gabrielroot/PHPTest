from flask import render_template, Blueprint, redirect, request, flash, jsonify
from forms.UserForm import UserCreate
from models.UserModel import UserModel
from sqlalchemy.exc import IntegrityError
from app import db

user_routes = Blueprint('user_routes', __name__, url_prefix='/user', template_folder='templates/user')

@user_routes.route('/', methods=['GET'])
def index():
    users = db.session.execute(db.select(UserModel).order_by(UserModel.username)).scalars()
    return render_template('user/list.html', users=users)

@user_routes.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    form = UserCreate(request.form)
    user = db.get_or_404(UserModel, id)
    userOld = user 
      
    if request.method == 'POST':
        try:
            user.name=form.name.data
            user.email=form.email.data
            user.password=UserModel.hash_password(form.password.data) if form.password.data else UserModel.hash_password(userOld.password)
            user.username=form.username.data if form.username.data else userOld.username

            db.session.commit()

            flash("User edited successfully!", 'success')
            return redirect('/user')
        except:
            flash("An error occurred.", 'error')
          
    return render_template('user/edit.html', form=form, user=user)

@user_routes.route('/new', methods=['GET', 'POST'])
def new():
    form = UserCreate(request.form)
      
    if request.method == 'POST' and form.validate():
        user = UserModel(
          username=form.username.data,
          name=form.name.data,
          password=UserModel.hash_password(form.password.data),
          email=form.email.data
        )
        
        try:
          db.session.add(user)
          db.session.commit()
          
          flash("User created!", 'success')
          return redirect('/user')
        except IntegrityError:
          flash("This username already exists.", 'error')
          
    return render_template('user/new.html', form=form, user=UserModel())
  
@user_routes.route("/<int:id>/delete", methods=["POST"])
def user_delete(id):
    user = db.get_or_404(UserModel, id)

    if request.method == "POST":
        try:
          db.session.delete(user)
          db.session.commit()
        except:
            flash("An error occurred.", 'error')

    return redirect("/user")