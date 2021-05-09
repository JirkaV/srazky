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

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
FNAME = os.path.join(DATA_DIR, '{}_{}.html')

# odkazy jsou na vcerejsi den
URLS = {
    'hradecky': 'https://hydro.chmi.cz/hpps/hpps_pzv_list.php?sort=&sort_type=&fkraj=94&ftyp=&frbot=0&send=Vyhledat',
    'pardubicky': 'https://hydro.chmi.cz/hpps/hpps_pzv_list.php?srt=&objtyp%5B%5D=h&fkraj=12303&fobjtyp=&ok=Vyhledat',
}

def stahni_stanici(link, adresar, kraj):
    id_stanice = urlparse(link).query.split('=')[-1]
    soubor = adresar / '{}_{}.html.bz'.format(kraj, id_stanice)
    if soubor.exists():
        logging.info('{} exists'.format(soubor))
        return
    try:
        start_time = time.time()
        resp = requests.get(link)
        done_time = time.time()

        if resp.ok:
            f = bz2.open(soubor, mode='wb', compresslevel=9)
            f.write(resp.content)
            f.close()
            msg = '{} - [{}] "{}" ({} bytes, {:.3f} secs)'.format(start_time, resp.status_code, soubor,
                                                                  len(resp.content), done_time-start_time)
            logging.info(msg)
        else:
            logging.error('{} - [{}] {}'.format(start_time, resp.status_code, url))
    except IOError as err:
        logging.error('{} - [{}] {}: {}'.format(start_time, resp.status_code, url, str(err)))

def najdi_stanice(url):
    with open('par.data', 'rb') as f:
        data = f.read()

    page = html.fromstring(data)
    for link in page.xpath('//a/@href'):
        if 'seq=' in link:
            yield urljoin(url, link)

def stahni_vse(url, kraj):
    den = datetime.date.today().strftime('%Y%m%d')
    adr = Path('.') / 'studny' / den
    adr.mkdir(exist_ok=True)
    for link_stanice in najdi_stanice(url):
        stahni_stanici(link_stanice, adr, kraj)
        time.sleep(random.uniform(1, 3))

if __name__ == '__main__':
    adr = Path('.') / 'studny'
    adr.mkdir(exist_ok=True)

    for prefix, url in URLS.items():
        stahni_vse(url, prefix)
