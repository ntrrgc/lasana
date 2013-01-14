import re
import encodings.idna

extract_domain = re.compile(r'^([a-z]*://)([^/:]+)((:[0-9]+)?/.*)$')

def transform_url_to_idn(url):
    #Extract domain and other parts of the URL
    url_groups = extract_domain.match(url).groups()

    #Convert the domain from punycode to Unicode
    unicode_domain = []
    for domain_level in url_groups[1].split('.'):
        unicode_domain.append(encodings.idna.ToUnicode(domain_level))
    unicode_domain = '.'.join(unicode_domain)

    #Restore the URL with a new Unicode domain
    return ''.join([url_groups[0], unicode_domain, url_groups[2]])
