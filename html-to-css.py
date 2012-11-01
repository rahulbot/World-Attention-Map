
#http://pypi.python.org/pypi/incf.countryutils
from incf.countryutils import transformations
from BeautifulSoup import BeautifulSoup
import math

HTML_FILENAME = "gnews20101001.html"
CSS_FILENAME = "output/country_colors.css"
COLORS = [
  '#eeeeee',
  '#BBBBBB',
  '#888888',
  '#444444',
  '#111111',
]

def cn_to_cca2(country_name):
    if country_name == "Bosnia":
        return "ba"
    elif country_name == "Brunei":
        return "bn"
    elif country_name == "Congo Dem. Rep.":
        return 'cd'
    elif country_name == 'Congo Rep.':
        return 'cg'
    elif country_name == 'Guinea Bissau':
        return 'gw'
    elif country_name == 'Korea Dem. Rep.':
        return 'kp'
    elif country_name == 'Korea Rep.':
        return 'kr'
    elif country_name == 'Kyrgyzstan':
        return 'kg'
    elif country_name == 'Lao PDR':
        return 'la'
    elif country_name == 'Libya':
        return 'ly'
    elif country_name == 'Macao China':
        return 'mo'
    elif country_name == 'Macedonia FYR':
        return 'mk'
    elif country_name == 'Slovakia':
        return 'sk'
    elif country_name == 'St. Lucia':
        return 'lc'
    elif country_name == 'St. Vincent and the Grenadines':
        return 'vc'
    elif country_name == 'United Kingdom':
        return 'gb'
    elif country_name == 'United States':
        return 'us'
    elif country_name == 'West Bank and Gaza':
        return 'ps'
    elif country_name == 'Yugoslavia':
        return 'yu'
    return transformations.ccn_to_cca2( transformations.cn_to_ccn(country_name) ).lower()

# open the file with the html table
print "Parsing from "+HTML_FILENAME
f = open(HTML_FILENAME, 'r')
html = f.read()
soup = BeautifulSoup(html)

# parse out / normalize the country and hits
country_info = {}
i = 0
log_values = []
raw_values = []
for tr in soup.findAll('tr'):
    if i<2:
        i = i+1
        continue
    children =  tr.findChildren()
    country = children[0].contents[0]
    cca2 = cn_to_cca2(country)
    hits = ''.join(children[4].contents)
    country_info[cca2] = {
      'hits': int(hits),
      'log_hits': math.log10( float(int(hits)) ),
      'country': country
    }
    log_values.append( country_info[cca2]['log_hits'] )
    raw_values.append( country_info[cca2]['hits'] )
    i = i+1
  
print "  found "+str(len(country_info))+" country rows"
max_log_val = max(log_values)
raw_max_val = max(raw_values)
min_log_val = min(log_values)
raw_min_val = min(raw_values)
print "  hits range from "+str(raw_min_val)+" to "+str(raw_max_val)
print "  log10 of hits ranges from "+str(min_log_val)+" to "+str(max_log_val)
range_width = (max_log_val - min_log_val) / float(len(COLORS))
print "    bucket size is "+str(range_width)
log_threshold = min_log_val
while log_threshold <= max_log_val:
    raw_threshold = math.pow(10, log_threshold)
    print "    bucket = "+str(raw_threshold)+ "("+str(log_threshold)+")"
    log_threshold = log_threshold + range_width

# figure out what color to make each one
for cca2 in country_info:
    info = country_info[cca2]
    bucket = int( math.floor( (info['log_hits'] - min_log_val) / range_width) )
    country_info[cca2]['color'] = COLORS[min([bucket,len(COLORS)-1])]
    
# hand tweak some countries that has been created since the data was collected
# Set Serbia to be Kosovo
country_info['rs'] = country_info['yu']
country_info['xk'] = country_info['yu']
country_info['al'] = country_info['yu']
# Set South Sudan to Sudan
country_info['ss'] = country_info['sd']
# Set East Timor to Indonesia
country_info['tl'] = country_info['id']
    
# spit out some CSS to use
output_file = open(CSS_FILENAME,'w')
for cca2 in country_info:
    color = country_info[cca2]['color']
    output_file.write('.'+cca2+' { fill: '+color+'; }\n')

print "Wrote output to "+CSS_FILENAME