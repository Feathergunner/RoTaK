#!usr/bin/python
# -*- coding: utf-8 -*-import string

import xml.etree.ElementTree as ET
import re

#import RulesData

# parse tikz templates:
tree = ET.parse("xml/tikz_template.xml")
root = tree.getroot()
tikzcommands = {}
for comp in root:
	if comp.tag == "tikzline":
		tikzcommands[comp.attrib["name"]] = comp.attrib["command"]
		
class Card:
	def __init__(self, xml_component=None):
		self.id = ""
		self.name = ""

		self.faction_id = ""	
		#self.race = ""
		#self.party = ""
		
		self.level = 0
		self.strength = 0
		self.actions = 0
		self.costs = 0
		self.cardclass = ""
		self.rows = []
		self.ruleids = []

		if not xml_component == None:
			warning = False
			if "name" in xml_component.attrib:
				self.name = xml_component.attrib["name"]
			else:
				warning = True
				self.name = "Unknown"
			if "id" in xml_component.attrib:
				self.id = xml_component.attrib["id"]
			else:
				warning = True
				self.id = "Undefined"
				
			if "faction_id" in xml_component.attrib:
				self.faction_id = xml_component.attrib["faction_id"]
			else:
				warning = True
				
			if "level" in xml_component.attrib:
				self.level = int(xml_component.attrib["level"])
			else:
				warning = True
				self.level = 1
			if "strength" in xml_component.attrib:
				self.strength = int(xml_component.attrib["strength"])
			else:
				warning = True
				self.strength = 0
			if "actions" in xml_component.attrib:
				self.actions = int(xml_component.attrib["actions"])
			else:
				warning = True
				self.costs = 0
			if "costs" in xml_component.attrib:
				self.costs = int(xml_component.attrib["costs"])
			else:
				warning = True
				self.costs = 0
			if "cardclass" in xml_component.attrib:
				self.cardclass = xml_component.attrib["cardclass"]
			else:
				warning = True
				self.cardclass = "Unknown"
				
			self.statkey = str(self.strength)+"$\mid$"+str(self.actions)+"$\mid$"+str(self.costs)
				
			if "image" in xml_component.attrib:
				self.image = "../img/"+xml_component.attrib["image"]
			#elif self.race == "NEUTRAL" and self.party == "Wetter":
			#	self.image = "../symbol_weather.jpg"
			else:
				warning = True
				self.image = "../img/default.jpg"
				
			self.rows = []
			#self.rulesstrings = []
			self.ruleids = []
			for child in xml_component:
				if child.tag == "row":
					self.rows.append(child.attrib["name"])
				if child.tag == "rule":
					rule_id = child.attrib["id"]
					self.ruleids.append(rule_id)
					#self.rulesstrings.append(rulesdata[rule_id].construct_card_text())
					#self.rules.append(child.attrib["name"])
				
			self.rowkey = ""
			for i in range(len(self.rows)):
				self.rowkey += self.rows[i][0]
				if i < len(self.rows)-1:
					self.rowkey += "|"
			if warning:
				print ("Warning! Missing key!")

	def __str__(self):
		description = self.name + " ("+str(self.id)+"), "
		description += "level: "+str(self.level)+", "
		description += self.faction_id + ", "
		description += self.cardclass + ", "
		description += str(self.strength)+"/"+str(self.actions)+"/"+str(self.costs)+", "
		description += self.cardclass + ", "
		description += str(self.rows)
		description += str(self.ruleids)
		
		return description		
		
	def __repr__(self):
		return str(self)

	def construct_rulesstrings(self, rulesdata, racename):
		rulesstrings = []
		for rule_id in self.ruleids:
			rulesstrings.append(rulesdata.get_card_text(rule_id, racename))

		return rulesstrings

	def construct_tikzcode(self, factiondata, rulesdata, posx=0, posy=0, dx=6.5, dy=9):
		corner_rad = 0.5
		inner_corner_rad = corner_rad/2

		color = factiondata.get_color(self.faction_id)
		color_border_bg = color+"!10"
		color_bg = color+"!60"
		titleposx = corner_rad
		titleposy = dy-corner_rad

		img_dx_base = dx-1
		img_dy_base = (dx-1)*3.0/4.0
		img_pos_x = posx+dx/2.0
		img_pos_y = posy+titleposy-img_dy_base/2.0-0.5

		if self.level == 3:
			card_level_color = "gold"
		elif self.level == 2:
			card_level_color = "silver"
		elif self.level == 1:
			card_level_color = "bronze"
		else:
			card_level_color = color_bg

		card_levelstring = ""
		for i in range(self.level):
			card_levelstring += "\\bigstar"

		if len(self.faction_id) > 1:
			rf_key = self.faction_id[0]+"$\\mid$"+self.faction_id[1]
		else:
			rf_key = self.faction_id

		replace_dict = {
			"$$$PX$$$" : str(posx),
			"$$$PY$$$" : str(posy),
			"$$$PXI$$$" : str(posx+corner_rad),
			"$$$PYI$$$" : str(posy+corner_rad),
			"$$$PXII$$$" : str(posx+inner_corner_rad),
			"$$$PYII$$$" : str(posy+inner_corner_rad),
			"$$$PXDX$$$" : str(posx+dx),
			"$$$PYDY$$$" : str(posy+dy),
			"$$$PXDXI$$$" : str(posx+dx-corner_rad),
			"$$$PYDYI$$$" : str(posy+dy-corner_rad),
			"$$$PXDXII$$$" : str(posx+dx-inner_corner_rad),
			"$$$PYDYII$$$" : str(posy+dy-inner_corner_rad),
			"$$$CORNERRAD$$$" : str(corner_rad),
			"$$$RADI$$$" : str(inner_corner_rad),
			"$$$TW$$$" : str(dx-1),
			"$$$PXTX$$$" : str(posx+titleposx),
			"$$$PYTY$$$" : str(posy+titleposy),
			"$$$PXDXDELTA$$$" : str(posx+dx-0.7),
			"$$$PYDYDELTA$$$" : str(posy+dy-0.7),
			"$$$IMGBPX$$$" : str(img_pos_x),
			"$$$IMGBPY$$$" : str(img_pos_y),
			"$$$IMGPX$$$" : str(img_pos_x),
			"$$$IMGPY$$$" : str(img_pos_y),
			"$$$IMGDX$$$" : str(img_dx_base-0.5),
			"$$$IMGDY$$$" : str(img_dy_base-0.5),
			"$$$SX$$$" : str(posx+(dx-corner_rad)+0.3),
			"$$$SSY$$$" : str(img_pos_y+1.1),
			"$$$SAY$$$" : str(img_pos_y),
			"$$$SCY$$$" : str(img_pos_y-1.1),
			"$$$RULEX$$$" : str(posx+corner_rad*0.8),
			"$$$RULEY$$$" : str(posy+titleposy-img_dy_base-2+corner_rad*0.8),
			"$$$ROWY$$$" : str(posy+titleposy-img_dy_base-1),
			"$$$NAME$$$" : self.name,
			"$$$KEY$$$" : rf_key,
			"$$$COLOR$$$" : color,
			"$$$COLOR_BG$$$" : color_bg,
			"$$$COLOR_BORDER$$$" : color_border_bg,
			"$$$IMG$$$" : self.image,
			"$$$STRENGTH$$$" : str(self.strength),
			"$$$ACTIONS$$$" : str(self.actions),
			"$$$COSTS$$$" : str(self.costs),
			"$$$RULES$$$" : "\\\\\n".join(self.construct_rulesstrings(rulesdata, factiondata.get_race(self.faction_id))),
			"$$$LEVEL$$$" : card_levelstring,
			"$$$IMGBORDERCOLOR$$$" : card_level_color
		}
		replace_regex = re.compile("|".join(map(re.escape, replace_dict.keys(  ))))

		card_border = replace_regex.sub(lambda match: replace_dict[match.group(0)], tikzcommands["draw_bg_border"])+"\n"
		card_bg = replace_regex.sub(lambda match: replace_dict[match.group(0)], tikzcommands["draw_bg"])+"\n"
		card_title = replace_regex.sub(lambda match: replace_dict[match.group(0)], tikzcommands["card_title"])+"\n"
		card_rpkey = replace_regex.sub(lambda match: replace_dict[match.group(0)], tikzcommands["card_rpkey"])+"\n"
		img_border = ""

		if self.level >= 3:
			img_border += replace_regex.sub(lambda match: replace_dict[match.group(0)], tikzcommands["img_border"]).replace("$$$IMGBDX$$$",str(img_dx_base)).replace("$$$IMGBDY$$$",str(img_dy_base))+"\n"

		if self.level >= 2:
			img_border += replace_regex.sub(lambda match: replace_dict[match.group(0)], tikzcommands["img_border"]).replace("$$$IMGBDX$$$",str(img_dx_base-0.2)).replace("$$$IMGBDY$$$",str(img_dy_base-0.2))+"\n"
		
		img_border += replace_regex.sub(lambda match: replace_dict[match.group(0)], tikzcommands["img_border"]).replace("$$$IMGBDX$$$",str(img_dx_base-0.4)).replace("$$$IMGBDY$$$",str(img_dy_base-0.4))+"\n"
		img_image = replace_regex.sub(lambda match: replace_dict[match.group(0)], tikzcommands["img_image"])+"\n"
		card_stat_strength = replace_regex.sub(lambda match: replace_dict[match.group(0)], tikzcommands["card_stat_strength"])+"\n"
		card_stat_actions = replace_regex.sub(lambda match: replace_dict[match.group(0)], tikzcommands["card_stat_actions"])+"\n"
		card_stat_costs = replace_regex.sub(lambda match: replace_dict[match.group(0)], tikzcommands["card_stat_costs"])+"\n"
		card_level = replace_regex.sub(lambda match: replace_dict[match.group(0)], tikzcommands["card_level"])+"\n"
		card_rules = replace_regex.sub(lambda match: replace_dict[match.group(0)], tikzcommands["rules"])+"\n"
		
		card_data_rows = ""
		rows_symbol_offset = 1
		for r in self.rows:
			if r == "CLOSE":
				rowimg = "../img/symbol_sword.jpg"
			if r == "RANGED":
				rowimg = "../img/symbol_bow.jpg"
			if r == "SUPPORT":
				rowimg = "../img/symbol_scroll.jpg"
			if r == "WEATHER":
				rowimg = "../img/symbol_weather.jpg"
			card_data_rows += replace_regex.sub(lambda match: replace_dict[match.group(0)], tikzcommands["row"]).replace("$$$ROWIMG$$$", rowimg).replace("$$$ROWX$$$", str(posx+rows_symbol_offset))+"\n"
			rows_symbol_offset += 1.1

		return card_border + card_bg + card_title + img_border + img_image + card_rpkey + card_stat_strength + card_stat_actions + card_stat_costs + card_level + card_data_rows + card_rules