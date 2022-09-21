import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import lxml.html
import datetime

sender_email = "andy@smr-electronics.co.uk"
receiver_email = "andy@smr-electronics.co.uk"
password = '6h2f~5tZ'

message = MIMEMultipart('related')
message["Subject"] = "iRIS Report " + datetime.datetime.today().strftime('%d/%m/%Y')
message["From"] = sender_email
message["To"] = receiver_email
message.preamble = 'This is a multi-part message in MIME format.'
message_alt = MIMEMultipart("alternative")
message.attach(message_alt)


# Create the plain-text and HTML version of your message
text = """\
Hi,
How are you?
Real Python has many great tutorials:
www.realpython.com"""
html = """\
<html>
  <body>
    <p>Hi,<br>
       How are you?<br>
       <a href="http://www.realpython.com">Real Python</a> 
       has many great tutorials.
    </p>
  </body>
</html>
"""

part_text = MIMEText(lxml.html.fromstring(html).text_content().encode('utf-8'), 'plain', _charset='utf-8')
part_html = MIMEText(html.encode('utf-8'), 'html', _charset='utf-8')


# Turn these into plain/html MIMEText objects
#part_text = MIMEText(text, "plain")
#part_html = MIMEText(html, "html")




# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
message_alt.attach(part_text)
message_alt.attach(part_html)

for n in range(2, 6):
    f = open('/home/pi/Documents/Email/' + str(n) + '.png', 'rb')
    img_data = f.read()
    f.close()
    image = MIMEImage(img_data, name='image' + str(n))  
    image.add_header('Content-ID', '<image' + str(n) + '>')
    message.attach(image)
message_alt.attach(MIMEText('<img src="cid:image2"><img src="cid:image3"><img src="cid:image4"><img src="cid:image5"><img src="cid:imageIO"><img src="cid:imageFF">', 'html'))
#message_alt.attach(MIMEText('<img src="cid:image2"><img src="cid:image3"><img src="cid:image4"><img src="cid:image5">', 'html'))


f = open('/home/pi/Documents/Email/IO.png', 'rb')
img_data = f.read()
f.close()
image = MIMEImage(img_data, name='imageIO') 
image.add_header('Content-ID', '<imageIO>')
message.attach(image)

f = open('/home/pi/Documents/Email/FF.png', 'rb')
img_data = f.read()
f.close()
image = MIMEImage(img_data, name='imageFF') 
image.add_header('Content-ID', '<imageFF>')
message.attach(image)


# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("onyx.cloudns.io", 465, context=context) as server:
    print('Sending mail...')
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )
