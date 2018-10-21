# -*- coding: utf-8 -*-
import smtplib
import email.mime.application

# Create a text/plain message
msg = email.mime.Multipart.MIMEMultipart()
msg['Subject'] = 'Greetings'
msg['From'] = 'baturin.ivan9@gmail.com'
msg['To'] = 'baturin.ivan9@gmail.com'

# The main body is just another attachment
body = email.mime.Text.MIMEText("""Hello, how are you? I am fine.
This is a rather nice letter, don't you think?""")
msg.attach(body)

# PDF attachment
filename='pytest.py'
fp=open(filename,'rb')
att = email.mime.application.MIMEApplication(fp.read(),_subtype='pdf')
fp.close()
att.add_header('Content-Disposition','attachment',filename=filename)
msg.attach(att)

# send via Gmail server
# NOTE: my ISP, Centurylink, seems to be automatically rewriting
# port 25 packets to be port 587 and it is trashing port 587 packets.
# So, I use the default port 25, but I authenticate.
s = smtplib.SMTP('smtp.gmail.com')
s.starttls()
s.login('baturin.ivan9@gmail.com','Ivanbaturin1999')
s.sendmail('baturin.ivan9@gmail.com',['baturin.ivan9@gmail.com'], msg.as_string())
s.quit()