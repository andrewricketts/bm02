print('Importing..')

import matplotlib.pyplot as plt
#from matplotlib.ticker import (MultipleLocator)
import matplotlib as mpl
from matplotlib.figure import Figure
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates

import smtplib, ssl
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import base64
from datetime import date, timedelta
import datetime
import numpy
import sys
#from datetime import datetime

def main():
    if(len(sys.argv) > 1):
        arg = sys.argv[1].split('/')
        ddn = datetime.datetime(int(arg[2]), int(arg[1]), int(arg[0]))
    else:
        ddn = date.today() - timedelta(days=1)
    for g in range(2, 5):
        makegraph(g, ddn)
    dpgraph(ddn)
    #message = ''
    #sendmail(message, ddn)
   

def readfile(fname):
    f = open(fname, 'r')
    raw = f.readlines()
    f.close()
    return raw

def dpgraph(ddn):
    dt = ddn.strftime('%Y%m%d')
    raw = readfile('/home/pi/Documents/iRIS/iris-' + dt + '.csv')
    print('Generating Dew Point graph..')
    mpl.rcParams['toolbar'] = 'None'
    fig = plt.figure()
    ax = plt.subplot()
    hdt = ddn.strftime('%d/%m/%Y')
    x, y = [], []
    fig.canvas.header_visible = False
    ax.xaxis.set_major_formatter(DateFormatter('%H'))
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=60))
    raw.pop(0)
    for line in raw:
        data = line.split(',')
        dto = datetime.datetime.strptime(data[1],'%H:%M:%S')
        x.append(dto) #data[1])
        C5 = float(data[3])
        C6 = float(data[4])
        dp = 243.04*(numpy.log(C6/100)+(17.625*C5/(243.04+C5)))/(17.625-numpy.log(C6/100)-(17.625*C5/(243.04+C5)))
        y.append(float(dp))
    plt.xlim(datetime.datetime.strptime('00:00:00','%H:%M:%S'),datetime.datetime.strptime('23:59:59','%H:%M:%S')) 
    plt.title('Dew Point', fontsize=24)
    plt.title(hdt, loc='right', fontsize=8)
    plt.plot(x,y)
    #plt.show()
    #plt.gcf().autofmt_xdate()
    #plt.xticks(rotation='vertical', fontsize=8)
    plt.savefig('/home/pi/Documents/Email/5.png')

def makegraph(col, ddn):
    dt = ddn.strftime('%Y%m%d')
    raw = readfile('/home/pi/Documents/iRIS/iris-' + dt + '.csv')
    header = raw[0].split(',')
    print('Generating ' + header[col].replace('\n','') + ' graph..')
    mpl.rcParams['toolbar'] = 'None'
    fig = plt.figure()
    ax = plt.subplot()
    hdt = ddn.strftime('%d/%m/%Y')
    x, y = [], []
    fig.canvas.header_visible = False
    #ax.xaxis.set_major_locator(MultipleLocator(30))
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=60))
    ax.xaxis.set_major_formatter(DateFormatter('%H'))
    raw.pop(0)
    for line in raw:
        data = line.split(',')
        dto = datetime.datetime.strptime(data[1],'%H:%M:%S')
        x.append(dto) #data[1])
        y.append(float(data[col]))
    plt.xlim(datetime.datetime.strptime('00:00:00','%H:%M:%S'),datetime.datetime.strptime('23:59:59','%H:%M:%S'))
    plt.title(header[col].replace('\n',''), fontsize=24)
    plt.title(hdt, loc='right', fontsize=8)
    plt.plot(x,y)
    #plt.show()
    #plt.gcf().autofmt_xdate()
    #plt.xticks(rotation='vertical', fontsize=8)
    plt.savefig('/home/pi/Documents/Email/' + str(col) + '.png')



def sendmail(message, ddn):
    print('Sending mail...')
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "theinvisiblewiz@gmail.com"
    password = 'Slothy77!!'
    receiver_email = "andrew.ricketts1@gmail.com" 
    msg = MIMEMultipart("related")
    #msg.attach(MIMEMultipart('alternative'))
    hdt = ddn.strftime('%d/%m/%Y')
    msg['Subject'] = 'iRIS Report ' + hdt
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.preamble = 'This is a multi-part message in MIME format.'
    msgalt = MIMEMultipart('alternative')
    msg.attach(msgalt)

    msgtxt = MIMEText('This is an alternative plain text message')
    msgalt.attach(msgtxt)

    #msghtml = MIMEText('<img src="cid:image1"><img src="cid:image2"><img src="cid:image3">', 'html')
    #msgalt.attach(msghtml)

    for n in range(2, 6):
        f = open('/home/pi/Documents/iRIS/' + str(n) + '.png', 'rb')
        img_data = f.read()
        f.close()
        image = MIMEImage(img_data, name='image' + str(n))  
        #msgalt.attach(MIMEText('<img src="cid:image' + str(n) + '"><br>', 'html'))   
        image.add_header('Content-ID', '<image' + str(n) + '>')
        #image.add_header('Content-Disposition', 'attachment; filename=' + str(n) + '.png')
        msg.attach(image)
    msgalt.attach(MIMEText('<img src="cid:image2"><img src="cid:image3"><img src="cid:image4"><img src="cid:image5">', 'html'))
    #if attachment:
    #    part = MIMEBase("application","octet-stream")
    #    part.set_payload(attachment)
    #    msg.attach(part)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

main()
