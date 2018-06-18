from bs4 import BeautifulSoup
import requests
import csv


def get_soup(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    return soup


def get_pages_amount(soup):
    page_nav = soup.find('div', class_='page-nav td-pb-padding-side')
    number_of_last_page = page_nav.find('a', class_='last')['title']
    return number_of_last_page


def get_articles(soup):
    h3_tags = soup.find_all('h3', class_='entry-title td-module-title')
    articles = {}
    for tag in h3_tags:
        a_tag = tag.find('a')
        title = a_tag['title']
        href = a_tag['href']
        articles[title] = href
    return articles


def print_commands(commands):
    for key, val in commands.items():
        print('{}. {}'.format(str(key), val))


def user_input():
    try:
        command = int(input('Введите номер категории: '))
        return command
    except ValueError:
        return user_input()


def chose_category():
    commands = {1: 'news',
                2: 'learn',
                3: 'startups',
                4: 'work'}
    print_commands(commands)
    command = user_input()
    if command in commands.keys():
        return commands[command]
    else:
        chose_category()


def write_to_csv(articles):
    with open('techRocks.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, val in articles.items():
            writer.writerow([key, val])


def main():
    articles = {}
    page = 1
    pages_amount = 1
    category = chose_category()
    while page <= pages_amount:
        url = 'https://techrocks.ru/category/{}/page/{}/'.format(category, str(page))
        soup = get_soup(url)
        articles_on_page = get_articles(soup)
        articles.update(articles_on_page)
        if page == 1:
            pages_amount = int(get_pages_amount(soup))
        page += 1
    write_to_csv(articles)


if __name__ == '__main__':
    main()
