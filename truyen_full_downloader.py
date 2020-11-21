import requests
from bs4 import BeautifulSoup


class Chapter:
    def __init__(self, url):
        self.url = url
        self.soup = None
        try:
            response = requests.get(url)
            if response.status_code == 200:
                self.soup = BeautifulSoup(response.content, 'html.parser')
            response.close()
        except Exception as e:
            raise e

    def get_content(self):
        chapter = self.soup.find("div", {"id": "chapter-c"})
        text = chapter.getText()
        return text

    def get_next_url(self):
        next_element = self.soup.find("a", {"id": "next_chap"})
        next_url = next_element['href']
        if next_url == "javascript:void(0)":
            next_url = None
        return next_url


def get_all_chapter(url, file_name):
    try:
        print("*", url)
        chapter = Chapter(url)
        content = chapter.get_content()
        with open(file_name, "a") as appender:
            appender.write(content)
        next_chapter_url = chapter.get_next_chapter_url()
        if chapter.get_next_url() is not None:
            get_all_chapter(next_chapter_url, file_name)
    except Exception as e:
        print(str(e))
