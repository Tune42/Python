import re

def domain_name(url):
    regex = re.compile(r'''
    (http://|https://)?
    (www.)?
    ([0-9a-zA-Z-]+)
    .
    ''', re.VERBOSE)

    domain = regex.findall(url)[0][2]
    return domain

print(domain_name("http://github.com/carbonfive/raygun")) # == "github" 
print(domain_name("http://www.zombie-bites.com")) # == "zombie-bites"
print(domain_name("https://www.cnet.com")) # == "cnet"