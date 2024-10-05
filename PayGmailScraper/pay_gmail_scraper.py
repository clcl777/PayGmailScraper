import os.path

from .gmail_setup import gmail_setup
from .payment.ana_pay import AnaPayParseGmail
from .payment.rakuten_pay import RakutenPayParseGmail
from .payment_information import PaymentInformation


class PayGmailScraper:
    def __init__(self, credentials_path: str, token_path: str | None = None) -> None:
        if not token_path:
            token_path = os.path.join(os.path.dirname(credentials_path), "token.json")
        self.service = gmail_setup(credentials_path, token_path)
        print("Gmail API setup complete.")

    def get_payments_ana_pay(self) -> list[PaymentInformation]:
        ana_pay_gmail_scraper = AnaPayParseGmail(self.service)
        return ana_pay_gmail_scraper.get_all_payment_info()

    def get_payments_rakuten_pay(self) -> list[PaymentInformation]:
        rakuten_pay_gmail_scraper = RakutenPayParseGmail(self.service)
        return rakuten_pay_gmail_scraper.get_all_payment_info()
