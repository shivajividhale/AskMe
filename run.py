from flask import Flask, request, redirect
import twilio.twiml
import urllib
import urllib2
import logging
import sys
import xml.etree.ElementTree as ET

wolfram_api = 'TRR8TK-VHV99K9UE8'

app = Flask(__name__)

# Try adding your own number to this list!
@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
	"""Respond and greet the caller by name."""
	from_number = request.values.get('From', None)
	content = request.values.get('Body', None)
	content = urllib.pathname2url(content)
	url = "http://api.wolframalpha.com/v2/query?appid=" + wolfram_api + "&input=" + content + "&format=plaintext"
		
	req = urllib2.Request(url)
	resp = urllib2.urlopen(req).read()
	f = open("temp.xml", "w")
	f.write(resp)
	f.close()
	tree = ET.parse("temp.xml")
	root = tree.getroot()
	if root.attrib['success'] == "true":
		pod = root[1]
		subpod = pod[0]
		message = subpod[0].text
	else:
		message = "No results found!"
	logging.warning(message)
	resp = twilio.twiml.Response()
	resp.message(message)
	return str(resp)
		
if __name__ == "__main__":
	app.run(debug=True)
