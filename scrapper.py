"""
This file contains the script for scrapping process
"""

import requests
import argparse
from bs4 import BeautifulSoup


def scraper(posts):
    """
    Main scrapper function
    """
    BASE_URL = "https://improvado.io"
    OUTPUT_FILE = "data/blogposts.txt"
    url = f"{BASE_URL}/blog"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    blog_posts = soup.find("div", class_="blog-posts")
    dyn_list = blog_posts.find("div", class_="w-dyn-list")
    list_div = dyn_list.find("div", role="list")
    list_items = list_div.find_all("div", role="listitem")

    posts = min(posts, len(list_items))

    with open(OUTPUT_FILE, "w") as f:
        for post in list_items[:posts]:
            link = post.find("a")["href"]
            full_url = f"{BASE_URL}{link}"
            print(f"Processing post: {full_url}")
            post_page = requests.get(full_url)
            post_soup = BeautifulSoup(post_page.content, "html.parser")
            content_div = post_soup.find("div", id="content")
            rich_text_div = content_div.find("div", class_="c-rich-text-blog")
            paragraphs = rich_text_div.find_all("p")
            text_content = "\n\n".join([p.get_text() for p in paragraphs])
            f.write(text_content + "\n\n")

    print(f"Content of {posts} posts saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Scrape blog posts from the Improvado website."
    )
    parser.add_argument("--posts", type=int, help="number of posts to read")
    args = parser.parse_args()
    scraper(args.posts)
