'''
Módul que conté la classe ModifyMemberWindow.
És la finestra en la qual es modifiquen les dades del faller i
es guarden en la base de dades.
'''
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import platform
from pathlib import Path

from utils import Utils

from member import Member
from family import Family
from falla import Falla
from category import Category


class ModifyMemberWindow(tk.Toplevel):
	'''
	Esta classe representa una nova finestra
	que depén de la finestra principal.

	Atributs:
	---------
	master : tk.Tk o tk.Toplevel
		La instància principal de l'aplicació o de la finestra
		que crea esta nova finestra.
	'''


	def __init__(self, master = None):
		'''
		Inicialitza una nova instància de la classe ModifyMemberWindow.

		Paràmetres:
		-----------
		master : tk.Tk o tk.Toplevel, opcional
			La instància principal de l'aplicació o de la finestra
			que crea esta nova finestra.
			Si no se proporciona, se creará una nueva instancia de tk.Tk().
		'''
		super().__init__(master)
		self.master = master
		operating_system = platform.system()
		base_path = Path(__file__).parent.resolve()
		if operating_system == 'Windows':
			self.iconbitmap(base_path / 'images' / 'escut.ico')
		self.resizable(0, 0)
		self.title("Modificar Dades del Faller")
		utils = Utils()
		utils.define_global_style()
		self.configure(bg = "#ffffff", pady = 5, padx = 5)

		self.name = tk.StringVar()
		self.surname = tk.StringVar()
		self.birthdate = tk.StringVar()
		self.gender = tk.IntVar()
		self.dni = tk.StringVar()
		self.address = tk.StringVar()
		self.phone_number = tk.StringVar()
		self.email = tk.StringVar()
		self.family = tk.IntVar()

		self.id = 0
		self.family_id = 0
		self.family_ids = []
		self.final_family_id = 0

		# Frames en els que dividim la finestra.
		label_style_data = ttk.Label(
			self, text = "Introduir dades", style = "Title.TLabel"
		)
		label_frame_data = ttk.LabelFrame(
			self, style = "BorderLine.TFrame", labelwidget = label_style_data
		)
		label_frame_data.grid(
			row = 0, column = 0, padx = 5, pady = 5, ipadx = 4, ipady = 5
		)

		label_style_family = ttk.Label(
			self, text = "Buscar familiar del faller", style = "Title.TLabel"
		)
		label_frame_family = ttk.LabelFrame(
			self, style = "BorderLine.TFrame", labelwidget = label_style_family
		)
		label_frame_family.grid(
			row = 1, column = 0, padx = 5, pady = 5, ipady = 5
		)

		# Widgets per a cada frame.

		# Frame Dades personals.
		self.label_name = ttk.Label(
			label_frame_data, text = "Nom", style = "Label.TLabel"
		)
		self.label_name.grid(
			row = 0, column = 0, padx = 7, pady = 2, sticky = "w"
		)

		self.entry_name = ttk.Entry(label_frame_data, textvariable = self.name)
		self.entry_name.grid(row = 1, column = 0, padx = 7)
		self.entry_name.focus()

		self.label_surname = ttk.Label(
			label_frame_data, text = "Cognoms", style = "Label.TLabel"
		)
		self.label_surname.grid(row = 0, column = 1, pady = 2, sticky = "w")

		self.entry_surname = ttk.Entry(
			label_frame_data, width = 30, textvariable = self.surname
		)
		self.entry_surname.grid(row = 1, column = 1)

		self.label_gender = ttk.Label(
			label_frame_data, text = "Sexe", style = "Label.TLabel"
		)
		self.label_gender.grid(
			row = 2, column = 0, padx = 7, pady = 5, sticky = "w"
		)

		self.radio_button_male = ttk.Radiobutton(
			label_frame_data,
			text = "M",
			style = "Radio.TRadiobutton",
			variable = self.gender,
			value = 1
		)
		self.radio_button_female = ttk.Radiobutton(
			label_frame_data,
			text = "F",
			style = "Radio.TRadiobutton",
			variable = self.gender,
			value = 2
		)
		self.radio_button_male.grid(
			row = 3, column = 0, padx = 7, sticky = "w"
		)
		self.radio_button_female.grid(row = 3, column = 0)

		self.label_birthdate = ttk.Label(
			label_frame_data,
			text = "Data de naixement",
			style = "Label.TLabel"
		)
		self.label_birthdate.grid(row = 2, column = 1, pady = 5, sticky = "w")

		self.entry_birthdate = ttk.Entry(
			label_frame_data, width = 30, textvariable = self.birthdate
		)
		self.entry_birthdate.grid(row = 3, column = 1)

		self.label_dni = ttk.Label(
			label_frame_data, text = "DNI", style = "Label.TLabel"
		)
		self.label_dni.grid(
			row = 4, column = 0, padx = 7, pady = 2, sticky = "w"
		)

		self.entry_dni = ttk.Entry(label_frame_data, textvariable = self.dni)
		self.entry_dni.grid(row = 5, column = 0, padx = 7)

		self.label_address = ttk.Label(
			label_frame_data, text = "Adreça", style = "Label.TLabel"
		)
		self.label_address.grid(row = 4, column = 1, pady = 2, sticky = "w")

		self.entry_address = ttk.Entry(
			label_frame_data, width = 30, textvariable = self.address
		)
		self.entry_address.grid(row = 5, column = 1)

		self.label_phone_number = ttk.Label(
			label_frame_data, text = "Telèfon", style = "Label.TLabel"
		)
		self.label_phone_number.grid(
			row = 6, column = 0, padx = 7, pady = 2, sticky = "w"
		)

		self.entry_phone_number = ttk.Entry(
			label_frame_data, textvariable = self.phone_number
		)
		self.entry_phone_number.grid(row = 7, column = 0, padx = 7)

		self.label_email = ttk.Label(
			label_frame_data,
			text = "Correu electrònic",
			style = "Label.TLabel"
		)
		self.label_email.grid(row = 6, column = 1, pady = 2, sticky = "w")

		self.entry_email = ttk.Entry(
			label_frame_data, width = 30, textvariable = self.email
		)
		self.entry_email.grid(row = 7, column = 1)

		# Frame Familiar del faller.
		self.label_family_option = ttk.Label(
			label_frame_family,
			text = "Familiar en la falla",
			style = "Label.TLabel"
		)
		self.label_family_option.grid(
			row = 0, column = 0, padx = 5, pady = 2, sticky = "w"
		)

		self.radio_button_family_yes = ttk.Radiobutton(
			label_frame_family,
			text = "Si",
			style = "Radio.TRadiobutton",
			variable = self.family,
			value = 1,
			command = self.enable_family
		)
		self.radio_button_family_no = ttk.Radiobutton(
			label_frame_family,
			text = "No",
			style = "Radio.TRadiobutton",
			variable = self.family,
			value = 2,
			command = self.disable_family
		)
		self.radio_button_family_yes.grid(
			row = 1, column = 0, padx = 5, sticky = "w"
		)
		self.radio_button_family_no.grid(row = 1, column = 0)

		self.label_family_name = ttk.Label(
			label_frame_family,
			text = "Cognoms i nom:",
			style = "Label.TLabel"
		)
		self.label_family_name.grid(
			row = 2, column = 0, padx = 5, pady = 2, sticky = "w"
		)

		self.combo_box_member_family = ttk.Combobox(
			label_frame_family, width = 30, postcommand = self.display_family
		)
		self.combo_box_member_family.grid(row = 3, column = 0, padx = 5)
		self.combo_box_member_family.bind(
			"<<ComboboxSelected>>", self.select_family
		)

		# Botons.
		self.button_update = ttk.Button(
			self,
			text = "Actualitzar dades",
			style = "Button.TButton",
			command = self.update
		)
		self.button_update.grid(row = 3, column = 0, padx = 5, pady = 5)


	def fill_in_fields(self, id):
		'''
		Ompli el formulari complet a partir de l'id del faller.

		Paràmetres:
		-----------
		id : integer
			Identificador del faller passat per la finestra "gestionar".
		'''
		self.id = id
		result = Member.get_member(id)
		family = Family(result[12], result[13], result[14])
		member = Member(
			result[0],
			result[1],
			result[2],
			result[3],
			result[4],
			result[5],
			result[6],
			result[7],
			result[8],
			result[11],
			family
		)
		self.name.set(member.name)
		self.surname.set(member.surname)
		if member.gender == 'M':
			self.gender.set(1)
		elif member.gender == 'F':
			self.gender.set(2)
		utils = Utils()
		birthdate = utils.convert_to_spanish_date(member.birthdate)
		self.birthdate.set(birthdate)
		self.dni.set(member.dni)
		self.address.set(member.address)
		self.phone_number.set(member.phone_number)
		self.email.set(member.email)
		self.family_id = str(member.family.id)
		result = family.get_members(family.id)
		for values in result:
			family_member = Member(
				values[0],
				values[1],
				values[2],
				values[3],
				values[4],
				values[5],
				values[6],
				values[7],
				values[8],
				values[11],
				family
			)
			family.members_list.append(family_member)
		family_members_list = []
		for family_member in family.members_list:
			if family_member.id != id:
				family_members_list = family_members_list + [
					(family_member.surname + ", " + family_member.name)
				]
		if len(family.members_list) > 1:
			self.family.set(1)
			self.combo_box_member_family.set(family_members_list[0])
		elif len(family.members_list) == 1:
			self.family.set(2)
			self.disable_family()
		self.grab_set()
		self.transient(self.master)
		self.mainloop()

	
	def enable_family(self):
		'''
		Habilita el combobox per a indicar la familia del faller
		quan el Radiobutton de familia esta en "si".
		'''
		result = Member.get_member(self.id)
		family = Family(result[12], result[13], result[14])
		self.combo_box_member_family.configure(state = "normal")
		result = family.get_members(family.id)
		for values in result:
			family_member = Member(
				values[0],
				values[1],
				values[2],
				values[3],
				values[4],
				values[5],
				values[6],
				values[7],
				values[8],
				values[11],
				family
			)
			family.members_list.append(family_member)
		family_members_list = []
		for family_member in family.members_list:
			if family_member.id != self.id:
				family_members_list = family_members_list + [
					(family_member.surname + ", " + family_member.name)
				]
		if len(family.members_list) > 1:
			self.combo_box_member_family.set(family_members_list[0])

	
	def disable_family(self):
		'''
		Deshabilita el combobox per a indicar la familia del faller
		quan el Radiobutton de familia esta en "no" i elimina el seu contingut.
		'''
		self.combo_box_member_family.configure(state = "disabled")
		self.combo_box_member_family.delete(0, tk.END)
		self.combo_box_member_family.set("")
		self.final_family_id = 0

	
	def display_family(self):
		'''
		Controla el combobox comparant la cadena escrita amb la base de dades
		i mostrant els resultats en el combobox.
		Utilitza l'atribut "self.family_ids" per a passar el identificador de
		familia a la funció "select_family".
		'''
		falla = Falla()
		surname = self.combo_box_member_family.get()
		falla.get_members("surname", surname)
		family_list = []
		self.family_ids = []
		for member in falla.members_list:
			self.family_ids = self.family_ids + [member.family.id]
			family_list = family_list + [(member.surname + ", " + member.name)]
		self.combo_box_member_family["values"] = family_list


	def select_family(self, event):
		'''
		Controla la selecció del combobox per a guardar l'identificador
		de la familia i omplir les dades a partir d'aquest.
		'''
		index = self.combo_box_member_family.current()
		self.final_family_id = self.family_ids[index]
		self.family_ids = []
	

	def update(self):
		'''
		Es fica en marxa al fer clic en el botó "actualitzar".
		Es lligen totes les dades presents en el formulari i
		s'actualitza la base de dades.
		En el cas del canvi de familia, s'evalúa si aquest canvi
		existeix i es recalculen els diferents descomptes familiars.
		'''
		valor=messagebox.askquestion(
			"Modificar dades","Vols modificar les dades del faller?"
		)
		if valor=="yes":
			utils = Utils()
			try:
				birthdate = utils.convert_to_mariadb_date(self.birthdate.get())
			except ValueError:
				messagebox.showwarning(
					"Error", "El format per a la data ha de ser dd-mm-yyyy"
				)
			else:
				result = Member.get_member(self.id)
				old_family = Family(result[12], result[13], result[14])
				category = Category(
					result[15], result[16], result[17], result[18]
				)
				member = Member(
					result[0],
					result[1],
					result[2],
					result[3],
					result[4],
					result[5],
					result[6],
					result[7],
					result[8],
					result[11],
					old_family,
					category
				)
				member.name = self.name.get()
				member.surname = self.surname.get()
				member.gender = self.gender.get()
				member.dni = self.dni.get()
				member.address = self.address.get()
				member.phone_number = self.phone_number.get()
				member.email = self.email.get()
				
				# Canvis de familia.
				result = old_family.get_members(old_family.id)
				for values in result:
					family_member = Member(
						values[0],
						values[1],
						values[2],
						values[3],
						values[4],
						values[5],
						values[6],
						values[7],
						values[8],
						values[11],
						old_family,
						category)
					old_family.members_list.append(family_member)
				if old_family.id != self.final_family_id and \
					self.final_family_id != 0:
					# Si estava sol i entra en familia.
					if len(old_family.members_list) == 1:
						result = Family.get_family(self.final_family_id)
						new_family = Family(result[0], result[1], result[2])
						member.modify_member(
							self.id,
							member.name,
							member.surname,
							birthdate,
							member.gender,
							member.dni,
							member.address,
							member.phone_number,
							1,
							member.email,
							new_family.id,
							category.id
						)
						old_family.delete_family(self.family_id)
						result = new_family.get_members(new_family.id)
						new_family.members_list = []
						for values in result:
							category_member = Category(
								values[15], values[16], values[17], values[18]
							)
							family_member = Member(
								values[0],
								values[1],
								values[2],
								values[3],
								values[4],
								values[5],
								values[6],
								values[7],
								values[8],
								values[11],
								new_family,
								category_member
							)
							new_family.members_list.append(family_member)
						new_family.calculate_discount(new_family.members_list)
						new_family.modify_family(
							new_family.id,
							new_family.discount,
							new_family.is_direct_debited
						)
					# Si estava en familia i canvia de familia.
					else:
						result = Family.get_family(self.final_family_id)
						new_family = Family(result[0], result[1], result[2])
						member.modify_member(
							self.id,
							member.name,
							member.surname,
							birthdate,
							member.gender,
							member.dni,
							member.address,
							member.phone_number,
							1,
							member.email,
							new_family.id,
							category.id
						)
						# Actualitzem familia vella
						result = old_family.get_members(self.family_id)
						old_family.members_list = []
						for values in result:
							category_member = Category(
								values[15], values[16], values[17], values[18]
							)
							family_member = Member(
								values[0],
								values[1],
								values[2],
								values[3],
								values[4],
								values[5],
								values[6],
								values[7], 
								values[8],
								values[11],
								old_family,
								category_member
							)
							old_family.members_list.append(family_member)
						old_family.calculate_discount(old_family.members_list)
						old_family.modify_family(
							old_family.id,
							old_family.discount,
							old_family.is_direct_debited
						)
						# Actualitzem familia nova
						result = new_family.get_members(new_family.id)
						new_family.members_list = []
						for values in result:
							category_member = Category(
								values[15], values[16], values[17], values[18]
							)
							family_member = Member(
								values[0],
								values[1],
								values[2],
								values[3],
								values[4],
								values[5],
								values[6],
								values[7],
								values[8],
								values[11],
								new_family,
								category_member
							)
							new_family.members_list.append(family_member)
						new_family.calculate_discount(new_family.members_list)
						new_family.modify_family(
							new_family.id,
							new_family.discount,
							new_family.is_direct_debited
						)
				# Si estava en familia i passa a estar sol	
				elif len(old_family.members_list)>1 and self.final_family_id==0:
					Family.set_family(0, 0)
					result = Family.get_family(0)
					new_family = Family(result[0], result[1], result[2])
					member.modify_member(
						self.id,
						member.name,
						member.surname,
						birthdate,
						member.gender,
						member.dni,
						member.address,
						member.phone_number,
						1,
						member.email,
						new_family.id,
						category.id
					) 
					# Actualitzem familia vella
					result = old_family.get_members(old_family.id)
					old_family.members_list = []
					for values in result:
						category_member = Category(
							values[15], values[16], values[17], values[18]
						)
						family_member = Member(
							values[0],
							values[1],
							values[2],
							values[3],
							values[4],
							values[5],
							values[6],
							values[7],
							values[8],
							values[11],
							old_family,
							category_member
						)
						old_family.members_list.append(family_member)
					old_family.calculate_discount(old_family.members_list)
					old_family.modify_family(
						old_family.id, old_family.discount, old_family.is_direct_debited
					)
		falla = Falla()
		falla.regenerateBalance()
		self.destroy()