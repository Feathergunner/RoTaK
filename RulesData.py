#!usr/bin/python
# -*- coding: utf-8 -*-import string

import xml.etree.ElementTree as ET

import Card

class RulesData():
	'''
	Wrapper class that handles access to a set of Rules
	'''
	def __init__(self, xmlfile_rules="xml/rules.xml"):
		self.rules = {}

		tree = ET.parse(xmlfile_rules)
		root = tree.getroot()
		for comp in root:
			if comp.tag == "rule":
				newrule = Rule(comp)
				#print (newrule)
				self.rules[newrule.id] = newrule

	def get_card_text(self, rule_id, race):
		return self.rules[rule_id].construct_card_text(race)

	def get_type(self, rule_id):
		return self.rules[rule_id].type

	def get_label(self, rule_id, race):
		if race in self.rules[rule_id].labels:
			return self.rules[rule_id].labels[race]
		elif "GEN" in self.rules[rule_id].labels:
			return self.rules[rule_id].labels["GEN"]
		else:
			return None

	def get_effect(self, rule_id):
		return self.rules[rule_id].effect

	def get_costs(self, rule_id):
		return self.rules[rule_id].cost

	def get_tokendata(self, rule_id):
		return self.rules[rule_id].tokendata

class Rule:
	'''
	Data structure that contains the data of a single rule
	'''
	def __init__(self, xml_component):
		warning = False
		self.labels = {}
		self.tokendata = None

		if "id" in xml_component.attrib:
			self.id = xml_component.attrib["id"]
		else:
			warning = True
			self.id = "Unknown"
		if "cost" in xml_component.attrib:
			self.cost = int(xml_component.attrib["cost"])
		else:
			warning = True
			self.cost = 0
		if "effect" in xml_component.attrib:
			self.effect = xml_component.attrib["effect"]
		else:
			warning = True
			self.effect = "Unknown"
		if "type" in xml_component.attrib:
			self.type = xml_component.attrib["type"]
			if self.type not in ["active", "passive"]:
				warning = True
				self.type = "Unknown"
		else:
			warning = True
			self.effect = "Unknown"

		for child in xml_component:
			if child.tag == "label":
				for key in child.attrib:
					self.labels[key] = child.attrib[key]
			if child.tag == "token":
				self.tokendata = Card.Card()
				self.tokendata.name = child.attrib["name"]
				self.tokendata.strength = child.attrib["strength"]
				self.tokendata.actions = child.attrib["actions"]
				self.tokendata.costs = 0
				self.tokendata.level = 0
				if "image" in child.attrib:
					self.tokendata.image = "../img/"+child.attrib["image"]
				else:
					warning = True
					self.tokendata.image = "../img/default.jpg"
			
				self.tokendata.rows = []
				self.tokendata.rulesstrings = []
				self.tokendata.ruleids = []
				for grandchild in child:
					if grandchild.tag == "row":
						self.tokendata.rows.append(grandchild.attrib["name"])
					if grandchild.tag == "rule":
						rule_id = grandchild.attrib["id"]
						self.tokendata.ruleids.append(rule_id)
						#self.tokendata.rulesstrings.append(rulesdata[rule_id].construct_card_text(self.race))

	def construct_card_text(self, race):
		label = ""
		if race not in self.labels:
			if "GEN" in self.labels:
				label = self.labels["GEN"]
			else:
				print ("Error! Rule "+self.id+" not available for race!")
				return ""
		else:
			label = self.labels[race]

		if self.type == "active":
			return "\\textbf{"+label+"} ("+str(self.cost)+")"
		elif self.type == "passive":
			return "\\textit{"+label+"}"

	def __str__(self):
		description = "Rule: "+self.id+" labels: ("
		for key in self.labels:
			description += key+": "+self.labels[key]+" "
		description += ")"
		if not self.tokendata == None:
			description += " token: "+str(self.tokendata)
		return description

	def __repr__(self):
		return str(self)