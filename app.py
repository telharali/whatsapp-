import  streamlit as st
import matplotlib.pyplot as plt
import preprocess2,helper
import matplotlib.pyplot as plt
import seaborn as sns
import emoji 
st.sidebar.title("whatsapp")
uploaded=st.sidebar.file_uploader("choose a file")


if uploaded is not None:
    bytes_data  = uploaded.getvalue()
    data = bytes_data.decode('utf-8') 
    df = preprocess2.prepos(data)
    
    st.dataframe(df)


    # fetch unique users
    user_list=df['users'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"overall")


    selected_user=st.sidebar.selectbox('show analysis wrt',user_list)

    if st.sidebar.button("show analysis"):
        num_messages,words,num_madia_shered,num_links = helper.fetch_stats(selected_user,df)

# Top statistics Analysis
        st.title('Top Statistics')    

        col1,col2,col3,col4 = st.columns(4)


        with col1:
                st.header("Total Messages")
                st.title(num_messages) 
        with col2:
             st.header("Total words")
             st.title(words)        
        with col3:
              st.header("Shared madia")
              st.title(num_madia_shered) 
        with col4:
                st.header("Shared links")
                st.title(num_links)





   #chat time duration
        st.title('Chat Time Duration')
        m =len(df['month'].unique())
        y = m/12
        w = m*4
    
        col1,col2=st.columns(2)
        with col1:
          st.header('Weaks')
          st.title(w)
        with col2:
          st.header('Months')
          st.title(m)
                  


         # monthly timeline
               
        st.title('Monthly Timeline')
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax =plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        plt.show()
        st.pyplot(fig)

       # daily timeline 
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['message'],color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
 

      # activity map
        st.title('Activity Map')
        col1,col2 = st.columns(2)

        with col1:
             st.header('Most Busy Day')
             busy_day = helper.weak_activity_map(selected_user,df)
             fig,ax = plt.subplots()
             ax.bar(busy_day.index,busy_day.values)
             plt.xticks(rotation = "vertical")
             st.pyplot(fig)

        with col2:
                  
             st.header('Most Busy Month')
             busy_month = helper.month_activity_map(selected_user,df)
             fig,ax = plt.subplots()
             ax.bar(busy_month.index,busy_month.values, color='orange')
             plt.xticks(rotation = "vertical")
             st.pyplot(fig)

        st.title('Activity Heatmap')
        user_heatmap=helper.activity_heatmap(selected_user,df)
        fig,ax =plt.subplots()
        ax= sns.heatmap(user_heatmap)
        st.pyplot(fig)






      # finding the busiest users in the group (group level)  
        st.title("Most Busy Users")
        if selected_user=="overall":
           x,new_df  =   helper.most_busy_users(df)
           fig,ax =  plt.subplots()
          


              
           col1,col2=st.columns(2)


           with col1:
                ax.bar(x.index,x.values,color="red")
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
           with col2:
              st.dataframe(new_df)
          
      # emoji analysis 

        emoji_df = helper.emoji_helper(selected_user,df)
        st.title('Emoji Analysis' )
        col1,col2=st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            st.header('Total Emojis Shared')
            st.title(len(emoji_df))
