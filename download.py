import requests
import time

for year in range(1947, 2021):
    if year <= 1949:
        # Although there are midyear reports from 1949 to 1952, I ignore them
        url = 'https://fraser.stlouisfed.org/files/docs/publications/ERP/{0}/ERP_{0}_January.pdf'.format(
            year)
    elif year <= 1952:
        url = 'https://fraser.stlouisfed.org/files/docs/publications/ERP/{0}/ERP_January_{0}.pdf'.format(
            year)
    elif year <= 1986:
        url = 'https://fraser.stlouisfed.org/files/docs/publications/ERP/{0}/ERP_{0}.pdf'.format(
            year)
    elif year <= 1988:
        url = 'https://fraser.stlouisfed.org/files/docs/publications/ERP/{0}/ER_{0}.pdf'.format(
            year)
    elif year <= 2008:
        url = 'https://fraser.stlouisfed.org/files/docs/publications/ERP/{0}/ERP_{0}.pdf'.format(
            year)
    elif year == 2009:
        url = 'https://fraser.stlouisfed.org/files/docs/publications/ERP/{0}/{0}_ERP.pdf'.format(
            year)
    elif year == 2010:
        url = 'https://fraser.stlouisfed.org/files/docs/publications/ERP/{0}/erp_{0}.pdf'.format(
            year)
    elif year <= 2014:
        url = 'https://fraser.stlouisfed.org/files/docs/publications/ERP/{0}/{0}_erp.pdf'.format(
            year)
    elif year <= 2019:
        url = 'https://fraser.stlouisfed.org/files/docs/publications/ERP/{}_erp.pdf'.format(
            year)
    else:
        url = 'https://www.whitehouse.gov/wp-content/uploads/2020/02/2020-Economic-Report-of-the-President-WHCEA.pdf'

    output_filename = 'data/before_split/{}_erp.pdf'.format(year)

    myfile = requests.get(url)

    with open(output_filename, 'wb') as out:
        out.write(myfile.content)

    print(year)
    time.sleep(20)
