#!/usr/bin/python
#By Naresh Paturi
#script will maintain two tanks,sump and also a bore.
from hcsr04sensor import sensor
import argparse
import time
import RPi.GPIO as GPIO
import logging
import os
import sqlite3
import loger
GPIO.setmode(GPIO.BCM)

def water_lev(trig,echo):
	logger.debug('trig pin = gpio {}'.format(trig))
	logger.debug('echo pin = gpio {}'.format(echo))
	logger.debug('speed = {}'.format(speed))
	logger.debug('samples = {}'.format(samples))
	logger.debug('')
	value = sensor.Measurement(trig, echo)
	raw_distance = value.raw_distance(sample_size=samples, sample_wait=speed)
	imperial_distance = value.distance_imperial(raw_distance)
	metric_distance = value.distance_metric(raw_distance)
	logger.debug('The imperial distance is {} inches.'.format(imperial_distance))
	logger.debug('The metric distance is {} centimetres.'.format(metric_distance))
	return metric_distance
	
def water_check():
	'''Main function to run the sensor with passed arguments'''
	while True:
		logwater()
		for sen in [1,2]:
			logger.debug('inspecting sensor{}'.format(sen))
			lev=depth[sen]-water_lev(*u_sensor[sen])
			if (lev*100)/depth[sen] <= 30:
				logger.debug('low water in Tank {}'.format(sen))
				on_motor()
				time.sleep(2400)
		time.sleep(90)
			
def on_motor():
	logger.debug('inspecting sump')
	if ((depth[3]-water_lev(*u_sensor[3]))*100)/depth[3] >=40:
		logger.debug('truning on the sump motor')
		if run_sump():
			runbore()
			return
		return
	else:
		logger.debug('turning on the bore motor as not enough sump water')
		run_bore()
		return
		
def run_sump():
	#GPIO_moroto start
	logger.debug('sump motor running')
	GPIO.setup(sump_pin,GPIO.OUT)
	time.sleep(10)
	GPIO.output(sump_pin,GPIO.HIGH)

	if flow():
		logger.debug('no water fromsump')
		GPIO.output(sump_pin,GPIO.LOW)
		run_bore()
		return
	while overflow():
		#GPIO_moroto stop
		click=1
		logger.debug('turning off motor')
		if click >= 150:
			logger.debug('motor runn more than the limit')
			GPIO.output(sump_pin,GPIO.LOW)
			return
		time.sleep(10)
		click=+1
	GPIO.output(sump_pin,GPIO.LOW)
	return
		
def run_bore():
	logger.debug('HEMA hasnt Authorised me to run bore please run manually')
	time.sleep(100)
	return
	
def flow():
	logger.debug('checking flow')
	GPIO.setup(flow_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	GPIO.add_event_detect(flow_pin, GPIO.FALLING, callback=countPulse)
	count=0
	time.sleep(25)
	for _ in xrange(3):
		if count > 100:
			logger.debug('found flow')
			GPIO.remove_event_detect(flow_pin)
			return False
		else:
			logger.debug('waiting for water')
			time.sleep(25)
	GPIO.remove_event_detect(flow_pin)
	return True
	
def countPulse(flow_pin):
   global count
   if start_counter == 1:
      count = count+1

def overflow():
	if ((depth[2]-water_lev(*u_sensor[2]))*100)/depth[2] >=90:
		logger.debug('Tanks are full')
		return True
	else:
		logger.debug('not full')
		return False
		
def logwater():
	return
if __name__ == '__main__':
	logger = logging.getLogger('sweethome')
	logger.setLevel(logging.DEBUG)
	logger.addHandler(SQLiteHandler('debugLog.sqlite'))
	u_sensor={1:(5,6), 2:(13,19), 3:(20,21)}
	depth={1:100.00, 2:120.00, 3:400.00}
	sump_pin=16
	bore_pin=12
	flow_pin = 26
	samples=5
	speed=0.1
	count=0
	try:
		water_check()
	except:
		logger.debug('error')
		GPIO.cleanup() 
	finally:
		logger.debug('runnig finally')
		GPIO.cleanup()  
