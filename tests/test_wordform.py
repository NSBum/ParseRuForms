import unittest
import wordforms


class TestWordForms(unittest.TestCase):
    def testReturnTypeValid(self):
        rowstr = 'собачий\tпрл ед муж им\t39343'
        w = wordforms.WordForm(rowstr)
        self.assertEqual(w.word_type(), 'прл')

    def testReturnGenderMasculineValid(self):
        rowstr = 'собачий\tпрл ед муж им\t39343'
        w = wordforms.WordForm(rowstr)
        self.assertEqual(w.gender(), 'муж')

    def testReturnPluralitySingular(self):
        rowstr = 'собачий\tпрл ед муж им\t39343'
        w = wordforms.WordForm(rowstr)
        self.assertEqual(wordforms.Plurality.Singular, w.plurality())

    def testReturnPluralityPlural(self):
        rowstr = 'собачие\tпрл мн муж им\t39343'
        w = wordforms.WordForm(rowstr)
        self.assertEqual(wordforms.Plurality.Plural, w.plurality())

    def testReturnPluralityNotApplicable(self):
        rowstr = 'нехорошо\tнар опред кач\t202599'
        w = wordforms.WordForm(rowstr)
        self.assertEqual(wordforms.Plurality.NA, w.plurality())

    def testReturnSubtypeA(self):
        rowstr = 'одиннадцатый\tчисл поряд ед муж им\t4015498'
        w = wordforms.WordForm(rowstr)
        self.assertEqual('поряд', w.subtype())

    def testReturnSubtypeB(self):
        rowstr = 'перванш\tпрл неизм\t99820'
        w = wordforms.WordForm(rowstr)
        self.assertEqual('неизм', w.subtype())

    def testReturnSubsubtypeA(self):
        rowstr = 'приятельски\tнар опред спос\t204590'
        w = wordforms.WordForm(rowstr)
        self.assertEqual('спос', w.subsubtype())

    def testReturnCaseWhenPresent(self):
        rowstr = 'собачие\tпрл мн муж им\t39343'
        w = wordforms.WordForm(rowstr)
        self.assertEqual('им', w.case())

    def testReturnNoneCaseWhenAbsent(self):
        rowstr = 'нехорошо\tнар опред кач\t202599'
        w = wordforms.WordForm(rowstr)
        self.assertIsNone(w.case())

    def testReturnTransitiveWhenPresent(self):
        rowstr = 'проанатомировать\tгл сов перех инф\t174686'
        w = wordforms.WordForm(rowstr)
        self.assertEqual('перех', w.transitive())

    def testReturnIntrantiveWhenPresent(self):
        rowstr = 'пробавляться\tгл несов непер воз инф\t191486'
        w = wordforms.WordForm(rowstr)
        self.assertEqual('непер', w.transitive())

    def testReturnTransIntransitiveWhenPresent(self):
        rowstr = 'пробалтывать\tгл несов пер/не инф\t184997'
        w = wordforms.WordForm(rowstr)
        self.assertEqual('пер/не', w.transitive())

    def testReturnFutureTense(self):
        rowstr = 'пробаню\tгл сов перех буд ед 1-е\t1793819'
        w = wordforms.WordForm(rowstr)
        self.assertEqual('буд', w.tense())

    def testReturnFirstPerson(self):
        rowstr = 'пробаню\tгл сов перех буд ед 1-е\t1793819'
        w = wordforms.WordForm(rowstr)
        self.assertEqual(1, w.person())

    def testReturnSecondPerson(self):
        rowstr = 'пересечешься\tгл сов непер воз буд ед 2-е\t1898948'
        w = wordforms.WordForm(rowstr)
        self.assertEqual(2, w.person())

    def testReturnThirdPerson(self):
        rowstr = 'пересечется\tгл сов непер воз буд ед 3-е\t1898949'
        w = wordforms.WordForm(rowstr)
        self.assertEqual(3, w.person())

    def testReturnNoneForPersonlessWord(self):
        rowstr = 'микроцефалия\tсущ неод ед жен им\t151526'
        w = wordforms.WordForm(rowstr)
        self.assertIsNone(w.person())

    def testActiveParticiplePositive(self):
        rowstr = 'проделавший\tпрч сов перех прош ед муж вин\t2146394'
        w = wordforms.WordForm(rowstr)
        self.assertTrue(w.is_active_participle())

    def testActiveParticipleNegative(self):
        rowstr = 'проделанный\tпрч сов перех страд прош ед муж им\t2052749'
        w = wordforms.WordForm(rowstr)
        self.assertFalse(w.is_active_participle())

    def testBiaspectualPositive(self):
        rowstr = 'пробалтывать\tгл несов пер/не инф 2вид\t184997'
        w = wordforms.WordForm(rowstr)
        self.assertTrue(w.is_biaspectual())

    def testBiaspectualNegative(self):
        rowstr = 'пробалтывать\tгл несов пер/не инф\t184997'
        w = wordforms.WordForm(rowstr)
        self.assertFalse(w.is_biaspectual())

    def testBiaspectualNA(self):
        rowstr = 'приятельски\tнар опред спос\t204590'
        w = wordforms.WordForm(rowstr)
        self.assertIsNone(w.is_biaspectual())

    def testComparativeAdverb(self):
        rowstr = 'попродолжительнее\tнар сравн\t4062366'
        w = wordforms.WordForm(rowstr)
        self.assertEqual('сравн', w.comparative())

    def testNonComparativeAdverb(self):
        rowstr = 'хорошо\tнар опред кач\t206247'
        w = wordforms.WordForm(rowstr)
        self.assertNotEqual('сравн', w.comparative())
        self.assertNotEqual('прев', w.comparative())

    def testSuperlativeAdj(self):
        rowstr = 'храбрейший\tпрл прев ед муж им\t4024848'
        w = wordforms.WordForm(rowstr)
        self.assertEqual('прев', w.comparative())