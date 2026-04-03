# auto_blogger.py
import os
import time
import requests
from openai import OpenAI

# المفاتيح
BLOG_ID = os.getenv("BLOG_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

articles_per_day = 10
time_between_articles = 3600  # ساعة فاصل بين كل مقال

def generate_article():
    prompt = "Write a 3000-word trending news article in English with SEO-friendly titles and subtitles."
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role":"user","content":prompt}]
    )
    return response.choices[0].message.content

def get_image():
    url = f"https://api.pexels.com/v1/search?query=news&per_page=1"
    headers = {"Authorization": PEXELS_API_KEY}
    r = requests.get(url, headers=headers).json()
    return r['photos'][0]['src']['original']

def publish_article(title, content, image_url):
    post_url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    data = {"title": title, "content": f"<img src='{image_url}'/><p>{content}</p>"}
    requests.post(post_url, json=data, headers=headers)

for i in range(articles_per_day):
    content = generate_article()
    image_url = get_image()
    title = f"Trending Article {i+1}"
    publish_article(title, content, image_url)
    time.sleep(time_between_articles)
