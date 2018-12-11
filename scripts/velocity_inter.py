#!/usr/bin/env python

import rospy

from geometry_msgs.msg import Pose  #do zadawania punktow
from geometry_msgs.msg import Twist  #predkosc
from numpy import arctan2
import math


global rate


global publisher

pos1=0
pos2=0
pos3=0
global czas1,czas2
czas1 = 0.0
czas2 =0.0
global lista,mess,msg
lista=list()
mess=Twist()
msg=Twist()

mess.linear.x=0.0
mess.linear.y=0.0
mess.linear.z=0.0
mess.angular.x=0.0
mess.angular.y=0.0
mess.angular.z=0.0




def stworz_wiadomosc(ktora):
	global msg
	if(ktora == 1):
   		msg.linear.x=0.7
    		msg.linear.y=0.0
   		msg.linear.z=0.0
   		msg.angular.x=0.0
    		msg.angular.y=0.0
   		msg.angular.z=0.0
   	 	return msg
	if(ktora == 2):
   		msg.linear.x=0.0
    		msg.linear.y=0.0
   		msg.linear.z=0.0
   		msg.angular.x=0.0
    		msg.angular.y=0.0
   		msg.angular.z=0.7
   	 	return msg
	if(ktora == 0):
   		msg.linear.x=0.0
    		msg.linear.y=0.0
   		msg.linear.z=0.0
   		msg.angular.x=0.0
    		msg.angular.y=0.0
   		msg.angular.z=0.0
   	 	return msg
		

def callback(data):
	global publisher, czas1,czas2
        print "kat"
        g = Twist()
	m=Twist()
	s=Twist()
	x = data.position.x
	y = data.position.y
        kat=arctan2(y,x)
	#zakladamy w=1.0
	w=0.7
	czas1=kat/w;


	odleglosc=math.sqrt(x*x+y*y)
	v=0.7
	czas2=odleglosc/v;



def listener():
	global publisher, mess, rate, pop, now, czas1, czas2
	rospy.init_node('sterowanie', anonymous = False)
	rospy.Subscriber('new_pose', Pose, callback)
	rospy.Subscriber('new_pose', Pose, callback)
	publisher = rospy.Publisher('/mux_vel_nav/cmd_vel', Twist, queue_size=10)
	rate=rospy.Rate(10)
	pop=rospy.get_time()
	now = rospy.get_time()
	czas3=0.0;
	#rospy.spin()
	while not rospy.is_shutdown():
		if(czas1 > 0):	
			mess=stworz_wiadomosc(2)
			pop=now
			now = rospy.get_time()
			czas1= czas1 - (now-pop)
			publisher.publish(mess)
			czas3=2.0
		elif(czas3>0):
			mess=stworz_wiadomosc(0)
			pop=now
			now = rospy.get_time()
			czas3= czas3 - (now-pop)
			publisher.publish(mess)

		elif(czas2 > 0):	
			mess=stworz_wiadomosc(1)
			pop=now
			now = rospy.get_time()
			czas2= czas2 - (now-pop)
			publisher.publish(mess)
		else :
			mess=stworz_wiadomosc(0)
			pop=now
			now = rospy.get_time()
			publisher.publish(mess)

		rate.sleep()
	#tworz wiadomosc

if __name__ == '__main__':
	listener()
