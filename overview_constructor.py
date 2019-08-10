#!usr/bin/python
# -*- coding: utf-8 -*-import string

import sys
import re
import os

import CardSet
import RulesData
import FactionData
import helper

factiondata = FactionData.FactionData()
rulesdata = RulesData.RulesData()


def construct_overview_pdf(cd, race, cards_in_landscape=False, outputfilename="output"):
	templatefile = open('template.tex')

	tikzcode_cards = cd.construct_tikz_cards(factiondata, rulesdata, scale=0.8)
	texcode_rules_passive, texcode_rules_active = cd.construct_tex_rules(rulesdata, race)
	replace_dict = {
		"$$$CARDS$$$" : tikzcode_cards,
		"$$$RULES_PASSIVE$$$" : texcode_rules_passive,
		"$$$RULES_ACTIVE$$$" : texcode_rules_active
		}
	if cards_in_landscape:
		replace_dict["$$$FORMAT$$$"] = "[landscape]"
		replace_dict["$$$FORMAT_CHANGE_BEGIN$$$"] = "\\begin{landscape}\n"
		replace_dict["$$$FORMAT_CHANGE_END$$$"] = "\\end{landscape}\n"
	else:
		replace_dict["$$$FORMAT$$$"] = ""
		replace_dict["$$$FORMAT_CHANGE_BEGIN$$$"] = ""
		replace_dict["$$$FORMAT_CHANGE_END$$$"] = ""
	replace_regex = re.compile("|".join(map(re.escape, replace_dict.keys(  ))))

	outputfile = open("tex/"+outputfilename+".tex", 'w', encoding='utf-8')
	for line in templatefile:
		outputfile.write(replace_regex.sub(lambda match: replace_dict[match.group(0)], line))
	templatefile.close()
	outputfile.close()

	helper.construct_pdf(outputfilename)

def construct_overview_puretikz(cd, race, outputfilename="output"):
	tikzcode_cards = cd.construct_tikz_cards(factiondata, rulesdata, scale=0.75)
	texcode_rules_passive, texcode_rules_active = cd.construct_tex_rules(rulesdata, race)

	outputfile_cards = open("tex/"+outputfilename+"_puretikz_cards.tex", 'w', encoding='utf-8')
	outputfile_cards.write(tikzcode_cards)
	outputfile_cards.close()

	outputfile_rules = open("tex/"+outputfilename+"_puretikz_rules.tex", 'w', encoding='utf-8')
	outputfile_rules.write("\\textbf{Passive Sonderregeln:}\n")
	outputfile_rules.write(texcode_rules_passive)
	outputfile_rules.write("\\textbf{Aktive Sonderregeln:}\n")
	outputfile_rules.write(texcode_rules_active)
	outputfile_rules.close()

def construct_overview(code="ALL", only_puretikz=False):
	if not os.path.exists("tex"):
		os.makedirs("tex/")
	
	if code == "ALL":
		codes = factiondata.get_all_keys()
	elif code in factiondata:
		codes = [code]
	else:
		print ("Error! Faction id "+code+" unknown!")
		return

	for army_code in codes:
		print (army_code)
		race = factiondata.get_race(army_code)

		cd = CardSet.CardSet("xml/Factions/"+army_code+"_cards.xml")
		rulesdata = RulesData.RulesData()

		#print ("Carddata:")
		#print (cd)
		if not only_puretikz:
			construct_overview_pdf(cd, race, cards_in_landscape=False, outputfilename=army_code)
		else:
			construct_overview_puretikz(cd, race, outputfilename=army_code)


if __name__ == "__main__":
	if len(sys.argv) < 2:
		construct_overview(only_puretikz=True)
	else:
		army_code = sys.argv[1]
		construct_overview(army_code)