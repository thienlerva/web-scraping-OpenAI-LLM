Using OpenAI to summarize websites.

import os
from dotenv import load_dotenv
from scraper import fetch_website_contents
from IPython.display import Markdown, display
from openai import OpenAI

# Load environment variables in a file called .env

load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

# Check the key

if not api_key:
    print("No API key was found - please head over to the troubleshooting notebook in this folder to identify & fix!")
elif not api_key.startswith("sk-proj-"):
    print("An API key was found, but it doesn't start sk-proj-; please check you're using the right key - see troubleshooting notebook")
elif api_key.strip() != api_key:
    print("An API key was found, but it looks like it might have space or tab characters at the start or end - please remove them - see troubleshooting notebook")
else:
    print("API key found and looks good so far!")


# Let's make a request to the OpenAI API

message = "Hello, GPT! This is my first ever message to you! Hi!"

messages = [{"role": "user", "content": message}]

messages

openai = OpenAI()

response = openai.chat.completions.create(
    model="gpt-5-nano", messages=messages
)
response.choices[0].message.content


# Let's read in the contents of the website

website_contents = fetch_website_contents("https://edwarddonner.com")

# Let's print the first 1000 characters of the website contents

print(website_contents)


# Define our system prompt

system_prompt = """
You are a snarky assistant that analyzes the contents of a website,
and provides a short, snarky, humorous summary, ignoring text that might be navigation related.
Respond in markdown. Do not wrap the markdown in a code block - respond just with the markdown.
"""

# Define our user prompt

user_prompt_prefix = """
Here is the website contents.
Provide a short summary of the this website.
If it includes news or announcements, provide a list of the key items.

"""


# The API from OpenAi expects to receive messages in this particular format.

[{"role": "system", "content": system_prompt},
 {"role": "user", "content": user_prompt_prefix + website_contents}]


 messages = [{"role": "system", "content": "You are a helpful assistant"},
 {"role": "user", "content": "What is the capital of France?"}]


# Let's call the API

response = openai.chat.completions.create(model="gpt-4.1-nano", messages=messages)

# Let's print the response

response.choices[0].message.content


# Function creates the format above

def message_for(website):
    return [{"role": "system", "content": system_prompt},
 {"role": "user", "content": user_prompt_prefix + website}]

message_for(website_contents)


# Bring it together

def summarize_website(url):
    website = fetch_website_contents(url)
    response = openai.chat.completions.create(
        model="gpt-4.1-mini",
        messages=message_for(website)
    )
    return response.choices[0].message.content

summarize_website("https://edwarddonner.com")


# A function to display this nicely in the output, using Markdown

def display_summary(url):
    summary = summarize_website(url)
    display(Markdown(summary))

# Let's try it out
display_summary("https://edwarddonner.com")




# Excercise: try it out on a different website, and see if you can get it to work.

system_prompt = """
You are a greate assistant that can summarize a website.

"""

user_prompt_prefix = """
Here is the website contents.
Provide a summary of the stock market news.
If it includes news or announcements, provide a list of the key items.

"""

def message_for(website):
    return [{"role": "system", "content": system_prompt},
 {"role": "user", "content": user_prompt_prefix + website}]

message_for(website_contents)

def summarize_stock_market_news(url):
    website = fetch_website_contents(url)
    response = openai.chat.completions.create(
        model="gpt-4.1-mini",
        messages=message_for(website)
    )
    return response.choices[0].message.content


def display_summary(url):
    summary = summarize_stock_market_news(url)
    display(Markdown(summary))

# Let's try it out
display_summary("https://www.cnbc.com")

