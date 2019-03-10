import os
import time
import logging
import datetime
import requests
import lxml.html

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
FNAME = os.path.join(DATA_DIR, '{}_{}.html')

# odkazy jsou na vcerejsi den
URLS = {
  'hradecky': 'http://hydro.chmi.cz/hpps/hpps_act_rain.php?day_offset=-1&fpob=&fucpov=&fkraj=10838',
  'pardubicky': 'http://hydro.chmi.cz/hpps/hpps_act_rain.php?day_offset=-1&fpob=&fucpov=&fkraj=12303',
}

logging.basicConfig(filename='srazky.log',
                    level=logging.INFO,  # don't log requests DEBUG msgs
                    format='%(asctime)s - %(levelname)s: %(message)s',
                    datefmt='%Y%m%d%Y %I:%M:%S %p')


if __name__ == '__main__':
    os.chdir('/home/jirka/vojta')
    vcera = str(datetime.date.today() - datetime.timedelta(days=1))
    for prefix, url in URLS.items():
        fname = FNAME.format(prefix, vcera)
        now = (datetime.datetime.now())
        start_time = time.time()
        resp = requests.get(url)
        done_time = time.time()
        if resp.ok:
            with open(fname, 'wb') as f:
                f.write(resp.content)
            msg = '{} - [{}] "{}" ({} bytes, {:.3f} secs)'.format(now, resp.status_code, fname,
                                                                  len(resp.content), done_time-start_time)
            logging.info(msg)
        else:
            logging.error('{} - [{}] {}'.format(now, resp.status_code, url))

