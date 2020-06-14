import PyPDF2

def make_pres_pdf(year, start_page, end_page):
    reader = PyPDF2.PdfFileReader(
        './data/after_split/{}_excl_app.pdf'.format(year))

    writer = PyPDF2.PdfFileWriter()

    for page in range(start_page - 1, end_page):

        writer.addPage(reader.getPage(page))

    output_filename = './data/pres_pdf/{}_pres.pdf'.format(year)

    with open(output_filename, 'wb') as output:
        writer.write(output)

year = range(1947, 2021)

start_page = [10, 9, 9, \
    9, 9, 9, 9, 4, 5, 5, 5, 5, 5, \
    5, 5, 11, 11, 11, 9, 9, 9, 9, 9, \
    9, 9, 9, 9, 9, 9, 9, 9, 9, 9, \
    9, 9, 9, 9, 7, 9, 9, 9, 9, 9, \
    9, 9, 9, 9, 9, 4, 7, 9, 9, 9, \
    4, 4, 4, 5, 8, 5, 5, 5, 5, 4, \
    8, 8, 7, 7, 8, 8, 8, 8, 8, 8, \
    8]

end_page = [11, 18, 26, \
    25, 33, 39, 35, 6, 8, 8, 9, 8, 9, \
    7, 7, 35, 30, 26, 27, 27, 32, 34, 30, \
    17, 15, 13, 13, 16, 14, 14, 17, 29, 21, \
    21, 25, 16, 14, 13, 15, 17, 14, 16, 17, \
    14, 16, 11, 11, 14, 9, 10, 11, 11, 12, \
    8, 6, 5, 6, 9, 7, 7, 7, 7, 8, \
    14, 12, 9, 9, 11, 11, 11, 11, 16, 11, \
    13]

for year, start_page, end_page in zip(year, start_page, end_page):
    make_pres_pdf(year, start_page, end_page)

