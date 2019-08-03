#!usr/bin/python
# -*- coding: utf-8 -*-import string

import os
from subprocess import call

import helper

def construct_tikzcode_marker(n_mb=40, n_mm=40, n_a=40):
	px = 0
	py = 0
	tikzcode = "\\begin{tikzpicture}\n"
	counts = [n_mb, n_mm, n_a]
	colors = ["blue", "red", "green"]
	labels = ["+", "-", "A"]
	for k in range(3):
		i=0
		while i < counts[k]:
			for j in range(15):
				tikzcode += "\\node[draw, rounded corners=.2cm, rectangle, fill="+colors[k]+"!50, minimum width=1cm, minimum height=1cm] at ("+str(px)+","+str(py)+") {\\textbf\\huge "+labels[k]+"};\n"
				px += 1
				i += 1
			py += 1
			px = 0

	tikzcode += "\\end{tikzpicture}\n"

	return tikzcode

def construct_tex_marker():
	outputfilename = "marker"
	templatefile = open('template.tex')
	outputfile = open("tex/"+outputfilename+".tex", 'w', encoding='utf-8')

	for line in templatefile:
		if not "center" in line:
			outputfile.write(line)
		else:
			break
	templatefile.close()
	
	outputfile.write("\\begin{landscape}\n")
	outputfile.write(construct_tikzcode_marker(100, 100, 100))
	outputfile.write("\\end{landscape}\n\\end{document}")
	outputfile.close()

	helper.construct_pdf(outputfilename)

if __name__ == "__main__":
	construct_tex_marker()