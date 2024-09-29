import base64

from dateutil import parser

from PayGmailScraper.parse_gmail_base import ParseGmailBase
from PayGmailScraper.payment_information import PaymentInformation


class AnaPayParseGmail(ParseGmailBase):
    def __init__(self, service):
        email_address = "payinfo@121.ana.co.jp"
        email_title = "ご利用のお知らせ"
        super().__init__(email_address, email_title, service)
        self.payment_name = "ANA Pay"

    def _parse_email(self, response: dict) -> PaymentInformation:
        payment_info = PaymentInformation()
        payment_info.payment_method = self.payment_name
        for header in response["payload"]["headers"]:
            if header["name"] == "Date":
                date_str = header["value"].replace(" +0900 (JST)", "")
                payment_info.email_date = parser.parse(date_str)
        data = response["payload"]["body"]["data"]
        body = base64.urlsafe_b64decode(data).decode()
        for line in body.splitlines():
            if line.startswith("ご利用"):
                key, value = line.split("：")
                if key == "ご利用日時":
                    payment_info.payment_date = parser.parse(value)
                elif key == "ご利用金額":
                    payment_info.price = int(value.replace(",", "").replace("円", ""))
                elif key == "ご利用店舗":
                    payment_info.store = value
        return payment_info
