import re

_rule_re = re.compile(r'''
    (?P<static>[^<]*)                           # static rule data
    <
    (?:
        (?P<converter>[a-zA-Z_][a-zA-Z0-9_]*)   # converter name
        (?:\((?P<args>.*?)\))?                  # converter arguments
        \:                                      # variable delimiter
    )?
    (?P<variable>[a-zA-Z_][a-zA-Z0-9_]*)        # variable name
    >
''' , re.VERBOSE)

def parse_rule(rule):
        pos = 0
        end = len(rule)
        do_match = _rule_re.match
        used_names = set()
        while pos < end:
            m = do_match(rule, pos)
            if m is None:
                break
            data = m.groupdict()
            if data['static']:
                yield None, None, data['static']
            variable = data['variable']
            converter = data['converter'] or 'default'
            if variable in used_names:
                raise ValueError('variable name %r used twice.' % variable)
            used_names.add(variable)
            yield converter, data['args'] or None, variable
            pos = m.end()
        if pos < end:
            remaining = rule[pos:]
            if '>' in remaining or '<' in remaining:
                raise ValueError('malformed url rule: %r' % rule)
            yield None, None, remaining

