'''
	From D Crawler
	--------------------------
	crawls through the EDGAR database through their web 
	portal using the form: 
	
		http://www.sec.gov/edgar/searchedgar/currentevents.htm

	PLEASE NOTE:
	this program bypasses the robots.txt which
	explicitly states that crawlers may not access
	/cgi-bin

		Disallow: /cgi-bin

	then it looks for hyperlinks with the content
	"D" or whatever form is desired. Then it takes 
	the url and adjusts it to view the right content

	requirements:
	
		mechanize - git://github.com/jjlee/mechanize.git

'''
import mechanize
import urlparse
from bs4 import BeautifulSoup

br = mechanize.Browser()
#bypassing robots.txt
br.set_handle_robots(False)
#the search parameters are as follows:
#	q1=amount of business days into the past (e.g: 1 = today, 2 = today + yesterday)
#		*also the amount of times this has to loop
#	q2=form series ID? (if not then 6)
#	q3=specific form ID
q1=20
q2=6
q3="D"

#processing of page assuming the routing stays the same! :D
#	- have to create a workaround: making a links list because following links
#	  while parsing leads to not completing the for loop?... Ya..
class parsePage:
	def __init__(self,q1,q2,q3):
		self.links = []
		self.q1 = q1
		self.q2 = q2
		self.q3 = q3

	#get all links with D
	def getLinks(self):
		for i in range(q1+1):
			try:
				br.open('http://www.sec.gov/cgi-bin/current.pl?q1=%s&q2=%s&q3=%s'%((i),self.q2,self.q3))
			except:
				print "404 URL NOT FOUND"
				return
			# o = urlparse.urlparse(br.geturl())
			# base = urlparse.urlunparse((o.scheme, o.netloc, '', '', '', ''))
			base = "http://www.sec.gov"

			for link in br.links():
				if link.text == "D":
					url = link.url.translate(None,'-').replace('index.html','/primary_doc.xml')
					self.links.append(url)
	
	#f7 duplicate removing algo
	def f7(self, seq):
	    seen = set()
	    seen_add = seen.add
	    return [ x for x in seq if not (x in seen or seen_add(x))]
	
	#remove duplicates
	def removeDup(self):
		self.links = self.f7(self.links)
	#process links
	def process(self):
		i = 0
		for link in self.links:
			# if i >= 1:
			# 	break
			# i += 1
			try:
				thing = br.open(link)
			except:
				print "BAD LINK"

			r = thing.read()
			if "06c" in r:
				bs = BeautifulSoup(r)
				print bs.edgarsubmission.primaryissuer.entityname.string
				print thing.geturl()
	def run(self):
		self.getLinks()
		self.removeDup()
		self.process()

p = parsePage(q1,q2,q3)
p.run()

