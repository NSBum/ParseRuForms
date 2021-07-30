## Russian Morphology Table

This is a script to generate a MySQL database containing 142,679 Russian words and their inflected morphologies. It is adapted from original work by М. Хаген and derivative work Yury Korol. Mostly, I've collected the database and the source text file in one location and made some changes in the database structure to make it more reflective of English terminology (for example _"soul"_ → _"animacy"_, etc.)

_(N.B. A word about the origin of this data. It seems to be derived from a work by М. Хаген "Полная парадигма. Морфология." This text is circulating on the web in various places and I'm unaware of whether this is licensed or the intellectual property of it is protected in some way. Any infringement is unintentional. This source text re-encoded in UTF-8 is included in the repository.)_ <sup>*</sup>

### Database source

The parsing of the original text file was done by Yury Korol as described in [this blog post](https://shra.ru/2017/03/morfologicheskijj-slovar-russkogo-yazyka-v-vide-sql-skripta/#comments) - _"Морфологический словарь русского языка в виде SQL скрипта"_. The format is logical for the most part and is noted below. I may work with this a little to clear up issues related to biaspectual verbs.

### Database structure

The MySQL database consists of a single table `words` containing the root words and inflected forms.

| Field        | Original field name* | Type         | Explanation                                                                           |
| :----------- | -------------------- | ------------ | :------------------------------------------------------------------------------------ |
| IID          | IID                  | int          | key (суррогатный ключ)                                                                |
| word         | word                 | varchar[100] | word form (root or inflected)                                                         |
| code         | code                 | int          | integer code of this word form                                                        |
| code_parent  | code_parent          | int          | an integer that refers to the base word form                                          |
| type         | type                 | foreign key  | row id in ru_words_types table                                                        |
| type_sub     | type_sub             | enum         | [1]                                                                                   |
| type_ssub    | type_ssub            | enum         | [2]                                                                                   |
| plural       | plural               | boolean      | 1 if plural or 0 otherwise                                                            |
| gender       | gender               | foreign key  |                                                                                       |
| wcase        | wcase                | foreign key  |                                                                                       |
| comp         | comp                 | enum         | comparative, superlative degree; one of 'сравн','прев'                                |
| animacy      | soul                 | boolean      | 1 if animate, 0 if inanimate                                                          |
| v_transit    | transit              | enum         | transitive vs intransitive; one of 'перех','непер','пер/не'; переходность глагола.    |
| v_perfect    | perfect              | boolean      | 1 if perfective, 0 if imperfective                                                    |
| v_person     | face                 | enum         | person (лицо глагола), 1,2, or 3 or 0 = ‘безл’                                        |
| v_biaspect   | kind                 | enum         | 1 if biaspectual, 0 if not; None if not a verb                                        |
| v_tense      | time                 | enum         | one of ‘прош’, ‘наст’, ‘буд’                                                          |
| v_inf        | inf                  | boolean      | 1 if an infinitive, 0 otherwise                                                       |
| v_reflect    | vozv                 | boolean      | 1 if reflexive, 0 otherwise                                                           |
| v_voice      | nakl                 | enum         | one of 'пов','страд'; наклонение или залог глагола. 'пов' = 'повелительное наклонение |
| short        | short                | bool         | 1 if adjective short form, 0 or NULL otherwise                                        |
| v_activepart | -                    | varchar[5]   | type of participle                                                                    |
[ru_words]

<sup>*</sup> A comment from the database creator, notes the following about licensing:
> База распространялась бесплатно автором в виде текстовых файлов. Я лишь потрудился перевести её в sql скрипт. Потому распространяется это скрипт «бездваздмездно», с учетом того, что вы используете это как есть, принимая на себя ответственность за все возможные риски.

<sup>†</sup> This pertains, of course, only to verbs. As a practical matter in the table as previously parsed, the value of this field is always either `NULL` or "2вид". The meaning of the latter appears to be "biaspectual" and in that case the `perfect` field is `NULL`.

#### Part of speech types table

This table is `ru_words_types`.

| Field    | Type        | Explanation                 |
| :------- | ----------- | :-------------------------- |
| id       | TINYINT     | row index                   |
| pos      | VARCHAR[6]  | Russian desc as in original |
| pos_full | VARCHAR[15] | Full Russian desc           |
| pos_en   | VARCHAR[20] | English desc                |
| upos     | VARCHAR[5]  | UD UPOS type                |

#### Cases table

This table is `ru_words_cases`.

| Field     | Type        | Explanation                 |
| :-------- | ----------- | :-------------------------- |
| id        | TINYINT     | row index                   |
| wcase     | VARCHAR[4]  | Russian desc as in original |
| case_full | VARCHAR[15] | Full Russian desc           |
| case_en   | VARCHAR[15] | English desc                |
| case_ud   | VARCHAR[5]  | Case universal dependency   |

#### Genders table

This table is `ru_words_genders`.

| Field   | Type    | Explanation                 |
| :------ | ------- | :-------------------------- |
| id      | TINYINT | row index                   |
| ru      | VARCHAR | Russian desc as in original |
| ru_full | VARCHAR | Full Russian desc           |
| en      | VARCHAR | English desc                |

### References

Another derivative project from Hagen's text file is a sqlite3 database with a Java access wrapper [Github: sdreger/WordsFinder](https://github.com/sdreger/WordsFinder). This developer has made some attempt to simplify the structure a bit and make the data more relational.


part of speech - one of 'част','межд','прл','прч','сущ','нар','гл','дееп',  'союз','предик','предл','ввод','мест','числ'

### Usage

#### Building the MySQL tables

TBD

#### Querying the database

Some examples of useful database queries:

1. Find the genitive (singular and plural) of the word _собака_:

```sql
SELECT w.code, w.code_parent, w.word, w.wcase
FROM ru_words w 
INNER JOIN ru_roots AS r on w.code_parent = r.code
INNER JOIN ru_words_cases c ON c.id = w.wcase 
WHERE r.word = 'собака' AND c.case_en = 'genitive';
```

### Notes

[1]: Subtypes: one of 'поряд', 'кол', 'собир', 'неопр', 'врем', 'обст', 'опред', 'счет', 'неизм'; подтипы используются в основном для числительных и наречий.

[2]: Sub-subtype - one of 'кач','спос','степ','места','напр','врем','цель', 'причин'; под-подтипы задействованы только для наречий.

grammatical case, one of 'им','род','дат','вин','тв','пр','зват','парт','мест'

one of 'муж','жен','ср','общ'

