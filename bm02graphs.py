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
    makegraph(ddn)
    #dpgraph(ddn)
    #message = ''
    #sendmail(message, ddn)
   

def readfile(fname):
    f = open(fname, 'r')
    raw = f.readlines()
    f.close()
    return raw

def makegraph(ddn):
    dt = ddn.strftime('%Y%m%d')
    raw = readfile('/home/pi/Documents/BM-02/bm02-' + dt + '.csv')
    header = raw[0].split(',')
    print('Generating IO graph..')
    mpl.rcParams['toolbar'] = 'None'
    fig = plt.figure()
    ax = plt.subplot()
    hdt = ddn.strftime('%d/%m/%Y')
    x, y1, y2 = [], [], []
    fig.canvas.header_visible = False
    #ax.xaxis.set_major_locator(MultipleLocator(30))
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=60))
    ax.xaxis.set_major_formatter(DateFormatter('%H'))
    raw.pop(0)
    for line in raw:
        data = line.split(',')
        dto = datetime.datetime.strptime(data[1],'%H:%M:%S')
        x.append(dto) #data[1])
        y1.append(float(data[2]))
        y2.append(float(data[3]))
    plt.xlim(datetime.datetime.strptime('00:00:00','%H:%M:%S'),datetime.datetime.strptime('23:59:59','%H:%M:%S'))
    plt.title('BM-02 Celsius', fontsize=24)
    plt.title(hdt, loc='right', fontsize=8)
    plt.plot(x,y1,'r')
    plt.plot(x,y2,'b')
    ax.legend(['Indoor','Outdoor'])
    #plt.show()
    #plt.gcf().autofmt_xdate()
    #plt.xticks(rotation='vertical', fontsize=8)
    plt.savefig('/home/pi/Documents/Email/IO.png')


    

main()
