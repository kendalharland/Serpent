#!/usr/bin/python

"""python

Badassify your python script by turning your code
into an actual python wrapped around a sword. I'm 
not shitting you.
"""

import compiler
import subprocess
import os
import re
import sys
import math

serpent = True
sleep = False

alphabet = [
	"PY", "PT", "PH", "PO", "PN", "YP", "YT", "YH", 
	"YO", "YN", "TP", "TY", "TH", "TO", "TN", "HP",
	"HY", "HT", "HO", "HN", "OP", "OY", "OT", "OH",
	"ON", "NP", "NY", "NT", "NH", "NO", "PP", "YY"
]

def hex_to_serpent_sword_alphabet(hexidecimal):
	"""hex_to_serpent_sword_alphabet"""
	return [alphabet[digit % 32]+str(int(math.floor(digit/32))) for digit in hexidecimal]


def serpent_sword_alphabet_to_hex(sentence):
	"""serpent_sword_alphabet_to_hex"""
	return [alphabet.index(symbol[0:-1]) + int(symbol[-1])*32 for symbol in sentence]


def gen_serpent_body(sss):
	stage = {
		"0": " "*27+ "%s | |z\n",
		"1": " "*26+"%s| | |\n",
		"2": " "*28+  "%s| |\n",
		"3": " "*29+   "|%s|\n",
		"4": " "*29+  "| |%s\n",
		"5": " "*29+  "| | %s\n",
		"6": " "*29+  "| | |%s\n",
		"7": " "*28+ "z| | |%s\n",
	}

	i, body = 1,""
	while len(sss) > 0:
		body += stage[str(i)] % sss.pop(0)
		i = (i + 1) % 8
	while i % 8 != 0:
		body += stage[str(i)] % 'zz '
		i = (i + 1) % 8
	return body


def lex_hex(infile):
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


try:
	assert sys.argv[0].split('.')[-2][0:2] == "ss"
except AssertionError:
	serpent = False

if sys.argv[0].split('.')[-1] == "pyc":
	sleep = True
	

if sleep:
	pass

elif serpent:
	
	pyc = serpent_sword_alphabet_to_hex(lex_hex(sys.argv[0]))
	pycout = ".".join(sys.argv[0].split(".")[0:-1])+'.pyc'

	with open(pycout, "wb") as f:
		for val in pyc:	
			f.write(chr(val))

	cmd = "python %s %s" % (pycout, " ".join(sys.argv[1:]))
	subprocess.call(cmd, shell=True)
	os.remove(pycout)

else:

	compiler.compileFile(sys.argv[0])
	tmp, sss = [], []

	with open(sys.argv[0]+'c', 'r') as pyc:
		for line in pyc:
			for char in line:
				tmp.append(int(char.encode('hex'), 16))
	os.remove(sys.argv[0]+'c') # Delete temporary pyc file

	sss = hex_to_serpent_sword_alphabet(tmp)
	rev = serpent_sword_alphabet_to_hex(sss)
	
	try:
		assert rev == tmp
	except AssertionError:
		sys.stderr.write("Error in hex/serpent_sword conversion")

	ssoutput = sys.argv[0].split('.')[0]+'.ss.py'
	with open(ssoutput, 'w') as f:
		header = "#!/usr/bin/python\nimport serpent\n\"\"\"\n"
		hb = " "*30+"___\n"+" "*29+"{ _ }\n"+" "*30+"|/|\n"+" "*29+"{___}\n"
		mh = " "*30+"|_|\n"+" "*30+"|/|\n"
		g1 = " "*20+"."+" "*9+"|/|"+" "*9+".\n"+" "*20+"(\\"+"_"*8+"|w|"+"_"*8+"/)\n"
		g2 = " "*20+"( "+"_"*19+" )\n"+" "*21+"v       | | |       v\n"
		bl = (" "*29+"| | |\n")*3
		s1 = " "*29+"| | |"+sss.pop(0)+'.'+sss.pop(0)+'\n'
		s2 = " "*29+"| | |"+" "*3+"*"+" "*3+sss.pop(0)+'\n'
		s3 = " "*28+"z| | |"+sss.pop(0)+'.'+sss.pop(0)+'\n'
		serpentBody = gen_serpent_body(sss)
		bm = (" "*29+"z | |"+'\n')*2+(" "*29+"| | |"+'\n')*2
		sp = " "*29+" \|/\n"+" "*31+'v\n'
		f.write(header+hb+mh+g1+g2+bl+s1+s2+s3+serpentBody+bm+sp+"\"\"\"")

	sys.exit("Serpent file: '%s' generated" % ssoutput)