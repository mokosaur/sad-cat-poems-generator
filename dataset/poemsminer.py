import requests
from bs4 import BeautifulSoup
import os


def mine(url, author, filename='poems'):
    """Finds all poems written by the author and saves them to a file.

    :param url: Author's page
    :param author: Author's name
    :param filename: Name of a generated file
    """
    response = requests.get(url)
    if response.status_code == 200:
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        links = get_links(soup, url)
        if not os.path.exists(author):
            os.makedirs(author)
        with open(os.path.join(author, '%s.txt' % filename), 'w', encoding='utf8') as file:
            for link in links:
                try:
                    page = requests.get(link).content
                    poem_soup = BeautifulSoup(page, 'html.parser')
                    title, poem = get_poem(poem_soup)
                    if "english" not in title and "esperanto" not in title and "[en]" not in title:
                        file.write("# %s\n\n" % title)
                        file.write("%s\n" % poem)
                except requests.exceptions.ConnectionError:
                    print("Failed to connect with %s." % link)


def get_links(soup, url):
    """Parses a page to find links to poems.

    :param soup: BeautifulSoup object with the parsed HTML
    :param url: Author's page
    :return: List of urls with poems
    """
    return [a.get('href') for ul in soup.find_all('ul') for a in ul.find_all('a') if a.get('href').startswith(url)]


def get_poem(soup):
    """Parses a page to get the title and the content of a poem.

    :param soup: BeautifulSoup object with the parsed HTML
    :return: 2-tuple containing the title and the content of the poem.
    """
    title = soup.title.text
    poem = soup.find(attrs={"class": "blog-post"}).text
    return title, poem


if __name__ == '__main__':
    mine('https://poezja.org/wz/Białoszewski_Miron/', 'bialoszewski')
    mine('https://poezja.org/wz/Baczyński_Krzysztof_Kamil/', 'baczynski')
    mine('https://poezja.org/wz/Herbert_Zbigniew/', 'herbert')
    mine('https://poezja.org/wz/Leśmian_Bolesław/', 'lesmian')
    mine('https://poezja.org/wz/Szymborska_Wisława/', 'szymborska')
    mine('https://poezja.org/wz/Mickiewicz_Adam/', 'mickiewicz')
    mine('https://poezja.org/wz/Kochanowski_Jan/', 'kochanowski')
    mine('https://poezja.org/wz/Słowacki_Juliusz/', 'slowacki')
