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

before running make sure to run requirements.txt using pip!
