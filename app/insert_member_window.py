'''
Módul que conté la classe InsertMemberWindow.
És la finestra en la qual s'indiquen les dades del nou faller per a guardar-lo
a la base de dades.
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


class InsertMemberWindow(tk.Toplevel):
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
		Inicialitza una nova instància de la classe InsertMemberWindow.

		Parametres:
		-----------
		master : tk.Tk o tk.Toplevel, opcional
			La instància principal de l'aplicació o de la finestra
			que crea esta nova finestra.
			Si no es proporciona, es creará una nueva instancia de tk.Tk().
		'''
		super().__init__(master)
		self.master = master
		operating_system = platform.system()
		base_path = Path(__file__).parent.resolve()
		if operating_system == 'Windows':
			self.iconbitmap(base_path / 'images' / 'escut.ico')
		self.resizable(0, 0)
		self.title("Introduir Faller")
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

		self.family_ids = [] # Guarda els id_familia de la llista del combo.
		self.final_family_id = 0 # Guarda el valor final de l'id_familia.
		
		# Frames en els que dividim la finestra.
		label_style_data = ttk.Label(
			self, text = "Introduir dades", style = "Titol.TLabel"
		)
		label_frame_data = ttk.LabelFrame(
			self, style = "Marc.TFrame", labelwidget = label_style_data
		)
		label_frame_data.grid(
			row = 0, column = 0, padx = 5, pady = 5, ipadx = 4, ipady = 5
		)

		label_style_family = ttk.Label(
			self, text = "Buscar familiar del faller", style = "Titol.TLabel"
		)
		label_frame_family = ttk.LabelFrame(
			self, style = "Marc.TFrame", labelwidget = label_style_family
		)
		label_frame_family.grid(
			row = 1, column = 0, padx = 5, pady = 5, ipady = 5
		)

		# Widgets per a cada frame.

		# Frame "Introduir dades".
		self.label_name = ttk.Label(
			label_frame_data, text = "Nom", style = "Etiqueta.TLabel"
		)
		self.label_name.grid(
			row = 0, column = 0, padx = 7, pady = 2, sticky = "w"
		)

		self.entry_name = ttk.Entry(label_frame_data, textvariable = self.name)
		self.entry_name.grid(row = 1, column = 0, padx = 7)

		self.label_surname = ttk.Label(
			label_frame_data, text = "Cognoms", style = "Etiqueta.TLabel"
		)
		self.label_surname.grid(row = 0, column = 1, pady = 2, sticky = "w")

		self.entry_surname = ttk.Entry(
			label_frame_data, width = 30, textvariable = self.surname
		)
		self.entry_surname.grid(row = 1, column = 1)

		self.label_gender = ttk.Label(
			label_frame_data, text = "Sexe", style = "Etiqueta.TLabel"
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
			style = "Etiqueta.TLabel"
		)
		self.label_birthdate.grid(row = 2, column = 1, pady = 5, sticky = "w")

		self.entry_birthdate = ttk.Entry(
			label_frame_data, width = 30, textvariable = self.birthdate
		)
		self.entry_birthdate.grid(row = 3, column = 1)

		self.label_dni = ttk.Label(
			label_frame_data, text = "DNI", style = "Etiqueta.TLabel"
		)
		self.label_dni.grid(
			row = 4, column = 0, padx = 7, pady = 2, sticky = "w"
		)

		self.entry_dni = ttk.Entry(label_frame_data, textvariable = self.dni)
		self.entry_dni.grid(row = 5, column = 0, padx = 7)

		self.label_address = ttk.Label(
			label_frame_data, text = "Adreça", style = "Etiqueta.TLabel"
		)
		self.label_address.grid(row = 4, column = 1, pady = 2, sticky = "w")

		self.entry_address = ttk.Entry(
			label_frame_data, width = 30, textvariable = self.address
		)
		self.entry_address.grid(row = 5, column = 1)

		self.label_phone_number = ttk.Label(
			label_frame_data, text = "Telèfon", style = "Etiqueta.TLabel"
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
			style = "Etiqueta.TLabel"
		)
		self.label_email.grid(row = 6, column = 1, pady = 2, sticky = "w")

		self.entry_email = ttk.Entry(
			label_frame_data, width = 30, textvariable = self.email
		)
		self.entry_email.grid(row = 7, column = 1)

		# Frame "Buscar familiar del faller".
		self.label_family_option = ttk.Label(
			label_frame_family,
			text = "Familiar en la falla?",
			style = "Etiqueta.TLabel"
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
			text = "Cognoms i nom",
			style = "Etiqueta.TLabel"
		)
		self.label_family_name.grid(
			row = 2, column = 0, padx = 5, pady = 2, sticky = "w"
		)

		self.combo_box_member_family = ttk.Combobox(
			label_frame_family, 
			width = 30, 
			postcommand = self.display_family
		)
		self.combo_box_member_family.grid(
			row = 3, column = 0, padx = 5
		)
		self.combo_box_member_family.bind(
			"<<ComboboxSelected>>", self.select_family
		)
		self.combo_box_member_family.configure(state = "disabled")

		# Botó "Introduir".
		self.button_insert = ttk.Button(
			self,
			text = "Introduir",
			style = "Boto.TButton",
			command = self.insert_member
		)
		self.button_insert.grid(row = 3, column = 0, padx = 5, pady = 5)

		# Paràmetres d'inici de la finestra.
		self.entry_name.focus()
		self.gender.set(1)
		self.family.set(2)
		self.grab_set()
		self.transient(self.master)


	def enable_family(self):
		'''
		Habilita el combobox per a indicar la familia del faller
		quan el Radiobutton de familia està en "si".
		'''
		self.combo_box_member_family.configure(state = "normal")

	
	def disable_family(self):
		'''
		Deshabilita el combobox per a indicar la familia del faller
		quan el Radiobutton de familia està en "no" i elimina el seu contingut.
		'''
		self.combo_box_member_family.configure(state = "disabled")
		self.combo_box_member_family.delete(0, tk.END)
		self.combo_box_member_family.set("")


	def display_family(self):
		'''
		Controla el combobox comparant la cadena escrita amb la base de dades
		i mostrant els resultats en el combobox.
		Utilitza la variable global "self.family_ids"
		per a guardar tots els identificadors del llistat.
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
		de la familia a la variable "self.final_family_id"
		'''
		index = self.combo_box_member_family.current()
		self.final_family_id = self.family_ids[index]
		self.family_ids = []
	

	def insert_member(self):
		'''
		Es fica en marxa al apretar el botó de "Introduir".
		Dona d'alta les dades introduides del nou faller a la base de dades.
		Si conforma una familia nova la dona d'alta.
		Si ja pertany a una familia l'inclou en ella i
		recalcula el descompte familiar.
		Crea un historial per al faller nou.
		Neteja el formulari per a introduir un nou faller.
		'''
		valor = messagebox.askquestion(
			"Alta nova", "Donar d'alta el nou faller?"
		)
		if valor == "yes":
			utils = Utils()
			try:
				birthdate = utils.convert_to_mariadb_date(self.birthdate.get())
			except:
				messagebox.showerror(
					"Error",
					"El format per a la data ha de ser dd-mm-aaaa i ser vàlida"
				)
			else:
				if self.family.get() == 1:
					result = Family.get_family(self.final_family_id)
					family = Family(result[0], result[1], result[2])
					Member.set_member(self.name.get(),
							self.surname.get(),
							birthdate,
							self.gender.get(),
							self.dni.get(),
							self.address.get(),
							self.phone_number.get(),
							1,
							self.email.get(),
							family.id,
							None)
					result = family.get_members(family.id)
					for values in result:
						category = Category(
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
							family,
							category
						)
						family.members_list.append(family_member)
					family.calculate_discount(family.members_list)
					family.modify_family(
						family.id, family.discount, family.is_direct_debited
					)
				else:
					Family.set_family(0, 0)
					result = Family.get_family(0)
					family = Family(result[0], result[1], result[2])
					Member.set_member(self.name.get(),
							self.surname.get(),
							birthdate,
							self.gender.get(),
							self.dni.get(),
							self.address.get(),
							self.phone_number.get(),
							1,
							self.email.get(),
							family.id,
							None)
			
			# Creem un historial nou i l'omplim

			result = Member.get_last_member()
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
			result[11]
			)
			falla = Falla()
			falla.get_current_falla_year()
			member.set_membership_history(member.id, "vocal", "Sants Patrons", falla.falla_year)

			self.name.set("")
			self.surname.set("")
			self.birthdate.set("")
			self.address.set("")
			self.dni.set("")
			self.phone_number.set("")
			self.email.set("")
			self.gender.set(1)
			self.family.set(2)
			self.disable_family()
			self.entry_name.focus()
