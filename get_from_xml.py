import os
import xml.etree.ElementTree as ET
import sys
from shutil import rmtree
import csv
from tqdm import tqdm

def write_to_csv(data):
	with open ('export.csv', 'a', encoding='utf-8') as file:
		writer = csv.writer	(file, delimiter='\t')
		writer.writerow((data['DATE'],
							 data['LPU_1'],
							 data['NHISTORY'],
							 data['FNS']))

# составляем список файлов .xml
HHM = []
LHM = []
CCM = []
LCM = []

# цикл для обработки всех файлов .xml
for d, dirs, files in os.walk(os.getcwd()):
	for i in files:
		if i.startswith('HHM') and i.lower().endswith('.xml') and 'old' not in i.lower():
			HHM.append(i)
		elif i.startswith('LHM') and i.lower().endswith('.xml') and 'old' not in i.lower():
			LHM.append(i)
		elif i.startswith('CCM') and i.lower().endswith('.xml') and 'old' not in i.lower():
			CCM.append(i)
		elif i.startswith('LCM') and i.lower().endswith('.xml') and 'old' not in i.lower():
			LCM.append(i)

print(f'HHM: {HHM}')
print(f'LHM: {LHM}')
print(f'------------------')
print(f'CCM: {CCM}')
print(f'LCM: {LCM}')


if os.path.exists('export.csv'):
		os.remove('export.csv')

data = {'DATE': 'Дата',
		'LPU_1': 'Район',
		'NHISTORY': '№ КВ',
		'FNS': 'ФИО'}
# запись заголовков
write_to_csv(data)

data.clear ()
# для обычных реестров
for file_hhm, file_lhm in zip(HHM, LHM):
	print(f'Просмотр файлов {file_hhm} и {file_lhm}...')
	tree_hhm = ET.parse(file_hhm)
	root_hhm = tree_hhm.getroot()
	tree_lhm = ET.parse(file_lhm)
	root_lhm = tree_lhm.getroot()

	# цикл для прохождения по каждой записи в каждом HHM файле
	for elem in root_hhm.findall('ZAP'):					# тэг начала каждой записи
		for j in elem.findall("./Z_SL[FOR_POM='2']"):
			for i in j.findall("./SL/PODR"):
				if i.text in ['68', '97']:
					data[''.join([k.text for k in j.findall("./IDCASE")])] = { 
																			'DATE': ''.join([k.text for k in j.findall("./DATE_Z_1")]),
																			'LPU_1': ''.join([k.text for k in j.findall("./SL/LPU_1")]),
																			'NHISTORY': ''.join([k.text for k in j.findall("./SL/NHISTORY")])
																			}
	# поиск данных о пациенте в LHM файле
	for id_ in tqdm(data.keys()):
		for elem in root_lhm.findall('PERS'):
			for i in elem.findall("./[ID_PAC='%s']" % id_):
				FNS = []
				for k in i.findall("FAM"):
					FNS.append(k.text)
				for k in i.findall("IM"):
					FNS.append(k.text.capitalize ())
				for k in i.findall("OT"):
					FNS.append(k.text.capitalize ())
				data[str(id_)]['FNS'] = ' '.join([k for k in FNS])
				# замена кодов LPU на названия районов
				if data[str(id_)]['LPU_1'] == '1050000':
					data[str(id_)]['LPU_1'] = 'Пенза'
				elif data[str(id_)]['LPU_1'] == '105R032':
					data[str(id_)]['LPU_1'] = 'Н.Ломов'
				elif data[str(id_)]['LPU_1'] == '105R026':
					data[str(id_)]['LPU_1'] = 'Сердобск'
				elif data[str(id_)]['LPU_1'] == '105R030':
					data[str(id_)]['LPU_1'] = 'Кузнецк'
				elif data[str(id_)]['LPU_1'] == '105R019':
					data[str(id_)]['LPU_1'] = 'Каменка'
				# запись в итоговый CSV файл
				write_to_csv(data[str(id_)])
data.clear ()
# для онко реестров
for file_ccm, file_lcm in zip(CCM, LCM):
	print(f'Просмотр файлов {file_ccm} и {file_lcm}...')
	tree_ccm = ET.parse(file_ccm)
	root_ccm = tree_ccm.getroot()
	tree_lcm = ET.parse(file_lcm)
	root_lcm = tree_lcm.getroot()

	# цикл для прохождения по каждой записи в каждом CCM файле
	for elem in root_ccm.findall('ZAP'):					# тэг начала каждой записи
		for j in elem.findall("./Z_SL[FOR_POM='2']"):
			for i in j.findall("./SL/PODR"):
				if i.text in ['68', '97']:
					data[''.join([k.text for k in j.findall("./IDCASE")])] = { 
																			'DATE': ''.join([k.text for k in j.findall("./DATE_Z_1")]),
																			'LPU_1': ''.join([k.text for k in j.findall("./SL/LPU_1")]),
																			'NHISTORY': ''.join([k.text for k in j.findall("./SL/NHISTORY")])
																			}
	# поиск данных о пациенте в LCM файле
	for id_ in tqdm(data.keys()):
		for elem in root_lcm.findall('PERS'):
			for i in elem.findall("./[ID_PAC='%s']" % id_):
				FNS = []
				for k in i.findall("FAM"):
					FNS.append(k.text)
				for k in i.findall("IM"):
					FNS.append(k.text.capitalize ())
				for k in i.findall("OT"):
					FNS.append(k.text.capitalize ())
				data[str(id_)]['FNS'] = ' '.join([k for k in FNS])
				# замена кодов LPU на названия районов
				if data[str(id_)]['LPU_1'] == '1050000':
					data[str(id_)]['LPU_1'] = 'Пенза'
				elif data[str(id_)]['LPU_1'] == '105R032':
					data[str(id_)]['LPU_1'] = 'Н.Ломов'
				elif data[str(id_)]['LPU_1'] == '105R026':
					data[str(id_)]['LPU_1'] = 'Сердобск'
				elif data[str(id_)]['LPU_1'] == '105R030':
					data[str(id_)]['LPU_1'] = 'Кузнецк'
				elif data[str(id_)]['LPU_1'] == '105R019':
					data[str(id_)]['LPU_1'] = 'Каменка'
				# запись в итоговый CSV файл
				write_to_csv(data[str(id_)])

print('\nСписок создан!')
os.system("pause")