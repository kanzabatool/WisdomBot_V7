import os
import requests

file = ['sub-fileAL',
 'sub-fileAN',
 'sub-fileAR',
 'sub-fileBA',
 'sub-fileBE',
 'sub-fileBI',
 'sub-fileBL',
 'sub-fileBO',
 'sub-fileBR',
 'sub-fileBU',
 'sub-fileCA',
 'sub-fileCH',
 'sub-fileCL',
 'sub-fileCO',
 'sub-fileCR',
 'sub-fileDE',
 'sub-fileDI',
 'sub-fileDO',
 'sub-fileMA',
 'sub-fileME',
 'sub-fileMI',
 'sub-fileMO',
 'sub-fileMU',
 'sub-fileMY',
 'sub-filePA',
 'sub-filePE',
 'sub-filePH',
 'sub-filePI',
 'sub-filePL',
 'sub-filePO',
 'sub-filePR',
 'sub-fileSA',
 'sub-fileSC',
 'sub-fileSE',
 'sub-fileSH',
 'sub-fileSI',
 'sub-fileSO',
 'sub-fileSP',
 'sub-fileST',
 'sub-fileSU',
 'file-E',
 'file-F',
 'file-G',
 'file-H',
 'file-I',
 'file-J',
 'file-K',
 'file-L',
 'file-N',
 'file-O',
 'file-Q',
 'file-R',
 'file-T',
 'file-U',
 'file-V',
 'file-W',
 'file-X',
 'file-Y',
 'file-Z',
 'sub-fileA',
 'sub-fileB',
 'sub-fileC',
 'sub-fileD',
 'sub-fileM',
 'sub-fileP',
 'sub-fileS',
 'fileCustomWords']

for f in file:
    if os.path.isfile('../lib/data/split/split-conceptnet/' + f) == False:
        url = 'https://wisdom-bot.s3-eu-west-1.amazonaws.com/split/' + f
        r = requests.get(url, allow_redirects=True)
        open('../lib/data/split/split-conceptnet/' + f, 'wb').write(r.content)