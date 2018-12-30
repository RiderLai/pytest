def tag(name, *content, cls=None, **attrs):
    if cls is not None:
        attrs['class'] = cls

    if attrs:
        attr_string = ''.join(' %s="%s"' % (key, value) for key, value in sorted(attrs.items()))
    else:
        attr_string = ''

    if content:
        return '\n'.join('<%s%s>%s</%s>' % (name, attr_string, c, name) for c in content)
    else:
        return '<%s%s />' % (name, attr_string)


print(tag('p', '123', '321'))
print(tag('br'))
# print(tag('span', '123', '321', cls='icon', attrs={'style': 'background:red;'}))
print(tag('span', '123', '321', cls='icon', style='background:red;'))
print(tag(**{'name': 'span', 'cls': 'icon', 'style': 'background: red;'}))