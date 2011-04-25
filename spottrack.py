import urllib2
from xml.etree import ElementTree as ET
from cStringIO import StringIO

class LivePosition(object):

	def __init__(self, lat, lon):
		self.lat = lat
		self.lon = lon

	def __repr__(self):
		return  "LivePosition(%f, %f)" % (self.lat, self.lon)

class LiveFeedDocument(object):

	def __init__(self, xml_data, tracker_name):
		self.tracker_name = tracker_name
		self.positions = self._parse_xml(xml_data)
	

	def _parse_xml(self, xml_data):
		doc = ET.parse(StringIO(xml_data)).getroot()
		messages = doc.findall("message")
		positions = []
		for message in messages:
			tracker_name = message.findtext("esnName")
			message_type = message.findtext("messageType")
			print tracker_name,message_type
			if message_type == "TRACK" and tracker_name == self.tracker_name:
				try:
					lat = float(message.findtext("latitude"))
					lon = float(message.findtext("longitude"))
				except Exception,e:
					print "Failed to parse lat/lon with exception",str(e)
				positions.append(LivePosition(lat, lon))
		return positions

	def last_position(self):
		if len(self.positions) > 0:
			return self.positions[0]
		else:
			return None







class LiveCommunicator(object):

	def __init__(self, tracker_id):
		self.tracker_id = tracker_id

	def load_data(self):
		url = "http://share.findmespot.com/messageService/guestlinkservlet?glId=%s&completeXml=true" % (self.tracker_id,)
		connection = urllib2.urlopen(url)

		data =  connection.read()

		connection.close()

		return data