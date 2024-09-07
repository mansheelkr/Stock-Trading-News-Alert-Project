from twilio.rest import Client
import requests
from datetime import datetime, timedelta

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
account_sid = 'ACa830d8521a19efa8f54c65511fe5312d'
auth_token = '26a9c60ab3777bd0a00056a1bef07b11'


## STEP 1: Use https://newsapi.org/docs/endpoints/everything
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stock_parameters = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK,
    'apikey': 'GP4H32E33EBE2DVB'
    }

stock_response = requests.get(url=STOCK_ENDPOINT, params=stock_parameters)
stock_response.raise_for_status()
stock_data = stock_response.json()

yesterday = datetime.now() - timedelta(days=1)
day_before_yesterday = datetime.now() - timedelta(days=2)

yesterday_closing_price = stock_data['Time Series (Daily)'][yesterday.strftime('%Y-%m-%d')]['4. close']
day_before_yesterday_closing_price = stock_data['Time Series (Daily)'][day_before_yesterday.strftime('%Y-%m-%d')]['4. close']

print(yesterday_closing_price)
print(day_before_yesterday_closing_price)

positive_difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None

if positive_difference > 0:
    up_down = '🔺'
else:
    up_down = '🔻'
    
print(positive_difference)

#HINT 2: Work out the value of 5% of yerstday's closing stock price. 
percentage_difference = round(positive_difference / float(yesterday_closing_price) * 100)
print(percentage_difference)


if abs(percentage_difference) > 3:
    
    ## STEP 2: Use https://newsapi.org/docs/endpoints/everything
    # Instead of printing ("Get News"), actually fetch the first 3 articles for the COMPANY_NAME. 
    news_parameters = {
        'q': COMPANY_NAME,
        'from': yesterday.strftime('%Y-%m-%d'),
        'sortBy': 'popularity',
        'apiKey': '34ce822008e24759b1939abe7daf4011'
        }
    
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_parameters)
    news_response.raise_for_status()
    news_data = news_response.json()
    news_data = news_data['articles']
    news_data = news_data[:3]
    
    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    # Send a separate message with each article's title and description to your phone number. 
    formatted_articles = [f'{STOCK}: {up_down}{abs(percentage_difference)}% \nHeadline: {article["title"]} \nBrief: {article["description"]}' for article in news_data]
    
    client = Client(account_sid, auth_token)

    for article in formatted_articles:
        message = client.messages.create(
          from_='whatsapp:+14155238886',
          body=article,
          to='whatsapp:+13478259718'
        )

    print(message.status)

#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

