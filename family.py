from database import Database

class Family():

	def __init__(self, id: int, discount: float, is_direct_debited: bool):

		self.id = id
		self.discount = discount
		self.is_direct_debited = is_direct_debited
		self.members_list = []


	@classmethod
	def get_family(cls, id):
		db = Database('sp')
		if id == 0:
			family = db.select_last_family()
		else:
			family = db.select_family(id)
		db.close_connection()
		return family
	

	@classmethod
	def set_family(cls, discount, is_direct_debited):
		db = Database('sp')
		db.insert_family(discount, is_direct_debited)
		db.close_connection()


	def modify_family(self, id, discount, is_direct_debited):
		db = Database('sp')
		db.update_family(id, discount, is_direct_debited)
		db.close_connection()


	def get_members(self, id):
		db = Database('sp')
		result = db.select_members_by_family(id)
		db.close_connection()
		return result


	def calculate_discount(self, members_list):
		'''
		A partir del llistat de fallers d'una mateixa familia calculem el descompte segons els membres actius.

		Paràmetres:
		-----------
		llistat_fallers : llista
			Llistat de fallers que pertanyen a la mateixa familia.
		'''
		family_members = 0
		is_maximum_fee = False
		for member in members_list:
			if member.is_registered:
				family_members = family_members + 1
				if member.category.id == 1:
					is_maximum_fee = True
		print(family_members)
		if is_maximum_fee and family_members == 3:
			self.discount = 5
		elif is_maximum_fee and family_members >= 4:
			self.discount = 10
		else:
			self.discount = 0


	def calculate_family_members(self, members_list):
		'''
		A partir del llistat de fallers d'una mateixa familia calculem els membres actius.

		Paràmetres:
		-----------
		members_list : list
			Llistat de fallers que pertanyen a la mateixa familia.

		Retorna:
        --------
        family_members : int
            Membres actius de la familia.
		'''
		family_members = 0
		for member in members_list:
			if member.is_registered:
				family_members = family_members + 1
		return family_members