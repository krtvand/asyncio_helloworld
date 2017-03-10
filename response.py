import asyncio
import aiohttp
import logging
import sys
import time

import requests
from requests.exceptions import RequestException


# Зададим параметры логгирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(u'%(levelname)-8s [%(asctime)s]  %(message)s')
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

async def a_make_request(site):
    async with aiohttp.ClientSession() as session:
        async with session.get(site) as resp:
            logger.debug('Checking %s, response code: %s' % (site, resp.status))

async def main(urls):
    coroutines_ = [a_make_request(url) for url in urls]
    start_time = time.time()
    completed, pending = await asyncio.wait(coroutines_)
    elapsed = time.time() - start_time
    print('elapsed time for async get {}'.format(elapsed))

def make_request(site):
    """Функция проверки доступности одного сайта
    :param site: Адрес сайта для проверки
    :return: Dictionary, где ключ - сайт, значение - код ответа (200, 404)
    """
    result = {}
    try:
        r = requests.get(site, timeout=5, verify=True)
        result[site] = r.status_code
        # Если код ответа веб сервера 200, значит сайт доступен
        # if r.status_code == 200:
        #     logger.warning('Site is availble: %s responce code: %s' %
        #                    (site, r.status_code))
        logger.debug('Checking %s, response code: %s' % (site, r.status_code))
    # Обрабатываем ошибки модуля Requests
    except RequestException as e:
        result[site] = -1
        logger.debug('Error %s, message: %s' % (site, e))
    # Пропускаем прочие ошибки подключения
    except:
        result[site] = -1
        logger.debug('Error: %s Other exception' % site)
    return result

if __name__ == '__main__':
    SITE_LIST = ['http://example.com', 'http://lenta.ru', 'http://rambler.ru']
    event_loop = asyncio.get_event_loop()

    try:
        print('start')
        event_loop.run_until_complete(main(SITE_LIST))
    finally:
        event_loop.close()

    print('')
    start_time = time.time()
    for url in SITE_LIST:
        make_request(url)
    elapsed = time.time() - start_time
    print('elapsed time for sync get {}'.format(elapsed))
