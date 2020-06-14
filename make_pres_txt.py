import data_func
import re

def make_pres_txt(year):
    text = data_func.convert_pdf_to_string(
    './data/pres_pdf/{}_pres.pdf'.format(year))

    text = text.replace('\n', ' ')
    text = text.replace('Digitized for FRASER', '')
    text = text.replace('http://fraser.stlouisfed.org/', '')
    text = text.replace('Federal Reserve Bank of St. Louis', '')
    text = text.replace('\x0c', '')
    text = text.replace('- ', '')
    text = text.replace('—', ' ')

    text = re.sub('\\.\\s+', '\n', text)

    output_filename = 'data/pres_txt/{}_pres.txt'.format(year)

    with open(output_filename, 'w') as out:
        out.write(text)


for year in range(1947, 2021):
    make_pres_txt(year)

