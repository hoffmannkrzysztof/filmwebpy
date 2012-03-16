import re

def get_real_id(*strings):
    for text in strings:
        text = str(text)

        found = re.search("http://([0-9]{1,2}).fwcdn.pl/(p|po)/([0-9]{1,4})/([0-9]{1,4})/(?P<id>[0-9]{1,9})/([0-9]{1,9}).([0-9]{1}).jpg",text)
        if found is not None:
            return int(found.group('id'))

        found = re.search("dropdownTarget (?P<id>[0-9]*)_(FILM|SERIAL)", text)
        if found is not None:
            return int(found.group('id'))

        list =  re.findall(r'-([0-9]*)', text)
        if len(list) and list[-1].isdigit():
            return int(list[-1])

    return 0


def canonicalname(title):

    splited = title.split(" ")
    name = splited[0]
    surname = splited[1:]
    surname.extend( [name] )

    return " ".join( surname )


def get_text_or_none(var,typ='str'):
    if typ=='int':
        try:
            return int(var.text)
        except:
            return 0
    else:
        try:
            return var.text
        except:
            return ''