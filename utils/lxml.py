def text(root, path):
    element = root.xpath(path)
    if element:
        return element[0].text
    else:
        return ''

def text_builder(element):    
    elements = element.xpath('.//child::text()')
    string = ''
    for element in elements:
        string += f'{element}'
    
    return string

def number(element):
    if isinstance(element, list) and len(element):
        element = element[0]

    try:
        return float(f'{element}'.replace(',', '.'))
    except:
        return 0