import os
import os.path

from flask import json, redirect, request, session, url_for
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def gmail_setup(credentials_path: str | None, auth_type: str, token_path: str):
    """Gmail APIを設定し、サービスオブジェクトを返す"""
    if auth_type == "desktop":
        if not credentials_path:
            raise ValueError("デスクトップアプリの場合、credentials.jsonのパスを指定してください。")
        return gmail_setup_desktop(credentials_path, token_path)
    elif auth_type == "web":
        return gmail_setup_web(credentials_path)
    else:
        raise ValueError("auth_typeは 'desktop' または 'web' を指定してください。")


def gmail_setup_desktop(client_secrets_path: str, token_path: str):
    """デスクトップアプリ用のGmail APIセットアップ"""
    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                print("トークンのリフレッシュに失敗しました。無効なトークンファイルを削除します。")
                os.remove(token_path)
                return gmail_setup_desktop(client_secrets_path, token_path)
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, "w") as token:
            token.write(creds.to_json())
    try:
        service = build("gmail", "v1", credentials=creds)
        return service
    except HttpError as e:
        print(f"An error occurred: {e}")
        raise


def gmail_setup_web(credentials_path: str):
    """Webアプリ用のGmail APIセットアップ。"""
    global flow
    global credentials

    if "credentials" in session:
        credentials = Credentials(**session["credentials"])
    else:
        credentials = None

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            try:
                credentials.refresh(Request())
                session["credentials"] = credentials_to_dict(credentials)
            except Exception as e:
                print("トークンのリフレッシュに失敗しました。再認証を行います。")
                print(f"Error: {e}")
                return redirect("/authorize")
        else:
            return redirect("/authorize")

    try:
        service = build("gmail", "v1", credentials=credentials)
        return service
    except HttpError as e:
        print(f"An error occurred: {e}")
        raise


def authorize(credentials_path: str | None = None):
    """ユーザーをGoogleのOAuth 2.0認証ページにリダイレクトします。"""
    global flow
    # グローバルまたは設定から client_secrets_data を取得
    client_secrets_data = get_credentials_data(credentials_path)
    flow = Flow.from_client_config(
        client_secrets_data, scopes=SCOPES, redirect_uri=url_for("oauth2callback_route", _external=True)
    )
    authorization_url, state = flow.authorization_url(access_type="offline", include_granted_scopes="true")
    session["state"] = state
    return redirect(authorization_url)


def get_credentials_data(credentials_path: str | None):
    """クライアントシークレットデータを取得します。"""
    # 環境変数またはファイルから取得
    if credentials_path:
        with open(credentials_path, "r") as f:
            return json.load(f)

    credentials_json = os.environ.get("CREDENTIALS_JSON")
    if credentials_json:
        return json.loads(credentials_json)

    raise ValueError("CREDENTIALS_JSON 環境変数が設定されていません。")


def credentials_to_dict(credentials):
    """Credentialsオブジェクトを辞書に変換します。"""
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }


def oauth2callback():
    """OAuth 2.0のコールバックを処理し、資格情報をセッションに保存します。"""
    global flow
    global credentials
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    session["credentials"] = credentials_to_dict(credentials)
    return redirect("/")
