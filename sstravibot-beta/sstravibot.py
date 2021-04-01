# Python BOT for ss-travi.com
# building class

import time
from sys import stdout

import requests

URL_BASE      = 'https://s2.ss-travi.com'
URL_BUILDID   = URL_BASE + '/build.php?id='
URL_VILLAGE1  = URL_BASE + '/village1.php'
URL_VILLAGE2  = URL_BASE + '/village2.php'
URL_STATISTICS= URL_BASE + '/statistics.php'
s = requests.session()

# connect
username = "Welcome"
password = "6425311"
'''
connect = s.post('http://ss-travi.com/s1/index.php', data={'login':username,'password':password})
if connect.url == URL_VILLAGE1:
	print 'connected successfully'
elif(connect.url == 'http://ss-travi.com/s1/index.php'):
	print 'cant connect'
elif connect.text.find("All good things must come to an end") > 0:
	print 'game over'
elif connect.text.find('<h1 class="will-open">SERVER START IN</h1>') > 0:
	print 'server is still ain\'t started'
'''
class building:
    name          = ""
    current_level = 0
    max_level     = 0
    id            = 0
    raw_html  	  = ""

    def __init__(self, id):
		if(int(id) < 1 or int(id) > 40):
			raise ValueError("can't create instance of building : id value must be 1 - 40")
		self.id = int(id)
		self.update_raw_html()
		self.set_building_name()
		self.set_current_level()
		self.set_max_level()
		return
		
    def upgrade_max(self):
			global s
			global URL_BUILDID
			url = URL_BUILDID + str(self.id)
			res = s.post(url)
			if(self.is_fully_upgraded()):
				print self.name + " is fully upgraded"
				return
			elif(self.is_warehouse_not_upgraded()):
				print "can\'t upgrade " + self.name + ", the warehouse is to litte"
			elif(self.is_granary_not_upgraded()):
				print "can\'t upgrade " + self.name + ", the granary is to litte"
			elif(self.is_empty_field()):
				print "this place is empty field"
			else:
				while(not self.is_fully_upgraded()) and (not self.is_warehouse_not_upgraded()) and (not self.is_granary_not_upgraded()):
					self.update_raw_html()
					if(self.raw_html.find("<a class=\"build\" href=\"") > 0):
						self.upgrade()
						time.sleep(1)

    def upgrade(self):
			if(self.is_fully_upgraded()):
				print self.name + " is fully upgraded"
			elif(self.raw_html.find("<a class=\"build\" href=\"") > 0):
				current_level = self.current_level
				url_upgrade = self.get_url_upgrade()
				res = s.post(url_upgrade)
				self.set_current_level()
			if(current_level + 1 == self.current_level):
				print self.name + " upgraded to level " + str(self.current_level)

			elif(self.is_warehouse_not_upgraded()):
				print "can\'t upgrade " + self.name + ", the warehouse to litte"
			elif(self.is_granary_not_upgraded()):
				print "can\'t upgrade " + self.name + ", the granary to litte"
			elif(self.is_warhouse_and_granary_upgraded()):
				print "can\'t upgrade " + self.name + ", the warehouse and granary to litte"
			elif(self.not_enough_resources()):
				print "can\'t upgrade " + self.name + ", not enough resources"
			else:
				print "Can\'t upgrade" +  self.name + ", unknown error"

    def is_fully_upgraded(self):
		self.update_raw_html()
		if(self.raw_html.find('fully upgraded') > 0):
			return True
		else:
			return False

    def not_enough_resources(self):
			if self.raw_html.find('enough'):
				return True
			else:
				return False

    def is_warehouse_not_upgraded(self):
			self.update_raw_html()
			if(self.raw_html.find('Upgrade your warehouse') > 0):
				return True
			else:
				return False

    def is_granary_not_upgraded(self):
			self.update_raw_html()
			if(self.raw_html.find('Upgrade your granary') > 0):
				return True
			else:
				return False

    def is_warhouse_and_granary_upgraded(self):
			self.update_raw_html()
			if(self.raw_html.find('Upgrade your warehouse and granary') > 0):
				return True
			else:
				return False

    def set_building_name(self):
			if(self.is_empty_field()):
				self.name = "Empty field"
			else:
				name = self.raw_html.split("<h1>")
				name = name[0].split(" level")
				self.name = str(name[0])
				print "building name: ", self.name, type(self.name)

    def set_current_level(self):
			self.update_raw_html()
			if(self.is_empty_field()):
				self.current_level = 0
			else:
				level = self.raw_html.split("level ")
				level = level[1].split('<')
				self.current_level = int(level[0])

    def set_max_level(self):
			if(self.id < 19):
				self.max_level = 25

    def is_empty_field(self):
			self.update_raw_html()
			if(self.name == "Empty field" or self.raw_html.find("Empty field") > 0):
				return True
			else:
				return False

    def update_raw_html(self):
		global s
		global URL_BUILDID
		url = URL_BUILDID + str(self.id)
		res = s.post(url)
		self.raw_html = res.text

    def get_url_upgrade(self):
		url_upgrade = self.raw_html.split("<a class=\"build\" href=\"")
		url_upgrade = url_upgrade[1].split("\">")
		url_upgrade = "http://ss-travi.com/s1/" + str(url_upgrade[0])
		return url_upgrade

    def get_url_construct(self, html):
		url_construct = html.split('<a class="build" href="')[-1]
		url_construct =	url_construct.split("\">")
		url_construct = "http://ss-travi.com/s1/" + str(url_construct[0])
		return url_construct

    def construct(self, building_name):
		building_name = building_name.lower()
		if(not self.is_empty_field()):
			print "can\'t build here, this field is built allready."
			return -1

		options = self.get_construct_options()
		if(building_name not in options):
			print "can\'t build " + building_name + " cause its not appears in the list."
			return -2

		res = s.post(options[building_name])
		print 'constructing ' + building_name + ' .',
		time.sleep(1)
		print ' .'
		time.sleep(1)
		self.name = building_name
		res = s.post(URL_STATISTICS)
		if(not self.is_empty_field()):
			print building_name + ' is built successfully.'
			self.set_building_name()
		else:
			self.name = "Empty field"
			print building_name + ' is not built successfully'

    def get_construct_options(self):
		temp = self.raw_html.split("<h2>")
		options = {}

		for i in range(1, len(temp)):
			if(temp[i].find('<a class="build" href=')):
				option_name          = temp[i].split('</h2>')[0].lower()
				options[option_name] = self.get_url_construct(temp[i])

		return options

