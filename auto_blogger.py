import requests
import random
import os

# =========================
# 🔑 CONFIG (GitHub Secrets)
# =========================
BLOG_ID = os.getenv("BLOG_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

# =========================
# 📰 اختيار الموضوع من الأقسام
# =========================
def get_topic():
    categories = {
        "Global News": ["latest world events", "politics", "technology breakthroughs"],
        "Sports": ["football latest news", "basketball updates", "Olympics highlights"],
        "Trending": ["viral news", "celebrity news", "social media trends"]
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
    Include:
    - A strong, SEO-optimized title
    - Headings and subheadings
    - Structured paragraphs
    - Engaging introduction and conclusion
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
# 🖼️ جلب أكثر من صورة
# =========================
def get_images(count=3):
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
# 🧩 تشغيل السكريبت
# =========================
def main():
    category, topic = get_topic()
    print("Category:", category)
    print("Topic:", topic)

    article = generate_article(category, topic)
    title = article.split("\n")[0]  # أول سطر كعنوان

    images = get_images(count=3)
    result = publish(title, article, images)

    print("Published:", result)

if __name__ == "__main__":
    main()
