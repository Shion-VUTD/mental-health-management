# やばめなツイだけ取り出してGoogle Calendarに保存

import datetime
import googleapiclient.discovery
import google.auth
import pandas as pd
from datetime import datetime,timezone,timedelta
import requests
import  pytz



# ①Google APIの準備をする

SCOPES = ['https://www.googleapis.com/auth/calendar']
calendar_id = ''
# Googleの認証情報をファイルから読み込む
gapi_creds = google.auth.load_credentials_from_file('mental-health-manager-bb748e3043b7.json', SCOPES)[0]
# APIと対話するためのResourceオブジェクトを構築する
service = googleapiclient.discovery.build('calendar', 'v3', credentials=gapi_creds)

negative_words_list = [
    '不安','しにた','死', '動悸','眠れな','つらい','苦しい','恐怖','怖い','しんど','めんどくさい','つかれた','したくない','疲れ','悪い','体調不良','悲し','かなし','痛','いたい'
    ]


def change_time_from_utc(u_time):
    #イギリスのtimezoneを設定するために再定義する
    utc_time = datetime(u_time.year, u_time.month,u_time.day, 
    u_time.hour,u_time.minute,u_time.second, tzinfo=timezone.utc)
    #タイムゾーンを日本時刻に変換
    jst_time = utc_time.astimezone(pytz.timezone("Asia/Tokyo"))
    return jst_time


def insert_tweet_log(tweet_time_utc: str, tweet: str):
    """ツイートをGoogle Calendarに書き出す"""

    dte_utc = datetime.strptime(tweet_time_utc, '%Y-%m-%dT%H:%M:%S.000Z')
    dte_jst = change_time_from_utc(dte_utc)

    body = {
        # 予定のタイトル
        'summary': 'Needs to protect your mental health.',
        # 予定の開始時刻
        'start': {
            'dateTime': dte_jst.isoformat(),
            'timeZone': 'Japan'
        },
        # 予定の終了時刻
        'end': {
            'dateTime': (dte_jst + timedelta(minutes=1)).isoformat(),
            'timeZone': 'Japan'
        },
        'description': tweet,
        'colorId': '8'
    }
    event = service.events().insert(calendarId=calendar_id, body=body).execute()


df = pd.read_csv("past_tweets.csv")
df_length = len(df)

for i in range(df_length):
    tweet_time = df.loc[i, 'created_at']
    tweet = df.loc[i, 'text']
    for negative_word in negative_words_list:
        if negative_word in tweet:
            insert_tweet_log(tweet_time_utc=tweet_time, tweet=tweet)
            break