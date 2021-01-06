import os
import datetime
import lxml.html

DEBUG = False

ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

ONE_DAY = datetime.timedelta(days=1)
FNAME = os.path.join(ROOT_DIR, '{}_{}.html')

def dny_v_mesici(yyyymm):
    '''for 201902 yields "2019-02-01" .. "2019-02-28"'''
    year = int(yyyymm[:4])
    month = int(yyyymm[4:])
    d = datetime.date(year=year, month=month, day=1)
    while d.month == month:
        yield d.strftime('%Y-%m-%d')
        d = d + ONE_DAY

def data_z_html(html_content):
    dom = lxml.html.fromstring(html_content)
    div_srazky = dom.xpath('//div[@class="tsrz"]')[0]
    tr_elements = div_srazky.xpath('.//tr')
    stanice = {}
    for elem in tr_elements:
        cells = elem.getchildren()
        jmeno_stanice = cells[0].text_content().strip('\n')
        try:
            souhrn_srazek = float(cells[-1].text_content())
        except ValueError:
            continue  # sumarni radek?

        stanice[jmeno_stanice] = souhrn_srazek
    return stanice

def data_pro_mesic(kraj, mesic):
    data = {}
    for den in dny_v_mesici(mesic):
        if DEBUG:
            print(den)
        try:
            with open(FNAME.format(kraj, den), 'rb') as f:
                data[den] = data_z_html(f.read())
        except (FileNotFoundError, IndexError):
            data[den] = None
    return data

if __name__ == '__main__':
    import pprint
    pprint.pprint(data_pro_mesic('hradecky', '201901'))
