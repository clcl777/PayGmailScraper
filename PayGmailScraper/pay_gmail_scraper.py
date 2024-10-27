from .gmail_setup import gmail_setup
from .payment.ana_pay import AnaPayParseGmail
from .payment.rakuten_pay import RakutenPayParseGmail
from .payment_information import PaymentInformation


class PayGmailScraper:

    def __init__(self, auth_type: str = "desktop", credentials_path: str | None = None, token_path: str = "token.json"):
        """
        PayGmailScraperを初期化します。

        :param auth_type: 'desktop' または 'web' を指定。
        :param client_secrets: デスクトップアプリの場合はclient_secrets.jsonのパス、Webアプリの場合は不要。
        :param token_path: デスクトップアプリの場合のトークンファイルのパス。
        """
        if auth_type == "desktop" and not credentials_path:
            raise ValueError("デスクトップアプリの場合、client_secrets のパスを指定してください。")

        self.service = gmail_setup(credentials_path, auth_type=auth_type, token_path=token_path)
        if not self.service:
            raise Exception("Gmail APIのセットアップに失敗しました。")
        print("Gmail API setup complete.")

    def get_payments_ana_pay(self) -> list[PaymentInformation]:
        ana_pay_gmail_scraper = AnaPayParseGmail(self.service)
        return ana_pay_gmail_scraper.get_all_payment_info()

    def get_payments_rakuten_pay(self) -> list[PaymentInformation]:
        rakuten_pay_gmail_scraper = RakutenPayParseGmail(self.service)
        return rakuten_pay_gmail_scraper.get_all_payment_info()
