from fparser import *
from files import *
from utils import *
from db import *
import config
from wordforms import WordForm
from enum import Enum
import re
import os

DEBUG = False


if __name__ == '__main__':
    config.dbconfig = config.load_config()['db']
    wdb = Database()
    wdb.connect()
    wdb.setup_tables()
    wdb.load_normalizations()

    if DEBUG:
        p = FileParser(fp_to_parse('parsetest01.txt'))
        while True:
            try:
                for w in next(p):
                    if w.form == 'телевизор':
                        print(w)
                    wdb.save_word(w)
            except StopIteration:
                break
        wdb.conn.commit()
        print(f'{fn} completed')
        wdb.derive_roots()
        print("done")
        wdb.close()
        exit()

    line_idx = 0
    parse_dir = parse_dir()
    parse_fns = []
    for root, dirs, files in os.walk(parse_dir):
        for fn in files:
            if re.match(r'хаген_\d\.txt', fn):
                parse_fns.append(os.path.join(parse_dir, fn))
    parse_fns.sort()
    for fn in parse_fns:
        p = FileParser(fp_to_parse(fn))
        while True:
            try:
                for w in next(p):
                    wdb.save_word(w)
            except StopIteration:
                break
        wdb.conn.commit()
        print(f'{fn} completed')
    wdb.derive_roots()
    print("done")
    wdb.close()
