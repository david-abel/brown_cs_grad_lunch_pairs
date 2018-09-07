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

def make_new_pairs(list_of_students):
	'''
	Args:
		list_of_students (list)

	Returns:
		(dict): Key=student, Val=student
		(list)
	'''


	pairings = {}
	new_student_list = []
	random.shuffle(list_of_students)


	for student in list_of_students:

		if student in new_student_list:
			# Already handled this student.
			continue

		# Grab random new partner.
		possible_partners = [x for x in list_of_students if x != student and not student.is_past_partner(x)]
		if len(possible_partners) == 0:
			# All out of partners.
			raise ValueError("No possible partners remain.")

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
		list_of_students.remove(student)
		list_of_students.remove(partner)

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