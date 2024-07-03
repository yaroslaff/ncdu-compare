#!/usr/bin/env python3

import argparse
import json
import os

__version__ = '0.0.8'

args = None


class Directory:
    root = None
    name = None
    
    
    def __init__(self, data, parent=None):
        my_node = data[0]
        if parent:
            self.root = os.path.join(parent, my_node['name'])
        else:
            self.root = my_node['name']

        self.name = my_node['name']

        self.files = {}
        self.directories = {}
        self.asize = 0
        self.dsize = 0

        for n in data[1:]:
            if isinstance(n, dict):
                if 'asize' in n and 'dsize' in n:
                    # some special file misses it
                    self.files[n['name']] = n
                    self.asize += n['asize']
                    self.dsize += n['dsize']

            elif isinstance(n, list):
                d = Directory(n, self.root)
                self.directories[d.name] = d
                self.asize += d.asize
                self.dsize += d.dsize

    def __repr__(self):
        return f'DIR <{self.root}>'

    def dump(self, prefix=""):
        print(f"{prefix}{self.name}/")
        for n in self.directories.values():
            n.dump(prefix=prefix+"  ")
        for n in self.files:
            print(f"{prefix}  {n}")
        
    def __iter__(self):
        yield { 'path': self.root, 'type': 'DIR', 'asize': self.asize, 'dsize': self.dsize }
        for f in self.files.values():
            f['path'] = os.path.join(self.root, f['name'])
            f['type'] = 'FILE'
            yield f
        
        for d in self.directories.values():
            yield from d

    def as_dict(self):
        d = dict()
        for n in self:
            d[n['path']] = n 
        return d

def get_args():

    epilog = f'''Generate files with ncdu: ncdu -0xo /tmp/ncdu0 /var/log
    '''

    parser = argparse.ArgumentParser(description=f'Compare old and new ncdu dumps. ver. {__version__}',
        formatter_class=argparse.RawTextHelpFormatter, epilog=epilog)
    parser.add_argument('old', help='old ncdu dump')
    parser.add_argument('new', help='new ncdu dump')
    parser.add_argument('-e', '--error', default='replace', help='Unicode error handling mode: replace (default), ignore , strict, surrogateescape')

    return parser.parse_args()

def kmgt(num):
    """
    Convert a number into a human-readable string with K, M, G, T suffixes.

    Parameters:
    num (float): The number to be converted.

    Returns:
    str: The human-readable string.
    """
    suffixes = ['K', 'M', 'G', 'T']
    magnitude = 0
    
    while abs(num) >= 1000 and magnitude < len(suffixes):
        magnitude += 1
        num /= 1000.0
    
    if magnitude == 0:
        return f"{num:.0f}"
    else:
        return f"{num:.2f}{suffixes[magnitude-1]}"


def report(path, old, new):
    try:
        t = old['type']
    except TypeError:
        t = new['type']

    try:
        oasize = old.get('asize')
    except AttributeError:
        oasize = 0

    try:
        nasize = new.get('asize')
    except AttributeError:
        nasize = 0

    diff = nasize - oasize
    diff_si = kmgt(diff)
    nasize_si = kmgt(nasize)
    oasize_si = kmgt(oasize)

    if not diff:
        return

    # print(f"{diff} {verdict} {t} {path} ({oasize} => {nasize})")
    print(f"{diff} {t} {path} ({oasize_si} => {nasize_si} ({diff_si}))")


def main():
    global args
    args = get_args()
    errors = args.error



    with open(args.old, encoding='utf-8', errors=errors) as fh:
        old_data = json.load(fh)

    with open(args.new, encoding='utf-8', errors=errors) as fh:
        new_data = json.load(fh)

    new = Directory(new_data[3], parent = None)
    old = Directory(old_data[3], parent = None)
    # new.dump()

    nd = new.as_dict()
    od = old.as_dict()

    nkeys = set(nd.keys())
    okeys = set(od.keys())
    # deleted = [ n for n in okeys if not n in nkeys ]
    deleted = okeys - nkeys

    for path in nkeys:
        report(path, od.get(path), nd.get(path))

    for path in deleted:
        report(path, od.get(path), None)


if __name__ == '__main__':
    main()

