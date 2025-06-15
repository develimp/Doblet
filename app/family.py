'''
Proporciona la classe "Family".
'''
from database import Database


class Family():
	'''
	Aquesta classe controla els atributs
	de la taula "family" de la base de dades.

	Atributs:
	---------
	id : int
		El identificador a la taula "family" de la base de dades.
	discount : float
		Tant per cent de descompte que correspon a la familia.

	Mètodes:
	--------
	@classmethod get_family(id): list
	delete_family(id)
	get_members(id): list
	calculate_discount(members_list)
	calculate_family_members(members_list): int
	'''


	def __init__(self, id: int, discount: float):
		'''
		Inicialitza una nova instància de la classe Family.

		Paràmetres:
		-----------
		id : int
			El identificador a la taula "family" de la base de dades.
		discount : float
			Tant per cent de descompte que correspon a la familia.
		'''
		self.id = id
		self.discount = discount
		self.members_list = []


	@classmethod
	def get_family(cls, id):
		'''
		Recupera les dades de la familia i les retorna en forma de llista.
		Si es passa id = 0 retorna l'última familia de la taula.

		Paràmetres:
		-----------
		id : int
			El identificador de la familia.

		Retorna:
		--------
		family : list
			Llista amb totes les dades de la familia.
		'''
		db = Database('sp')
		if id == 0:
			family = db.select_last_family()
		else:
			family = db.select_family(id)
		db.close_connection()
		return family
	

	@classmethod
	def set_family(cls, discount):
		'''
		Inserta a la taula family una nova familia amb els paràmetres passats.

		Paràmetres:
		-----------
		discount : float
			Tant per cent de descompte que correspon a la familia.
		'''
		db = Database('sp')
		db.insert_family(discount)
		db.close_connection()


	def modify_family(self, id, discount):
		'''
		Modifica les dades de la familia.

		Paràmetres:
		-----------
		id : int
			El identificador a la taula "family" de la base de dades.
		discount : float
			Tant per cent de descompte que correspon a la familia.
		'''
		db = Database('sp')
		db.update_family(id, discount)
		db.close_connection()


	def delete_family(self, id):
		'''
		Elimina de la base de dades la familia indicada.

		Paràmetres:
		-----------
		id : int
			El identificador de la familia.
		'''
		db = Database('sp')
		db.delete_family(id)
		db.close_connection()


	def get_members(self, id):
		'''
		A partir de l'id de la familia retorna un llistat dels seus membres.

		Paràmetres:
		-----------
		id : int
			El identificador de la familia.

		Retorna:
		--------
		result: list
			Llistat de característiques de membres de la familia.
		'''
		db = Database('sp')
		result = db.select_members_by_family(id)
		db.close_connection()
		return result


	def calculate_discount(self, members_list):
		'''
		A partir del llistat de fallers d'una mateixa familia
		calculem el descompte segons els membres actius.

		Paràmetres:
		-----------
		members_list : list
			Llistat de fallers que pertanyen a la mateixa familia.
		'''
		family_members = 0
		is_maximum_fee = False
		for member in members_list:
			if member.is_registered:
				family_members = family_members + 1
				if member.category.id == 1:
					is_maximum_fee = True
		if is_maximum_fee and family_members == 3:
			self.discount = 5
		elif is_maximum_fee and family_members >= 4:
			self.discount = 10
		else:
			self.discount = 0


	def calculate_family_members(self, members_list):
		'''
		A partir del llistat de fallers d'una mateixa familia
		calculem els membres actius.

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