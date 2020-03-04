import os
from pathlib import Path
import textract
import re

first_letter = ''
pattern0 = re.compile(r'(Frühjahr|Herbst|Frühsommer)?(\s\d\d)?\s?\d\d\d\d')
pattern1 = re.compile(r'Straßennamen:[\n\s]*([^\n:]+)$', re.MULTILINE)
pattern2 = re.compile(r'Stand:?[\n\s]*([^\n]+)', re.MULTILINE)
pattern3 = re.compile(r'_(\d+).pdf')

source = 'static/schleichwege'
target = 'content/schleichwege-streets.md'

with open(target, 'w') as markdown_file:
	for filename in sorted(os.listdir(source)):
		basename = Path(filename).stem

		if not filename.endswith('pdf'):
			continue

		# Extract text from PDF
		text = textract.process(f'{source}/{filename}').decode("utf-8")

		# Remove date
		text = pattern0.sub('', text)

		# Extract names
		name = None	
		match = pattern1.search(text)
		if match != None:
			name = match.group(1)
		else:
			match = pattern2.search(text)
			if match != None:
				name = match.group(1)
		if name != None:
			name = name.strip()

		# Print header
		if basename[0] != first_letter:
			first_letter = basename[0]
			print(f'\n<a name="{first_letter.lower()}"></a>  \n### {first_letter}', file=markdown_file)	

		count_match = pattern3.search(filename)
		if count_match != None and count_match.group(1) not in name:
			name += f' {count_match.group(1)}'

		# Print street entries
		print(f'[{name}](schleichwege/{filename})  ', file=markdown_file)
