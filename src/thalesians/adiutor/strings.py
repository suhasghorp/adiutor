import io
import re

import thalesians.adiutor.checks as our_checks

import unidecode

def sanitize_str(raw_str):
    processed_str = raw_str
    processed_str = unidecode.unidecode(processed_str)
    processed_str = processed_str.lower()
    processed_str = re.sub(r'[_\W]+', '_', processed_str)
    return processed_str

def make_unique_str(raw_str, strs):
    processed_str = raw_str
    if processed_str in strs:
        i = 1
        candidate_str = f'{processed_str}_{i}'
        while candidate_str in strs:
            i += 1
            candidate_str = f'{processed_str}_{i}'
        processed_str = candidate_str
    return processed_str

def enquote(s, quote='"', escape=True):
    s = str(s)
    if escape: s = str(s).replace('\\', "\\\\").replace(quote, '\\' + quote)
    return quote + s + quote

class ToStringHelper(object):
    def __init__(self, typ=None):
        self.set_type(typ)
        self._properties = []
        self._str = None
        
    def set_type(self, typ=None):
        if typ is not None:
            if not our_checks.is_type(typ): typ = type(typ)
            typ = typ.__name__
        self._type_name = typ
        return self
        
    def add(self, name, value):
        self._properties.append((name, value))
        self._str = None
        return self
    
    def add_all_properties(self, o, ignore_dunders=True):
        if hasattr(o, '__dict__'):
            for prop, value in vars(o).items():
                if ignore_dunders and prop.startswith('__'): continue
                self.add(prop, value)
        return self
    
    def _should_enquote(self, o):
        return our_checks.is_string(o)
    
    def to_string(self):
        if self._str is None:
            s = io.StringIO()
            if self._type_name is not None: s.write(self._type_name)
            s.write('(')
            for i, p in enumerate(self._properties):
                if i > 0: s.write(', ')
                s.write(p[0])
                s.write('=')
                v = p[1]
                if self._should_enquote(v): s.write(enquote(v))
                else: s.write(str(v))
            s.write(')')
            self._str = s.getvalue()
        return self._str
                
    def __str__(self):
        return self.to_string()

def _test():
    import doctest
    doctest.testmod(verbose=False)

if __name__ == '__main__':
    _test()
