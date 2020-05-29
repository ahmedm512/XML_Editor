import re


def get_type_(source):
    '''
    :param name: XML filename
    :return:  A List of dictionaries of the XML file
    '''

    lines = []
    so = []
    types = []
    errors = []

    def get_body(line, index, line_number, tag_name):
        if index == -1 and tag_name == 0:
            for t in range(len(types)):
                if types[index]['type'] == 'openTag':
                    return {
                        'type': 'body',
                        'body': line,
                        'tag_name': types[index]['tag_name'],
                        'line_number': line_number,
                        'index': index
                    }
                index -= 1
            return 0

        start = line[index:].find('>') + index
        end = line[start:].find('<') + 1 + start
        if line[start:].find('<') == -1:
            end = len(line)
        current_tag = line[start:end]
        tag = current_tag[1:len(current_tag) - 1]
        if (current_tag.startswith('>')) and (current_tag.endswith('<')) and tag:
            return {
                'type': 'body',
                'body': tag,
                'tag_name': tag_name,
                'line_number': line_number
            }
        if (current_tag.startswith('>')) and (current_tag.endswith('>')) and tag:
            return {
                'type': 'error',
                'val': '< is missing',
                'solu': 'replace/',
                'line_number': line_number
            }
        if (current_tag.startswith('>')) and (current_tag.find('/') != -1) and tag:
            return {
                'type': 'error',
                'val': '< is missing',
                'solu': 'replace/',
                'line_number': line_number
            }
        if (current_tag.startswith('>')):
            tag = tag.strip()
            if tag:  return {
                'type': 'body',
                'body': tag,
                'tag_name': tag_name,
                'line_number': line_number
            }

    def get_type(line, start, line_number):
        v = []
        end = line[start:].find('>') + 1 + start
        if end == 0:
            end = len(line)

        current_tag = line[start:end]

        if (current_tag.startswith('<')) and (current_tag.find('!') == 1):
            return {
                'type': 'comment',
                'val': current_tag,
                'line_number': line_number
            }
        if (current_tag.endswith('>')) and (current_tag[-2] == '-'):
            return {
                'type': 'comment',
                'val': current_tag,
                'line_number': line_number
            }
        if line[start:].find('>') == -1:
            return {
                'type': 'error',
                'val': "tags must end with >",
                'line_number': line_number,
                'solu': 'at the end'
            }
        if (current_tag.startswith('<')) and (current_tag.endswith('>')) and (current_tag.find('?') == 1):
            return {
                'type': 'xml_decleration',
                'val': current_tag,
                'line_number': line_number
            }

        if (current_tag.startswith('<')) and (current_tag.endswith('>')) and (current_tag.find('/') == 1):
            tag = current_tag[2:len(current_tag) - 1]
            if tag.find('<') != -1 or tag.find('>') != -1:
                return {
                    'type': 'error',
                    'val': "found extra <",
                    'line_number': line_number,
                    'solu': 'replace'  # replace < with ><
                }
            return {
                'type': 'closeTag',
                'tag_name': tag,
                'line_number': line_number
            }
        if current_tag.startswith('<') and current_tag.endswith('>') and (current_tag[-2] == '/'):
            tag = current_tag[1:len(current_tag) - 1]
            name_attr = tag.split(' ', 1)
            attr = name_attr[1] if len(name_attr) - 1 else ''
            if tag.find('<') != -1 or tag.find('>') != -1:
                return {
                    'type': 'error',
                    'val': "found extra / or<",
                    'line_number': line_number,
                    'solu': 'replace'
                }
            return {
                'type': 'selfClosingTag',
                'tag_name': name_attr[0],
                'attr': attr,
                'line_number': line_number,
                'body': 0
            }
        if current_tag.startswith('<') and current_tag.endswith('>'):
            tag = current_tag[1:len(current_tag) - 1]
            name_attr = tag.split(' ', 1)
            attr = name_attr[1] if len(name_attr) - 1 else 0
            if tag.find('<') != -1 or tag.find('>') != -1:
                return {
                    'type': 'error',
                    'val': "found extra / or <",
                    'line_number': line_number,
                    'solu': 'find&replace'
                }
            return {
                'type': 'openTag',
                'tag_name': name_attr[0],
                'attr': attr,
                'line_number': line_number,
                'body': v
            }


    for line in source:
        line =line.replace('<<','<')
        line = line.replace('>>', '>')

        x = line.strip()
        if len(x) > 0:
            so.append(line)
            lines.append(x)

    lines = [x for x in lines if x != '']
    for i, line in enumerate(lines):
        if line.startswith('<') and line.find('>') == -1 and line.find('/') !=-1:
            e={
            'type': 'error',
            'val': "tags must end with >",
            'line_number': i,
            'solu':'at the end'}

        if not line.startswith('<') and line.find('<') != -1 and line.find('>') != -1:
            if line.find('>') < line.find('<'):
                e=({
                    'type': 'error',
                    'val': "< is missing",
                    'line_number': i,
                    'solu': '< at begining'})
                line = line[line.find('>') + 1:]
        if not line.startswith('<') and line.find('<') != -1 and line.find('>') != -1:
            if line.find('<') < line.find('>'):
                d = get_body(line, -1, i, 0)
                if d:
                    types.append(d)
                else:

                    e=({
                        'type': 'error',
                        'val': "Content is not allowed in prolog.",
                        'line_number': i,
                        'solu': 'delete body before <'})
            line = line[line.find('<'):]

        for m in re.finditer('<', line):
            types.append(get_type(line, m.start(), i))

            if types[-1]['type'] == 'openTag':
                body = get_body(line, m.start(), i, types[-1]['tag_name'])
                if body:
                    types.append(body)
                    if body['type'] == 'error':
                        if errors and errors[-1] != types[-1]:
                            errors.append(types[-1])
                        elif not errors:
                            errors.append(types[-1])
                    else:
                        types[-2]['body'].append(body['body'])
                        types[-2]['hasBody'] = True

                #else:   types[-2]['hasBody'] = False
        if line.find('<') == -1 and line.find('>') == -1:
            body = get_body(line, -1, i, 0)
            if body:
                types.append(body)
                if types[-1]['type'] == 'error':
                    if errors and errors[-1] != types[-1]:
                        errors.append(types[-1])
                    elif not errors:
                        errors.append(types[-1])
                else:types[body['index'] ]['body'].append(body['body'])
            else:
                types.append({
                    'type': 'error',
                    'val': "Content is not allowed in prolog.",
                    'line_number': i
                    , 'solu': 'delete line'})
                errors.append(types[-1])
            continue
        if line.find('<') == -1 and line.find('>') != -1:
            d = get_type(line, 0, i)
            if d:
                types.append(d)
                if types[-1]['type'] == 'error':
                    if errors and errors[-1] != types[-1]:
                        errors.append(types[-1])
                    elif not errors:
                        errors.append(types[-1])
            else:
                types.append({
                    'type': 'error',
                    'val': "< is missing",
                    'line_number': i,
                    'solu': '< at begining'})
                if errors and errors[-1] !=types[-1] :
                    errors.append(types[-1])
                elif not errors:
                    errors.append(types[-1])

    return types