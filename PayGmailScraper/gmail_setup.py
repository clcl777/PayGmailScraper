import os
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def gmail_setup(credentials_path: str, token_path: str):
    """Gmail APIを設定し、サービスオブジェクトを返します。"""
    creds = None
    # トークンファイルが存在する場合、そこから資格情報を読み込みます。
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    # 資格情報がない、または無効な場合は再認証します。
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print("トークンのリフレッシュに失敗しました。トークンファイルを削除して再認証します。")
                print(f"Error: {e}")
                # 無効なトークンファイルを削除
                os.remove(token_path)
                # 再帰的に関数を呼び出して再認証
                return gmail_setup(credentials_path, token_path)
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
            # 次回の実行のためにトークンを保存
            with open(token_path, "w") as token:
                token.write(creds.to_json())
    try:
        # Gmail APIを呼び出す
        service = build("gmail", "v1", credentials=creds)
        return service
    except HttpError as e:
        print(f"An error occurred: {e}")
        raise