class troops:
    def __init__(self):
        pass

    def train_clubswingers(self, barracks_id, num_of_clubs = -1):
        barracks = building(barracks_id)
        if(barracks.name != 'Barracks'):
            raise ValueError("the barracks_id given is not of the barracks")
        highest_clubs_available = int(barracks.raw_html.split("_tf11\').value=")[1].split(';')[0])
        if(int(num_of_clubs) > highest_clubs_available or num_of_clubs == -1):
			global s
			global URL_BUILDID
			res = s.post(URL_BUILDID + str(barracks_id), data={"tf[11]" : str(highest_clubs_available)})
			print "trained " + str(highest_clubs_available) + " clubswingers"

class account:
	villages = 1
	def __init__(self, username, password):
		self.username = username
		self.password = password
		self.connect()
		self.get_villages()

	def connect(self):
		global s
		connect = None
		connect_url = None
		try:
			headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
			connect = s.post('http://ss-travi.com/s1/index.php',headers=headers, data={'login' : self.username, 'password' : self.password} )
			
		except Exception as e:
			pass

		'''
		if connect_url == URL_VILLAGE1 :
			print 'connected successfully'
			return True
		elif connect.url == 'http://ss-travi.com/s1/index.php':
			print 'cant connect'
			return False
		if connect.url == URL_VILLAGE1 :
			print 'connected successfully'
			return True
		elif connect.url == 'http://ss-travi.com/s1/index.php':
			print 'cant connect'
			return False'''

	def select_village(self, village_index):
		if self.villages is village:
			raise Exception("this account have only one village")
		else:
			res = s.post(URL_VILLAGE1 + "?vid=" + str(village_index))

	def get_villages(self):
		global s
		res = s.post(URL_VILLAGE1)
		if not res.text.find('?vid=') > 0:
			self.villages = village()
		else:
			pass

class village:
    troops    = troops()
    village1_raw_html  = ""
    village2_raw_html  = ""
    def __init__(self):
			self.get_raw_html(1)
			self.get_raw_html(2)
			self.buildings = [0] * 40
			self.get_buildings()
			print type(self.buildings[21])
			self.get_name()
			self.get_troops()
			print self.is_building_built("main building")

    def full_construct(self):
			self.building_construct("rally point")
			self.building_construct("wall")
			self.building_construct("warehouse")
			self.building_construct("granary")

    def demolish(self):
			pass

    def building_demolish(self, name):
	#	res = s.post(URL_BUILDID + idmb + name)
			pass

    def building_construct(self, building_name, upgrademax = False):
			if building_name == "rally point":
				if self.buildings[39].is_empty_field():
					self.buildings[39].construct("rally point")
					if upgrademax:
						self.buildings[39].b.upgrade_max()

			elif building_name == "wall":
				if self.buildings[40].is_empty_field():
					self.buildings[40].construct("wall")
					if upgrademax:
						self.buildings[40].b.upgrade_max()

					else:
						b = building(self.get_empty_field())
						b.construct(name)
			if upgrademax:
				b.upgrade_max()


    def get_raw_html(self, village):
			if village == 1:
				res = s.post(URL_VILLAGE1)
				if res.text.find('<area href="build.php?id=1"'):
					self.village1_raw_html = res.text
				else:
					print 'cant get village1_raw_html'
			elif village == 2:
				res = s.post(URL_VILLAGE2)
				if res.text.find('<area href="build.php?id=31"'):
					self.village2_raw_html = res.text
				else:
					print 'cant get village2_raw_html'
			else:
				raise ValueError("get_raw_html(self, village): village value must be 1 or 2")

    def get_buildings(self):
			for bid in range(19, 40): # CHANGE TO 40 back!!
				stdout.write('\rgetting buildings, bid=%d' % bid)
				self.buildings[bid] = building(bid)
				stdout.flush()
				time.sleep(1)
			print type(self.buildings[21]), self.buildings[21]
			stdout.write('\rgot all the buildings\n')

    def get_name(self):
			pass

    def get_empty_field(self):
			for ia in range(19,39):
				if self.buildings[ia].is_empty_field():
					return ia
			return False

    def get_troops(self):
			pass

    def is_building_built(self, building_name):
			for it in range(1,40):
				print str(it), self.buildings[it], self.buildings[it].name
		#	if str(self.buildings[it].name).lower() == str(building_name).lower():
		#		return True

			return False

class attack:
	pass

#--------------------------------------------------------------------------------------------------------------
#---------------------END OF CLASSES---------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------

def deleteme(name):
	to = 0
	for ia in range(19,39):
		b = building(ia)
		if b.is_empty_field():
			to = ia
			break

	b = building(to)
	b.construct(name)
	b.upgrade_max()

acc = account(username, password)
