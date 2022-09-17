
import serial
import datetime
import os
from os import path


def addtolog(msg):
    application_path = os.path.dirname(os.path.abspath(__file__))
    logfile = path.join(application_path,'bm02-' + datetime.datetime.now().strftime('%Y%m%d') + '.csv')
    dt = datetime.datetime.now().strftime('%d/%m/%y,%H:%M:%S')  
    if(os.path.isfile(logfile)):
        print('exists')
        f = open(logfile, 'a')
    else:
        print('missing')
        f = open(logfile, 'w')
        f.write('Date,Time,Inside,Outside\n')
    f.write(dt + ',' + msg + '\n')
    f.close()


def main():
	port = '/dev/ttyUSB1'
	ser = serial.Serial(timeout=1)
	ser.baudrate = 115200
	ser.port = port
	ser.open()
	ser.flush()
	ser.flushInput()
	ser.flushOutput()
	lastmin = datetime.datetime.now().minute
	lasthour = datetime.datetime.now().hour
	a,b,c = 0,0,0
	while True:
		try:
			line = ser.readline()
			line = str(line, 'utf-8')
			line = line[:-2]
			dat = line.split(',')
			print(line)
			a += float(dat[0])
			b += float(dat[1])
			c += 1
			print(round(float(dat[0]),1),round(float(dat[1]),1),c)
			#if datetime.datetime.now().minute != lastmin:
			if datetime.datetime.now().hour != lasthour:
				print('WRITE')
				addtolog(str(round(a/c,1)) + ',' + str(round(b/c,1)))
				#lastmin = datetime.datetime.now().minute
				lasthour = datetime.datetime.now().hour
				a,b,c = 0,0,0
		except:
			pass

if __name__ == "__main__":
    main()
