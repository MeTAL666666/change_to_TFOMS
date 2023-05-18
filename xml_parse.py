import os
import xml.etree.ElementTree as ET
from shutil import rmtree
from zip_archive_create import *

# удаляем папку с измененными файлами, если она есть
if os.path.exists('new'):
	rmtree('new')
# составляем список файлов .xml
files_list = []
for d, dirs, files in os.walk(os.getcwd()):
	for i in files:
		if i.lower().endswith('.xml'):
			files_list.append(i)
print(files_list, '\n')
message = []
# цикл для обработки всех файлов .xml
for file in files_list:
	print(f'Просмотр файла {file}...')
	tree = ET.parse(file)
	root = tree.getroot()
	# цикл для прохождения по каждой записи в каждом файле
	for elem in root.findall('ZAP'):					# тэг начала каждой записи
		for i in elem.findall("./Z_SL[FOR_POM='2']"):
			# для взрослых
			for j in i.findall("./SL[PODR='97']"):
				for k in j.findall("LPU_1"):
					if k.text in ['105R005', '105R008', '105R015', '105R014',
								 '105R016', '105R037', '105R002', '105R012',
								 '105R006', '105R035', '105R009', '105R007', 
								 '105R039', '105R003', '105R010', '105R013', 
								 '105R036', '105R038', '105R011', '105R040', 
								 '105R004', '105R001', '105R041']:
						k.text = '1050000'
					elif k.text in ['105R031', '105R033', '105R018', '105R034', '105R017']:
						k.text = '105R032'
					elif k.text in ['105R025', '105R021', '105R022']:
						k.text = '105R026'
					elif k.text in ['105R027', '105R029', '105R028']:
						k.text = '105R030'
					elif k.text in ['105R023', '105R020', '105R024']:
						k.text = '105R019'

				for k in j.findall("USL/LPU_1"):
					if k.text in ['105R005', '105R008', '105R015', '105R014',
								 '105R016', '105R037', '105R002', '105R012',
								 '105R006', '105R035', '105R009', '105R007', 
								 '105R039', '105R003', '105R010', '105R013', 
								 '105R036', '105R038', '105R011', '105R040', 
								 '105R004', '105R001', '105R041']:
						k.text = '1050000'
					elif k.text in ['105R031', '105R033', '105R018', '105R034', '105R017']:
						k.text = '105R032'
					elif k.text in ['105R025', '105R021', '105R022']:
						k.text = '105R026'
					elif k.text in ['105R027', '105R029', '105R028']:
						k.text = '105R030'
					elif k.text in ['105R023', '105R020', '105R024']:
						k.text = '105R019'

				for k in j.findall('IDDOKT'):
					k.text = '018-607-077 48'

				for k in j.findall('USL/MR_USL_N/CODE_MD'):
					k.text = '018-607-077 48'

				for k in j.findall("PRVS"):
					k.text = '76'

				for k in j.findall("USL/MR_USL_N/PRVS"):
					k.text = '76'
			
			# для детей
			for j in i.findall("./SL[PODR='68']"):
				for k in j.findall("LPU_1"):
					if k.text in ['105R005', '105R008', '105R015', '105R014',
								 '105R016', '105R037', '105R002', '105R012',
								 '105R006', '105R035', '105R009', '105R007', 
								 '105R039', '105R003', '105R010', '105R013', 
								 '105R036', '105R038', '105R011', '105R040', 
								 '105R004', '105R001', '105R041']:
						k.text = '1050000'
					elif k.text in ['105R031', '105R033', '105R018', '105R034', '105R017']:
						k.text = '105R032'
					elif k.text in ['105R025', '105R021', '105R022']:
						k.text = '105R026'
					elif k.text in ['105R027', '105R029', '105R028']:
						k.text = '105R030'
					elif k.text in ['105R023', '105R020', '105R024']:
						k.text = '105R019'

				for k in j.findall("USL/LPU_1"):
					if k.text in ['105R005', '105R008', '105R015', '105R014',
								 '105R016', '105R037', '105R002', '105R012',
								 '105R006', '105R035', '105R009', '105R007', 
								 '105R039', '105R003', '105R010', '105R013', 
								 '105R036', '105R038', '105R011', '105R040', 
								 '105R004', '105R001', '105R041']:
						k.text = '1050000'
					elif k.text in ['105R031', '105R033', '105R018', '105R034', '105R017']:
						k.text = '105R032'
					elif k.text in ['105R025', '105R021', '105R022']:
						k.text = '105R026'
					elif k.text in ['105R027', '105R029', '105R028']:
						k.text = '105R030'
					elif k.text in ['105R023', '105R020', '105R024']:
						k.text = '105R019'

				for k in j.findall('IDDOKT'):
					k.text = '053-643-138 45'

				for k in j.findall('USL/MR_USL_N/CODE_MD'):
					k.text = '053-643-138 45'

				for k in j.findall("PRVS"):
					k.text = '49'

				for k in j.findall("USL/MR_USL_N/PRVS"):
					k.text = '49'
	# создать папку для размещения измененных файлов
	if not os.path.exists('new'):
		os.makedirs('new')
	print(f'Изменение данных в файле {file}...\n')
	tree.write('new/' + file, encoding="windows-1251")
print("Все файлы обработаны" + '\nСоздание архивов...')
make_lists_files()
os.system("pause")