Config = {
  r'EditLabel\.Caption': {
    r'\bД[Гг]З\b': 'ЗДЗ',
  },
  r'Caption': {
    r'KL': 'P',
    r'DI': 'B',
    r'\bД[Гг]З\b': 'ЗДЗ',
  },
  r'Title|Items\.Strings': {
    r'\bKL(?=\d|\b)': 'P',
    r'\bDI(?=\d|\b)': 'B',
    r'\bД[Гг]З\b': 'ЗДЗ',
  },
  r'CaptionMask': {
    r'KL': 'P',
    r'DI': 'B',
  },
}

"""
Конфигурационный файл для описания замен в текстовых константах свойств
    компонентов фалов *.dfm представляет собой словарь словарей.
Ключами внешнего словаря являются регулярные выражения Python, обозначающие
    свойства компонентов, в текстовых значения которых будут производиться замены.
    Значенниями этих ключей являются внутренние словари собственно замен.
Ключами внутреннего словаря являются регулярные выражения Python, обозначающие
    что будет заменяться, а значения этих ключей являэтся выражения, на которые
    будут заменяться соответствующие ключи
        КРАТКИЙ СПРАВОЧНИК ПО RE
    .       Один любой символ, кроме новой строки \n.
    ?       0 или 1 вхождение шаблона слева
    +       1 и более вхождений шаблона слева
    *       0 и более вхождений шаблона слева
    \w      Любая цифра или буква (\W — все, кроме буквы или цифры)
    \d      Любая цифра [0-9] (\D — все, кроме цифры)
    \s      Любой пробельный символ (\S — любой непробельный символ)
    \b      Граница слова
    [..]    Один из символов в скобках ([^..] — любой символ, кроме тех, что в скобках)
    \       Экранирование специальных символов (\. означает точку или \+ — знак «плюс»)
    ^ и $   Начало и конец строки соответственно
    {n,m}   От n до m вхождений ({,m} — от 0 до m)
    a|b     Соответствует a или b
    (..)    Группирует выражение и возвращает найденный текст
    (?:..)  Группирует выражение и не возвращает найденный текст
    (?#..)  Комментарий. Содержимое в круглых скобках игнорируется
    (?=..)  соответствует позиции, сразу после которой начинается соответствие шаблону
    (?!..)  соответствует позиции, сразу после которой НЕ может начинаться шаблон
    (?<=..) соответствует позиции, которой может заканчиваться шаблон ... (Длина фикс)
    (?<!..) соответствует позиции, которой НЕ может заканчиваться шаблон
Экранируемые символы
\t, \n, \r  Символ табуляции, новой строки и возврата каретки соответственно
\\ \. \? \+ \* \^ \$ \| \[ \{ \( \)  Экранирование спецсимволов
\число      соотв группе с номером "число" (1..99)
"""