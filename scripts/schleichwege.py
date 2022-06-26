#!/usr/bin/env python3

import os
from pathlib import Path
import textract
import re
import unicodedata

first_letter = ''
pattern0 = re.compile(r'(Frühjahr|Herbst|Frühsommer|November)?(\s\d\d)?\s?\d\d\d\d')
pattern1 = re.compile(r'Straßennamen:?[\n\sx]*([^\n:]+)$', re.MULTILINE)
pattern2 = re.compile(r'Stand:?[\n\s]*([^\n]+)', re.MULTILINE)
pattern3 = re.compile(r'_(\d+).pdf')

source = 'static/schleichwege'
target = 'content/schleichwege-streets.md'
filename_mapping = {
	' ': '_',
	'ä': 'ae',
	'ü': 'ue',
	'ö': 'oe',
	'ß': 'ss',
	'Ä': 'Ae',
	'Ü': 'Ue',
	'Ö': 'Oe',
	'.': ''
}

def replace_many(string, mapping):
	new_string = string
	for key in mapping:
		new_string = new_string.replace(key, mapping[key])
	return new_string

def get_valid_filename(name):
    """
    Taken from https://github.com/django/django/blob/main/django/utils/text.py

    Return the given string converted to a string that can be used for a clean
    filename. Remove leading and trailing spaces; convert other spaces to
    underscores; and remove anything that is not an alphanumeric, dash,
    underscore, or dot.
    >>> get_valid_filename("john's portrait in 2004.jpg")
    'johns_portrait_in_2004.jpg'
    """
    s = str(name).strip().replace(" ", "_")
    s = re.sub(r"(?u)[^-\w.]", "", s)
    if s in {"", ".", ".."}:
        raise SuspiciousFileOperation("Could not derive file name from '%s'" % name)
    return s

with open(target, 'w') as markdown_file:
	for filename in sorted(os.listdir(source), key=str.casefold):
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
		if basename[0].upper() != first_letter:
			first_letter = basename[0].upper()
			print(f'\n### {first_letter}', file=markdown_file)	

		count_match = pattern3.search(filename)
		mapped_name = get_valid_filename(replace_many(name, filename_mapping))
		if count_match != None and count_match.group(1) not in mapped_name:
			name += f' {count_match.group(1)}'

		# New filename
		new_filename = get_valid_filename(replace_many(name, filename_mapping)) + '.pdf'
		if new_filename != filename:
			print(f"{filename} -> {new_filename}")
			os.rename(f'{source}/{filename}', f'{source}/{new_filename}')

		# Print street entries
		print(f'[{name}](schleichwege/{new_filename})  ', file=markdown_file)
