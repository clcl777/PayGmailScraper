from PayGmailScraper import PayGmailScraper

client = PayGmailScraper("desktop", "credentials.json")
ana_pay_list = client.get_payments_ana_pay()
print(ana_pay_list)
# rakuten_pay_list = client.get_payments_rakuten_pay()
# print(rakuten_pay_list)
