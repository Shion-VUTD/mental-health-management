#ライブラリのインポート
import tweepy
from datetime import datetime,timezone,timedelta
import pytz
import pandas as pd
import requests
import  pytz
import time

#関数:　UTCをJSTに変換する
def change_time_from_utc(u_time):
    #イギリスのtimezoneを設定するために再定義する
    utc_time = datetime(u_time.year, u_time.month,u_time.day, 
    u_time.hour,u_time.minute,u_time.second, tzinfo=timezone.utc)
    #タイムゾーンを日本時刻に変換
    jst_time = utc_time.astimezone(pytz.timezone("Asia/Tokyo"))
    # 文字列で返す
    str_time = jst_time.strftime("%Y-%m-%d_%H:%M:%S")
    return str_time

def change_time_to_utc(jst_time):
    tz_jst = timezone(timedelta(hours=9))
    #イギリスのtimezoneを設定するために再定義する
    jst_time = datetime(jst_time.year, jst_time.month,jst_time.day, 
    jst_time.hour,jst_time.minute,jst_time.second, tzinfo=tz_jst)
    #タイムゾーンを標準時に変換
    utc_time = jst_time.astimezone(timezone.utc)

    return utc_time

#Twitterの認証
api_key = ""
api_secret = ""
bearer_token = ""
access_key = ""
access_secret = ""
auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)      


client = tweepy.Client(
    bearer_token, api_key, api_secret, access_key, access_secret,
    return_type = requests.Response,
    wait_on_rate_limit=True)

end_isoform = change_time_to_utc(datetime.now()).isoformat()
start_isoform = change_time_to_utc(datetime(2020, 6, 22, 0, 0, 0)).isoformat()
iteration_num = 33
max_results = 100
cols = ['edit_history_tweet_ids', 'created_at','id','author_id', 'text']
df = pd.DataFrame(index=[], columns=cols)

for iter in range(iteration_num):

    # ツイートを取得してtweetsという変数に代入
    tweets = client.get_users_tweets(
        id = "1327954104153382917",
        tweet_fields=['author_id', 'created_at'],
        start_time=start_isoform,
        end_time=end_isoform,
        max_results=max_results)


    #抽出したデータから必要な情報を取り出す
    #取得したツイートを一つずつ取り出して必要な情報をtweet_dataに格納する

    # Save data as dictionary
    tweets_dict = tweets.json() 

    # Extract "data" value from dictionary
    tweets_data = tweets_dict['data'] 

    # Transform to pandas Dataframe
    df_block = pd.json_normalize(tweets_data) 
    sample_num = len(df_block)
    last_date_str = df_block.loc[sample_num-1, 'created_at']
    end = datetime.strptime(last_date_str, '%Y-%m-%dT%H:%M:%S.000Z') - timedelta(minutes=1)
    end_isoform = end.isoformat() + "Z"

    df = pd.concat([df, df_block])
    print(f'{iter}th iteration completed.')
    time.sleep(1)



df.to_csv("mental-health-management/past_tweets.csv")
print(df)

