import re 
import pandas as pd
def prepos(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s(?:AM|PM)\s-\s'
    messages = re.split(pattern,data)[1:]
    dates = re.findall(pattern,data)

    df =pd.DataFrame({'user_message':messages,'dates':dates})

    df['dates']=pd.to_datetime(df['dates'],format='%m/%d/%y, %I:%M %p - ') 


    users=[]
    message=[]
    for i in df['user_message']:
         x=re.split('([\w\W]+?):\s',i)
         if x[1:]:
            users.append(x[1])
            message.append(x[2])
         else:
            users.append('group_notification')
            message.append(x[0])




    df['users']=users
    df['message']=message
    df.drop(columns=['user_message'],inplace=True)

    df['only_date']=df['dates'].dt.date
    df['year'] = df['dates'].dt.year
    df['month_num'] = df['dates'].dt.month
    df['month']  = df['dates'].dt.month_name()
    df['day ']= df['dates'].dt.day
    df['day_name']= df['dates'].dt.day_name()
    df['hour'] = df['dates'].dt.hour
    df['minute'] = df['dates'].dt.minute


    period=[]
    for hour in df[['day_name','hour']]['hour']:
        if hour == 23 :
            period.append(str(hour)+ '-' + str('00'))
        elif  hour == 0 :
              period.append(str('00')+ '-' + str(hour+1))
        else:
            period.append(str(hour)+ '-' + str(hour+1))      

    df['period']=period
    return df         