import matplotlib.pyplot as plt
import pandas as pd
from urlextract import URLExtract
from collections import Counter
extract=URLExtract()
import emoji
def fetch_stats(selected_user,df):


    if selected_user != "overall":

        df=df[df['users']==selected_user]

    num_messages=df.shape[0]

    words=[]
    for i in df['message']:
         words.extend(i.split())


    num_madia_shered = df[df['message']=='<Media omitted>\n'].shape[0]

    links=[]
    for message in df["message"]:
        links.extend(extract.find_urls(message))     



    return num_messages,len(words),num_madia_shered,len(links)


def most_busy_users(df):
    x=df["users"].value_counts().head()
    df= round((df['users'].value_counts()/ df.shape[0])*100,2).reset_index().rename(
           columns = {'index':'name','users':'percent'})
    return x 
def monthly_timeline(selected_user,df):
    if selected_user!='overall':
        df=df[df['users']==selected_user]

    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time =[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))

    timeline['time'] = time    

    return timeline 
def daily_timeline(selected_user,df):
    if selected_user!='overall':
       df=df[df['users']==selected_user]
    daily_timeline=df.groupby('only_date').count()['message'].reset_index() 

    return daily_timeline

def weak_activity_map(selected_user,df):
  if selected_user!='overall':
     df=df[df['users']==selected_user]
  return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
     if selected_user!='overall':
        df=df[df['users']==selected_user]

     return df['month'].value_counts()


def activity_heatmap(selected_user,df):
      if selected_user!='overall':
        df=df[df['users']==selected_user]
      user_heatmap=df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)    

      return user_heatmap





def emoji_helper(selected_user, df):
    if selected_user != 'overall':
        df = df[df['users'] == selected_user]
    
    emojis = []
    
    # Loop through each message and check for emojis
    for message in df["message"]:
        emojis.extend([char for char in message if char in emoji.EMOJI_DATA])

    # Create a DataFrame to count the emojis
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    emoji_df.columns = ['Emoji', 'Count']
    
    return emoji_df