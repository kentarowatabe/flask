from email_validator import validate_email,EmailNotValidError
from flask import (
    Flask,
    render_template,
    url_for,
    current_app,
    g,
    request,
    redirect,
    flash
)
import logging
from flask_debugtoolbar import DebugToolbarExtension
import os
from flask_mail import Mail,Message
app = Flask(__name__)
app.config["SECRET_KEY"] = "2AZSMss3p5QPbvY2hBsJ"
app.logger.setLevel(logging.DEBUG)
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
toolbar = DebugToolbarExtension(app)

#環境変数の取得
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")#使用するメールサーバ★
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")#使用するポート番号★
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")#暗号化通信の利用有無★
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")#送信元メールアドレス★
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")#メールアカウントのパスワード★
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")#表示用の送信元情報

mail = Mail(app)

@app.route("/")
def index():
    return "Hello,Flaskbook!"

@app.route("/hello/<name>",methods=["GET","POST"],endpoint="hello-endpoint")
def hello(name):
    return f"Hello,{name}!"

@app.route("/name/<name>")
def show_name(name):
    return render_template("index.html",name=name)

with app.test_request_context():
    print(url_for("index"))
    print(url_for("hello-endpoint",name="world"))
    print(url_for("show_name",name="ichiro",page="1"))

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/contact/complete",methods=["GET","POST"])
def contact_complete():
    if request.method == "POST": #POST通信なら
        username = request.form["username"] #POSTデータからusername取り出し
        email = request.form["email"] #POSTデータからemail取り出し
        description = request.form["description"] #POSTデータからdescription取り出し

        is_valid = True

        if not username: #usernameが空の場合
            flash("ユーザ名は必須です") #flashにメッセージ蓄積
            is_valid = False
        
        if not email: #emailが空の場合
            flash("メールアドレスは必須です") #flashにメッセージ蓄積
            is_valid = False
        
        try:
            validate_email(email) #email_validetorによるメールアドレスの形式チェック
        except EmailNotValidError: #例外が発生した場合（＝メールアドレスの形式ではない場合）
            flash("メールアドレスの形式で入力してください") #flashにメッセージ蓄積
            is_valid = False
        
        if not description: #descriptionが空の場合
            flash("問い合わせ内容は必須です")#flashにメッセージ蓄積
            is_valid = False
        
        if not is_valid:#is_validがTrueでない（Falseの）場合
            return redirect(url_for("contact")) #問い合わせフォームへリダイレクト
        
        send_email( #関数send_emailの呼び出し。カッコ内は関数に渡す引数
            email,
            "問い合わせありがとうございました。",
            "contact_mail",
            username=username,
            description=description,
        )
        #is_validがTrueの場合
        flash("問い合わせ内容はメールにて送信しました")
        return redirect(url_for("contact_complete"))
    
    return render_template("contact_complete.html")

def send_email(to,subject,template,**kwargs):
    msg=Message(subject,recipients=[to])#件名、受信者の設定

    #contact_mail.txt,username,descriptionを渡す(インストールアプリ対応)
    msg.body=render_template(template + ".txt",**kwargs)

    #contact_mail.heml,username,descriptionを渡す(Webアプリ対応)
    msg.html=render_template(template+".html",**kwargs)

    mail.send(msg)#メールの送信