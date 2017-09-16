#!/usr/bin/python

from hcsr04sensor import sensor
import argparse
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

def water_check():
	'''Main function to run the sensor with passed arguments'''
	while True:
		for sen in [1,2]:
			print('inspecting sensor{}'.format(sen))
			trig,echo=u_sensor[sen]
			print('trig pin = gpio {}'.format(trig))
			print('echo pin = gpio {}'.format(echo))
			print('speed = {}'.format(speed))
			print('samples = {}'.format(samples))
			print('')
			value = sensor.Measurement(trig, echo)
			raw_distance = value.raw_distance(sample_size=samples, sample_wait=speed)
			imperial_distance = value.distance_imperial(raw_distance)
			metric_distance = depth[sen]-value.distance_metric(raw_distance)
			print('The imperial distance is {} inches.'.format(imperial_distance))
			print('The metric distance is {} centimetres.'.format(metric_distance))
			if (metric_distance*100)/depth[sen] <= 40:
				print('low water in Tank {}'.format(sen))
				on_motor()
			time.sleep(90)
			
def on_motor():
	sump=sensor.Measurement(u_sensor[3]).raw_distance(sample_size=samples, sample_wait=speed)
	if ((depth[3]-sump.distance_metric(sump))*100)/depth[3] >=40:
		print('truning on the sump motor')
		run_sump()
		retun
	else:
		print('turning on the bore motor as not enough sump water')
		run_bore()
		return
		
def run_sump():
	#GPIO_moroto start
	print('sump motor running')
	time.sleep(10)
	if flow():
		print('no water fromsump')
		run_bore()
	while overflow():
		#GPIO_moroto stop
		click=1
		print('turning off motor')
		if click >= 150:
			print('motor runn more than the limit')
			return
		time.sleep(10)
		click=+1
		return
		
def run_bore():
	print('HEMA hasnt Authorised me to run bore please run manually')
	return
	
def flow():
	print('checking flow')
	GPIO.setup(flow_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	GPIO.add_event_detect(flow_pin, GPIO.FALLING, callback=countPulse)
	count=0
	time.sleep(25)
	for _ in xrange(3):
		if count > 100:
			print('found flow')
			return False
		else:
			print('waiting for water')
			time.sleep(25)
	return True
	
def countPulse(flow_pin):
   global count
   if start_counter == 1:
      count = count+1

def overflow():
	tank2=sensor.Measurement(u_sensor[2]).raw_distance(sample_size=samples, sample_wait=speed)	
	if ((depth[2]-sump.distance_metric(tank2))*100)/depth[2] >=90:
		print('Tanks are full')
		return True
	else:
		print('not full')
		return False
		
if __name__ == '__main__':
	u_sensor={1:(26,20), 2:(21,19), 3:(16,13)}
	depth={1:100.00, 2:120.00, 3:400.00}
	flow_pin = 6
	samples=5
	speed=0.1
	count=0
	water_check()