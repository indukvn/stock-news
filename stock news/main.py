import requests
# for sms
# from twilio.rest import Client

# for mail
import smtplib

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

#use your api keys to get it working
STOCK_API_KEY = "your stock api"
NEWS_API = "your news api"

#for sending sms
# ACC_SID = "AC4a4fd3dd230577de25d0e330afb2ed3f"
# AUTH_TOKEN = "7ae8e89c63b6aad362d284a3b8dd8931"

# for mail
email = "your@gmail.com"
password = "your app password"

params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

response = requests.get(STOCK_ENDPOINT, params=params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

dat_before_yesterday_data = data_list[1]
dat_before_yesterday_closing_price = dat_before_yesterday_data["4. close"]
print(dat_before_yesterday_closing_price)

difference = float(yesterday_closing_price) - float(dat_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

diff_percent = round((difference / float(yesterday_closing_price)) * 100)
print(diff_percent)

if abs(diff_percent) > 3:
    news_params = {
        "apiKey": NEWS_API,
        "q": COMPANY_NAME
    }
    response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = response.json()["articles"]

    three_articles = articles[:3]
    print(three_articles)

    formatted_articles = [f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. " \
                          f"\nBrief: {article['description']}" for article in three_articles]

#for sms
    # client = Client(ACC_SID, AUTH_TOKEN)
    # for article in formatted_articles:
    #     message = client.messages.create(
    #         body=article,
    #         from_="+16184266505",
    #         to="+918919822678"
    #     )

#for mail
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(email, password)
    for article in formatted_articles:
        connection.sendmail(
            from_addr=email,
            to_addrs="receiver mail id",
            msg=article
        )
