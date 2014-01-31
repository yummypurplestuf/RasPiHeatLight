import mechanize
import re


def main():
	# will be used later on using mechanize 
    # Generates a web browser instance 
    # Opens www.whatsmyip.com/ and gets external IP address
    br = mechanize.Browser()

    # Browser options
    br.set_handle_equiv(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)

    # Follows refresh 0 but not hangs on refresh > 0
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    # User-Agent makes the destination website think it's from a real person
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    html = br.open('http://www.weather.com/')
    html = html.read()
    html = unicode(html, errors='ignore')
    
    # for f in br.forms():
    #     print f
    br.select_form(nr=0)
    br['where'] = "Olivet, MI"
    html = br.submit()
    html = html.read()
    outside_list = []
    match = re.search('<span itemprop="temperature-fahrenheit">(\d*)</span>', html)
    outside_list.append(match.group(1))
    match = re.search('<span class="wx-unit">(.)</span>', html) 
    
    outside_list.append(u'\xb0'.encode("UTF-8") + match.group(1))
    print outside_list


if __name__ == "__main__": main()