import requests
from bs4 import BeautifulSoup
import regex


def get_abstract(p_url):
    resp = requests.get(p_url)
    # print(resp)
    html = resp.text
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.find('h1', attrs={'class': 'title mathjax'}).get_text()
    title = title.replace('Title:', '')

    abstract = soup.find('blockquote', attrs={'class': 'abstract mathjax'}).get_text()
    abstract = abstract.replace('Abstract:', '')
    abstract = abstract.replace('\n', ' ').strip()
    abstract = regex.sub("[ ]{2,}", " ", abstract)

    result = (title, abstract)
    return result


def cornell_crawler(query, max_pages, RESULT_PATH):
    f = open(RESULT_PATH + "/%s.txt" % str(query), 'w', encoding='utf-8')

    n_query = query.replace(' ', '+')
    print('Crawling...')
    for i in range(max_pages):
        num = i * 50
        url = 'https://arxiv.org/search/?query=' + n_query + '&searchtype=all&abstracts=show&order=-announced_date_first&size=50&start=' + str(
            num)
        resp = requests.get(url)
        html = resp.text
        soup = BeautifulSoup(html, 'html.parser')

        papers = soup.findAll('p', attrs={'class': 'list-title is-inline-block'})
        p_links = []
        for p in papers:
            p_links.append(p.find('a')['href'])

        for p in p_links:
            paper_details = get_abstract(p)
            f.write("{}\n{}\n".format(paper_details[0], paper_details[1]))
        print('Page {} complete: Total {} papers crawled.'.format(i + 1, 50 * (i + 1)))


if __name__ == '__main__':
    PATH = input('Result path : ')
    query = input('Search keyword : ')
    max_pages = int(input('Max pages (50 papers per page) : '))

    cornell_crawler(query, max_pages, PATH)