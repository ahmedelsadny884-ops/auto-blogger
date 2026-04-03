import requests
import random
import os
import time

# =========================
# 🔑 CONFIG (GitHub Secrets)
# =========================
BLOG_ID = os.getenv("BLOG_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

# =========================
# 📰 اختيار الموضوع من كل المجالات
# =========================
def get_topic():
    categories = {
        "Global News": ["world events", "politics", "economy", "technology", "science"],
        "Sports": ["football", "basketball", "tennis", "Olympics", "cricket"],
        "Entertainment": ["movies", "celebrity news", "music", "viral trends"],
        "Trending": ["social media trends", "viral news", "internet challenges", "fashion trends"]
    }
    category = random.choice(list(categories.keys()))
    topic = random.choice(categories[category])
    return category, topic

# =========================
# ✍️ توليد المقال
# =========================
def generate_article(category, topic):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    prompt = f"""
    Write a professional 3000-word news article about "{topic}" in the {category} category.
    Requirements:
    - SEO-optimized catchy title
    - Headings and subheadings
    - Structured paragraphs
    - Include relevant images descriptions (AI-generated image suggestions)
    - Engaging introduction and conclusion
    - Written in fluent English
    """
    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    return result["choices"][0]["message"]["content"]

# =========================
# 🖼️ جلب صور ممتازة لكل مقال
# =========================
def get_images(count=5):
    url = f"https://api.pexels.com/v1/search?query=news&per_page={count}"
    headers = {"Authorization": PEXELS_API_KEY}
    response = requests.get(url, headers=headers)
    data = response.json()
    return [photo["src"]["large"] for photo in data["photos"]]

# =========================
# 🚀 نشر على بلوجر
# =========================
def publish(title, content, images):
    post_url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}

    # دمج الصور في المقال
    html_content = f"<h1>{title}</h1>\n"
    for img in images:
        html_content += f'<img src="{img}" style="width:100%; margin:20px 0;">\n'
    html_content += f"<div>{content}</div>"

    data = {"kind": "blogger#post", "title": title, "content": html_content}
    response = requests.post(post_url, headers=headers, json=data)
    return response.json()

# =========================
# 🧩 تشغيل السكريبت – 10 مقالات يوميًا مع ساعة فاصل بين كل مقال
# =========================
def main():
    for i in range(10):
        print(f"=== Article {i+1} / 10 ===")
        category, topic = get_topic()
        print("Category:", category)
        print("Topic:", topic)

        article = generate_article(category, topic)
        title = article.split("\n")[0]  # أول سطر كعنوان

        images = get_images(count=5)  # 5 صور لكل مقال
        result = publish(title, article, images)

        print("Published:", result)
        print("Waiting 1 hour before next article...\n")
        time.sleep(3600)  # ساعة انتظار بين المقالات

if __name__ == "__main__":
    main()
