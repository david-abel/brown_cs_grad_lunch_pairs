class Student(object):

	def __init__(self, email, area="", previous_partners=None):
		# self.name = name
		self.email = email
		self.area = area
		self.previous_partners = previous_partners if previous_partners is not None else []

	def get_area(self):
		return self.area

	def get_name(self):
		return self.email.split("@")[0]

	def add_partner(self, new_partner):
		'''
		Args:
			new_partner (Student)
		'''
		if self.is_past_partner(new_partner):
			print "Warning: trying to add already existing partner (" + new_partner.get_name() + ") to " + self.name + "."
			return

		self.previous_partners.append(new_partner.get_name())

	def is_past_partner(self, other_student):
		'''
		Args:
			new_partner (Student)
		'''
		return other_student.get_name() in self.previous_partners

	def __str__(self):
		return self.email + ":" + self.area + ":" + str(self.previous_partners)
