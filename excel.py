from io import BytesIO
import xlsxwriter
from analyza import data_pro_mesic

KRAJE = ['hradecky', 'pardubicky']

def vyrob_excel(obdobi, kraje=KRAJE):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    for kraj in kraje:
        worksheet = workbook.add_worksheet(kraj)

        data = data_pro_mesic(kraj, obdobi)

        # zjisti jmena vsech stanic zminenych v mesici
        stanice = set()
        for data_dne in data.values():
            if data_dne is not None:
                stanice |= set(data_dne.keys())
        stanice = sorted(list(stanice))

        # hlavicka
        for sloupec, nazev_stanice in enumerate(stanice, start=1):
            worksheet.write(0, sloupec, nazev_stanice)

        dny = sorted(data.keys())

        for radek, den in enumerate(dny, start=2):

            worksheet.write(radek, 0, den)

            data_dne = data[den]

            for sloupec, jmeno_stanice in enumerate(stanice, start=1):
                try:
                    hodnota = data_dne[jmeno_stanice]
                except (KeyError, TypeError):
                    hodnota = None
                if hodnota is None:  # muze byt i chybejici soubor
                    hodnota = 'nejsou data'
                worksheet.write(radek, sloupec, hodnota)

    workbook.close()
    return output.getvalue()

if __name__ == '__main__':
    vyrob_excel('201901', KRAJE)
    vyrob_excel('201902', KRAJE)
