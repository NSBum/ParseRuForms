from typing import List, Optional
from enum import Enum
import utils
from functools import lru_cache


class Plurality(Enum):
    Singular = 0
    Plural = 1
    NA = 2


class WordForm(object):
    @classmethod
    @lru_cache(maxsize=10)
    def types(cls):
        return ['част', 'межд', 'прл', 'прч', 'сущ', 'нар', 'гл',
                'дееп', 'союз', 'предик', 'предл', 'ввод', 'мест', 'числ',
                'мод']

    @classmethod
    @lru_cache(maxsize=10)
    def genders(cls):
        return ['муж', 'жен', 'ср', 'общ']

    @classmethod
    @lru_cache(maxsize=10)
    def subtypes(cls):
        return ['поряд', 'кол', 'собир', 'неопр', 'врем',
                'обст', 'опред', 'счет', 'неизм']

    @classmethod
    @lru_cache(maxsize=10)
    def subsubtypes(cls):
        return ['кач', 'спос', 'степ', 'места', 'напр',
                'врем', 'цель', 'причин']

    @classmethod
    @lru_cache(maxsize=10)
    def cases(cls):
        return ['им', 'род', 'дат', 'вин', 'тв', 'пр', 'зват', 'парт', 'мест']

    @classmethod
    @lru_cache(maxsize=10)
    def transitives(cls):
        return ['перех', 'непер', 'пер/не']

    @classmethod
    @lru_cache(maxsize=10)
    def tenses(cls):
        return ['прош', 'наст', 'буд']

    @classmethod
    @lru_cache(maxsize=10)
    def persons(cls):
        return ['1-е', '2-е', '3-е', 'безл']

    @classmethod
    @lru_cache(maxsize=10)
    def voices(cls):
        return ['пов', 'страд']

    @classmethod
    @lru_cache(maxsize=10)
    def comparatives(cls):
        return ['сравн', 'прев']

    @classmethod
    @lru_cache(maxsize=10)
    def animacies(cls):
        return ['одуш', 'неод']

    @classmethod
    def type_code_for_type(cls, t: str) -> int:
        return next((l[0] for l in WordForm.pos_list if l[1] == t), 15)

    @classmethod
    def gender_code_for_gender(cls, t: str) -> Optional[int]:
        return next((l[0] for l in WordForm.gender_list if l[1] == t), None)

    @classmethod
    def case_code_for_case(cls, t: str) -> Optional[int]:
        return next((l[0] for l in WordForm.case_list if l[1] == t), None)

    def __init__(self, row: str):
        items = row.split('\t')
        self.form = items[0]
        # if self.form == 'басу':
        #     print(items)
        self.attributes: List[str] = items[1].split()
        self.code = int(items[2])
        self.parent_code = 0

    def __str__(self):
        return f'{self.form} - {self.attributes} - {self.code} - parent {self.parent_code}'

    def __repr__(self):
        return self.__str__()

    def _intersection(self, source_list: List[str]) -> Optional[str]:
        intersection = list(set(self.attributes) & set(source_list))
        try:
            return intersection[0]
        except IndexError:
            return None

    def word_type(self):
        return self._intersection(WordForm.types())

    def gender(self):
        return self._intersection(WordForm.genders())

    def subtype(self):
        return self._intersection(WordForm.subtypes())

    def subsubtype(self):
        return self._intersection(WordForm.subsubtypes())

    def case(self):
        return self._intersection(WordForm.cases())

    def transitive(self):
        return self._intersection(WordForm.transitives())

    def tense(self):
        return self._intersection(WordForm.tenses())

    def person(self):
        p = self._intersection(WordForm.persons())
        if not p:
            return None
        if p == '1-е':
            return 1
        elif p == '2-е':
            return 2
        elif p == '3-е':
            return 3
        elif p == 'безл':
            return 0
        return None

    def voice(self):
        return self._intersection(WordForm.voices())

    def is_active_participle(self) -> Optional[int]:
        if self.word_type() != 'прч':
            return None
        if self.voice() != 'страд':
            return 1
        return 0

    def participle_type(self) -> Optional[str]:
        p = self.is_active_participle()
        if p is None:
            return None
        assert(0 <= p <= 1)
        return ['страд', 'дейст'][p]

    def is_biaspectual(self) -> Optional[int]:
        if self.word_type() != 'гл':
            return None
        if '2вид' in self.attributes:
            return 1
        return 0

    def comparative(self) -> Optional[bool]:
        if self.word_type() != 'прл' and self.word_type() != 'нар':
            return None
        return self._intersection(WordForm.comparatives())

    def plurality(self) -> Plurality:
        maybe_plurality = self._intersection(['ед', 'мн'])
        if maybe_plurality == 'ед':
            return Plurality.Singular
        elif maybe_plurality == 'мн':
            return Plurality.Plural
        return Plurality.NA

    def animacy(self) -> Optional[int]:
        if self.word_type() != 'прл' and self.word_type() != 'сущ':
            return None
        if self._intersection(WordForm.animacies()) == 'неод':
            return 0
        elif self._intersection(WordForm.animacies()) == 'одуш':
            return 1
        return None

    def is_perfective(self) -> Optional[int]:
        if self.word_type() not in ['гл', 'прч', 'дееп']:
            return None
        mark = self._intersection(['сов', 'несов'])
        if mark == 'сов':
            return 1
        elif mark == 'несов':
            return 0
        return None

    def is_infinitive(self) -> Optional[int]:
        if self.word_type() != 'гл':
            return None
        if self._intersection(['инф']):
            return 1
        else:
            return 0

    def is_reflexive(self) -> Optional[int]:
        if self.word_type() != 'гл':
            return None
        if self._intersection(['воз']):
            return 1
        else:
            return 0

    def is_short(self) -> Optional[int]:
        if self.word_type() != 'прл' and self.word_type() != 'прч':
            return None
        s = self._intersection(['крат'])
        if s == 'крат':
            return 1
        return 0

