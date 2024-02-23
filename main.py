import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything" #article discovery

#STOCK_API_KEY = "GO TO THE STOCK NEWS ENDPOINT AND GET YOUR OWN API"
# NEWS_API_KEY = "GO TO THE NEWS API ENDPOINT AND GET YOUR OWN API"
# TWILIO_SID = "LOG IN TO TWILIO AND GET YOUR SID"
# TWILIO_AUTH_TKEN = "LOG IN TO TWILIO AND GET YOUR AUTH TOKEN"

#Getting yesterday's closing stock price.

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}
response = requests.get(STOCK_ENDPOINT, params=stock_params)
stock_data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in stock_data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]
print(yesterday_closing_price)

#Getting the day before yesterday's closing stock price
day_before_yesterday = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday["4. close"]
print(day_before_yesterday_closing_price)


#Printing out the positive difference between yesterdays closing price and the day before it closing price.
#used abs to get absolute number

difference = (float(yesterday_closing_price)- float(day_before_yesterday_closing_price))
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

#Printing out the percentage difference between yesterday closing price and day before yesterday closing price
diff_percent = round(difference / float(yesterday_closing_price)) * 100
print(diff_percent)

#using the News API to get articles related to the COMPANY_NAME.

if abs(diff_percent) > 0:
    news_params = {
        "apikey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]
    print(articles)

#gives me the first three articles that discuss about the company name. Used slice operator
    three_articles = articles[:3]
    print(three_articles)

#Using list comprehension to create a list of the first three articles with the company name
    formatted_articles = [f"{STOCK_NAME}: {up_down} {diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
    print(formatted_articles)
#Sent each article as a separate message via Twilio.

    client = Client(TWILIO_SID, TWILIO_AUTH_TKEN)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            # from_ = "Your Twilio Phone number",
            # to= "Your actual Phone Number"

        )
