#!/usr/bin/python

"""Serpent

Badassify your python script by turning your code
into an actual python wrapped around a sword.

(More documentation to come later) 

The MIT License (MIT)

Copyright (c) 2013 Kendal Harland

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import compiler
import subprocess
import os
import re
import sys
import math

"""script statuses

These are used to indicate what type of script was passed 
to the serpent module. 

_PYTHON    => convert the script to a _SERPENT file.
_SERPENT   => execute the script.
_BYTECODE  => let the python compiler handle execution
"""

_SERPENT = 0
_PYTHON = 1
_BYTECODE =2

"""_AUTO_REMOVE_SERPENT_PYC

Set to False to prevent autmomatic deletion of the serpent.pyc
file that gets generated when this file is included in another
module
"""

_AUTO_REMOVE_SERPENT_PYC = True

"""alphabet

This is the alphabet we are mapping our hex code to. There are
32 symbols in the alphabet and 255 possible 2-digit hex values.
To map a character to a value, we simply take its 32-modulus and
append the number of its occurence in the modulus cycle, with 0
meaning "1st", 1 mean "2nd" and so on. For example: 

Given the hex digit 65:
	
	65 % 32 = 1
	floor( 65 / 32 ) = 2

	so the alphabet symbol for 65 is the symbol at index 1: 'PT2'.
	65 is also the 3rd occurrence of a 32-modulus of 1 (with 1 
	being the first occurrence and 33 being the second of course.)
	so the code for this hex symbol is PT2

"""

alphabet = [
	"PY", "PT", "PH", "PO", "PN", "YP", "YT", "YH","YO", "YN","TP", "TY", "TH", "TO", "TN", "HP",
	"HY", "HT", "HO", "HN", "OP", "OY", "OT", "OH",	"ON", "NP", "NY", "NT", "NH", "NO", "PP", "YY"
]


def _hex_to_serpent_sword_alphabet(hexidecimal):
	"Convert the python bytecode into the serpent alphabet"
	return [alphabet[digit % 32]+str(int(math.floor(float(digit)/32.0))) for digit in hexidecimal]


def _serpent_sword_alphabet_to_hex(sentence):
	"Convert the serpent alphabet string back to python bytecode"
	return [alphabet.index(symbol[0:-1]) + int(symbol[-1])*32 for symbol in sentence]


def _gen_serpent_body(sss):
	"Generate the serpent body of the bytecode file"
	stage = {
		"0": " "*8+ "%s | |z\n",
		"1": " "*7+"%s| | |\n",
		"2": " "*9+  "%s| |\n",
		"3": " "*10+   "|%s|\n",
		"4": " "*10+  "| |%s\n",
		"5": " "*10+  "| | %s\n",
		"6": " "*10+  "| | |%s\n",
		"7": " "*9+ "z| | |%s\n",
	}

	index = 1
	body = ""

	while len(sss) > 0:
		body += stage[str(index)] % sss.pop(0)
		index = (index + 1) % 8
	while index % 8 != 0:
		body += stage[str(index)] % 'zz '
		index = (index + 1) % 8
	return body


def _lex_hex(infile):
	"Extract the serpent string from the ss file"
	with open(infile, 'r') as source:
		regex = re.compile(r'[PYTHON][PYTHON][0-9]')
		tokens = []
		for line in source:
			pos = 0
			while(pos < len(line)):
				match = regex.match(line, pos)
				if match:
					tokens.append(match.group(0))
				pos += 1
		return tokens


def _get_script_type(script):
	"Return the type of script that was called"
	if script.split('.')[-1] == "py":
		if script.split('.')[-2][0:2] == "ss":
			return _SERPENT
		return _PYTHON
	elif script.split('.')[-1] == "pyc":
		return _BYTECODE
	

"""Execution

Here we decided if we should sleep, execute the program,or convert it to serpent code.
If the program is being executed, we converted the serpent code within it back to bytecode,
write the pyc file, call it as a subprocess and then tell this module to sleep until complete.
If the file is being converted we compile the source, then convert the bytecode to serpent 
code and draw the serpent code to the new ss.py file with this module as the only imported
module. When that ss.py file is compiled, this file do extract the code and run the pyc file.
This is easier than obfuscating the actual python code because we don't need to worry about 
whitespace when writing the pyc file.
"""

scriptType = _get_script_type(sys.argv[0])

if scriptType is _BYTECODE:

	pass

elif scriptType is _SERPENT:

	pyc = _serpent_sword_alphabet_to_hex(_lex_hex(sys.argv[0]))
	pycout = ".".join(sys.argv[0].split(".")[0:-1])+".pyc"

	with open(pycout, "wb") as f:
		for val in pyc:
			f.write(chr(val))

	cmd = "python %s %s" % (pycout, " ".join(sys.argv[1:]))
	subprocess.call(cmd, shell=True)
	os.remove(pycout)

elif scriptType is _PYTHON:

	compiler.compileFile(sys.argv[0])
	tmp, sss = [], []

	with open(sys.argv[0]+'c', 'r') as pyc:
		for line in pyc:
			for char in line:
				tmp.append(int(char.encode('hex'), 16))
	os.remove(sys.argv[0]+'c') # Delete temporary pyc file

	sss = _hex_to_serpent_sword_alphabet(tmp)
	rev = _serpent_sword_alphabet_to_hex(sss)
	
	try:
		assert rev == tmp
	except AssertionError:
		sys.stderr.write("Error in hex/serpent_sword conversion")

	ssoutput = sys.argv[0].split('.')[0]+'.ss.py'
	with open(ssoutput, 'w') as f:
		header = "#!/usr/bin/python\nimport serpent\n\"\"\"\n"
		content = [
			"           ___\n",
			"          { _ }\n",
			"           |/|\n",
			"          {___}\n",
			"           |_|\n",
			"           |/|\n",
			" .         |/|         .\n",
			" (\\________|w|________/)\n",
			" ( ___________________ )\n",
			"  v       | | |       v\n",
			"          | | |\n",
			"          | | |\n",
			"          | | |"+sss.pop(0)+'.'+sss.pop(0)+"\n",
			"          | | |   *   "+sss.pop(0)+"~~~<\n",
			"         z| | |"+sss.pop(0)+"."+sss.pop(0)+"\n",
			_gen_serpent_body(sss),
			"          z | |\n",
			"          z | |\n",
			"          | | |\n",
			"          | | |\n",
			"           \|/\n",
			"            v\n",
			"\"\"\""
		]
		f.write(header+"".join(content))

	if _AUTO_REMOVE_SERPENT_PYC:
		try:
			os.remove("./serpent.pyc")
		except OSError:
			pass

	sys.exit("Serpent file: '%s' generated" % ssoutput)

else:

	sys.exit("SerpentError, unknown filetype (%s)" % sys.argv[0])