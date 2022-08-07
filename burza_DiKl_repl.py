0<1# :: ^
""" Со след строки bat-код до последнего :: и тройных кавычек
@setlocal enabledelayedexpansion & py -3 -x "%~f0" %*
@(IF !ERRORLEVEL! NEQ 0 echo ERRORLEVEL !ERRORLEVEL! & pause)
@exit /b !ERRORLEVEL! :: Со след строки py-код """

ps_ = '__cached__' not in dir() or not __doc__

from pathlib import Path
import os, sys, time, re
from copy import deepcopy
# from munch import Munch as eD
from addict import Dict as eD
import yaml
from pprint import pprint

debug = False  # True  #
pfp_out = None
repls_all = 0

# ============================================================================
def prinm(*ps, **ds):
    print(*ps, **ds)
    not debug and print(*ps, **ds, file=fstr)

# ============================================================================
def main():
    global debug, fold, pfp_out, Config

    fpConfig = sorted(Path('.').glob('Config.py'))
    if not fpConfig:
        prinm('? нет файлов Config.py')
        return
    exec(fpConfig[0].read_text('utf8'), globals())
#    prinm(Config)

    prinm('Проверка наличия необходимых файлов')
    if len(sys.argv) > 1:
        fold = Path(sys.argv[1])
    else:
        prinm(f'\t? Нет параметров, перетащите папку на скрипт')
        if debug:
            fold = Path('DFM_1')
        else:
            return

    if not fold.exists():
        prinm(f'\t? Путь "{fold.name}" не найден')
        return

    # Определение имени и пересоздание выходной папки  DFM_1_(3)
    if debug:
        pfp_out = Path('DFM_1_(3)')
        if pfp_out.exists():
            os.system(f'rd /q /s {pfp_out.name} >nul')
    else:
        fp_out = re.sub(r'(_\(\d+\))$', '', str(fold))
        for i in range(2, 10):
            pfp_out = Path(f'{fp_out}_({i})')
            if not pfp_out.exists():
                break
        else:
            tmp_outs = sorted(Path(fold.parent).glob(f'{fp_out}_(*)'),
                                    key=lambda x: x.stat().st_mtime)
            if fold in tmp_outs:
                tmp_outs.remove(fold)
            pfp_out = tmp_outs[0]
            os.system(f'rd /q /s {pfp_out} >nul')
    pfp_out.mkdir()
    print(f'Выходная папка: {pfp_out.name}')

    files_replaces(fold)

def pys_from_ems(ems):
    lines = []
    for s in ems.split('\n'):
        sps = re.match(r'(^\s*)(.*?)\s*$', s).groups()
        sps1 = ''.join(s.strip("'") if s[:1] == "'" else
            ''.join(re.sub(r'\#\d+', lambda m: chr(int(m.group(0)[1:])), s))
            for s in re.split(r"('[^']+')", sps[-1]))
        lines.append([sps[0], sps1])
    return lines

def ems_from_pys(pys):
    ems = []
    for sp, py in pys:
        emcs = [sp]
        ms = []
        for ch in py:
            if 32 <= ord(ch) < 128 and ch != "'":
                ms.append(ch)
                continue
            if ms:
                emcs.append(f"'{''.join(ms)}'")
                ms = []
            emcs.append(f"#{ord(ch)}")
        if ms:
            emcs.append(f"'{''.join(ms)}'")
        ems.append(''.join(emcs))
    return '\n'.join(ems)

# ============================================================================
def fun_reps(m):
    global repls_count, repls_all
    txt = m.group(0)
    for fnd, rep in reps.items():
        if re.match(fnd, txt):
            break
    else:
        return txt  # без каких либо замен, пожарный вариант
    txt, n = re.subn(fnd, rep, txt)
    repls_all += n
    repls_count += n
    return txt

# ============================================================================
def fun_props(m):
    global reps
    txt = m.group(0)

    for props, reps in Config.items():
        if re.match(f' *({props})', txt):
            break
    else:
        return txt  # без каких либо замен, пожарный вариант

    *prop, ems = re.split(r'( = \(?)', txt, 1)
    if prop and prop[-1][-1:] == '(' and  ems[-2:] == ')\n':
        ems = ems[:-2] + '\n'  # Удаление закрыв скобки
    pys = pys_from_ems(ems)

    for spy in pys:  # '|'.join Чтобы по ключам пройтись один раз
        spy[1], n = re.subn('|'.join(reps.keys()), fun_reps, spy[1])

    ems = ems_from_pys(pys)
    if prop and prop[-1][-1:] == '(':
        ems = ems[:-1] + ')\n'  # Добавление закрыв скобки

    txt = ''.join(prop) + ems
    return txt

# ============================================================================
def files_replaces(fold):
    """ Построение списка параметров переменных """
    global repls_count

    # выделяем все непустые дфм файлы
    fpnes = sorted((fpne for fpne in fold.glob('*_*_*.dfm') if fpne.is_file()
                    and re.match(r'\d+_\d+_\d+_\d+\.dfm', fpne.name)
                    and fpne.stat().st_size > 5),
                    key=lambda fpne: fpne.stat().st_size, reverse=True)
    if not fpnes:
        prinm(f'\t? Файлов "*_*_*.dfm" нет')
        return False
    prinm(f'Принято в обработку {len(list(fpnes))} непустых файлов')

    file_count = 0
    for i, fpne in enumerate(fpnes, 1):
        # Обрабатываем каждый файл по отдельности
        prinm(end=f'{i:3}: {fpne.name:16} ')
        txt = fpne.read_text('utf8')
        repls_count = 0
        txt, props_count = re.subn(r'(?m)^( +)(%s) = .+$\n(?:\1  .+\n)*' %
                                '|'.join(Config.keys()), fun_props, txt)
                                # '|'.join Чтобы по ключам пройтись один раз
        prinm(f'{props_count:5}/{repls_count:<5}')
        if repls_count == 0:
            continue
        file_count += 1
        pfp_out.joinpath(fpne.name).write_text(txt, 'utf8')

    prinm(f'\nИзменено файлов: {file_count}')
    prinm(f'Всего замен: {repls_all}')

# ============================================================================
if __name__ == '__main__':
    if debug:
        main()
    else:
        fne_txt_out = 'out.txt'
        with open(fne_txt_out, 'w', encoding='utf8') as fstr:
            main()
        if pfp_out is not None:
            os.system(f'move /y {fne_txt_out} {pfp_out} >nul')
            os.startfile(str(pfp_out / fne_txt_out))
        else:
            os.system(f'del /q {fne_txt_out} >nul')
    if not ps_: os.system('timeout /t 60')
