#!usr/bin/python
# -*- coding: utf-8 -*-import string

import xml.etree.ElementTree as ET
import sys
import re

import CardSet
import RulesData
import FactionData
import helper

factiondata = FactionData.FactionData()
rulesdata = RulesData.RulesData()

def construct_deck(deck_xml_filename):
	tree = ET.parse("xml/Decks/"+deck_xml_filename)
	root = tree.getroot()
	cards = {}
	main_faction_id = ""
	name = ""
	for comp in root:
		if comp.tag == "card":
			cards[comp.attrib["id"]] = {key : comp.attrib[key] for key in comp.attrib}#{faction_id: comp.attrib["faction_id"], amount : int(comp.attrib["amount"])}
		if comp.tag == "meta":
			main_faction_id = comp.attrib["main_faction_id"]
			name = comp.attrib["name"]

	print (cards)
	print ("parse card data...")
	cds = {}
	for card_id in cards:
		#print (card_id)
		faction_id = cards[card_id]["faction_id"]
		if not faction_id in cds:
			cds[faction_id] = CardSet.CardSet("xml/Factions/"+faction_id+"_cards.xml")

	print (cds)
	print ("construct deck...")
	num_cards = 0
	num_levels = [0,0,0]
	sum_costs = 0
	combined_carddata = CardSet.CardSet()
	

	for card_id in cards:
		print (card_id+": "+str(cards[card_id]))
		faction_id = cards[card_id]["faction_id"]
		for i in range(int(cards[card_id]["amount"])):
			if not faction_id[0] == "N":
				num_cards += 1
				sum_costs += cds[faction_id].cards[card_id].costs
				num_levels[cds[faction_id].cards[card_id].level-1] += 1
			combined_carddata.cards[card_id+"_"+str(i)] = cds[faction_id].cards[card_id]
			#combined_carddata.rules = {**combined_carddata.rules, **cds[faction_id].rules}

	tokens = {}
	for c_id in combined_carddata.cards:
		for r_id in combined_carddata.cards[c_id].ruleids:
			if not rulesdata.get_tokendata(r_id) == None:
				#combined_carddata.rules[r_id].tokendata.faction_id = faction_id#(combined_carddata.rules, race, party)
				rulesdata.get_tokendata(r_id).faction_id = faction_id#(combined_carddata.rules, race, party)
				for i in range(5):
					tokens["t_"+r_id+"_"+str(i)] = rulesdata.get_tokendata(r_id)
	combined_carddata.cards = {**combined_carddata.cards, **tokens}

	print (combined_carddata)
	print ("Number of cards: "+str(num_cards))
	print ("level 1: "+str(num_levels[0]))
	print ("level 2: "+str(num_levels[1]))
	print ("level 3: "+str(num_levels[2]))
	print ("total costs: "+str(sum_costs))

	tikzcode_cards = combined_carddata.construct_tikz_cards_uniquecoords(factiondata, rulesdata)
	texcode_rules_passive, texcode_rules_active = combined_carddata.construct_tex_rules(rulesdata, factiondata.get_race(main_faction_id))

	templatefile = open('template.tex')
	replace_dict = {
		"$$$CARDS$$$" : tikzcode_cards,
		"$$$RULES_PASSIVE$$$" : texcode_rules_passive,
		"$$$RULES_ACTIVE$$$" : texcode_rules_active
		}
	replace_dict["$$$FORMAT$$$"] = "[landscape]"
	replace_dict["$$$FORMAT_CHANGE_BEGIN$$$"] = "\\begin{landscape}\n"
	replace_dict["$$$FORMAT_CHANGE_END$$$"] = "\\end{landscape}\n"
	replace_regex = re.compile("|".join(map(re.escape, replace_dict.keys(  ))))

	outputfilename = "deck_"+name
	outputfile = open("tex/"+outputfilename+".tex", 'w', encoding='utf-8')
	for line in templatefile:
		outputfile.write(replace_regex.sub(lambda match: replace_dict[match.group(0)], line))
	templatefile.close()
	outputfile.close()

	helper.construct_pdf(outputfilename)

	'''
	outputfile_deck = open("tex/deck_"+name+".tex", 'w', encoding='utf-8')
	outputfile_deck.write(tikzcode_cards)
	outputfile_deck.write("\\newpage\n")
	outputfile_deck.write("\\textbf{Passive Sonderregeln:}\n")
	outputfile_deck.write(texcode_rules_passive)
	outputfile_deck.write("\\textbf{Aktive Sonderregeln:}\n")
	outputfile_deck.write(texcode_rules_active)
	outputfile_deck.close()
	'''

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print ("No deck description file specified!")
	else:
		deck_xml_filename = sys.argv[1]
		construct_deck(deck_xml_filename)