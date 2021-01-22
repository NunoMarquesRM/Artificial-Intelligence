#!/usr/bin/env python
# coding: utf8
import rospy
from std_msgs.msg import Int32,String
import sys
import tty

# ---------------------------------------------------------------
def questions():
	# node name
	rospy.init_node('questions_keyboard')
	pub=rospy.Publisher('questions_keyboard',String,queue_size=10)
	r = rospy.Rate(10)
	
	# show questions
	print ' ************************'
	print '    QUESTIONS '
	print ' ************************'
	print '  01-How many rooms are not occupied?'
	print '  02-How many suites did you find until now?'
	print '  03-Is it more probable to find people in the corridors or inside the rooms?'
	print '  04-If you want to find a computer, to which type of room do you go to?'
	print '  05-What is the number of the closest single room?'
	print '  06-How can you go from the current room to the elevator?'
	print '  07-How many books do you estimate to find in the next 2 minutes?'
	print '  08-What is the probability of finding a table in a room without books but that has at least one chair?'
	print '  09-How many different types of objects have you discovered until now?'
	print '  10-Which objects were discovered in the current room until now?'
	print '  11-What is the number of the room that contains more objects?'
	print '  12-What is the number of the room that contains the mysterious object?'

	tty.setcbreak(sys.stdin)

	while not rospy.is_shutdown():
		# read from keyboard
		k=sys.stdin.read(2)
		if int(k) < 1 or int(k) >12:
			continue
		pub.publish(k)
		#print 'Asked question: ' , k
		
# ---------------------------------------------------------------
if __name__ == '__main__':
	questions()
