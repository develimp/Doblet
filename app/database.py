import mysql.connector
from tkinter import messagebox
import subprocess
from pathlib import Path
from dotenv import load_dotenv
import os

from utils import Utils
from create_database import CreateDatabase


class Database:
	'''
	Aquesta classe controla la conexió amb MariaDb i totes les operacions CRUD
	amb la base de dades.

	Atributs:
	---------
	db_name : string
		Nom de la base de dades.
	'''
	def __init__(self, db_name):
		'''
		Inicialitza una nova instància de la classe Database.
		Conexió MariaDb.

		Paràmetres:
		-----------
		db_name : string
			Nom de la base de dades.
		'''
		dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
		load_dotenv(dotenv_path)
		
		try:
			self.mysqlConnection = mysql.connector.connect(
				host = os.getenv("MYSQL_HOST"),
				user = os.getenv("MYSQL_USER"),
				password = os.getenv("MYSQL_PASSWORD"),
				database = db_name
			)
			if self.mysqlConnection.is_connected():
				self.mysqlCursor = self.mysqlConnection.cursor()
		except:
			messagebox.showerror(
				"Error",
				"No s'ha pogut establir la conexió amb la base de dades."
			)
			self.verify_existence_db(db_name)

	
	def close_connection(self):
		'''
		Tancament de la conexió.
		'''
		self.mysqlCursor.close()
		self.mysqlConnection.close()


	def verify_existence_db(self, db_name):
		'''
		Verifica la existència de la base de dades i en cas contrari la crea.

		Paràmetres:
		-----------
		db_name : string
			Nom de la base de dades.
		'''
		try:
			self.mysqlConnection = mysql.connector.connect(
				host = "localhost",
				user = "root",
				password = "hamuclaulo07"
			)
			if self.mysqlConnection.is_connected():
				self.mysqlCursor = self.mysqlConnection.cursor()
			else:
				messagebox.showerror(
					"Error",
					"No s'ha pogut establir la conexió amb la base de dades."
				)
			query = f"SHOW DATABASES LIKE '{db_name}'"
			self.mysqlCursor.execute(query)
			result = self.mysqlCursor.fetchone()
			self.close_connection()
			if result:
				pass
			else:
				messagebox.showerror(
					"Error",
					"La base de dades no existeix"
				)
				CreateDatabase()
				value = messagebox.askquestion("Restaurar","Vols restaurar la base de dades?")
				if value == "yes":
					self.restore_backup_database("root", "hamuclaulo07", "sp")
				else:
					messagebox.showinfo("Info", "La base de dades es crearà automàticament")
					self.insert_initial_data('sp')
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"No s'ha pogut verificar l'existència de la base de dades."
			)

	
	def insert_initial_data(self, db_name):

		try:
			self.mysqlConnection = mysql.connector.connect(
				host = "localhost",
				user = "root",
				password = "hamuclaulo07",
				database = db_name
			)
			if self.mysqlConnection.is_connected():
				self.mysqlCursor = self.mysqlConnection.cursor()
		except:
			messagebox.showerror(
				"Error",
				"No s'ha pogut establir la conexió amb la base de dades."
			)
		self.insert_falla_year()
		self.insert_category(360, "adult", "major de 18 anys")
		self.insert_category(225, "cadet", "entre 14 i 17 anys")
		self.insert_category(150, "jovenil", "entre 10 i 13 anys")
		self.insert_category(95, "infantil", "entre 5 i 9 anys")
		self.insert_category(40, "bebe", "menor de 5 anys")


	def create_backup_database(self, user, password, db_name):
		try:
			base_path = Path(__file__).parent.resolve()

			structure_file = (base_path.parent / 'db' / 'dump' / '01_backup_structure.sql')
			data_file = (base_path.parent / 'db' / 'dump' / '02_backup_data.sql')
			routines_triggers_file = (base_path.parent / 'db' / 'dump' / '03_backup_routines_triggers.sql')
			command_structure = f"docker exec mariadb mysqldump -u {user} -p{password} --no-data --skip-triggers {db_name} > {structure_file}"
			process = subprocess.run(command_structure, shell = True, check = True)
			command_data = f"docker exec mariadb mysqldump -u {user} -p{password} --no-create-info --skip-triggers {db_name} > {data_file}"
			process = subprocess.run(command_data, shell = True, check = True)
			command_routines_triggers = f"docker exec mariadb mysqldump -u {user} -p{password} --no-create-info --no-data --routines --triggers {db_name} > {routines_triggers_file}"
			process = subprocess.run(command_routines_triggers, shell = True, check = True)

			if process.returncode == 0:
				messagebox.showinfo("Backup", "S'ha creat la copia de seguretat correctament")

		except subprocess.CalledProcessError:
			messagebox.showerror("Backup", "Error en la creació del backup")


	def restore_backup_database(self, user, password, db_name):
		base_path = Path(__file__).parent.resolve()
		structure_file = (base_path.parent / 'db' / 'dump' / '01_backup_structure.sql')
		data_file = (base_path.parent / 'db' / 'dump' / '02_backup_data.sql')
		routines_triggers_file = (base_path.parent / 'db' / 'dump' / '03_backup_routines_triggers.sql')
		host = "localhost"
		port = 3306
		command_structure = f"mysql -u {user} -p{password} -h{host} -P{port} {db_name} < {structure_file}"
		command_data = f"mysql -u {user} -p{password} -h{host} -P{port} {db_name} < {data_file}"
		command_routines_triggers = f"mysql -u {user} -p{password} -h{host} -P{port} {db_name} < {routines_triggers_file}"
		try:
			process = subprocess.run(command_structure, shell = True, check = True)

			if process.returncode == 0:
				messagebox.showinfo("Backup", "L'estructura de la còpia de seguretat s'ha restaurat correctament")

			process = subprocess.run(command_data, shell = True, check = True)

			if process.returncode == 0:
				messagebox.showinfo("Backup", "Les dades de la còpia de seguretat s'han restaurat correctament")

			process = subprocess.run(command_routines_triggers, shell = True, check = True)

			if process.returncode == 0:
				messagebox.showinfo("Backup", "Els triggers i procediments de la còpia de seguretat s'han restaurat correctament")

		except subprocess.CalledProcessError:
			messagebox.showerror("Backup", "Error en la restauració del backup")


	# Mètodes per a operacions CRUD en la taula member.
	def insert_member(
			self,
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
		Escriu a la base de dades les dades del faller que se li passa
		com a paràmetre a la taula "member".

		Paràmetres:
		-----------
		name : string
			Nom el faller.
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
		query = "INSERT INTO member \
			(name, surname, birthdate, gender, dni, address, phoneNumber, \
				isRegistered, email, familyFk, categoryFk) \
					VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
		data = name, surname, birthdate, gender, dni, address, phone_number, \
			is_registered, email, id_family, id_category
		try:
			self.mysqlCursor.execute(query, data)
			self.mysqlConnection.commit()
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al insertar faller a la base de dades"
			)


	def count_members(self):
		'''
		Compta en la taula "member" la quantitat de fallers totals.

		Retorna:
		--------
		members_count : int
			Quantitat de fallers a la taula.
		'''
		query = "SELECT COUNT(*) FROM member"
		try:
			self.mysqlCursor.execute(query)
			total_members = self.mysqlCursor.fetchone()
			return total_members[0]
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir la quantitat de fallers de la base de dades"
			)


	def select_member(self, id):
		'''
		Llig de la taula "member" aquell faller amb
		l'id que se li passa per paràmetre.

		Paràmetres:
		-----------
		id : int
			Identificador del faller.

		Retorna:
		--------
		member : list
			Llistat de les dades del faller.
		'''
		query = "SELECT * FROM member INNER JOIN family \
			ON member.familyFk = family.id INNER JOIN category \
				ON member.categoryFk = category.id where member.id = %s"
		try:
			self.mysqlCursor.execute(query, (id,))
			member = self.mysqlCursor.fetchone()
			return member
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir membre de la base de dades"
			)


	def select_last_member(self):
		'''
		Llig l'últim registre de la taula "member".

		Retorna:
		--------
		member : list
			Llistat de les dades del faller.
		'''
		query = "SELECT * FROM member ORDER BY id DESC LIMIT 1"
		try:
			self.mysqlCursor.execute(query)
			member = self.mysqlCursor.fetchone()
			return member
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir l'últim membre de la base de dades"
			)


	def select_members_by_surname(self, surname):
		'''
		Llig de la taula "member" tots aquells fallers
		amb un cognom que conté la cadena passada per paràmetre.

		Paràmetres:
		-----------
		surname : string
			Cadena a la que s'ha de pareixer el cognom dels fallers.

		Retorna:
		--------
		members_list : list
			Llistat de fallers.
		'''
		query = "SELECT * FROM member INNER JOIN family \
			ON member.familyFk = family.id INNER JOIN category \
				ON member.categoryFk = category.id \
					WHERE member.surname LIKE %s"
		try:
			self.mysqlCursor.execute(query, (f"%{surname}%",))
			members_list = self.mysqlCursor.fetchall()
			return members_list
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir membres per cognom a la base de dades"
			)


	def select_adult_members(self):
		'''
		Llig de la taula "member" tots aquells fallers amb 14 anys o més
		(categories 1 i 2) i els afegeix a una llista de fallers.

		Retorna:
		--------
		members_list : list
			Llistat de fallers.
		'''
		query = "SELECT * FROM member INNER JOIN family \
			ON member.familyFk = family.id INNER JOIN category \
				ON member.categoryFk = category.id \
					WHERE member.isRegistered and \
						(member.categoryFk = 1 or member.categoryFk = 2) \
							ORDER BY member.surname"
		try:
			self.mysqlCursor.execute(query)
			members_list = self.mysqlCursor.fetchall()
			return members_list
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir els membres adults de la base de dades"
			)


	def select_underage_members(self):
		'''
		Llig de la taula "member" tots aquells fallers amb menys de 18 anys
		(categories 3, 4 i 5) i els afegeix a una llista de fallers.

		Retorna:
		--------
		members_list : list
			Llistat de fallers.
		'''
		query = "SELECT * FROM member INNER JOIN family \
			ON member.familyFk = family.id INNER JOIN category \
				ON member.categoryFk = category.id \
					WHERE member.isRegistered and \
						(member.categoryFk = 3 or member.categoryFk = 4 \
							or member.categoryFk = 5) \
								ORDER BY member.surname"
		try:
			self.mysqlCursor.execute(query)
			members_list = self.mysqlCursor.fetchall()
			return members_list
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir els membres menors d'edat de la base de dades"
			)


	def select_registered_members(self, is_registered):
		'''
		Llig de la taula "member" tots aquells fallers actius
		i els afegeix a una llista de fallers.

		Retorna:
		--------
		members_list : list
			Llistat de fallers.
		'''
		query = "SELECT * FROM member INNER JOIN family \
			ON member.familyFk = family.id INNER JOIN category \
				ON member.categoryFk = category.id \
					WHERE member.isRegistered = %s \
						ORDER BY member.surname"
		try:
			self.mysqlCursor.execute(query, (is_registered,))
			members_list = self.mysqlCursor.fetchall()
			return members_list
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir els membres actius de la base de dades"
			)


	def select_members_by_family(self, id_family):
		'''
		Llig de la taula "member" tots aquells fallers
		amb l'identificador de familia passat per paràmetre.

		Paràmetres:
		-----------
		id_family : int
			Identificador de la familia del faller.

		Retorna:
		--------
		members_list : list
			Llistat de fallers.
		'''
		query = "SELECT * FROM member INNER JOIN family \
			ON member.familyFk = family.id INNER JOIN category \
				ON member.categoryFk = category.id WHERE member.familyFk = %s"
		try:
			self.mysqlCursor.execute(query, (id_family,))
			members_list = self.mysqlCursor.fetchall()
			return members_list
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir els membres per familia de la base de dades"
			)


	def select_members_by_category(self, id_category):
		'''
		Llig de la taula "member" tots aquells fallers
		amb l'identificador de categoria passat per paràmetre.

		Paràmetres:
		-----------
		id_category : int
			Identificador de la categoria del faller.

		Retorna:
		--------
		members_list : list
			Llistat de fallers.
		'''
		query = "SELECT * FROM member INNER JOIN family \
			ON member.familyFk = family.id INNER JOIN category \
				ON member.categoryFk = category.id WHERE member.isRegistered = 1 AND member.categoryFk = %s"
		try:
			self.mysqlCursor.execute(query, (id_category,))
			members_list = self.mysqlCursor.fetchall()
			return members_list
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir els membres per categoria de la base de dades"
			)


	def update_member(
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
		Actualitza la taula "member" amb les dades del faller
		que se li passa per paràmetre.

		Paràmetres:
		-----------
		id : int
			Identificador del faller.
		name : string
			Nom el faller.
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
		query = "UPDATE member SET name = %s, surname = %s, birthdate = %s, \
			gender = %s, dni = %s, address = %s, phoneNumber = %s, \
				isRegistered = %s, email = %s, familyFk = %s, categoryFk = %s \
					WHERE id = %s"
		data = name, surname, birthdate, gender, dni, address, \
			phone_number, is_registered, email, id_family, id_category, id
		try:
			self.mysqlCursor.execute(query, data)
			self.mysqlConnection.commit()
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al actualitzar les dades del faller a la base de dades"
			)


	# Mètodes per a operacions CRUD en la taula family.
	def insert_family(self, discount):
		'''
		Escriu a la base de dades les dades de la familia que se li passa
		com a paràmetre a la taula "family".

		Paràmetres:
		-----------
		discount : float
			Descompte familiar.
		'''
		query = "INSERT INTO family (discount) \
			VALUES (%s)"
		try:
			self.mysqlCursor.execute(query, discount)
			self.mysqlConnection.commit()
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al insertar una nova familia a la base de dades"
			)


	def select_family(self, id):
		'''
		Llig de la taula "family" aquella familia
		amb l'id que se li passa per paràmetre.

		Paràmetres:
		-----------
		id : integer
			Identificador de la familia.

		Retorna:
		--------
		family : list
			Llista de dades de la familia.
		'''
		query = "SELECT * FROM family where id = %s"
		try:
			self.mysqlCursor.execute(query, (id,))
			family = self.mysqlCursor.fetchone()
			return family
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir una familia de la base de dades"
			)


	def select_last_family(self):
		'''
		Llig l'últim registre de la taula "family".

		Retorna:
		--------
		family : list
			Llista de dades de la familia.
		'''
		query = "SELECT * FROM family ORDER BY id DESC LIMIT 1"
		try:
			self.mysqlCursor.execute(query)
			family = self.mysqlCursor.fetchone()
			return family
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir l'última familia de la base de dades"
			)


	def select_families(self):
		'''
		Llig tot el contingut de la taula "family" i els afegeix a una llista de families.

		Retorna:
		--------
		families_list : list
			Llistat de families.
		'''
		query = "SELECT * FROM family"
		try:
			self.mysqlCursor.execute(query)
			families_list = self.mysqlCursor.fetchall()
			return families_list
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir les families de la base de dades"
			)


	def select_discount_by_member(self, id_member):
		'''
		Llig de la taula "family" el descompte familiar.

		Paràmetres:
		-----------
		id_member : integer
			Identificador del membre de la familia.

		Retorna:
		--------
		discount : float
			Llista de dades de la familia.
		'''
		query = "SELECT discount FROM family INNER JOIN member \
			ON family.id = member.familyFk WHERE member.id = %s"
		try:
			self.mysqlCursor.execute(query, (id_member,))
			discount = self.mysqlCursor.fetchone()
			return discount
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir el descompte familiar de la base de dades"
			)


	def update_family(self, id, discount):
		'''
		Actualitza la taula "family" amb les dades
		de la familia que se li passa per paràmetre.

		Paràmetres:
		-----------
		id : int
			Identificador de la familia.
		discount : float
			Descompte familiar.
		'''
		query = "UPDATE family SET discount = %s \
			WHERE id = %s"
		data = discount, id
		try:
			self.mysqlCursor.execute(query, data)
			self.mysqlConnection.commit()
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al modificar la familia de la base de dades"
			)


	def delete_family(self, id):
		'''
		Elimina de la base de dades la familia, el id de la qual,
		se li passa per paràmetre.

		Paràmetres:
		-----------
		id : int
			Identificador de la familia a eliminar.
		'''
		query = "DELETE FROM family WHERE id = %s"
		try:
			self.mysqlCursor.execute(query, (id,))
			self.mysqlConnection.commit()
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al eliminar la familia de la base de dades"
			)


	# Mètodes per a operacions CRUD en la taula movement.
	def select_fee_assignment_movements_by_member(self, id_member, falla_year):
		'''
		Llig els moviments d'assignació de quota del faller i exercici
		passats per paràmetre.

		Paràmetres:
		-----------
		id_member : int
			Identificador del faller.
		falla_year : int
			Exercici faller.

		Retorna:
		--------
		movements_list : list
			Llistat de moviments.
		'''
		query = "SELECT amount FROM movement \
			WHERE memberFk = %s and idType = 1 \
				and idConcept = 1 and fallaYearFk = %s"
		try:
			self.mysqlCursor.execute(query, (id_member, falla_year))
			movements_list = self.mysqlCursor.fetchall()
			return movements_list
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir els moviments d'assignació de quota"
			)


	def select_lottery_assignment_movements_by_member(
			self,
			id_member,
			falla_year
		):
		'''
		Llig els moviments d'assignació de loteria del faller
		i exercici passats per paràmetre.

		Paràmetres:
		-----------
		id_member : int
			Identificador del faller.
		falla_year : int
			Exercici faller.
		
		Retorna:
		--------
		movements_list : list
			Llistat de moviments.
		'''
		query = "SELECT amount FROM movement \
			WHERE memberFk = %s and idType = 1 and \
				idConcept = 2 and fallaYearFk = %s"
		try:
			self.mysqlCursor.execute(query, (id_member, falla_year))
			movements_list = self.mysqlCursor.fetchall()
			return movements_list
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir els moviments d'assignacio de loteria"
			)


	def select_raffle_assignment_movements_by_member(
			self,
			id_member,
			falla_year
		):
		'''
		Llig els moviments d'assignació de rifa del faller
		i exercici passats per paràmetre.

		Paràmetres:
		-----------
		id_member : int
			Identificador del faller.
		falla_year : int
			Exercici faller.
		
		Retorna:
		--------
		movements_list : list
			Llistat de moviments.
		'''
		query = "SELECT amount FROM movement \
			WHERE memberFk = %s and idType = 1 \
				and idConcept = 3 and fallaYearFk = %s"
		try:
			self.mysqlCursor.execute(query, (id_member, falla_year))
			movements_list = self.mysqlCursor.fetchall()
			return movements_list
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir els moviments d'assignacio de rifa"
			)


	def select_fee_payment_movements_by_member(self, id_member, falla_year):
		'''
		Llig els moviments de pagament de quota del faller
		i exercici passats per paràmetre.

		Paràmetres:
		-----------
		id_member : int
			Identificador del faller.
		falla_year : int
			Exercici faller.

		Retorna:
		--------
		movements_list : list
			Llistat de moviments.
		'''
		query = "SELECT amount FROM movement \
			WHERE memberFk = %s and idType = 2 \
				and idConcept = 1 and fallaYearFk = %s"
		try:
			self.mysqlCursor.execute(query, (id_member, falla_year))
			movements_list = self.mysqlCursor.fetchall()
			return movements_list
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir els moviments de pagament de quota")


	def select_lottery_payment_movements_by_member(
			self,
			id_member,
			falla_year
		):
		'''
		Llig els moviments de pagament de loteria del faller
		i exercici passats per paràmetre.

		Paràmetres:
		-----------
		id_member : int
			Identificador del faller.
		falla_year : int
			Exercici faller.

		Retorna:
		--------
		movements_list : list
			Llistat de moviments.
		'''
		query = "SELECT amount FROM movement \
			WHERE memberFk = %s and idType = 2 \
				and idConcept = 2 and fallaYearFk = %s"
		try:
			self.mysqlCursor.execute(query, (id_member, falla_year))
			movements_list = self.mysqlCursor.fetchall()
			return movements_list
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir els moviments de pagament de loteria"
			)


	def select_raffle_payment_movements_by_member(self, id_member, falla_year):
		'''
		Llig els moviments de pagament de rifa del faller
		i exercici passats per paràmetre.

		Paràmetres:
		-----------
		id_member : int
			Identificador del faller.
		falla_year : int
			Exercici faller.

		Retorna:
		--------
		movements_list : list
			Llistat de moviments.
		'''
		query = "SELECT amount FROM movement \
			WHERE memberFk = %s and idType = 2 \
				and idConcept = 3 and fallaYearFk = %s"
		try:
			self.mysqlCursor.execute(query, (id_member, falla_year))
			movements_list = self.mysqlCursor.fetchall()
			return movements_list
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir els moviments de pagament de rifa"
			)


	def select_payment_movements_by_date(self, date, description):
		'''
		Llig tots els moviments de pagament de la data
		passada per paràmetre.

		Paràmetres:
		-----------
		date : string
			Data.
		description : string
			Dexcripció de pagat per caixa o banc.

		Retorna:
		--------
		movements_list : list
			Llistat de moviments.
		'''
		query = "SELECT * FROM movement \
			INNER JOIN member ON movement.memberFk = member.id \
			WHERE transactionDate = %s and idType = 2 \
				and description = %s"
		try:
			self.mysqlCursor.execute(query, (date, description))
			movements_list = self.mysqlCursor.fetchall()
			return movements_list
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir els moviments del dia"
			)


	def insert_movement(
			self,
			transaction_date,
			amount,
			id_type,
			id_concept,
			falla_year,
			id_member,
			description,
			receipt_number
		):
		'''
		Escriu a la base de dades el moviment que se li passa
		com a paràmetre a la taula "movement".

		Paràmetres:
		-----------
		transaction_date : date
			Data en que s'efectua el moviment.
		amount : float
			Quantitat de diners.
		id_type : int
			Tipo de moviment. Pot ser assignació o pagament.
		id_concept : int
			Concepte. Pot ser quota, loteria o rifa.
		falla_year : int
			Exercici faller.
		id_member : int
			Identificador del faller sobre el que es fa el moviment.
		description : string
			Descripció del moviment.
		receipt_number : int
			Número de rebut.
		'''
		query = "INSERT INTO movement \
			(transactionDate, amount, idType, idConcept, fallaYearFk, \
				memberFk, description, receiptNumber) \
					VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
		data = transaction_date, amount, id_type, id_concept, \
			falla_year, id_member, description, receipt_number
		try:
			self.mysqlCursor.execute(query, data)
			self.mysqlConnection.commit()
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al insertar un moviment a la base de dades"
			)


	def select_movements_by_member(self, id_member, falla_year):
		'''
		Llig de la taula "movement" tots aquells moviments amb
		l'identificador de faller i l'exercici passats per paràmetre.

		Paràmetres:
		-----------
		id_member : int
			Identificador del faller.
		falla_year : int
			Exercici per al qual es volen recuperar les dades.

		Retorna:
		--------
		movements_list : list
			Llistat de moviments.
		'''
		query = "SELECT * FROM movement WHERE memberFk = %s AND fallaYearFk = %s"
		try:
			self.mysqlCursor.execute(query, (id_member, falla_year))
			movements_list = self.mysqlCursor.fetchall()
			return movements_list
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir els moviments per faller de la base de dades"
			)


	# Mètodes per a operacions CRUD en la taula category.
	def insert_category(self, fee, name, description):
		'''
		Escriu a la base de dades la categoria que se li passa
		com a paràmetre a la taula "category".

		Paràmetres:
		-----------
		fee : float
			Quota.
		name : string
			Nom de la categoria.
		description : string
			Descripció de la categoria.
		'''
		query = "INSERT INTO category (fee, name, description) VALUES (%s, %s, %s)"
		data = fee, name, description
		try:
			self.mysqlCursor.execute(query, data)
			self.mysqlConnection.commit()
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al insertar una categoria a la base de dades"
			)


	def select_category(self, id):
		'''
		Llig de la taula "category" aquella categoria 
		amb l'id que se li passa per paràmetre.

		Paràmetres:
		-----------
		id : int
			Identificador de la categoria.

		Retorna:
		--------
		category : list
			Llistat de dades de la categoria.
		'''
		query = "SELECT * FROM category where id = %s"
		try:
			self.mysqlCursor.execute(query, (id,))
			category = self.mysqlCursor.fetchone()
			return category
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir la categoria de la base de dades"
			)


	def select_categories(self):
		'''
		Llig totes les categories de la taula "category"

		Retorna:
		--------
		categories_list : list
			Llistat de categories.
		'''
		query = "SELECT * FROM category"
		try:
			self.mysqlCursor.execute(query)
			categories_list = self.mysqlCursor.fetchall()
			return categories_list
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir les categories de la base de dades"
			)


	def select_fee_by_member(self, id_member):
		'''
		Llig de la taula "category" en combinació amb la taula "member"
		la quota de la categoria a la que pertany el faller.

		Paràmetres:
		-----------
		id_member : int
			Identificador del faller.

		Retorna:
		--------
		fee : int
			Quota assignada al faller per la categoria a la que correspon.
		'''
		query = "SELECT fee FROM category INNER JOIN member \
			ON category.id = member.categoryFk WHERE member.id = %s"
		try:
			self.mysqlCursor.execute(query, (id_member,))
			fee = self.mysqlCursor.fetchone()
			return fee
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir la quota del faller de la base de dades"
			)


	def update_category(self, id, fee, name, description):
		'''
		Actualitza la taula "category" amb les dades de la categoria
		que se li passa per paràmetre.

		Paràmetres:
		-----------
		id : int
			El identificador a la taula "category" de la base de dades.
		fee : float
			Quantitat a pagar corresponent a dita categoria.
		name : string
			Forma amb la que es nombra dita categoria.
		description : string
			Informació sobre les edats a les quals correspon la categoria.
		'''
		query = "UPDATE category \
			SET fee = %s, name = %s, description = %s WHERE id = %s"
		data = fee, name, description, id
		try:
			self.mysqlCursor.execute(query, data)
			self.mysqlConnection.commit()
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al modificar les dades de la categoria"
			)


	def select_current_falla_year(self):
		'''
		Llig l'exercici actual.

		Retorna:
		--------
		falla_year : int
			Exercici actual.
		'''
		query = "SELECT code FROM fallaYear ORDER BY code DESC LIMIT 1"
		try:
			self.mysqlCursor.execute(query)
			falla_year = self.mysqlCursor.fetchone()
			return falla_year[0]
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir l'exercici a la base de dades"
			)

	# Mètodes per a operacions CRUD en la taula lottery
	def select_lotteries_list(self):
		'''
		Llig el llistat de sortejos guardats

		Retorna:
		--------
		lotteries_list : list
			Llistat de sortejos guardats.
		'''
		query = "SELECT DISTINCT lotteryName, fallaYearFk FROM lottery"
		try:
			self.mysqlCursor.execute(query)
			lotteries_list = self.mysqlCursor.fetchall()
			return lotteries_list
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir el llistat de sortejos"
			)


	def select_lotteries_by_lottery_name(self, lottery_name, falla_year):
		query = "SELECT * FROM lottery INNER JOIN member \
			ON lottery.memberFk = member.id \
				WHERE lottery.lotteryName = %s \
					AND lottery.fallaYearFk = %s"
		try:
			data = lottery_name, falla_year
			self.mysqlCursor.execute(query, data)
			lottery_list = self.mysqlCursor.fetchall()
			return lottery_list
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir el llistat del sorteig de la base de dades"
			)


	def insert_lottery(
		self,
		lottery_id,
		lottery_name,
		falla_year,
		tickets_male,
		tickets_female,
		tickets_childish,
		tenths_male,
		tenths_female,
		tenths_childish,
		assigned,
		id_member
	):
		query = """INSERT INTO lottery 
			(lotteryId, lotteryName, fallaYearFk, memberFk, 
			ticketsMale, ticketsFemale, ticketsChildish,
			tenthsMale, tenthsFemale, tenthsChildish, isAssigned)
				SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
					WHERE NOT EXISTS (
						SELECT 1 FROM lottery WHERE lotteryId = %s AND lotteryName = %s AND fallaYearFk = %s
					)"""
		data = lottery_id, lottery_name, falla_year, id_member, tickets_male, tickets_female, tickets_childish, tenths_male, tenths_female, tenths_childish, assigned, lottery_id, lottery_name, falla_year
		try:
			self.mysqlCursor.execute(query, data)
			self.mysqlConnection.commit()
		except mysql.connector.Error as e:
			print({e})
			messagebox.showerror(
				"Error",
				"Error al insertar la loteria"
			)


	def update_lottery(
		self,
		lottery_id,
		lottery_name,
		falla_year,
		tickets_male,
		tickets_female,
		tickets_childish,
		tenths_male,
		tenths_female,
		tenths_childish,
		id_member
	):
		query = """UPDATE lottery SET memberFk = %s,
			ticketsMale = %s, ticketsFemale = %s, ticketsChildish = %s,
			tenthsMale = %s, tenthsFemale = %s, tenthsChildish = %s
			WHERE lotteryId = %s AND lotteryName = %s AND fallaYearFk = %s"""
		data = id_member, tickets_male, tickets_female, tickets_childish, tenths_male, tenths_female, tenths_childish, lottery_id, lottery_name, falla_year
		try:
			self.mysqlCursor.execute(query, data)
			self.mysqlConnection.commit()
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al actualitzar les dades de la loteria a la base de dades"
			)


	def update_lottery_assigned(self, lottery_id, lottery_name, falla_year):
		query = """UPDATE lottery SET isAssigned = 1 WHERE lotteryId = %s AND lotteryName = %s AND fallaYearFk = %s"""
		data = lottery_id, lottery_name, falla_year
		try:
			self.mysqlCursor.execute(query, data)
			self.mysqlConnection.commit()
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al actualitzar les assignacions de la loteria a la base de dades"
			)


	def delete_lottery(self, lottery_id, lottery_name, falla_year):
		query = """DELETE FROM lottery WHERE lotteryId = %s AND lotteryName = %s AND fallaYearFk = %s"""
		data = lottery_id, lottery_name, falla_year
		try:
			self.mysqlCursor.execute(query, data)
			self.mysqlConnection.commit()
		except mysql.connector.Error as e:
			print({e})
			messagebox.showerror(
				"Error",
				"Error al eliminar les dades de la loteria a la base de dades"
			)


	# Mètodes per a operacions CRUD en la taula summaryMembersFallaYear
	def insert_summary(
		self,
		id_member,
		assignedFee,
		assignedLottery,
		assignedRaffle,
		payedFee,
		payedLottery,
		payedRaffle
	):
		'''
		Escriu a la base de dades les dades del resum de l'exercici del faller
		que se li passen com a paràmetre a la taula "summaryMembersFallaYear".

		Paràmetres:
		-----------
		id_member : int
			Id del faller.
		assignedFee : float
			Quota assignada.
		assignedLottery : float
			Loteria assignada.
		assignedRaffle : float
			Rifa assignada.
		payedFee : float
			Quota pagada.
		payedLottery : float
			Loteria pagada.
		payedRaffle : float
			Rifa pagada.
		'''
		falla_year = None
		query = "INSERT INTO summaryMembersFallaYear \
			(memberFk, fallaYearFk, assignedFee, assignedLottery, assignedRaffle, payedFee, \
				payedLottery, payedRaffle) \
					VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
		data = id_member, falla_year, assignedFee, assignedLottery, assignedRaffle, payedFee, payedLottery, payedRaffle
		try:
			self.mysqlCursor.execute(query, data)
			self.mysqlConnection.commit()
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al insertar el resum anual del faller"
			)


	def select_summary_by_falla_year(self, falla_year):
		'''
		Llig de la taula "summaryMembersFallaYear" els ids de faller i els resultats finals
		d'aquells fallers amb resultat diferent de 0 corresponents a l'exercici passat per paràmetre.

		Paràmetres:
		-----------
		falla_year : int
			Exercici per al qual es volen recuperar les dades.

		Retorna:
		--------
		summary_list : list
			Llistat resum de fallers de l'exercici anterior.
		'''
		query = "SELECT memberFk, difference FROM summaryMembersFallaYear WHERE fallaYearFk = %s AND difference <> 0"
		try:
			self.mysqlCursor.execute(query, (falla_year,))
			summary_list = self.mysqlCursor.fetchall()
			return summary_list
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir els resultats de l'exercici anterior"
			)


	# Mètodes per a operacions CRUD en la taula fallaYear.
	def insert_falla_year(self):
		'''
		Escriu a la base de dades un nou exercici.
		'''
		code = None
		created = None
		query = "INSERT INTO fallaYear (code, created) VALUES (%s, %s)"
		data = code, created
		try:
			self.mysqlCursor.execute(query, data)
			self.mysqlConnection.commit()
		except mysql.connector.Error as e:
			messagebox.showerror(
				"Error",
				f"Error al insertar el nou exercici: {e}"
			)


	def update_falla_year_end(self, code):
		'''
		Escriu a la base de dades la data del final d'exercici a la taula "fallaYear".
		
		Paràmetres:
		-----------
		code : int
			Any de l'exercici.
		'''
		finished = None
		query = "UPDATE fallaYear SET finished = %s WHERE code = %s"
		data = finished, code
		try:
			self.mysqlCursor.execute(query, data)
			self.mysqlConnection.commit()
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al insertar la data de final d'exercici"
			)


	# Mètodes per a operacions CRUD en la taula membershipHistory.
	def select_membership_history(self, id_member):
		query = "SELECT * FROM membershipHistory WHERE memberFk = %s"
		try:
			self.mysqlCursor.execute(query, (id_member,))
			membership_history = self.mysqlCursor.fetchall()
			return membership_history
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir l'historial del faller de la base de dades"
			)


	def insert_membership_history(self, fallaYearFk, position, falla, memberFk):
		query = "INSERT INTO membershipHistory (fallaYearFk, position, falla, memberFk) \
			VALUES (%s, %s, %s, %s)"
		data = fallaYearFk, position, falla, memberFk
		try:
			self.mysqlCursor.execute(query, data)
			self.mysqlConnection.commit()
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al insertar un nou historial de faller a la base de dades"
			)


	def update_membership_history(self, falla_year, position, falla, id_member):
		query = """UPDATE membershipHistory SET falla = %s, position = %s 
			WHERE memberFk = %s AND fallaYearFk = %s"""
		data = falla, position, id_member, falla_year
		print(data)
		try:
			self.mysqlCursor.execute(query, data)
			self.mysqlConnection.commit()
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al actualitzar les dades del historial del faller a la base de dades"
			)

	
	def upsert_membership_history(self, falla_year, position, falla, id_member):
		query = "CALL upsertMembershipHistory(%s, %s, %s, %s)"
		data = (id_member, falla_year, falla, position)
		try:
			self.mysqlCursor.execute(query, data)
			self.mysqlConnection.commit()
		except mysql.connector.Error as e:
			print("Error:", e)


	# Mètodes per a operacions CRUD en la taula balance.
	def select_balance(self, id_member):
		query = "SELECT feeAssigned, feePayed, lotteryAssigned, lotteryPayed, raffleAssigned, rafflePayed FROM balance WHERE memberFk = %s"
		try:
			self.mysqlCursor.execute(query, (id_member,))
			balance = self.mysqlCursor.fetchone()
			return balance
		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"Error al llegir el balanç del faller de la base de dades"
			)


	def regenerateBalance(self):
		query = "CALL regenerateBalance()"
		try:
			self.mysqlCursor.execute(query)
			self.mysqlConnection.commit()
		except mysql.connector.Error as e:
			print("Error:", e)