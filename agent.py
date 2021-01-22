#!/usr/bin/env python
# encoding: utf8
# Artificial Intelligence, UBI 2019-20
# Modified by: Nuno Marques - 38958 | Tomás Vicente - 39067

import rospy
from std_msgs.msg import String
from nav_msgs.msg import Odometry
import time
import math

x_ant = 0
y_ant = 0
obj_ant = ''
current_room = 1
previous_room = 1
types_objects_known = []
start_time = time.time()

class room:
	def __init__(self,x_min,x_max,y_min,y_max,list_objects,type_room):
		self.x_min = x_min
		self.x_max = x_max
		self.y_min = y_min
		self.y_max = y_max
		self.xy_med = (round((((x_max-x_min)/2)+x_min),2),round((((y_max-y_min)/2)+y_min),2))
		self.list_objects = list_objects
		self.type_room = type_room
		self.occupied = False
		self.persons = 0
		self.books = 0
		self.beds = 0
		self.chairs = 0
		self.tables = 0
		self.computers = 0
		self.isMistery = False

room1 = room(-15.7,3.7,-3.1,-1.4,[],'Corridor')
room2 = room(-11.9,-9.3,-1.1,5.1,[],'Corridor')
room3 = room(-12.1,3.7,5.1,7.4,[],'Corridor')
room4 = room(-4.2,-1.1,-1.1,5.1,[],'Corridor')
room5 = room(-15.7,-12.1,-0.9,2.7,[],'')
room6 = room(-15.7,-12.1,2.7,7.4,[],'')
room7 = room(-15.7,-10.9,7.4,11.2,[],'')
room8 = room(-10.9,-6.0,7.4,11.2,[],'')
room9 = room(-5.7,-1.1,7.4,11.2,[],'')
room10 = room(-0.6,3.7,7.4,11.2,[],'')
room11 = room(-1.1,3.7,2.2,5.1,[],'')
room12 = room(-1.1,3.7,-0.9,1.8,[],'')
room13 = room(-9.3,-7.0,-0.9,5.1,[],'')
room14 = room(-6.5,-4.2,-0.9,5.1,[],'')

rooms = [room1,room2,room3,room4,room5,room6,room7,room8,room9,room10,room11,room12,room13,room14]

dictionary = {'1': [],'2': [],'3': [],'4': [],'5': [],'6': [],'7': [],
		'8': [],'9': [],'10': [],'11': [],'12': [],'13': [],'14': []}

#-------------Return the number of the Room--------------------------
def room_number(x,y):
	for i in range(len(rooms)):
		if(x <= rooms[i].x_max and x >= rooms[i].x_min):
			if(y <= rooms[i].y_max and y >= rooms[i].y_min):
				return(i+1)
	return(-1)

#-------------Detects the object in a Room--------------------------
def new_object(objects):
	print(objects)
	objs = objects.split(',')
	for i in range(len(objs)):
		s = objs[i].split('_', 1)
		if(not({"type": s[0], "name": s[1]} in rooms[current_room-1].list_objects)):
			rooms[current_room-1].list_objects.append({"type": s[0], "name": s[1]})
			
			if(not(s[0] in types_objects_known)):
				types_objects_known.append(s[0])
			
			if(s[0] == 'person'):
				rooms[current_room-1].occupied = True
				rooms[current_room-1].persons += 1
				room_type()
			if(s[0] == 'book'):
				rooms[current_room-1].books += 1
				room_type()
			if(s[0] == 'chair'):
				rooms[current_room-1].chairs += 1
				room_type()
			if(s[0] == 'table'):
				rooms[current_room-1].tables += 1
				room_type()
			if(s[0] == 'computer'):
				rooms[current_room-1].computers += 1
				room_type()
			if(s[0] == 'bed'):
				rooms[current_room-1].beds += 1
				room_type()
			if(s[0] == 'mistery'):
				rooms[current_room-1].isMistery = True

#-------------Identify the type of room--------------------------
def room_type():
	if(current_room == 1 or current_room == 2 or current_room == 3 or current_room == 4):
		rooms[current_room-1].type_room = "Corridor"
	else:
		if(rooms[current_room-1].tables == 1 and rooms[current_room-1].chairs > 1):
			rooms[current_room-1].type_room = "Meeting Room"
		elif(rooms[current_room-1].beds > 0 and rooms[previous_room-1].type_room != "Corridor"):
			rooms[current_room-1].type_room = "Suite"
			rooms[previous_room-1].type_room = "Suite"
		elif(rooms[current_room-1].beds == 1):
			rooms[current_room-1].type_room = "Single Room"
		elif(rooms[current_room-1].beds == 2):
			rooms[current_room-1].type_room = "Double Room"	
		else:
			rooms[current_room-1].type_room = "Generic Room"

