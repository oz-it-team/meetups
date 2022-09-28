import requests
import json
from rss_parser import Parser


def get_feed():
    url = 'https://habr.com/ru/rss/best/weekly/?fl=ru'
    response = requests.get(url).content
    feed = Parser(xml=response, limit=5)
    return feed.parse().feed


def do_rewrite(text):
    url = "https://api.aicloud.sbercloud.ru/public/v2/rewriter/predict"
    data = {
        "instances": [
            {
                "text": text,
                "temperature": 0.9,
                "top_k": 50,
                "top_p": 0.7,
                "range_mode": "bertscore"
            }
        ]
    }

    response = requests.post(
        url=url,
        data=json.dumps(data),
        headers={"Content-Type": "application/json"}
    ).json()

    return response['prediction_best']['bertscore']


def send_message(text):
    url = f'https://api.telegram.org/bot{CHANGE_IT}/sendMessage?chat_id={CHANGE_IT}&text={text}&parse_mode=markdown'
    requests.get(url)


def create_message(title, text, url):
    return f'*{title}* \n\n {text} \n [Читать статью]({url})'


if __name__ == '__main__':
    for item in get_feed():
        send_message(
            create_message(
                title=item.title,
                text=do_rewrite(item.description),
                url=item.link
            )
        )
