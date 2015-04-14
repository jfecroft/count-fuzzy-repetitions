# pylint: disable=C0103
"""
convert lucretius xml to seperate text file for each book
"""
import xml.etree.ElementTree as ET
FILEN = 'lucretius-de_rerum_natura'
TREE = ET.parse('{}.xml'.format(FILEN))
ROOT = TREE.getroot()

BOOKS = ROOT.findall('.//*div1[@type="book"]')
for i, book in enumerate(BOOKS):
    book_text = ''
    for line in book.iter():
        if (line.tag in ['lb', 'del', 'add'] and
                line.attrib.get('n', '').endswith('a') is False):
            if (line.tag == 'lb' and book_text.endswith('\n') is False and
                    book_text):
                book_text += '\n'
            if line.text:
                book_text += line.text.rstrip('\n').encode('utf8')
            if line.tail:
                book_text += line.tail.rstrip('\n').encode('utf8')

    with open('{}-book{}.txt'.format(FILEN, i+1), 'w') as ofile:
        ofile.write(book_text)
