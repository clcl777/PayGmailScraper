# PayGmailScraper

## 概要
PayGmailScraperは、PayGmailのメールをスクレイピングして、支払い情報を取得するためのデスクトップアプリケーションです。  
現在、以下の支払い方法に対応しています。
- ANA Pay
- 楽天ペイ

## インストール
```
pip install -r pay-gmail-scraper
```

## 使い方
```Python
from PayGmailScraper import PayGmailScraper

client = PayGmailScraper("credentials.json")
ana_pay_list = client.get_payments_ana_pay()
print(ana_pay_list)
rakuten_pay_list = client.get_payments_rakuten_pay()
print(rakuten_pay_list)
```

## Requirements
```
google-api-python-client>=2.111.0,
google-auth>=2.29.0,
google-auth-oauthlib>=1.2.0,
```
Gmail APIを使用するために、認証情報のcredentials.jsonが必要