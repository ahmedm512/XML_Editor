def validate(source):
    import re
    valid = True
    lines = []
    types = []
    stack = []


    def get_type(line, start, line_number):
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
        if (current_tag.startswith('<')) and (current_tag.endswith('>')) and (current_tag.find('?') == 1):
            return {
                'type': 'xml_decleration',
                'val': current_tag,
                'line_number': line_number
                    }

        if (current_tag.startswith('<')) and (current_tag.endswith('>')) and (current_tag.find('/') == 1):
            tag = current_tag[2:len(current_tag)-1]
            if tag.find('<') != -1 or tag.find('>') != -1:
                return {
                    'type': 'error',
                    'val': "found extra / or < or  >",
                    'line_number': line_number
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
                    'val': "found extra / or < or  >",
                    'line_number': line_number
                }
            return {
                'type': 'selfClosingTag',
                'tag_name': name_attr[0],
                'attr': attr,
                'line_number': line_number
            }
        if current_tag.startswith('<') and current_tag.endswith('>'):
            tag = current_tag[1:len(current_tag)-1]
            name_attr = tag.split(' ', 1)
            attr = name_attr[1] if len(name_attr) - 1 else ''
            if tag.find('<') != -1 or tag.find('>') != -1:
                return {
                    'type': 'error',
                    'val': "found extra / or < or  >",
                    'line_number': line_number
                }

            return dict(type='openTag', tag_name=name_attr[0], attr=attr, line_number=line_number)


    for line in source:
        lines.append(line.strip())
    lines = [x for x in lines if x != '']
    for i, line in enumerate(lines):
        for m in re.finditer('<', line):
            types.append(get_type(line, m.start(), i))
    for i, tag in enumerate(types, start=1):
        if tag['type'] == 'openTag':
            stack.append(tag)
        if tag['type'] == 'closeTag':
            if stack:
                if stack[-1]['tag_name'] == tag['tag_name']:
                    stack.pop(-1)
                else:
                    valid = False
                    print('NO')
                    return valid

            else:
                valid = False
                print('NO')
                return valid
        if tag['type'] == 'body':
            if stack:
                continue
            else:
                valid = False
                print('NO')
                return valid
    if not stack:
        valid = True
        print('YES')
        return valid
    else:
        valid = False
        print('NO')
        return valid
