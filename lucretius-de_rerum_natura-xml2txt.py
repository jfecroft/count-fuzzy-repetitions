import xml.etree.ElementTree as ET
filen = 'lucretius-de_rerum_natura'
tree = ET.parse('{}.xml'.format(filen))
root = tree.getroot()

books = root.findall('.//*div1[@type="book"]')
for i, book in enumerate(books):
    book_text = ''
    for line in book.iter():
        if line.tag in ['lb', 'del', 'add'] and line.attrib.get('n' , '').endswith('a') is False:
            if line.tag == 'lb' and book_text.endswith('\n') is False and book_text:
                book_text += '\n'
            if line.text:
                book_text += line.text.rstrip('\n').encode('utf8')
            if line.tail:
                book_text += line.tail.rstrip('\n').encode('utf8')
          #  if line.attrib.get('n' , '').endswith('a'):
          #      import pdb
          #      pdb.set_trace()

    with open('{}-book{}.txt'.format(filen, i+1), 'w') as ofile:
        ofile.write(book_text)
