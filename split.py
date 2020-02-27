from PyPDF2 import PdfFileReader, PdfFileWriter

def pdf_split(year, app_A_start_page):

    input_filename = 'data/before_split/{}_erp.pdf'.format(year)

    pdf = PdfFileReader(input_filename)

    pdf_writer = PdfFileWriter()

    for page in range(app_A_start_page-1):
        pdf_writer.addPage(pdf.getPage(page))

    output_filename = 'data/after_split/{}_excl_app.pdf'.format(year)

    with open(output_filename, 'wb') as out:
        pdf_writer.write(out)

year = range(1947, 2021)
app_A_start_page = [44, 98, 110,
134, 176, 160, 160, 126, 79, 109, 85, 85, 78,
84, 82, 199, 160, 173, 177,193, 204, 201, 218,
148, 171, 182, 147, 233, 224, 159, 176, 244, 169,
190, 220, 222, 152, 208, 223, 241, 233, 236, 297,
271, 270, 285, 331, 255, 251, 265, 286, 267, 312,
278, 245, 295, 251, 270, 186, 252, 203, 202, 261,
310, 170, 291, 303, 350, 370, 386, 549, 514, 619,
348]

for year, app_A_start_page in zip(year, app_A_start_page):
    pdf_split(year, app_A_start_page)

