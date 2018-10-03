import requests, csv, re, pyperclip

# starting dictionary lists
basicList = [
    'npi',
    'status',
    'credential',
    'first_name',
    'last_name',
    'middle_name',
    'name',
    'gender',
    'sole_proprietor',
    'last_updated',
    'name_prefix',
    'enumeration_date'
    ]
taxonomiesList = [
    'taxonomies1',
    'taxonomies2',
    'taxonomies3',
    'taxonomies4',
    'taxonomies5',
    'taxonomies6',
    'taxonomies7',
    'taxonomies8',
    'taxonomies9',
    'taxonomies10'
    ]
addressesList = [
    'Address1',
    'Address2',
    'Address3',
    'Address4',
    'Address5',
    'Address6',
    'Address7',
    'Address8'
    ]
identifiersList = [
    'Identifier1',
    'Identifier2',
    'Identifier3',
    'Identifier4',
    'Identifier5',
    'Identifier6',
    'Identifier7',
    'Identifier8',
    'Identifier9',
    'Identifier10',
    'Identifier11',
    'Identifier12',
    'Identifier13',
    'Identifier14',
    'Identifier15'
    ]
# combination of sublists for master row
headers = basicList + taxonomiesList + addressesList + identifiersList
def main():
    # create regex object to check string
    npiRegex = re.compile(r'\d\d\d\d\d\d\d\d\d\d')
    # pull each NPI from the clipboard to check against the regex
    npiList = pyperclip.paste()
    # if it is, check the website
    url = "https://npiregistry.cms.hhs.gov/api/resultsDemo2/"
    npi_info = open(file="npi_file.txt", mode='w', newline='')
    csvFile = csv.DictWriter(f=npi_info, fieldnames=headers, delimiter='|')
    csvFile.writeheader()
    provRecord = {}
    for npi in npiList.split('\r\n'): # check for formatting 
        if npiRegex.match(npi):
            params = {'number':npi}
            r = requests.get(url=url, params=params)
            r.raise_for_status()
            npiDict = dict(r.json())
            results = npiDict['results'][0]
            provRecord = results['basic']
            provRecord['npi'] = npi
            for i, tax in enumerate(results['taxonomies']):
                provRecord[taxonomiesList[i]]=tax
            for i, add in enumerate(results['addresses']):
                provRecord[addressesList[i]]=add
            for i, iden in enumerate(results['identifiers']):
                provRecord[identifiersList[i]]=iden
            csvFile.writerow(rowdict=provRecord)
    npi_info.close()
if __name__ == '__main__':
    main()
