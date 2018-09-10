# Python imports
import os, sys, ast
import random
from collections import defaultdict

# Other imports.
from StudentClass import Student

AREAS = ["AI/ML/Robotics", "Algorithms and Theory", "Computational Biology", "Computer Vision", "Computing Education", "Data Science", "Graphics and Visualization", "Human-Computer Interaction", "Natural Language Processing", "Programming Languages", "Security and Cryptography", "Systems", "None of the above"]


# ===============
# == Load/Save ==
# ===============

def load_existing_students(file_name="members.txt"):
	'''
	Args:
		file_name (str)
	'''
	students_file = open(file_name, "r")

	students_list = []
	for line in students_file.readlines():
		line = line.strip().split(":")
		email, area, other_students = line[0], line[1], ast.literal_eval(line[2])
		
		next_student = Student(email=email, area=area, previous_partners=other_students)
		students_list.append(next_student)

	return students_list

def save_students(list_of_student_objects, file_name="members.txt"):
	'''
	Args:
		list_of_student_objects (list)
		file_name (str):
	'''
	out_file = open(file_name, "w")

	for student in list_of_student_objects:
		out_file.write(str(student))
		out_file.write("\n")

	out_file.close()
	

# ================
# == Make Pairs ==
# ================

def make_new_pairs(list_of_students, absent_list=[]):
	'''
	Args:
		list_of_students (list)
		absent_list (list)

	Returns:
		(dict): Key=student, Val=student
		(list)
	'''

	# Setup data structures.
	pairings = {}
	new_student_list = []
	random.shuffle(list_of_students)
	active_students = [s for s in list_of_students if s.get_email() not in absent_list]
	all_students = list_of_students[:]
	need_partners = []

	# Make pairings.
	for student in all_students:

		if student.get_email() in absent_list:
			# Student in absent list.
			new_student_list.append(student)
			continue

		if student in new_student_list:
			# Already handled this student.
			continue

		# Grab all possible partners.
		possible_partners = [x for x in active_students if x != student and not student.is_past_partner(x)]
		
		# Grab possible partners from different area.
		possible_diff_area_partners = [x for x in possible_partners if x.get_area() != student.get_area()]
		
		if len(possible_partners) == 0:
			# All out of partners.
			need_partners.append(student)
			continue

		# Choose new partner, prioritizing diff area.
		if len(possible_diff_area_partners) > 0:
			partner = random.choice(possible_diff_area_partners)
		else:
			partner = random.choice(possible_partners)

		# Make pairing.
		pairings[student] = partner
		pairings[partner] = student
		student.add_partner(partner)
		partner.add_partner(student)

		# Update student list.
		new_student_list.append(student)
		new_student_list.append(partner)

		# Remove.
		active_students.remove(student)
		active_students.remove(partner)

	if len(need_partners) > 0:
		extra_student = need_partners[0]
		temp_student = random.choice(new_student_list)
		other_temp_student = pairings[temp_student]
		new_student_list.remove(temp_student)
		new_student_list.remove(other_temp_student)

		# Make trio.
		pairings[extra_student] = [temp_student, other_temp_student]
		extra_student.add_partner(temp_student)
		extra_student.add_partner(other_temp_student)
		pairings[temp_student] = [extra_student, other_temp_student]
		temp_student.add_partner(extra_student)
		pairings[other_temp_student] = [extra_student, temp_student]
		other_temp_student.add_partner(extra_student)
		new_student_list.append(extra_student)
		new_student_list.append(temp_student)
		new_student_list.append(other_temp_student)

	return pairings, new_student_list

def main():

	file_name = "test_members.txt"
	
	# Test students.
	alice = Student("alice_madeup@brown.edu", "AI", previous_partners=[""])
	bob = Student("bob@brown.edu", "PL", previous_partners=[""])
	charlie = Student("bob@brown.edu", "Sys", previous_partners=[""])
	dan = Student("dan@brown.edu", "Theory", previous_partners=[""])
	students = [alice, bob, charlie, dan]

	# Save.
	save_students(students, file_name=file_name)

	# Load.
	student_list = load_existing_students(file_name=file_name)

	# Make new pairs.
	pairs, updated_student_list = make_new_pairs(student_list)

	# Save new list.
	save_students(updated_student_list, file_name=file_name)

	# Show pairings.
	print
	for k in pairs.keys():
		print k.get_name(), pairs[k].get_name()
	

if __name__ == "__main__":
	main()