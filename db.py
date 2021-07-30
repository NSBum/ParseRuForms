import mysql.connector as mysql
from files import fp_to_create_tables
import config
from wordforms import WordForm, Plurality
from typing import Union


def _query_value_or_skip(value: Union[int, str, bool, Plurality], q: str, quoted: bool) -> str:
    if isinstance(value, Plurality):
        if value and (value == Plurality.Singular or value == Plurality.Plural):
            return q + f'{value.value}, '
        else:
            return q + "NULL, "
    if isinstance(value, int):
        if quoted:
            return q + f'"{value}" ,'
        else:
            return q + f'{value}, '
    if value:
        if quoted:
            return q + f'"{value}" ,'
        else:
            return q + f'{value}, '
    else:
        return q + "NULL, "


class Database(object):
    def __init__(self):
        self.conn = None
        self.cursor = None

    def _setup_cases_table(self):
        self.cursor.execute('USE ru_morph')
        try:
            q = '''DROP TABLE IF EXISTS `ru_words_cases`'''
            self.cursor.execute(q)
            q = '''CREATE TABLE `ru_words_cases` (
                   `id` tinyint unsigned NOT NULL AUTO_INCREMENT COMMENT 'row index',
                   `wcase` varchar(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT 'case name in the Hagen file',
                   `case_full` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT 'full case name in Russian',
                   `case_en` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT 'case name in English',
                   `case_ud` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT 'case in Universal dependencies',
                   PRIMARY KEY (`id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci'''
            self.cursor.execute(q)
            self.cursor.execute('LOCK TABLES `ru_words_cases` WRITE')
            q = '''INSERT INTO `ru_words_cases` (`id`, `wcase`, `case_full`, `case_en`, `case_ud`)
                   VALUES
                        (1,'им','именительный','nominative','Nom'),
                        (2,'род','родительный','genitive','Gen'),
                        (3,'дат','дательный','dative','Dat'),
                        (4,'вин','винительный','accusative','Acc'),
                        (5,'тв','творительный','instrumental','Ins'),
                        (6,'пр','предложный','prepositional','Loc'),
                        (7,'зват','звательный','vocative','Voc'),
                        (8,'парт','разделительный','partitive','Par'),
                        (9,'мест','местный','locative','Loc')'''
            self.cursor.execute(q)
        except mysql.errors.DatabaseError:
            pass
        self.cursor.execute('UNLOCK TABLES')

    def _setup_genders_table(self):
        try:
            self.cursor.execute('USE ru_morph')
            self.cursor.execute('DROP TABLE IF EXISTS `ru_words_genders`')
            q = '''CREATE TABLE `ru_words_genders` (
                        `id` tinyint unsigned NOT NULL AUTO_INCREMENT COMMENT 'row index',
                        `ru` varchar(3) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT 'code used in Hagen table',
                        `ru_full` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT 'Russian name of gender',
                        `en` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT 'English name of gender',
                    PRIMARY KEY (`id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci'''
            self.cursor.execute(q)
            self.cursor.execute('LOCK TABLES `ru_words_genders` WRITE')
            q = '''INSERT INTO `ru_words_genders` (`id`, `ru`, `ru_full`, `en`)
                   VALUES
                        (1,'муж','мужской','masculine'),
                        (2,'жен','женский','feminine'),
                        (3,'ср','средний','neuter'),
                        (4,'общ','общий','common gender')'''
            self.cursor.execute(q)
            self.cursor.execute('UNLOCK TABLES')
        except mysql.errors.DatabaseError:
            pass

    def _setup_roots_table(self):
        try:
            self.cursor.execute('USE ru_morph')
            self.cursor.execute('DROP TABLE IF EXISTS `ru_roots`')
            q = '''CREATE TABLE `ru_roots` (
                    `id` int unsigned NOT NULL AUTO_INCREMENT,
                    `code` int DEFAULT NULL,
                    `word` varchar(100) DEFAULT NULL,
                    PRIMARY KEY (`id`),
                    FULLTEXT KEY `root_word` (`word`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci'''
            self.cursor.execute(q)
        except mysql.errors.DatabaseError:
            pass

    def _setup_persons_table(self):
        self.cursor.execute('USE ru_morph')
        try:
            self.cursor.execute('DROP TABLE IF EXISTS `ru_words_person`')
            q = '''CREATE TABLE `ru_words_person` (
                        `id` int unsigned NOT NULL AUTO_INCREMENT COMMENT 'row index',
                        `desc` varchar(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT 'the code used in Hagen txt file',
                        `number` tinyint unsigned DEFAULT NULL COMMENT '1 for 1st person, etc. 0 for безл',
                    PRIMARY KEY (`id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci'''
            self.cursor.execute(q)
            self.cursor.execute('LOCK TABLES `ru_words_person` WRITE')
            q = '''INSERT INTO `ru_words_person` (`id`, `desc`, `number`)
                   VALUES
                       (1,'1-е',1),
                       (2,'2-е',2),
                       (3,'3-е',3),
                       (4,'безл',0)'''
            self.cursor.execute(q)
        except mysql.errors.DatabaseError:
            pass
        self.cursor.execute('UNLOCK TABLES')

    def _setup_types_table(self):
        self.cursor.execute('USE ru_morph')
        try:
            self.cursor.execute('DROP TABLE IF EXISTS `ru_words_types`')
            q = '''CREATE TABLE `ru_words_types` (
                        `id` tinyint unsigned NOT NULL AUTO_INCREMENT,
                        `pos` varchar(6) NOT NULL DEFAULT '',
                        `pos_full` varchar(15) DEFAULT NULL,
                        `pos_en` varchar(20) DEFAULT NULL,
                        `upos` varchar(5) DEFAULT NULL,
                    PRIMARY KEY (`id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci'''
            self.cursor.execute(q)
            self.cursor.execute('LOCK TABLES `ru_words_types` WRITE')
            q = '''INSERT INTO `ru_words_types` (`id`, `pos`, `pos_full`, `pos_en`, `upos`)
                   VALUES
                        (1,'част','частица','particle','PART'),
                        (2,'межд','междометие','interjection','INTJ'),
                        (3,'прл','прилагательное','adjective','ADJ'),
                        (4,'прч','причастие','participle','VERB'),
                        (5,'сущ','существительное','noun','NOUN'),
                        (6,'нар','наречие','adverb','ADV'),
                        (7,'гл','глагол','verb','VERB'),
                        (8,'дееп','деепричастие','adverbial participle','VERB'),
                        (9,'союз','союз','conjunction','CCONJ'),
                        (10,'предик','предикатив','predicative','ADJ'),
                        (11,'предл','предлог','preposition','ADP'),
                        (12,'ввод','вводное слово','introductory','ADV'),
                        (13,'мест','местоимение','pronoun','PRON'),
                        (14,'числ','числительное','numeral','NUM'),
                        (15, 'мод','модальное', 'modal', 'ADV'),
                        (16, 'неизв', 'неизвестно', 'unknown', '?')'''
            self.cursor.execute(q)
        except mysql.errors.DatabaseError:
            pass
        self.cursor.execute('UNLOCK TABLES')

    def _setup_main_table(self):
        self.cursor.execute('USE ru_morph')
        try:
            self.cursor.execute('DROP TABLE IF EXISTS `ru_words`')
            q = '''CREATE TABLE `ru_words` (
                  `IID` int NOT NULL AUTO_INCREMENT,
                  `word` varchar(100) NOT NULL,
                  `code` int NOT NULL,
                  `code_parent` int NOT NULL,
                  `type` tinyint unsigned NOT NULL,
                  `type_sub` enum('поряд','кол','собир','неопр','врем','обст','опред','счет','неизм') DEFAULT NULL,
                  `type_ssub` enum('кач','спос','степ','места','напр','врем','цель','причин') DEFAULT NULL,
                  `plural` tinyint DEFAULT NULL,
                  `gender` tinyint unsigned DEFAULT NULL,
                  `wcase` tinyint unsigned DEFAULT NULL,
                  `comp` enum('сравн','прев') DEFAULT NULL,
                  `animacy` tinyint DEFAULT NULL,
                  `v_transit` enum('перех','непер','пер/не') CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
                  `v_perfect` tinyint DEFAULT NULL,
                  `v_person` tinyint unsigned DEFAULT NULL,
                  `v_biaspect` tinyint DEFAULT NULL,
                  `v_tense` enum('прош','наст','буд') DEFAULT NULL,
                  `v_inf` tinyint DEFAULT NULL,
                  `v_reflex` tinyint DEFAULT NULL,
                  `v_voice` enum('пов','страд') DEFAULT NULL,
                  `short` tinyint(1) DEFAULT NULL,
                  `v_activepart` varchar(5) DEFAULT NULL COMMENT 'NULL if not participle',
                  PRIMARY KEY (`IID`),
                  KEY `ru_word_type` (`type`),
                  KEY `ru_word_case_key` (`wcase`),
                  KEY `ru_word_gender_key` (`gender`),
                  KEY `code_index` (`code`),
                  KEY `code_parent_index` (`code_parent`),
                  FULLTEXT KEY `word_index` (`word`),
                  CONSTRAINT `ru_word_case_key` FOREIGN KEY (`wcase`) REFERENCES `ru_words_cases` (`id`),
                  CONSTRAINT `ru_word_gender_key` FOREIGN KEY (`gender`) REFERENCES `ru_words_genders` (`id`),
                  CONSTRAINT `ru_word_type` FOREIGN KEY (`type`) REFERENCES `ru_words_types` (`id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3'''
            self.cursor.execute(q)
        except mysql.errors.DatabaseError:
            pass
        self.cursor.execute('UNLOCK TABLES')

    def setup_tables(self):
        self._setup_cases_table()
        self._setup_genders_table()
        self._setup_persons_table()
        self._setup_types_table()
        self._setup_main_table()

    def connect(self):
        user = config.dbconfig['user']
        pw = config.dbconfig['pw']
        self.conn = mysql.connect(
            host="localhost",
            user=user,
            passwd=pw
        )
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()

    def show_dbs(self):
        self.cursor.execute('SHOW DATABASES')
        databases = self.cursor.fetchall()
        print(databases)

    def save_word(self, w: WordForm):
        if w.attributes is None or len(w.attributes) < 1:
            print(f'Missing attributes - {w} - skipped')
            return
        q = '''INSERT INTO `ru_words` (`word`, `code`, `code_parent`, `type`, `type_sub`, `type_ssub`, `plural`, 
        `gender`, `wcase`, `comp`, `animacy`, `v_transit`, `v_perfect`, `v_person`, `v_biaspect`, `v_tense`, `v_inf`, 
        `v_reflex`, `v_voice`, `short`, `v_activepart`) '''
        q += f'VALUES ( "{w.form}", {w.code}, {w.parent_code}, '
        wtype = w.word_type()
        type_code = WordForm.type_code_for_type(wtype)
        q = _query_value_or_skip(type_code, q, False)
        q = _query_value_or_skip(w.subtype(), q, True)
        q = _query_value_or_skip(w.subsubtype(), q, True)
        q = _query_value_or_skip(w.plurality(), q, False)
        gender = w.gender()
        gc = WordForm.gender_code_for_gender(gender)
        if gc:
            q = _query_value_or_skip(gc, q, False)
        else:
            q += 'NULL, '
        wcase = w.case()
        cc = WordForm.case_code_for_case(wcase)
        if cc:
            q = _query_value_or_skip(cc, q, False)
        else:
            q += 'NULL, '
        q = _query_value_or_skip(w.comparative(), q, True)
        q = _query_value_or_skip(w.animacy(), q, False)
        q = _query_value_or_skip(w.transitive(), q, True)
        q = _query_value_or_skip(w.is_perfective(), q, False)
        q = _query_value_or_skip(w.person(), q, False)
        q = _query_value_or_skip(w.is_biaspectual(), q, False)
        q = _query_value_or_skip(w.tense(), q, True)
        q = _query_value_or_skip(w.is_infinitive(), q, False)
        q = _query_value_or_skip(w.is_reflexive(), q, False)
        q = _query_value_or_skip(w.voice(), q, True)
        q = _query_value_or_skip(w.is_short(), q, False)
        q = _query_value_or_skip(w.participle_type(), q, True)
        q = q.rstrip(', ')
        q += f')'
        # print(q)
        try:
            self.cursor.execute(q)
        except mysql.errors.IntegrityError:
            print(f'ERROR - query = {q}')

    def load_all_pos(self):
        q = 'SELECT `id`, `pos` FROM `ru_words_types`'
        self.cursor.execute(q)
        r = self.cursor.fetchall()
        WordForm.pos_list = r

    def load_all_genders(self):
        q = 'SELECT `id`, `ru` FROM `ru_words_genders`'
        self.cursor.execute(q)
        r = self.cursor.fetchall()
        WordForm.gender_list = r

    def load_all_cases(self):
        # SELECT c.id FROM ru_words_cases c WHERE c.wcase = "{wcase}"
        q = 'SELECT `id`, `wcase` FROM `ru_words_cases`'
        self.cursor.execute(q)
        r = self.cursor.fetchall()
        WordForm.case_list = r

    def load_normalizations(self):
        self.load_all_cases()
        self.load_all_genders()
        self.load_all_pos()

    def derive_roots(self):
        q = ''' INSERT INTO ru_roots (code, word) 
                SELECT `code`, word FROM ru_words WHERE code_parent = 0
        '''
        self.cursor.execute(q)
