import smtplib
conn = smtplib.SMTP('smtp.gmail.com', 587)
conn.ehlo() #make sure connection ok
conn.starttls()
conn.login('mikebook24@gmail.com', 'passwordwouldgohere')
conn.sendmail('mikebook24@gmail.com', 'michael.book@globalhealth.com', 'Subject: So long...\n\nThis is the body, after the two newline characters.\n\n-Michael')