#!usr/bin/python
# -*- coding: utf-8 -*-import string

import os
from subprocess import call

def construct_pdf(filename):
	if not os.path.exists("tex"):
		os.makedirs("tex/")
	if not os.path.exists("pdf"):
		os.makedirs("pdf/")

	os.chdir("tex/")
	call(["pdflatex", "-output-directory=../pdf", filename+".tex"])
	os.chdir("..")
	call(["rm", "pdf/"+filename+".aux", "pdf/"+filename+".log"])