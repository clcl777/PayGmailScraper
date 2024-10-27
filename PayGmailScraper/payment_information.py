from dataclasses import dataclass
from datetime import datetime


@dataclass
class PaymentInformation:
    """支払い情報"""

    email_date: datetime | None = None
    payment_date: datetime | None = None
    price: int | None = None
    store: str | None = None
    payment_method: str | None = None

    def values(self) -> tuple[datetime | None, datetime | None, int | None, str | None]:
        return self.email_date, self.payment_date, self.price, self.store

    def to_dict(self) -> dict:
        return {
            "email_date": self.email_date.isoformat() if self.email_date else None,
            "payment_date": self.payment_date.isoformat() if self.payment_date else None,
            "price": self.price,
            "store": self.store,
            "payment_method": self.payment_method,
        }
