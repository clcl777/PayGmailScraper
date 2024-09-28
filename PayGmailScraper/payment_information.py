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
