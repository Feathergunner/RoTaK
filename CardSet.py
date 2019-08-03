#!usr/bin/python
# -*- coding: utf-8 -*-import string

import xml.etree.ElementTree as ET
import os
import re
from subprocess import call

import helper
import Card

class CardSet:
	def __init__(self, xmlfile_cards=""):
		if xmlfile_cards == "":
			self.cards = {}
		else:
			self.cards = self.parse_carddata(xmlfile_cards)
		
	def __str__(self):
		string = ""
		for key in self.cards:
			string += str(key)+":\n"
			string += str(self.cards[key])
			string += "\n\n"
			
		return string

	def parse_carddata(self, xmlfile):
		cards = {}
		used_rules = []
		card_id = 0
	
		tree = ET.parse(xmlfile)
		root = tree.getroot()
		for comp in root:
			if comp.tag == "card":
				newcard = Card.Card(comp)
				if newcard.id == "Undefined":
					this_id = str(card_id)
					card_id += 1
				else:
					this_id = newcard.id
				cards[this_id] = newcard
		return cards
	
	def construct_tikz_cards_uniquecoords(self, factiondata, rulesdata, scale=1.0):
		px = 0
		py = 0
		dx = 6.5
		dy = 9
		num_of_cards = len(self.cards)
		cardnumber = 0

		tikzcode = "\\begin{tikzpicture}[scale="+str(scale)+", every node/.style={scale="+str(scale)+"}]\n"

		for c in self.cards:
			tikzcode += self.cards[c].construct_tikzcode(factiondata, rulesdata, posx=px, posy=py)
			if px < 3*dx:
				px += dx
			else:
				if py == 0:
					px = 0
					py += dy
				else:
					if cardnumber < num_of_cards:
						tikzcode += "\\end{tikzpicture}\n\\begin{tikzpicture}[scale="+str(scale)+", every node/.style={scale="+str(scale)+"}]\n"
						px = 0
						py = 0
			cardnumber += 1
			
		tikzcode += "\\end{tikzpicture}\n"

		return tikzcode

	def construct_tikz_cards(self, factiondata, rulesdata, scale=1.0, with_card_ids=True):
		tikzcode = ""
		for c in self.cards:
			if with_card_ids:
				tikzcode += "\\begin{tabular}{c}\n"
			
			tikzcode += "\\begin{tikzpicture}[scale="+str(scale)+", every node/.style={scale="+str(scale)+"}]\n"
			tikzcode += self.cards[c].construct_tikzcode(factiondata, rulesdata, posx=0, posy=0)
			tikzcode += "\\end{tikzpicture}\n"

			if with_card_ids:
				tikzcode += "\\\\ \n"
				tikzcode += "\\verb+"+self.cards[c].id+"+\n"
				tikzcode += "\\end{tabular}\n"

		return tikzcode

	def construct_tex_rules(self, rulesdata, race):
		rule_ids_passive = []
		rule_ids_active = []
		texcode_rules_passive = ""
		texcode_rules_active = ""

		for c in self.cards:
			for r in self.cards[c].ruleids:
				if rulesdata.get_type(r) == "active":
					if r not in rule_ids_active:
						rule_ids_active.append(r)
				else:
					if r not in rule_ids_passive:
						rule_ids_passive.append(r)
	
		if len(rule_ids_passive) > 0:
			texcode_rules_passive = "\\begin{itemize}\n"
			for r in rule_ids_passive:
				desc = rulesdata.get_label(r, race)
				if desc == None:
					print ("Error: Rule "+r+" not specified for this race")
					desc = r
	
				texcode_rules_passive += "\\item \\textit{"+desc+"}"
				texcode_rules_passive += ": "+rulesdata.get_effect(r)+"\n"
			texcode_rules_passive += "\\end{itemize}\n"

		if len(rule_ids_active) > 0:
			texcode_rules_active = "\\begin{itemize}\n"
			for r in rule_ids_active:
				desc = rulesdata.get_label(r, race)
				if desc == None:
					print ("Error: Rule "+r+" not specified for this race")
					desc = r
	
				texcode_rules_active += "\\item \\textbf{"+desc+"}"
				texcode_rules_active += " ("+str(rulesdata.get_costs(r))+")"
				texcode_rules_active += ": "+rulesdata.get_effect(r)+"\n"
			texcode_rules_active += "\\end{itemize}\n"

		return texcode_rules_passive, texcode_rules_active

