from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from chatgpt_wrapper import ChatGPT
import googleapiclient.discovery
import urllib.parse
import re
import json

app = Flask(__name__)
api = Api(app)

def search_youtube(chatgpt_query):

    # Replace with your own API key
    api_key = ''

    # Create a YouTube API client
    youtube = googleapiclient.discovery.build(
        'youtube', 'v3', developerKey=api_key)

    # Define the search query
    query = chatgpt_query

    # Encode the query to URL format
    query = urllib.parse.quote_plus(query)

    # Search for the video
    search_responses = youtube.search().list(
        q=query,
        type='video',
        part='id,snippet',
        maxResults=8
    ).execute()

    results = []

    for video in search_responses['items']:
        video_title = video['snippet']['title']
        video_id = video['id']['videoId']
        result = (video_title, video_id)
        results.append(result)

    return results

# This is the class that will get a request with a topic, and return ChatGPT's response
class ChatGPTAPI(Resource):
    def post(self):
        chatGPT = ChatGPT()
        responses = {}

        topic = request.args['topic']
        # Format request 
        query = "Create a numbered list of subtopics (with no other informtion) required to understand " + topic

        # Get the response from ChatGPT
        response = chatGPT.ask(query)
        topics = response.split('\n')
        for searchPrompt in topics:
            if searchPrompt.strip() == "" or searchPrompt[0].isdigit() == False:
                topics.remove(searchPrompt)

        topics = [topic for topic in topics if topic.strip() != "" and topic[0].isdigit() == True]


        print(topics)

        topics = [topic.split('.')[1].strip() for topic in topics]
        responses['subtopics'] = topics

        chatGPT.page.close()

        subtopics_dict = {}
        
        # create a list of youtube search prompts by combining the subtopics with the topic
        searchPrompts = []
        for i, subtopic in enumerate(topics):
            searchPrompts.append(subtopic + " " + topic)

        print(searchPrompts)


        # Split the input string into lines
        # lines = searchPrompts.split('\n')

        # Loop through the lines and extract the subtopic and search term for each one
        for i, searchPrompt in enumerate(searchPrompts):
            videos = []

            print(searchPrompt)

            videos.append(search_youtube(searchPrompt))

            print(videos)

            subtopics_dict[topics[i]] = videos

        responses['searchPrompts'] = subtopics_dict

        # Return the response
        return responses
    
api.add_resource(ChatGPTAPI, '/chatgptapi')

if __name__ == '__main__':
    app.run()  # run our Flask app
