import mysql.connector
from pathlib import Path
from tkinter import messagebox


class CreateDatabase:
	'''
	Aquesta classe crea la base de dades completa.

	Atributs:
	---------
	db_name : string
		Nom de la base de dades.
	'''
	def __init__(self):
		'''
		Inicialitza una nova instància de la classe CreateDatabase.
		Conexió MariaDb.
		'''
		base_path = Path(__file__).parent.resolve()

		self.create_database(base_path.parent / 'db' / 'database_creation.sql')

		self.create_procedure_trigger(base_path.parent / 'db' / 'procedures' / 'calculateFallaYear.sql')
		self.create_procedure_trigger(base_path.parent / 'db' / 'procedures' / 'calculateMemberCategory.sql')
		self.create_procedure_trigger(base_path.parent / 'db' / 'procedures' / 'calculateMemberFallaAge.sql')
		self.create_procedure_trigger(base_path.parent / 'db' / 'procedures' / 'getCurrentDate.sql')
		self.create_procedure_trigger(base_path.parent / 'db' / 'procedures' / 'getCurrentFallaYear.sql')
		self.create_procedure_trigger(base_path.parent / 'db' / 'procedures' / 'modifyMembershipHistory.sql')
		self.create_procedure_trigger(base_path.parent / 'db' / 'procedures' / 'upsertMembershipHistory.sql')
		self.create_procedure_trigger(base_path.parent / 'db' / 'procedures' / 'insertBalance.sql')

		self.create_procedure_trigger(base_path.parent / 'db' / 'triggers' / 'fallaYear_beforeInsert.sql')
		self.create_procedure_trigger(base_path.parent / 'db' / 'triggers' / 'fallaYear_beforeUpdate.sql')
		self.create_procedure_trigger(base_path.parent / 'db' / 'triggers' / 'member_beforeInsert.sql')
		self.create_procedure_trigger(base_path.parent / 'db' / 'triggers' / 'member_beforeUpdate.sql')
		self.create_procedure_trigger(base_path.parent / 'db' / 'triggers' / 'movement_beforeInsert.sql')
		self.create_procedure_trigger(base_path.parent / 'db' / 'triggers' / 'summaryMembersFallaYear_beforeInsert.sql')
		self.create_procedure_trigger(base_path.parent / 'db' / 'triggers' / 'movement_afterInsert.sql')
		self.create_procedure_trigger(base_path.parent / 'db' / 'triggers' / 'member_afterInsert.sql')
		self.create_procedure_trigger(base_path.parent / 'db' / 'triggers' / 'member_afterUpdate.sql')


	def close_connection(self):
		'''
		Tancament de la conexió.
		'''
		self.mysqlCursor.close()
		self.mysqlConnection.close()


	def create_database(self, sql_file):
		'''
		Crea la BBDD i les taules
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
			with open(sql_file, 'r') as file:
				sql_script = file.read()

			for result in self.mysqlCursor.execute(sql_script, multi = True):
				pass

			self.mysqlConnection.commit()

		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"No s'ha pogut crear la base de dades"
			)
			if self.mysqlConnection:
				self.mysqlConnection.rollback()
		finally:
			self.close_connection()

	
	def create_procedure_trigger(self, sql_file):
		'''
		Crea els procediments i triggers
		'''
		try:
			self.mysqlConnection = mysql.connector.connect(
				host = "localhost",
				user = "root",
				password = "hamuclaulo07",
				database = 'sp'
			)
			if self.mysqlConnection.is_connected():
				self.mysqlCursor = self.mysqlConnection.cursor()
			else:
				messagebox.showerror(
					"Error",
					"No s'ha pogut establir la conexió amb la base de dades."
				)
			with open(sql_file, 'r') as file:
				sql_script = file.read()

			for result in self.mysqlCursor.execute(sql_script, multi = True):
				pass

			self.mysqlConnection.commit()

		except mysql.connector.Error:
			messagebox.showerror(
				"Error",
				"No s'ha pogut crear la base de dades"
			)
			if self.mysqlConnection:
				self.mysqlConnection.rollback()
		finally:
			self.close_connection()