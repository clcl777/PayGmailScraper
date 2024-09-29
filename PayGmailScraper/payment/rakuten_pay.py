import base64
import re

from dateutil import parser

from PayGmailScraper.pay_gmail_scraper_base import PayGmailScraperBase
from PayGmailScraper.payment_information import PaymentInformation


class RakutenPayGmailScraper(PayGmailScraperBase):
    def __init__(self):
        email_address = "no-reply@pay.rakuten.co.jp"
        email_title = "楽天ペイアプリご利用内容確認メール"
        super().__init__(email_address, email_title)
        self.payment_name = "楽天ペイ"

    def _parse_email(self, response: dict) -> PaymentInformation:
        payment_info = PaymentInformation()
        payment_info.payment_method = self.payment_name
        for header in response["payload"]["headers"]:
            if header["name"] == "Date":
                date_str = header["value"].replace(" +0900 (JST)", "")
                payment_info.email_date = parser.parse(date_str)
        data = response["payload"]["parts"][0]["body"]["data"]
        body = base64.urlsafe_b64decode(data).decode()
        for line in body.splitlines():
            if line.startswith("　　ご利用日時　　"):
                date_str = line.replace("　　ご利用日時　　", "")
                cleaned_date_str = re.sub(r"\(.*?\)", "", date_str)
                payment_info.payment_date = parser.parse(cleaned_date_str)
            elif line.startswith("　　ご利用店舗　　"):
                payment_info.store = line.replace("　　ご利用店舗　　", "")
            elif line.startswith("　　決済総額　　　"):
                payment_info.price = int(line.replace("　　決済総額　　　", "").replace("円", "").replace(",", ""))
        return payment_info


def get_payments_rakuten_pay() -> list[PaymentInformation]:
    rakuten_pay_gmail_scraper = RakutenPayGmailScraper()
    return rakuten_pay_gmail_scraper.get_all_payment_info()
