#! python3
import re
import pyperclip

#copy a large text, like a company directory pdf, before running this program
#after running this program, paste your clipboard into something like word

phoneRegex = re.compile(r'''
(((\d\d\d)|(\(\d\d\d\)))? #two possible forms of area code
(\s|-) #possible separator or leading whitespace
\d\d\d #first three digits
- #seperator
\d\d\d\d #following four digits
(((ext(\.)?\s)|x) #possible extension indicator
(\d{2,5}))?) #possible extension grouped with above line
''', re.VERBOSE)

emailRegex = re.compile(r'''
[a-zA-Z0-9_.+]+ #range of characters that can be in the name part
@
[a-zA-Z0-9_.+]+ #domain name part
''', re.VERBOSE)

#import text from clipboard
text = pyperclip.paste()

extractedEmail = emailRegex.findall(text) #only one group - ez
extractedPhone = phoneRegex.findall(text) #will return multiple groups as tuples

allPhoneNumbers = []
for phoneNumber in extractedPhone:
#append the 0 tuple which is full the full match and not one of the individual/optional groups
    allPhoneNumbers.append(phoneNumber[0]) 

#copy results to clipboard
results = '\n'.join(allPhoneNumbers) + '\n' + '\n'.join(extractedEmail)
pyperclip.copy(results)