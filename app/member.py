'''
Proporciona la classe "Member".
'''
from datetime import date, datetime

from database import Database

from family import Family
from category import Category

class Member():
	'''
	Aquesta classe controla els atributs
	de la taula "member" de la base de dades.

	Atributs:
	---------
	id : int
		El identificador a la taula "member" de la base de dades.
	name : string
		Nom del faller.
	surname : string
		Cognoms del faller.
	birthdate : date
		Data de naixement.
	gender : int
		Sexe.
	dni : string
		Dni.
	address : string
		Adreça.
	phone_number : string
		Telèfon.
	is_registered : bool
		Marca si està donat d'alta o no.
	email : string
		Correu electrònic.
	family : Family
		Familia a la que pertany.
	category : Category
		Categoria de la falla a la que pertany.

	Mètodes:
	--------
	@classmethod get_member(id): list
	@classmethod set_member(name, surname, birthdate, gender, dni, address,
		phone_number, is_registered, email, id_family, id_category)
	modify_member(id, name, surname, birthdate, gender, dni, address,
		phone_number, is_registered, email, id_family, id_category)
	get_membership_history(id)
	calculate_age(birthdate, falla_year): int
	calculate_category(age): int
	calculate_first_falla_year(birthdate): int
	pay_fee(transaction_date, amount, falla_year, description,
		receipt_number, id_member)
	pay_lottery(transaction_date, amount, falla_year, description,
		receipt_number, id_member)
	pay_raffle(transaction_date, amount, falla_year, description,
		receipt_number, id_member)
	'''


	def __init__(
		self,
		id: int,
		name: str,
		surname: str,
		birthdate: date,
		gender: int,
		dni: str,
		address: str,
		phone_number: str,
		is_registered: bool,
		email: str,
		family: Family = None,
		category: Category = None
	):
		'''
		Inicialitza una nova instància de la classe Member.

		Paràmetres:
		-----------
		id : int
			El identificador a la taula "member" de la base de dades.
		name : string
			Nom del faller.
		surname : string
			Cognoms del faller.
		birthdate : date
			Data de naixement.
		gender : int
			Sexe.
		dni : string
			Dni.
		address : string
			Adreça.
		phone_number : string
			Telèfon.
		is_registered : bool
			Marca si està donat d'alta o no.
		email : string
			Correu electrònic.
		family : Family
			Familia a la que pertany.
		category : Category
			Categoria de la falla a la que pertany.
		'''
		self.id = id
		self.name = name
		self.surname = surname
		self.birthdate = birthdate
		self.gender = gender
		self.dni = dni
		self.address = address
		self.phone_number = phone_number
		self.is_registered = is_registered
		self.email = email
		self.family = family
		self.category = category
		self.membership_history = {}


	@classmethod
	def get_member(cls, id):
		'''
		Recupera les dades del faller i les retorna en forma de llista.
		Si es passa id = 0 retorna l'últim membre de la taula.

		Paràmetres:
		-----------
		id : int
			El identificador del faller.

		Retorna:
		--------
		member : list
			Llista amb totes les dades del faller.
		'''
		db = Database('sp')
		if id == 0:
			member = db.select_last_member()
		else:
			member = db.select_member(id)
		db.close_connection()
		return member


	@classmethod
	def set_member(
		cls,
		name,
		surname,
		birthdate,
		gender,
		dni,
		address,
		phone_number,
		is_registered,
		email,
		id_family,
		id_category
	):
		'''
		Inserta a la taula member un nou faller amb els paràmetres passats.

		Paràmetres:
		-----------
		name : string
			Nom del faller.
		surname : string
			Cognoms del faller.
		birthdate : date
			Data de naixement.
		gender : int
			Sexe.
		dni : string
			Dni.
		address : string
			Adreça.
		phone_number : string
			Telèfon.
		is_registered : bool
			Marca si està donat d'alta o no.
		email : string
			Correu electrònic.
		id_family : int
			Identificador de la familia a la que pertany.
		id_category : int
			Identificador de la categoria de la falla a la que pertany.
		'''
		db = Database('sp')
		db.insert_member(
			name,
			surname,
			birthdate,
			gender,
			dni,
			address,
			phone_number,
			is_registered,
			email,
			id_family,
			id_category
		)
		db.close_connection()


	@classmethod
	def get_last_member(cls):
		db = Database('sp')
		member = db.select_last_member()
		db.close_connection()
		return member


	def modify_member(
		self,
		id,
		name,
		surname,
		birthdate,
		gender,
		dni,
		address,
		phone_number,
		is_registered,
		email,
		id_family,
		id_category
	):
		'''
		Modifica les dades del faller.

		Paràmetres:
		-----------
		id : int
			El identificador a la taula "member" de la base de dades.
		name : string
			Nom del faller.
		surname : string
			Cognoms del faller.
		birthdate : date
			Data de naixement.
		gender : int
			Sexe.
		dni : string
			Dni.
		address : string
			Adreça.
		phone_number : string
			Telèfon.
		is_registered : bool
			Marca si està donat d'alta o no.
		email : string
			Correu electrònic.
		id_family : int
			Identificador de la familia a la que pertany.
		id_category : int
			Identificador de la categoria de la falla a la que pertany.
		'''
		db = Database('sp')
		db.update_member(
			id,
			name,
			surname,
			birthdate,
			gender,
			dni,
			address,
			phone_number,
			is_registered,
			email,
			id_family,
			id_category
		)
		db.close_connection()


	def get_membership_history(self, id_member):
		'''
		Recupera l'historial del faller.

		Paràmetres:
		-----------
		id : int
			Identificador del faller.
		'''
		db = Database('sp')
		result = db.select_membership_history(id_member)
		db.close_connection()
		return result


	def set_membership_history(self, id_member, position, falla, falla_year):
		db = Database('sp')
		db.insert_membership_history(falla_year, position, falla, id_member)
		db.close_connection()


	def modify_membership_history(self, id_member, position, falla, falla_year):
		db = Database('sp')
		db.upsert_membership_history(falla_year, position, falla, id_member)
		db.close_connection()


	def calculate_age(self, birthdate, falla_year):
		'''
		A partir de la data de naixement i l'exercici actual
		calculem l'edat del faller a data 19 de març del present exercici.

		Paràmetres:
		-----------
		birthdate : string
			La data de naixement del faller.
		falla_year : int
			L'exercici actual.
		
		Retorna:
        --------
        age : int
            L'edat del faller a data 19 de març del present exercici.
		'''
		year = date.strftime(birthdate, '%Y')
		month = date.strftime(birthdate, '%m')
		day = date.strftime(birthdate, '%d')
		if int(month) > 3 or (int(month) == 3 and int(day) > 19):
			age = falla_year - int(year) - 1
		else:
			age = falla_year - int(year)
		return age
	

	@classmethod
	def calculate_category(cls, age):
		'''
		A partir de l'edat del faller assigna l'id
		de la categoria a la que pertany.

		Paràmetres:
		-----------
		age : int
			L'edat del faller a data 19 de març del present exercici.
		'''
		if age<5:
			category_id=5
		elif 5<=age<=9:
			category_id=4
		elif 10<=age<=13:
			category_id=3
		elif 14<=age<=17:
			category_id=2
		else:
			category_id=1
		return category_id
	

	def calculate_first_falla_year(self, birthdate):
		'''
		A partir de la data de naixement calculem
		quin podria haver segut el seu primer exercici.

		Paràmetres:
		-----------
		birthdate : string
			La data de naixement del faller.
		
		Retorna:
		--------
		first_falla_year : int
			Primer possible exercici del faller.
		'''
		year = date.strftime(birthdate, '%Y')
		month = date.strftime(birthdate, '%m')
		day = date.strftime(birthdate, '%d')
		if int(month) > 3 or (int(month) == 3 and int(day) > 19):
			first_falla_year = int(year) + 1
		else:
			first_falla_year = int(year)
		return first_falla_year