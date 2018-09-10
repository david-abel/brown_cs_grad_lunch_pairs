# Python imports.
import os
import sys

# Other imports.
import make_pairings as mp
import populate

def get_next_file_name(file_name_base):
	'''
	Args:
		file_name_base (str)

	Returns:
		(str): Full file name of PREVIOUS file (includes .txt extension)
		(str): Full file name NEXT file (includes .txt extension)

	Summary:
		Finds the current week number and adds it to the end. Used for backtracking/etc.
	'''
	path_to_lunch_pairs = os.path.dirname(os.path.abspath(__file__))
	files_in_dir = [f for f in os.listdir(path_to_lunch_pairs) if os.path.isfile(os.path.join(path_to_lunch_pairs, f)) and "fall_2018" in f]

	max_week_num = float("-inf")
	for pairing_file in files_in_dir:
		pairing_file_no_extension = pairing_file[:pairing_file.index(".")]
		week_num = int(pairing_file_no_extension.split("_")[-1])

		if week_num > max_week_num:
			max_week_num = week_num

	prev_name = file_name_base + "_" + str(max_week_num) + ".txt"
	next_name = file_name_base + "_" + str(max_week_num + 1) + ".txt"

	return prev_name, next_name

def main():

	absent_list = ["david_abel@brown.edu"]

	file_name_base = "fall_2018_members"
	prev_file_name, next_file_name = get_next_file_name(file_name_base)

	# Populate.
	# students = populate.populate()
	# mp.save_students(students, file_name="fall_2018_members_0.txt")
	# sys.exit(1)

	# Load.
	student_list = mp.load_existing_students(file_name=prev_file_name)

	# Make new pairs.
	pairs, updated_student_list = mp.make_new_pairs(student_list, absent_list)

	# Save new list.
	mp.save_students(updated_student_list, file_name=next_file_name)

	# Show pairings, formatted for HTML.
	for k in sorted(pairs.keys(), key=lambda x: x.get_name()):
		if type(pairs[k]) == list:
			print "<tr><td>" + k.get_name() + "</td><td>" + pairs[k][0].get_name() + "</td><td>" + pairs[k][1].get_name() + "</td></tr>"
		else:
			print "<tr><td>" + k.get_name() + "</td><td>" + pairs[k].get_name() + "</td></tr>"


if __name__ == "__main__":
	main()