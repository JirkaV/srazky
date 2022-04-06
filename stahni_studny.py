import os
import time
import logging
import datetime
import random
import bz2
from urllib.parse import urlparse, urljoin
from pathlib import Path
import requests
from lxml import html

logging.basicConfig(filename='studny.log',
                    level=logging.INFO,  # don't log requests DEBUG msgs
                    format='%(asctime)s - %(levelname)s: %(message)s',
                    datefmt='%Y%m%d%Y %I:%M:%S %p')

URLS = {
    'hradecky': 'https://hydro.chmi.cz/hpps/hpps_pzv_list.php?sort=&sort_type=&fkraj=86&ftyp=&frbot=0&send=Vyhledat',
    'pardubicky': 'https://hydro.chmi.cz/hpps/hpps_pzv_list.php?sort=&sort_type=&fkraj=94&ftyp=&frbot=0&send=Vyhledat',
}

def stahni(url):
    try:
        start_time = time.time()
        resp = requests.get(url)
        done_time = time.time()

        if resp.ok:
            msg = '{} - [{}] "{}" ({} bytes, {:.3f} secs)'.format(start_time, resp.status_code, url,
                                                                  len(resp.content), done_time-start_time)
            logging.info(msg)
            return resp
        else:
            logging.error('{} - [{}] {}'.format(start_time, resp.status_code, url))
    except IOError as err:
        logging.error('{} - {}: {}'.format(start_time, url, str(err)))

def stahni_stanici(url, adresar, kraj):
    id_stanice = urlparse(url).query.split('=')[-1]
    soubor = adresar / '{}_{}.html.bz'.format(kraj, id_stanice)
    if soubor.exists():
        logging.info('{} exists'.format(soubor))
        return
    resp = stahni(url)
    if resp is not None:
        f = bz2.open(soubor, mode='wb', compresslevel=9)
        f.write(resp.content)
        f.close()

def najdi_stanice(url):
    resp = stahni(url)
    if resp is not None:
        page = html.fromstring(resp.text)
        for link in page.xpath('//a/@href'):
            if 'seq=' in link:
                yield urljoin(url, link)

def stahni_vse(url, kraj):
    den = datetime.date.today().strftime('%Y%m%d')
    adr = Path('.') / 'studny' / den
    adr.mkdir(exist_ok=True)
    for link_stanice in najdi_stanice(url):
        time.sleep(random.uniform(3, 10))
        stahni_stanici(link_stanice, adr, kraj)

if __name__ == '__main__':
    adr = Path('.') / 'studny'
    adr.mkdir(exist_ok=True)

    for prefix, url in URLS.items():
        stahni_vse(url, prefix)
