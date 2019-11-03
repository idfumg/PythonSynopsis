#!/usr/bin/env python

import requests
from selenium.webdriver import Firefox
from contextlib import closing
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from pyvirtualdisplay import Display
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

serials = [
#   ('name',                   'season', 'series')
    ('гримм',                  '4',      '23'),
    ('гримм',                  '5',      '1'),
    ('сверхъестественное',     '10',     '24'),
    ('сверхъестественное',     '11',     '1'),
    ('спираль',                '2',      '14'),
    ('спираль',                '3',      '1'),
    ('древние',                '2',      '23'),
    ('древние',                '3',      '1'),
    ('дневники вампира',       '6',      '23'),
    ('дневники вампира',       '7',      '1'),
    ('черный список',          '2',      '23'),
    ('черный список',          '3',      '1'),
    ('вечность',               '1',      '23'),
    ('вечность',               '2',      '1'),
    ('агенты щ.и.т.',          '2',      '21'),
    ('агенты щ.и.т.',          '3',      '1'),
    ('теория большого взрыва', '8',      '25'),
    ('теория большого взрыва', '9',      '1'),
    ('игра престолов',         '5',      '11'),
    ('игра престолов',         '6',      '1'),
    ('флэш',                   '1',      '24'),
    ('флэш',                   '2',      '1')
]

def find_series_fanserials(browser, data):
    name = data[0] + ' ' + data[1] + ' сезон ' + data[2] + ' серия'
    rv = ''

    elem = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable((By.NAME, 'story'))
    )

#    elem.click()
    elem.clear()
    elem.send_keys(name)
    elem.send_keys(Keys.RETURN)

    try:

        articles = browser.find_elements_by_css_selector('article')
        for article in articles:
            h5 = article.find_element_by_tag_name('h5')
            if (name.lower() in h5.text.lower()):
                a = h5.find_element_by_partial_link_text(data[1] + ' сезон')
                rv = a.text + ' | ' + a.get_attribute('href')

    except NoSuchElementException:
        pass

    if rv:
        print('\n', rv)
    else:
        print('.', end='')

def find_series_kinogo(browser, data):
    name = data[0] + ' ' + data[1] + ' сезон'

    rv = ''

    elem = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable((By.NAME, 'story'))
    )

    elem.click()
    elem.clear()
    elem.send_keys(name)
    elem.send_keys(Keys.RETURN)

    try:

        link = browser.find_element_by_partial_link_text(data[1] + ' сезон')
        browser.get(link.get_attribute('href'))

        elem = browser.find_elements_by_class_name('quote')

    except NoSuchElementException:
        print('.', end='')
        return

    try:

        elem = elem[0].find_element_by_tag_name('li')

    except NoSuchElementException:
        print('.', end='')
        return

    if int(data[2]) == int(elem.text.split()[0]):
        rv = name + ' ' + elem.text
    elif int(data[2]) < int(elem.text.split()[0]):
        rv = name + ' ' + data[2] + ' серия'

    if rv:
        print('\n', rv)
    else:
        print('.', end='')

url_handler_map = [
    ('http://fanserials.tv/index.php?do=search', find_series_fanserials),
    ('http://kinogo.net', find_series_kinogo)
]

def main():
    display = Display(visible=0, size=(800, 600))
    display.start()

    with closing(Firefox()) as browser:
        for url, handler in url_handler_map:
            print('\n[' + url +']')
            browser.get(url)

            for data in serials:
                handler(browser, data)

    display.stop()

if __name__ == "__main__":
    main()
