from apps.app import db
from apps.auth.forms import SignUpForm,LoginForm
from apps.crud.models import User
from flask import Blueprint,render_template,flash,url_for,redirect,request
from flask_login import login_user,logout_user

auth = Blueprint( #blueprintの設定
    "auth",
    __name__, #このファイルのディレクトリ(flaskbook\auth)
    template_folder="templates", #使用するフォルダ
    static_folder="static", #使用するフォルダ
)

@auth.route("/") #/authがデフォルトパス
def index():
    return render_template("auth/index.html")

@auth.route("/signup",methods=["GET","POST"])
def signup():
    form = SignUpForm() #SignUpFormのインスタンス化
    if form.validate_on_submit(): #2回目ここ。サブミット時、データの内容が正しいか
        user = User( #入力内容の取り出し
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        if user.is_duplicate_email(): #メールアドレスの重複チェック
            flash("指定のメールアドレスは登録済みです。")
            return redirect(url_for("auth.signup")) #重複時はサインアップ画面に戻る
        db.session.add(user)
        db.session.commit() #DBへ登録
        login_user(user) #登録内容をセッションに保存
        next_ = request.args.get("next")
        if next_ is None or not next_.startswith("/"):
            next_ = url_for("crud.users")
        return redirect(next_)
    return render_template("auth/signup.html",form=form) #1回目はここ

@auth.route("/login",methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):#userにデータがあり、パスワードに不具合なし
            login_user(user) #ログイン処理（セッションにユーザーデータ保存)
            return redirect(url_for("crud.users"))#正しく処理できた場合
        flash("メールアドレスかパスワードが不正です")
    return render_template("auth/login.html",form=form)#1回目およびエラー時の遷移先

@auth.route("/logout")
def logout():
    logout_user() #ログアウトする（セッション情報の削除）
    return redirect(url_for("auth.login"))