#-------------Find all the paths from start to end--------------------------
def find_all_paths(graph, start, end, path=[]):
	path = path + [start]
	if start == end:
		return [path]
	if not graph.has_key(start):
		return []
	paths = []
	for node in graph[start]:
		if node not in path:
			newpaths = find_all_paths(graph, node, end, path)
			for newpath in newpaths:
				paths.append(newpath)
	return paths

# odometry callback
def callback(data):
	global x_ant, y_ant, previous_room, current_room
	x=data.pose.pose.position.x-15
	y=data.pose.pose.position.y-1.5
	# show coordinates only when they change

	if(x != x_ant or y != y_ant):
		print("(%.1f ; %.1f)") % (x,y)
		if(room_number(x,y) != -1 and current_room != room_number(x,y)):
			previous_room = current_room
			current_room = room_number(x,y)

			if(str(previous_room) not in dictionary[str(current_room)]):
				dictionary[str(current_room)].append(str(previous_room))
				dictionary[str(previous_room)].append(str(current_room))

	x_ant = x
	y_ant = y

# ---------------------------------------------------------------
# object_recognition callback
def callback1(data):
	global obj_ant
	obj = data.data
	if obj != obj_ant and data.data != "":
		new_object(data.data)
	obj_ant = obj

# ---------------------------------------------------------------
# questions_keyboard callback
def callback2(data):
	print("Question is %s") % data.data

	# Question 1 - How many rooms are not occupied?
	if(data.data == "01"):
		aux = 0
		# Search in all rooms how many are occupied
		for i in range(len(rooms)):
			if(rooms[i].occupied == True):
				aux += 1
		if(aux != 0):
			aux = 14 - aux
			print("Rooms not occupied: "+ str(aux))
		else:
			print("There is no one inside the rooms!")
	
	# Question 2 - How many suites did you find until now?
	elif(data.data == "02"):
		aux = 0
		for i in range(len(rooms)):
			if(rooms[i].type_room == "Suite"):
				aux += 1
		print("Total of Suites: "+str(int(aux/2)))
	
	# Question 3 - Is it more probable to find people in the corridors or inside the rooms?
	elif(data.data == "03"):
		qtd_person_c = 0.0
		qtd_person_r = 0.0
		qtd_person_total = 0.0
		prob_corr = 0.0
		prob_room = 0.0
		
		for i in range(len(rooms)):
			if(i < 4):
				qtd_person_c += rooms[i].persons
			else:
				qtd_person_r += rooms[i].persons
			qtd_person_total += rooms[i].persons
		if(qtd_person_total == 0):
			print("No one found yet!")
		else:
			prob_corr = qtd_person_c/qtd_person_total
			prob_room = qtd_person_r/qtd_person_total
			if(prob_corr > prob_room):
				print("It is more likely that people are on the corridors!")
			elif(prob_room > prob_corr):
				print("It is more likely that people are on the rooms!")
			else:
				print("The probabilities are the same!")
	
	# Question 4 - If you want to find a computer, to which type of room do you go to ?
	elif(data.data == "04"):
		qtd_single_room = 0.0
		qtd_double_room = 0.0
		qtd_suite_room = 0.0
		qtd_generic_room = 0.0
		total = len(rooms)
		
		for i in range(len(rooms)):
			if(rooms[i].type_room == "Single Room" and rooms[i].computers > 0):
				qtd_single_room += rooms[i].computers
			if(rooms[i].type_room == "Double Room" and rooms[i].computers > 0):
				qtd_double_room += rooms[i].computers
			if(rooms[i].type_room == "Suite" and rooms[i].computers > 0):
				qtd_suite_room += rooms[i].computers
			if(rooms[i].type_room == "Generic Room" and rooms[i].computers > 0):
				qtd_generic_room += rooms[i].computers
		
		if(qtd_single_room > (qtd_double_room or qtd_suite_room or qtd_generic_room)):
			print("Single Room (%.4f)") % (qtd_single_room/total)
		elif(qtd_double_room > (qtd_single_room or qtd_suite_room or qtd_generic_room)):
			print("Double Room (%.4f)") % (qtd_double_room/total)
		elif(qtd_suite_room > (qtd_single_room or qtd_double_room or qtd_generic_room)):
			print("Suite (%.4f)") % (qtd_suite_room/total)
		elif(qtd_generic_room > (qtd_single_room or qtd_double_room or qtd_suite_room)):
			print("Generic Room (%.4f)") % (qtd_generic_room/total)
		else:
			print("I could not find any computer yet!")
			
	# Question 5 - What is the number of the closest single room ?
	elif(data.data == "05"):
		flag_aux = True
		# Verify if agent has left the start room
		if(previous_room != current_room):
			b = 0
			aux_min = 100
			path_flag = 0
			for i in range(len(rooms)):
				if(rooms[i].type_room == "Single Room"):
					x0 = rooms[i].xy_med[0]
					y0 = rooms[i].xy_med[1]
					a = (x_ant-x0)**2+(y_ant-y0)**2
					b = math.sqrt(a)
					if(b < aux_min):
						aux_min = b
						path_flag = i+1
						flag_aux = False
			if(flag_aux):
				print("I could not find any Single Room!")
			else:
				print("Room "+str(path_flag))
		else:
			print("I have not visited any room before this one!")
	
	# Question 6 - How can you go from the current room to the elevator ?
	elif(data.data == "06"):
		print("The available paths to the elevator are:")
		print(find_all_paths(dictionary, str(current_room), "1"))

	# Question 7 - How many books do you estimate to find in the next 2 minutes ?
	elif(data.data == "07"):
		aux = 0
		for i in range(len(rooms)):
			aux += rooms[i].books
		med = 120*aux/(time.time()-start_time)
		print(int(round(med,0)))

	# Question 8 - What is the probability of finding a table in a room
	# without books but that has at least one chair ?
	elif(data.data == "08"):
		#P(T|BnC) = P(TnBnC)/P(BnC) = #TnBnC/#BnC [T = Table; B = Books (L=0); C = Chairs(C>=1)]
		qtd_chairs = 0.0
		qtd_total = 0.0
		qtd_rooms_bnc = 0.0
		qtd_rooms_tnbnc = 0.0
		prob = 0.0

		for i in range(len(rooms)):
			qtd_chairs += rooms[i].chairs
			qtd_total += len(rooms[i].list_objects)

		if(qtd_total == 0):
			print("I have not found any objects!")
		elif(qtd_chairs == 0):
			print("I have not found any chairs!")
		else:
			for j in range(len(rooms)):
				if(rooms[j].books == 0 and rooms[j].chairs >= 1):
					qtd_rooms_bnc += 1
				if(rooms[j].tables == 1 and rooms[j].books == 0 and rooms[j].chairs >= 1):
					qtd_rooms_tnbnc += 1
			prob = (qtd_rooms_tnbnc/qtd_rooms_bnc)
			print("Probability: %.3f") % prob

	# Question 9 - How many different types of objects have you discovered until now ?
	elif(data.data == "09"):
		if(len(types_objects_known) == 0):
			print("I have not found any objects!")
		else:
			print("I discovered: "+str(len(types_objects_known)))
	
	# Question 10 - Which objects were discovered in the current room until now ?
	elif(data.data == "10"):
		print("I discovered: "+str(rooms[current_room-1].list_objects))
	
	# Question 11 - What is the number of the room that contains more objects ?
	elif(data.data == "11"):
		aux_room = 0
		aux = 0
		big = 0
		for i in range(len(rooms)):
			if(rooms[i].list_objects > 0):
				aux = len(rooms[i].list_objects)
				if(aux > big):
					big = aux
					aux_room = i
		if(big == 0):
			print("I have not found any objects!")
		else:
			print("Room "+str(aux_room+1)+" ("+str(big)+")!")

	# Question 12 - What is the number of the room that contains the mysterious object ?
	elif(data.data == "12"):
		flag_aux = True
		for i in range(len(rooms)):
			if(rooms[i].isMistery == True):
				print("Room "+ str(i+1) + ": "+rooms[i].type_room)
				flag_aux = False
		if(flag_aux):
			print("The object was not discovered yet!")

# ---------------------------------------------------------------
def agent():
	rospy.init_node('agent')

	rospy.Subscriber("questions_keyboard", String, callback2)
	rospy.Subscriber("object_recognition", String, callback1)
	rospy.Subscriber("odom", Odometry, callback)

	rospy.spin()

# ---------------------------------------------------------------
if __name__ == '__main__':
	agent()
