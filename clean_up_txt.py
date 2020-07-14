import re

def clean_up_txt(year):
    input_filename = 'data/pres_txt_corrected/{}_pres.txt'.format(year)

    with open(input_filename, 'r') as f:
        text = f.read()
    
    text = re.sub(' +', ' ', text)
    text = re.sub(' \n', '\n', text)
    text = re.sub('\n', '.\n', text)
    text = re.sub(':.\n', ':\n', text)
    text = re.sub(';.\n', ';\n', text)
    text = re.sub('\\?.\n', '?\n', text)

    output_filename = 'data/pres_txt_corrected2/{}_pres.txt'.format(year)

    with open(output_filename, 'w') as f:
        f.write(text)


for year in range(1947, 2021):
    clean_up_txt(year)

