import os

from flask import Flask, jsonify, redirect

from PayGmailScraper import PayGmailScraper, authorize, oauth2callback

app = Flask(__name__)
app.secret_key = "your-secret-key"

# 開発環境で HTTPS を使用しない場合の設定
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# credentials_web.jsonのパスを指定　指定しない場合は環境変数から取得
CREDENTIALS_PATH = "credentials_web.json"


@app.route("/")
def index():
    try:
        client = PayGmailScraper("web")
        ana_pay_list = client.get_payments_ana_pay()
        print(ana_pay_list)
        ana_pay_list_dict = [payment.to_dict() for payment in ana_pay_list]
        # rakuten_pay_list = client.get_payments_rakuten_pay()
        # print(rakuten_pay_list)
        return jsonify(ana_pay_list_dict)
    except Exception as e:
        print(f"Error: {e}")
        return redirect("/authorize")


@app.route("/authorize")
def authorize_route():
    return authorize(CREDENTIALS_PATH)


@app.route("/oauth2callback")
def oauth2callback_route():
    return oauth2callback()


if __name__ == "__main__":
    app.run()
