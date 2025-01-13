import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import platform
from pathlib import Path

from utils import Utils
from report import Report


class ShowReportWindow(tk.Toplevel):
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
		Inicialitza una nova instància de la classe ShowReportWindow.

		Parametres:
		-----------
		master : tk.Tk o tk.Toplevel, opcional
			La instància principal de l'aplicació o de la finestra
			que crea esta nova finestra.
			Si no es proporciona, es creará una nueva instancia de tk.Tk().
		'''
		super().__init__(master)
		self.master = master
		self.sistema_operatiu = platform.system()
		base_path = Path(__file__).parent.resolve()
		if self.sistema_operatiu == 'Windows':
			self.iconbitmap(base_path / 'images' / 'escut.ico')
		self.resizable(0,0)
		self.title("Llistats")
		utils = Utils()
		utils.define_global_style()
		self.configure(bg = "#ffffff", pady = 5, padx = 5)

		self.movements_date = tk.StringVar()
		self.cash = tk.IntVar()
		self.bank = tk.IntVar()
		self.full_name = tk.IntVar()
		self.dni = tk.IntVar()
		self.address = tk.IntVar()
		self.phone_number = tk.IntVar()
		self.birthdate = tk.IntVar()
		self.email = tk.IntVar()
		self.adult = tk.IntVar()
		self.cadet = tk.IntVar()
		self.youth = tk.IntVar()
		self.childish = tk.IntVar()
		self.baby = tk.IntVar()
		self.option = tk.IntVar()
		self.initial_age = tk.IntVar()
		self.final_age = tk.IntVar()

		# Frames en els que dividim la finestra.
		label_style_day_movements = ttk.Label(
			self, text = "Moviments dia", style = "Title.TLabel"
		)
		label_frame_day_movements = ttk.LabelFrame(
			self,
			style = "BorderLine.TFrame",
			labelwidget = label_style_day_movements
		)
		label_frame_day_movements.grid(
			row = 0, column = 0, padx = 5, pady = 5, ipadx = 2, ipady = 3
		)

		label_style_accounting_reports = ttk.Label(
			self, text = "Llistats comptables", style = "Title.TLabel"
		)
		label_frame_accounting_reports = ttk.LabelFrame(
			self,
			style = "BorderLine.TFrame",
			labelwidget = label_style_accounting_reports
		)
		label_frame_accounting_reports.grid(
			row = 1, column = 0, padx = 5, pady = 5, ipadx = 2, ipady = 3
		)

		label_style_members = ttk.Label(
			self, text = "Llistat fallers", style = "Title.TLabel"
		)
		label_frame_members = ttk.LabelFrame(
			self, style = "BorderLine.TFrame", labelwidget = label_style_members
		)
		label_frame_members.grid(
			row = 2, column = 0, padx = 5, pady = 5, ipadx = 5, ipady = 5
		)

		label_style_other_reports = ttk.Label(
			self, text = "Altres llistats", style = "Title.TLabel"
		)
		label_frame_other_reports = ttk.LabelFrame(
			self,
			style = "BorderLine.TFrame",
			labelwidget = label_style_other_reports
		)
		label_frame_other_reports.grid(
			row = 3, column = 0, padx = 5, pady = 5, ipadx = 2, ipady = 3
		)

		# Widgets per a cada frame.

		# Frame "Moviments dia".
		self.label_movements_date = ttk.Label(
			label_frame_day_movements, text = "Data", style = "Label.TLabel"
		)
		self.label_movements_date.grid(row = 0, column = 0, padx = 5, pady = 5)

		self.entry_movements_date = ttk.Entry(
			label_frame_day_movements,
			width = 10,
			textvariable = self.movements_date
		)
		self.entry_movements_date.grid(row = 0, column = 1, padx = 5, pady = 5)

		self.check_button_cash = ttk.Checkbutton(
			label_frame_day_movements,
			text = "Efectiu",
			style = "Check.TCheckbutton",
			variable = self.cash
		)
		self.check_button_cash.grid(row = 0, column = 2, padx = 5, pady = 5)
		self.check_button_bank = ttk.Checkbutton(
			label_frame_day_movements,
			text="Banc",
			style="Check.TCheckbutton",
			variable = self.bank
		)
		self.check_button_bank.grid(row = 0, column = 3, padx = 5, pady = 5)

		self.button_day_movements = ttk.Button(
			label_frame_day_movements,
			text="Llistat moviments",
			style="Button.TButton",
			command = self.create_movements_report
		)
		self.button_day_movements.grid(row = 0, column = 4, padx = 5, pady = 5)

		# Frame "Llistats comptables"
		self.button_general = ttk.Button(
			label_frame_accounting_reports,
			text = "Llistat general",
			style = "Button.TButton",
			command = self.create_general_report
		)
		self.button_general.grid(row = 0, column = 0, padx = 5, pady = 3)

		self.button_general_families = ttk.Button(
			label_frame_accounting_reports,
			text = "Llistat general per families",
			style = "Button.TButton",
			command = self.create_general_families_report
		)
		self.button_general_families.grid(
			row = 0, column = 1, padx = 5, pady = 3
		)

		self.button_no_members = ttk.Button(
			label_frame_accounting_reports,
			text = "Llistat quotes no fallers",
			style = "Button.TButton",
			command = self.create_no_members_report
		)
		self.button_no_members.grid(row = 0, column = 2, padx = 5, pady = 3)

		# Frame "Llistat fallers".
		self.check_button_full_name = ttk.Checkbutton(
			label_frame_members,
			text = "Nom complet",
			style = "Check.TCheckbutton",
			variable = self.full_name
		)
		self.check_button_full_name.grid(
			row = 0, column = 0, padx = 5, pady = 2, sticky = "w"
		)

		self.check_button_dni = ttk.Checkbutton(
			label_frame_members,
			text = "DNI",
			style = "Check.TCheckbutton",
			variable = self.dni
		)
		self.check_button_dni.grid(
			row = 1, column = 0, padx = 5, pady = 2, sticky = "w"
		)

		self.check_button_address = ttk.Checkbutton(
			label_frame_members,
			text = "Adreça",
			style = "Check.TCheckbutton",
			variable = self.address
		)
		self.check_button_address.grid(
			row = 2, column = 0, padx = 5, pady = 2, sticky = "w"
		)

		self.check_button_phone_number = ttk.Checkbutton(
			label_frame_members,
			text = "Telèfon",
			style = "Check.TCheckbutton",
			variable = self.phone_number
		)
		self.check_button_phone_number.grid(
			row = 3, column = 0, padx = 5, pady = 2, sticky = "w"
		)

		self.check_button_birthdate = ttk.Checkbutton(
			label_frame_members,
			text = "Data de naixement",
			style = "Check.TCheckbutton",
			variable = self.birthdate
		)
		self.check_button_birthdate.grid(
			row = 4, column = 0, padx = 5, pady = 2, sticky = "w"
		)

		self.check_button_email = ttk.Checkbutton(
			label_frame_members,
			text = "Correu electrònic",
			style = "Check.TCheckbutton",
			variable = self.email
		)
		self.check_button_email.grid(
			row = 5, column = 0, padx = 5, pady = 2, sticky = "w"
		)

		self.radio_button_full = ttk.Radiobutton(
			label_frame_members,
			text = "Complet",
			style = "Radio.TRadiobutton",
			variable = self.option,
			value = 1,
			command = self.disable_options
		)
		self.radio_button_categories = ttk.Radiobutton(
			label_frame_members,
			text = "Per categories",
			style = "Radio.TRadiobutton",
			variable = self.option,
			value = 2,
			command = self.enable_categories
		)
		self.radio_button_ages = ttk.Radiobutton(
			label_frame_members,
			text = "Per edats",
			style = "Radio.TRadiobutton",
			variable = self.option,
			value = 3,
			command = self.enable_ages
		)
		self.radio_button_full.grid(
			row = 0, column = 3, padx = 5, pady = 2, sticky = "w"
		)
		self.radio_button_categories.grid(
			row = 0, column = 1, padx = 5, pady = 2, sticky = "w"
		)
		self.radio_button_ages.grid(
			row = 0, column = 2, padx = 5, pady = 2, sticky = "w"
		)

		self.check_button_adult = ttk.Checkbutton(
			label_frame_members,
			state = "disabled",
			text = "Adult",
			style = "Check.TCheckbutton",
			variable = self.adult
		)
		self.check_button_adult.grid(
			row = 1, column = 1, padx = 5, sticky = "w"
		)

		self.check_button_cadet = ttk.Checkbutton(
			label_frame_members,
			state = "disabled",
			text = "Cadet",
			style = "Check.TCheckbutton",
			variable = self.cadet
		)
		self.check_button_cadet.grid(
			row = 2, column = 1, padx = 5, sticky = "w"
		)

		self.check_button_youth = ttk.Checkbutton(
			label_frame_members,
			state = "disabled",
			text = "Juvenil",
			style = "Check.TCheckbutton",
			variable = self.youth
		)
		self.check_button_youth.grid(
			row = 3, column = 1, padx = 5, sticky = "w"
		)

		self.check_button_childish = ttk.Checkbutton(
			label_frame_members,
			state = "disabled",
			text = "Infantil",
			style = "Check.TCheckbutton",
			variable = self.childish
		)
		self.check_button_childish.grid(
			row = 4, column = 1, padx = 5, sticky = "w"
		)

		self.check_button_baby = ttk.Checkbutton(
			label_frame_members,
			state = "disabled",
			text = "Bebè",
			style = "Check.TCheckbutton",
			variable = self.baby
		)
		self.check_button_baby.grid(
			row = 5, column = 1, padx = 5, sticky = "w"
		)

		self.label_initial_age = ttk.Label(
			label_frame_members,
			text = "edat inicial",
			style = "Label.TLabel"
		)
		self.label_initial_age.grid(
			row = 1, column = 2, padx = 5, sticky = "w"
		)

		self.entry_initial_age = ttk.Entry(
			label_frame_members,
			width = 5,
			state = "disabled",
			textvariable = self.initial_age
		)
		self.entry_initial_age.grid(
			row = 2, column = 2, padx = 5, sticky = "w"
		)

		self.label_final_age = ttk.Label(
			label_frame_members,
			text = "edat final",
			style = "Label.TLabel"
		)
		self.label_final_age.grid(
			row = 3, column = 2, padx = 5, sticky ="w"
		)

		self.entry_final_age = ttk.Entry(
			label_frame_members,
			width = 5,
			state = "disabled",
			textvariable = self.final_age
		)
		self.entry_final_age.grid(
			row = 4, column = 2, padx = 5, sticky = "w"
		)

		self.button_members = ttk.Button(
			label_frame_members,
			text = "Llistat fallers",
			style = "Button.TButton",
			command = self.create_members_report
		)
		self.button_members.grid(
			row = 4, column = 3, rowspan = 2, sticky = "s"
		)

		# Frame "Altres llistats"
		self.button_registrations_cancellations = ttk.Button(
			label_frame_other_reports,
			text = "Llistat altes i baixes",
			style = "Button.TButton",
			command = self.create_registrations_cancellations_report
		)
		self.button_registrations_cancellations.grid(
			row = 0, column = 0, padx = 5, pady = 3
		)

		self.button_raffles = ttk.Button(
			label_frame_other_reports,
			text = "Llistat fallers amb rifa",
			style = "Button.TButton",
			command=self.create_raffles_report
		)
		self.button_raffles.grid(row=0, column=1, padx=5, pady=3)

		# Paràmetres d'inici de la finestra.
		utils = Utils()
		current_date = utils.calculate_current_date()
		self.movements_date.set(
			current_date[0] + "-" + current_date[1] + "-" + current_date[2]
		)
		self.cash.set(1)
		self.bank.set(1)
		self.full_name.set(1)
		self.dni.set(1)
		self.address.set(1)
		self.phone_number.set(1)
		self.birthdate.set(1)
		self.email.set(1)
		self.adult.set(1)
		self.option.set(1)
		self.grab_set()
		self.transient(self.master)


	def disable_options(self):
		'''
		Fica totes les opcions en "disabled"
		per a traure un llistat complet.
		'''
		self.check_button_adult.configure(state = "disabled")
		self.check_button_cadet.configure(state = "disabled")
		self.check_button_youth.configure(state = "disabled")
		self.check_button_childish.configure(state = "disabled")
		self.check_button_baby.configure(state = "disabled")
		self.entry_initial_age.configure(state = "disabled")
		self.entry_final_age.configure(state = "disabled")


	def enable_categories(self):
		'''
		Fica en "normal" les opcions de categoria.
		'''
		self.check_button_adult.configure(state = "normal")
		self.check_button_cadet.configure(state = "normal")
		self.check_button_youth.configure(state = "normal")
		self.check_button_childish.configure(state = "normal")
		self.check_button_baby.configure(state = "normal")
		self.entry_initial_age.configure(state = "disabled")
		self.entry_final_age.configure(state = "disabled")


	def enable_ages(self):
		'''
		Fica en "normal" les opcions d'edat.
		'''
		self.check_button_adult.configure(state = "disabled")
		self.check_button_cadet.configure(state = "disabled")
		self.check_button_youth.configure(state = "disabled")
		self.check_button_childish.configure(state = "disabled")
		self.check_button_baby.configure(state = "disabled")
		self.entry_initial_age.configure(state = "normal")
		self.entry_final_age.configure(state = "normal")


	def create_movements_report(self):
		'''
		Crea el llistat de moviments.
		'''
		report = Report()
		if self.cash.get() == 0 and self.bank.get() == 0:
			messagebox.showwarning(
				"Error",
				"Has de marcar una de les opcions per a fer el llistat"
			)
		else:
			report.movements_report(
				self.movements_date.get(), self.cash.get(), self.bank.get()
			)


	def create_general_report(self):
		'''
		Crea el llistat general.
		'''
		report = Report()
		report.general_report()


	def create_general_families_report(self):
		'''
		Crea el llistat general per families.
		'''
		report = Report()
		report.general_report_by_families()


	def create_no_members_report(self):
		'''
		Crea el llistat de membres borrats que han pagat part de la quota.
		'''
		report = Report()
		report.inactive_members_fees_report()


	def create_members_report(self):
		'''
		Crea el llistat de fallers segons les opcions marcades.
		'''
		report = Report()
		options_list = []
		if self.full_name.get() == 1:
			options_list.append("nom")
		if self.dni.get() == 1:
			options_list.append("dni")
		if self.address.get() == 1:
			options_list.append("adreça")
		if self.phone_number.get() == 1:
			options_list.append("telefon")
		if self.birthdate.get() == 1:
			options_list.append("naixement")
		if self.email.get() == 1:
			options_list.append("correu")
		if len(options_list) == 6:
			messagebox.showwarning(
				"Error",
				"Marca 5 opcions de dades com a màxim"
			)
		else:
			if self.option.get() == 1:
				if len(options_list) < 4:
					report.reduced_members_list(options_list)
				else:
					report.members_list(options_list)
			elif self.option.get() == 2:
				categories_list = []
				if self.adult.get() == 1:
					categories_list.append(1)
				if self.cadet.get() == 1:
					categories_list.append(2)
				if self.youth.get() == 1:
					categories_list.append(3)
				if self.childish.get() == 1:
					categories_list.append(4)
				if self.baby.get() == 1:
					categories_list.append(5)
				if len(options_list) < 4:
					report.reduced_members_list_by_categories(
						categories_list, options_list
					)
				else:
					report.members_list_by_categories(
						categories_list, options_list
					)
			elif self.option.get() == 3:
				if self.final_age.get() < self.initial_age.get():
					messagebox.showwarning(
						"Error",
						"L'edat final ha de ser major o igual que la inicial"
					)
				else:
					try:
						if len(options_list) < 4:
							report.reduced_members_list_by_age(
								self.initial_age.get(),
								self.final_age.get(),
								options_list
							)
						else:
							report.members_list_by_age(
								self.initial_age.get(),
								self.final_age.get(),
								options_list
							)
					except ValueError:
						messagebox.showwarning(
							"Error",
							"Has d'escriure un valor vàlid per a les edats"
						)


	def create_registrations_cancellations_report(self):
		'''
		Crea el llistat d'altes i baixes.
		'''
		report = Report()
		report.registrations_cancellations_list()
		

	def create_raffles_report(self):
		'''
		Crea el llistat de fallers amb rifa.
		'''
		report = Report()
		report.members_with_raffle_list()
