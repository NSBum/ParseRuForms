from collections.abc import Iterator, Iterable
from files import *
from wordforms import WordForm
from utils import strip_if_needed
from typing import List, Any


class FileParser(object):
    def __init__(self, fn: str):
        self.fn = fn
        self.fh = open(fn, 'r')
        self.endloc = file_endloc(self.fh)

    def read_to_empty_line(self) -> List[Any]:
        lines = []
        while True:
            line = self.fh.readline()
            if line.strip():
                lines.append(line)
                break
        while True:
            line = self.fh.readline()
            if not line.strip():
                break
            lines.append(line)
        return lines

    def __iter__(self):
        return self

    def __next__(self):
        if self.fh.tell() == self.endloc:
            raise StopIteration
        lines = self.read_to_empty_line()
        wlist = [WordForm(x) for x in lines]
        for idx, w in enumerate(wlist):
            if idx == 0:
                w.parent_code = 0
            else:
                w.parent_code = wlist[0].code
        return wlist

        # line = None
        # w = None
        # last_code = 0
        # while self.no_line:
        #     line = self.fh.readline()
        #     if len(line.strip()) != 0:
        #         self.new_word = True
        #         self.no_line = False
        # if line == '' and self.fh.tell() == endloc:
        #     raise StopIteration
        # line = strip_if_needed(line)
        # if line and len(line) > 0:
        #     w = WordForm(line)
        #     self.last_code = w.code
        #     if self.new_word:
        #         w.parent_code = 0
        #         self.new_word = False
        #     else:
        #         w.parent_code = self.last_code
        #     # if self.capture_code:
        #     #     self.parent_code = 0
        #     # # print(f'{w.form} - {w.code} - {parent_code}')
        #     # else:
        #     #     self.parent_code = w.code
        #     #     w.parent_code = self.parent_code
        #     #
        #     #     self.capture_code = False
        # # if len(line) == 0:
        #
        # return w



