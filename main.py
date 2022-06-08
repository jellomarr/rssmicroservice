from bs4 import BeautifulSoup
import requests
from requests_aws4auth import AWS4Auth
import boto3


#Accessing IAM user for local testing REF:https://stackoverflow.com/questions/60293311/how-to-send-a-graphql-query-to-appsync-from-python, probs change this for whichever auth is used
session = requests.Session()
credentials = boto3.session.Session().get_credentials()
session.auth = AWS4Auth(
    credentials.access_key,
    credentials.secret_key,
    boto3.session.Session().region_name,
    'appsync',
    session_token=credentials.token
)

#get the news data
SearchTerm = "Azure"

#the RSS link feed 
RSSLink = 'https://www.itnews.com.au/RSS/rss.ashx?type=Category&ID=977'

url = requests.get(RSSLink)

soup = BeautifulSoup(url.content, "xml")

items = soup.find_all('item')

# As found in AWS Appsync under Settings for your endpoint.
APPSYNC_API_ENDPOINT_URL = '' #API endpoint change this ting

for item in items:
  title = item.title.text
  description = item.description.text
  link = item.link.text
  pubDate = item.pubDate.text
  if SearchTerm in title:
    print(f"Title: {title}\n\nDescription: {description}\n\nLink: {link}\n\npubDate: {pubDate}\n\n----------\n\n")
    #make this a module
    query = f"""
        mutation MyMutation {{
           createNews (input: {{title: "{title}", description: "{description}", link: "{link}", pubDate: "{pubDate}"}}) {{
              description 
              link 
              pubDate 
              title
            }}
        }}"""
    print(query)

    # Now we can simply post the request for the mutation to the API...
    response = session.request(
    url=APPSYNC_API_ENDPOINT_URL,
    headers={'x-api-key': ''},
    method='POST',
    json={'query': query})
    print(response.json())
