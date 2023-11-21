
# importing of Packages which are Installed in the Local Machine
import tweepy as tw
import streamlit as st
import pandas as pd 
from transformers import pipeline

# creating a connection between our app and Twitter
access_token = 'NTFDWTJZXy1vbjUzdU8xbjJaSnY6MTpjaQ'
access_token_secret = 'yJkCnN1nyBcP6M09daxiVFr_cRDWkeAisQLnI3qQmcP0pv8eyf'
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

classifier = pipeline('sentiment-analysis') # Defining Instance of Sentiment Analysis

# Naming the Web App
st.title('Sentiment 2.0')
st.markdown('This app uses tweepy to get tweets from twitter based on the input name/phrase. '
            'It then processes the tweets through HuggingFace transformers pipeline function for sentiment analysis.'
            'The resulting sentiments and corresponding tweets are ,'
            ' then put in a dataframe for display which is what you see as result.')


# MAIN
def run():
    # Create a form in Streamlit
    with st.form(key='Enter name'):
        # Input field for the user to enter the name or hashtag for sentiment analysis
        search_input = st.text_input('Enter the product name or hashtag for which you want to know the sentiment')

        # Input field for the user to enter the number of latest tweets to analyze (with a range between 0 and 50, defaulting to 10)
        number_of_tweets = st.number_input('Enter the number of latest tweets for which you want to know the sentiment (Maximum 50 tweets)', 0, 50, 10)

        # Submit button to trigger the form submission
        submit_button = st.form_submit_button(label='Submit')

        # Check if the form has been submitted
        if submit_button:
            # Modify the search query based on whether the input contains the '#' symbol
            if '#' in search_input:
                search_query = search_input  # Use the input as it is if it contains '#'
            else:
                search_query = f"#{search_input}"  # Add '#' symbol for product names

            # Use Tweepy to fetch tweets based on the modified search query
            tweets = tw.Cursor(api.search_tweets, q=search_query, lang="en").items(number_of_tweets)

            # Extract text from fetched tweets
            tweet_list = [i.text for i in tweets]

            # Use the 'classifier' function to classify sentiments of the tweets
            p = [i for i in classifier(tweet_list)]

            # Extract sentiment labels from the classifier output
            q = [p[i]['label'] for i in range(len(p))]

            # Create a DataFrame to display the results
            df = pd.DataFrame(list(zip(tweet_list, q)), columns=['Latest ' + str(number_of_tweets) + ' Tweets' + ' on ' + search_input, 'sentiment'])

            # Display the DataFrame using Streamlit
            st.write(df)

# Run the Streamlit app if the script is executed directly
if __name__ == '__main__':
    run()
