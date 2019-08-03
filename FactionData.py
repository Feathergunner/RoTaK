#!usr/bin/python
# -*- coding: utf-8 -*-import string

import xml.etree.ElementTree as ET

class Faction():
	def __init__(self, xml_comp):
		self.id = xml_comp.attrib["id"]
		self.race_name = xml_comp.attrib["race_name"]
		self.faction_name = xml_comp.attrib["faction_name"]
		self.color = xml_comp.attrib["color"]

class FactionData():
	def __init__(self):
		tree = ET.parse("xml/factions_definition.xml")
		root = tree.getroot()
		self.factions = {}
		for comp in root:
			if comp.tag == "faction":
				new_faction = Faction(comp)
				self.factions[new_faction.id] = new_faction

	def __contains__(self, f_id):
		return f_id in self.factions
	
	def get_race(self, f_id):
		return self.factions[f_id].race_name

	def get_name(self, f_id):
		return self.factions[f_id].faction_name

	def get_color(self, f_id):
		return self.factions[f_id].color

	def get_all_keys(self):
		return [f_id for f_id in self.factions]

