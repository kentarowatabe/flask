from flask import Blueprint,render_template,redirect,url_for
from apps.app import db
from apps.crud.models import User
from apps.crud.forms import UserForm
from flask_login import login_required

crud = Blueprint(
    "crud",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@crud.route("/")
@login_required
def index():
    return render_template("crud/index.html")

@crud.route("/sql")
@login_required
def sql():
    db.session.query(User).all()
    return "コンソールログを確認してください。"

@crud.route("/users/new",methods=["GET","POST"])
@login_required
def create_user():
    form = UserForm() #フォームクラスのインスタンス化
    if form.validate_on_submit(): #サブミットされた時にバリデーション実行。エラーがない場合
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        ) #フォームに入力されたユーザー名、メールアドレス、パスワードの取り出し
        db.session.add(user) #DBへ追加(SQLとしてはINSERT文)
        db.session.commit() #DB更新確定
        return redirect(url_for("crud.users")) #users関数の呼び出し
    return render_template("crud/create.html",form=form) #サブミットされていない時→create.html表示

@crud.route("/users")
@login_required
def users():
    users = User.query.all() #DBから全件取り出して変数users
    return render_template("crud/index.html",users=users) #usersを渡してindex.html表示

@crud.route("/users/<user_id>",methods=["GET","POST"]) #<user_id>は選択したレコードのid
@login_required
def edit_user(user_id):
    form = UserForm() #フォームのインスタンス化

    user = User.query.filter_by(id=user_id).first() #DBからuser_idに一致するレコードの取り出し

    if form.validate_on_submit(): #サブミットされた時、フォームに入力されているデータでuserを変更してDBを更新
        user.username=form.username.data
        user.email = form.email.data
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("crud.users"))
    return render_template("crud/edit.html",user=user,form=form) #サブミットされていない時、userとフォームを渡してedit.html表示

@crud.route("/users/<user_id>/delete",methods=["POST"]) #<user_id>は選択したレコードのid
@login_required
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first() #DBからuser_idに一致するレコードの取り出し
    db.session.delete(user) #削除
    db.session.commit()
    return redirect(url_for("crud.users")) #users関数呼び出し
