from flaskblog import app,db,bcrypt
from flask import render_template,url_for, flash, redirect, request,abort
from flaskblog.forms import AccountForm, RegistrationForm,LoginForm,PostForm
from flaskblog.models import Post,User
from flask_login import login_user, current_user, logout_user,login_required



@app.route('/')
def indexpage():
    page = request.args.get('page',1, type=int)  # get integer after page argument
    # posts = Post.query.all()  # grab all of those posts from database.
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=5) # 5 posts for per page, reversed because we want see newer post top of our site.
    return render_template('index.html', posts=posts)



@app.route('/register',methods=["post","get"])
def registerpage():
    if current_user.is_authenticated:
        return redirect(url_for('indexpage'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Hesabınız başarıyla oluşturuldu. ', 'success')
        return redirect(url_for('loginpage'))
    return render_template('register.html', title='Kayıt ol', form=form)


@app.route('/login',methods=["post","get"])
def loginpage():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('indexpage'))
        else:
            flash('E-Posta veya şifre yanlış.', 'danger')
    return render_template('login.html', title='Giriş yap', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('indexpage'))



@app.route('/post/new',methods=["post","get"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Yazı ekleme işlemi başarılı.","success")
        return redirect(url_for('indexpage'))
    return render_template('new_post.html', title="Yazı ekle", form=form, h3="Yeni yazı ekle")


# Flask gives us the ability to add variables within our actual routes so
# If we want to create a route where the id of a post is actually part of we can create.
@app.route('/post/<int:post_id>', methods=["POST", "GET"])
def post(post_id):
    # fetch this posts if it exists.
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)



@app.route("/post/<int:post_id>/update",methods=["POST","GET"])
@login_required
def update_post(post_id):
    #fetch these posts if exists else 404
    post = Post.query.get_or_404(post_id)

    # if we want to make sure
    if post.author != current_user:
        return abort(403)
    else:
        form = PostForm()
        if form.validate_on_submit():

            post.title = form.title.data
            post.content = form.content.data
            db.session.commit()
            flash("Yazınız başarılı bir şekilde güncellendi.","success")
            redirect(url_for("post",post_id=post.id))
        elif request.method == "GET":
            form.title.data = post.title #submit edilmediyse form değişkenini dbdeki degiskene esle.
            form.content.data = post.content
        return render_template('new_post.html', title="Yazı güncelle", form=form,
                               h3="Yazı güncelle")
    


@app.route('/post/<int:post_id>/delete', methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id) # get post by id
    if post.author != current_user:
        abort(403)   # return error

    db.session.delete(post)
    db.session.commit()
    flash("Yazınız başarılı bir şekilde silindi.","success")
    return redirect(url_for('indexpage'))



@app.route('/account',methods=["post","get"])
@login_required
def account():
    form = AccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Profil bilgileriniz güncellendi!', 'success')
        return redirect(url_for('account'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template("account.html", title="Profil", form=form)


@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page',1, type=int)  # get integer after page argument
    user = User.query.filter_by(username=username).first_or_404()
    # posts = Post.query.all()  # grab all of those posts from database.
    # get by user
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page,per_page=5) # 5 posts for per page, reversed because we want see newer post top of our site.
    return render_template('user.html', posts=posts, user=user)