import zipfile
from glob import glob
import os
import shutil
import time
import sys

import winsound

__version__ = "1.0"
__status__ = "Production"

#extract_dir = r'!upload'                # конечная директория
#path_zip = glob(os.getcwd() + '/new') 	# директория с исходным архивом

def make_lists_files():
    """Создание попарных списков для архивирования.
    цикл for:
    после распаковки переходим в папку '105_ГБУЗ...'

    цикл for:
    удаляем все файлы, кроме .xml
    пропускаем исключение, если файл уже удален
    (нужно для работы цикла)

    Описание переменных:
    CCM, LCM, HHM, LHM - списки, с соответсвующими
    названиями файлов
    lists_files -- попарно составленные списки 'CCM_LCM' и 'HHM_LHM'
    check_on_off -- вкл/выкл функции проверки файлов (1-вкл, 0-выкл)

    """

    '''for file in os.listdir():
        if not file.lower().endswith('.xml', '.xls', '.xlsx', '.exe', '.py') and file not in ('new', 'dist', '__pycache__'):
            for f in file:
                try:
                    os.remove(file)
                except FileNotFoundError:
                    continue'''

    CCM = [f for f in os.listdir()if 'CCM' in f]
    LCM = [f for f in os.listdir()if 'LCM' in f]
    HHM = [f for f in os.listdir()if 'HHM' in f]
    LHM = [f for f in os.listdir()if 'LHM' in f]

    def check_files():
        """Проверка файлов на их 'парность' между собой.
        Сейчас выводится количество файлов, в идеале
        сделать вывод конкретных недостающих файлов.

        Реализовать либо в консольном виде, либо через PyQT.
        diff -- словарь, содержащий фразы с ошибками для конкретных ситуаций

        В данном случае каждый :
        Каждый if выполняется только при указанных условиях

        """

        diff = {'CCM_LCM':
                'Разное кол-во файлов CCM [' + str(len(CCM)) + '] и LCM [' +
                str(len(LCM)) + ']!',

                'HHM_LHM':
                'Разное кол-во файлов HHM [' + str(len(HHM)) + '] и LHM [' +
                str(len(LHM)) + ']!',

                'path_to_archive':
                os.getcwd()
                }

        if len(CCM) != len(LCM) and len(HHM) != len(LHM):  # не совпадают пары в 2-х списках
            print('АРХИВЫ НЕ СОЗДАНЫ!:', str(diff['CCM_LCM'] + diff['HHM_LHM']))
            os.system('pause')
            sys.exit()
        if len(CCM) != len(LCM):                           # не совпадаают пары только CCM_LCM 
            print('АРХИВЫ НЕ СОЗДАНЫ!:', str(diff['CCM_LCM']))
            os.system('pause')
            sys.exit()
        if len(HHM) != len(LHM):                           # не совпадаают пары только HHM_LHM
            print('АРХИВЫ НЕ СОЗДАНЫ!:', str(diff['HHM_LHM']))
            os.system('pause')
            sys.exit()

    check_on_off = 1

    if check_on_off :
        check_files()

    lists_files = {'CCM_LCM': list(zip(CCM, LCM)), 
                   'HHM_LHM': list(zip(HHM, LHM))
                   }

    make_zip_archives(lists_files)


def make_zip_archives(lists_files):
    """цикл for:
        проходимся по каждому значению словаря
        находим имя первого файла в каждом значении (а именно CCM, HHM)
        и называем его именем архив, добавляя .zip
             записываем файлы в архив, переходя при записи на один уровень выше
             по директории

    """
    os.chdir(os.getcwd()+'/new')

    for list_ in lists_files.values():
        for files in list_:
            name = files[0][:-4] + '.zip'
            z = zipfile.ZipFile(name, 'w', zipfile.ZIP_DEFLATED, compresslevel=9)
            for file in files:
                z.write(os.path.join(file))
            z.close()
    end_sound()
    cnt_zip = len([i for i in os.listdir() if i[-4:] == '.zip' ])
    print(F'Все архивы созданы ({cnt_zip} шт.)')


def end_sound():
    """Звуковой сигнал выполнения программы"""
    duration = 180  # millisecond
    freq = 550  # Hz
    time.sleep(0.1)
    winsound.Beep(freq, duration)