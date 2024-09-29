from abc import ABC, abstractmethod

from .payment_information import PaymentInformation


class ParseGmailBase(ABC):
    def __init__(self, email_address: str, email_title: str, service):
        self.query = f"from:{email_address} subject:{email_title}"
        self.service = service

    @abstractmethod
    def _parse_email(self, response: dict) -> PaymentInformation:
        pass

    def get_all_payment_info(self) -> list[PaymentInformation]:
        payment_info_list = []
        results = self.service.users().messages().list(userId="me", q=self.query).execute()
        messages = results.get("messages", [])
        for message in reversed(messages):
            response = self.service.users().messages().get(userId="me", id=message["id"]).execute()
            payment_info = self._parse_email(response)
            payment_info_list.append(payment_info)
        return payment_info_list
