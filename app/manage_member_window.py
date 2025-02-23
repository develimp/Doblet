'''
Módul que conté la classe ManageMemberWindow.
És la finestra en la qual es mostren totes les dades, pagaments, families
del faller. També és on es donen les altes i baixes i es fan assignacions.
'''
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import platform
from reportlab.lib.pagesizes import A4
from pathlib import Path
from decimal import Decimal

from utils import Utils

from falla import Falla
from member import Member
from family import Family
from category import Category
from report import Report
from modify_member_window import ModifyMemberWindow


class ManageMemberWindow(tk.Toplevel):
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
		Inicialitza una nova instància de la classe ManageMemberWindow.

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
		self.title("Gestionar Faller")
		utils = Utils()
		utils.define_global_style()
		self.configure(bg = "#ffffff", pady = 5, padx = 5)

		self.falla_year = tk.IntVar()
		self.id = tk.IntVar()
		self.name = tk.StringVar()
		self.birthdate = tk.StringVar()
		self.dni = tk.StringVar()
		self.address = tk.StringVar()
		self.phone_number = tk.StringVar()
		self.email = tk.StringVar()

		self.family_members = tk.IntVar()

		self.assigned_fee = tk.StringVar()
		self.payed_fee = tk.StringVar()
		self.debt_fee = tk.DoubleVar()
		self.pay_fee = tk.DoubleVar()
		self.assigned_lottery = tk.StringVar()
		self.payed_lottery = tk.StringVar()
		self.debt_lottery = tk.DoubleVar()
		self.pay_lottery = tk.DoubleVar()
		self.assigned_raffle = tk.StringVar()
		self.payed_raffle = tk.StringVar()
		self.debt_raffle = tk.DoubleVar()
		self.pay_raffle = tk.DoubleVar()
		self.total_assigned = tk.DoubleVar()
		self.total_payed = tk.DoubleVar()
		self.total_debt = tk.DoubleVar()
		self.pay_total = tk.DoubleVar()
		self.way_to_pay = tk.IntVar()
		
		self.family_assigned_fee = tk.StringVar()
		self.family_payed_fee = tk.StringVar()
		self.family_debt_fee = tk.DoubleVar()
		self.family_pay_fee = tk.DoubleVar()
		self.family_assigned_lottery = tk.StringVar()
		self.family_payed_lottery = tk.StringVar()
		self.family_debt_lottery = tk.DoubleVar()
		self.family_pay_lottery = tk.DoubleVar()
		self.family_assigned_raffle = tk.StringVar()
		self.family_payed_raffle = tk.StringVar()
		self.family_debt_raffle = tk.DoubleVar()
		self.family_pay_raffle = tk.DoubleVar()
		self.family_total_assigned = tk.DoubleVar()
		self.family_total_payed = tk.DoubleVar()
		self.family_total_debt = tk.DoubleVar()
		self.family_pay_total = tk.DoubleVar()
		self.family_way_to_pay = tk.IntVar()
		
		self.assignment_concept = tk.IntVar()
		self.assignment_description = tk.StringVar()
		self.total_assignment = tk.DoubleVar()

		self.member_ids = [] # Guarda els id_faller del llistat del combo.
		# Controla l'obertura de FinestraModificar.
		self.modify_member_window_opened = 0
		# Guardem l'id anteriorment buscat per a retornar-lo en cas d'error.
		self.previous_id = 0
		
		# Frames en els que dividim la finestra.
		label_frame_row1 = tk.LabelFrame(
			self, borderwidth = 0, background = "#ffffff"
		)
		label_frame_row1.pack(ipady = 5)
		label_frame_row2 = tk.LabelFrame(
			self, borderwidth = 0, background = "#ffffff"
		)
		label_frame_row2.pack(ipady = 5)
		label_frame_row3 = tk.LabelFrame(
			self, borderwidth = 0, background = "#ffffff"
		)
		label_frame_row3.pack(ipady = 5)

		label_style_falla_year = ttk.Label(
			label_frame_row1, text = "Exercici", style = "Title.TLabel"
		)
		label_frame_falla_year = ttk.LabelFrame(
			label_frame_row1,
			style = "BorderLine.TFrame",
			labelwidget = label_style_falla_year
		)
		label_frame_falla_year.grid(
			row = 0, column = 0, padx = 10, ipadx = 10, ipady = 5, sticky = "n"
		)

		label_style_search = ttk.Label(
			label_frame_row1, text = "Faller", style = "Title.TLabel"
		)
		label_frame_search = ttk.LabelFrame(
			label_frame_row1,
			style = "BorderLine.TFrame",
			labelwidget = label_style_search
		)
		label_frame_search.grid(row = 0, column = 1, padx = 10)

		label_style_family = ttk.Label(
			label_frame_row1, text = "Familia", style = "Title.TLabel"
		)
		label_frame_family = ttk.LabelFrame(
			label_frame_row1,
			style = "BorderLine.TFrame",
			labelwidget = label_style_family
		)
		label_frame_family.grid(row = 0, column = 2, padx = 10, ipady = 4)

		label_style_data = ttk.Label(
			label_frame_row1, text = "Dades Personals", style = "Title.TLabel"
		)
		label_frame_data = ttk.LabelFrame(
			label_frame_row1,
			style = "BorderLine.TFrame",
			labelwidget = label_style_data
		)
		label_frame_data.grid(row = 0, column = 3, padx = 10, ipady = 4)

		label_style_movements = ttk.Label(
			label_frame_row2, text = "Moviments", style = "Title.TLabel"
		)
		label_frame_movements = ttk.LabelFrame(
			label_frame_row2,
			style = "BorderLine.TFrame",
			labelwidget = label_style_movements
		)
		label_frame_movements.grid(row = 0, column = 0, padx = 15, ipadx = 5)

		label_style_family_movements = ttk.Label(
			label_frame_row2,
			text = "Moviments de la familia",
			style = "Title.TLabel"
		)
		label_frame_family_movements = ttk.LabelFrame(
			label_frame_row2, style = "BorderLine.TFrame",
			labelwidget = label_style_family_movements
		)
		label_frame_family_movements.grid(
			row = 0, column = 1, padx = 15, ipadx = 5
		)

		label_style_assign = ttk.Label(
			label_frame_row3, text = "Assignar", style = "Title.TLabel"
		)
		label_frame_assign = ttk.LabelFrame(
			label_frame_row3,
			style = "BorderLine.TFrame",
			labelwidget = label_style_assign
		)
		label_frame_assign.grid(
			row = 0, column = 0, padx = 15, ipady = 5, sticky = "n"
		)

		label_style_history = ttk.Label(
			label_frame_row3,
			text = "Historial de moviments",
			style = "Title.TLabel"
		)
		label_frame_history = ttk.LabelFrame(
			label_frame_row3,
			style = "BorderLine.TFrame",
			labelwidget = label_style_history
		)
		label_frame_history.grid(row = 0, column = 1, padx = 15)

		# Widgets per a cada frame.

		# Frame "Exercici".
		self.entry_falla_year = ttk.Entry(
			label_frame_falla_year,
			width = 10,
			style = "Entry.TEntry",
			state = "disabled",
			textvariable = self.falla_year
		)
		self.entry_falla_year.pack()

		# Frame "Buscar faller".
		self.label_id = ttk.Label(
			label_frame_search, text = "Id", style = "Label.TLabel"
		)
		self.label_id.grid(
			row = 0, column = 0, padx = 5, pady = 2, sticky = "w"
		)

		self.entry_id = ttk.Entry(
			label_frame_search, width = 8, textvariable = self.id
		)
		self.entry_id.grid(row = 1, column = 0, padx = 5)
		self.entry_id.bind('<Return>', self.search_by_id)
		self.entry_id.bind(
			'<FocusIn>',
			lambda event: self.select_content(event, self.entry_id)
		)

		self.label_name = ttk.Label(
			label_frame_search,
			text = "Cognoms i nom",
			style = "Label.TLabel"
		)
		self.label_name.grid(row = 0, column = 1, padx = 5, sticky = "w")

		self.combo_box_member = ttk.Combobox(
			label_frame_search, width = 30, postcommand = self.display_member
		)
		self.combo_box_member.grid(row = 1, column = 1, padx = 5)
		self.combo_box_member.bind("<<ComboboxSelected>>", self.select_member)

		self.button_register = ttk.Button(
			label_frame_search,
			state = "disabled",
			width = 15,
			style = "Button.TButton",
			text = "Donar d'alta",
			command = self.change_membership_status
		)
		self.button_register.grid(
			row = 2, column = 1, padx = 5, pady = 10, sticky = "e"
		)

		# Frame "Familia".
		self.label_family = ttk.Label(
			label_frame_family,
			text = "Membres de la familia",
			style = "Label.TLabel"
		)
		self.label_family.grid(
			row = 0, column = 0, padx = 5, pady = 2, sticky = "w"
		)

		self.combo_box_family = ttk.Combobox(
			label_frame_family, postcommand = self.display_family
		)
		self.combo_box_family.grid(row = 1, column = 0, padx = 5)
		self.combo_box_family.bind("<<ComboboxSelected>>", self.select_family)

		self.label_members = ttk.Label(
			label_frame_family,
			text = "Membres actius",
			style = "Label.TLabel"
		)
		self.label_members.grid(
			row = 2, column = 0, padx = 5, pady = 2, sticky = "w"
		)

		self.entry_members = ttk.Entry(
			label_frame_family,
			width = 4,
			style = "Entry.TEntry",
			state = "disabled",
			textvariable = self.family_members
		)
		self.entry_members.grid(row = 3, column = 0, padx = 5, sticky = "w")

		# Frame "Dades personals".
		self.label_birthdate = ttk.Label(
			label_frame_data,
			text = "Data de naixement",
			style = "Label.TLabel"
		)
		self.label_birthdate.grid(
			row = 0, column = 0, padx = 5, pady = 2, sticky = "w"
		)

		self.entry_birthdate = ttk.Entry(
			label_frame_data,
			style = "Entry.TEntry",
			state = "disabled",
			textvariable = self.birthdate
		)
		self.entry_birthdate.grid(row = 1, column = 0, padx = 5)

		self.label_dni = ttk.Label(
			label_frame_data, text = "DNI", style = "Label.TLabel"
		)
		self.label_dni.grid(
			row = 2, column = 0, padx = 5, pady = 2, sticky = "w"
		)

		self.entry_dni = ttk.Entry(
			label_frame_data,
			style = "Entry.TEntry",
			state = "disabled",
			textvariable = self.dni
		)
		self.entry_dni.grid(row = 3, column = 0, padx = 5)

		self.label_address = ttk.Label(
			label_frame_data, text = "Adreça", style = "Label.TLabel"
		)
		self.label_address.grid(row = 0, column = 1, padx = 5, sticky = "w")

		self.entry_address = ttk.Entry(
			label_frame_data,
			width = 30,
			style = "Entry.TEntry",
			state = "disabled",
			textvariable = self.address
		)
		self.entry_address.grid(row = 1, column = 1, padx = 5)

		self.label_email = ttk.Label(
			label_frame_data,
			text = "Correu electrònic",
			style = "Label.TLabel"
		)
		self.label_email.grid(row = 2, column = 1, padx = 5, sticky = "w")

		self.entry_email = ttk.Entry(
			label_frame_data,
			width = 30,
			style = "Entry.TEntry",
			state = "disabled",
			textvariable = self.email
		)
		self.entry_email.grid(row = 3, column = 1, padx = 5)

		self.label_phone_number = ttk.Label(
			label_frame_data,
			text = "Telèfon",
			style = "Label.TLabel"
		)
		self.label_phone_number.grid(
			row = 0, column = 2, padx = 5, sticky = "w"
		)

		self.entry_phone_number = ttk.Entry(
			label_frame_data,
			style = "Entry.TEntry",
			state = "disabled",
			textvariable = self.phone_number
		)
		self.entry_phone_number.grid(row = 1, column = 2, padx = 5)

		self.button_modify = ttk.Button(
			label_frame_data,
			state = "disabled",
			text = "Modificar dades",
			style = "Button.TButton",
			command = self.open_modify_member_window
		)
		self.button_modify.grid(
			row = 2, column = 2, padx = 5, rowspan = 2, sticky = "s" + "e"
		)

		#Frame "Moviments".
		self.label_assigned = ttk.Label(
			label_frame_movements, text = "Assignat", style = "Label.TLabel"
		)
		self.label_assigned.grid(row = 0, column = 1, pady = 2)

		self.label_payed = ttk.Label(
			label_frame_movements, text = "Pagat", style = "Label.TLabel"
		)
		self.label_payed.grid(row = 0, column = 2)

		self.label_difference = ttk.Label(
			label_frame_movements,
			text = "Diferència",
			style = "Label.TLabel"
		)
		self.label_difference.grid(row = 0, column = 3)

		self.label_fee = ttk.Label(
			label_frame_movements, text = "Quota", style = "Label.TLabel"
		)
		self.label_fee.grid(row = 1, column = 0, padx = 5, sticky = "e")

		self.entry_assigned_fee = ttk.Entry(
			label_frame_movements,
			width = 15,
			style = "Entry.TEntry",
			state = "disabled",
			textvariable = self.assigned_fee
		)
		self.entry_assigned_fee.grid(row = 1, column = 1)

		self.entry_payed_fee = ttk.Entry(
			label_frame_movements,
			width = 15,
			style = "Entry.TEntry",
			state = "disabled",
			textvariable = self.payed_fee
		)
		self.entry_payed_fee.grid(row = 1, column = 2)

		self.entry_debt_fee = ttk.Entry(
			label_frame_movements,
			width = 15,
			style = "Entry.TEntry",
			state = "disabled",
			textvariable = self.debt_fee
		)
		self.entry_debt_fee.grid(row = 1, column = 3)

		self.entry_pay_fee = ttk.Entry(
			label_frame_movements,
			width = 15,
			state = "disabled",
			textvariable = self.pay_fee
		)
		self.entry_pay_fee.grid(row = 1, column = 4)
		self.entry_pay_fee.bind(
			'<KeyRelease>',
			lambda event: self.calculate_totals(event, self.entry_pay_fee)
		)
		self.entry_pay_fee.bind(
			'<FocusIn>',
			lambda event: self.select_content(event, self.entry_pay_fee)
		)

		self.label_lottery = ttk.Label(
			label_frame_movements,
			text = "Loteria",
			style = "Label.TLabel"
		)
		self.label_lottery.grid(row = 2, column = 0, padx = 5, sticky = "e")

		self.entry_assigned_lottery = ttk.Entry(
			label_frame_movements,
			width = 15,
			style = "Entry.TEntry",
			state = "disabled",
			textvariable = self.assigned_lottery
		)
		self.entry_assigned_lottery.grid(row = 2, column = 1)

		self.entry_payed_lottery = ttk.Entry(
			label_frame_movements,
			width = 15,
			style = "Entry.TEntry",
			state = "disabled",
			textvariable = self.payed_lottery
		)
		self.entry_payed_lottery.grid(row = 2, column = 2)

		self.entry_debt_lottery = ttk.Entry(
			label_frame_movements,
			width = 15,
			style = "Entry.TEntry",
			state = "disabled",
			textvariable = self.debt_lottery
		)
		self.entry_debt_lottery.grid(row = 2, column = 3)

		self.entry_pay_lottery = ttk.Entry(
			label_frame_movements,
			width = 15,
			state = "disabled",
			textvariable = self.pay_lottery
		)
		self.entry_pay_lottery.grid(row = 2, column = 4)
		self.entry_pay_lottery.bind(
			'<KeyRelease>',
			lambda event: self.calculate_totals(event, self.entry_pay_lottery)
		)
		self.entry_pay_lottery.bind(
			'<FocusIn>',
			lambda event: self.select_content(event, self.entry_pay_lottery)
		)

		self.label_raffle = ttk.Label(
			label_frame_movements, text = "Rifa", style = "Label.TLabel"
		)
		self.label_raffle.grid(row = 3, column = 0, padx = 5, sticky = "e")

		self.entry_assigned_raffle = ttk.Entry(
			label_frame_movements,
			width = 15,
			style="Entry.TEntry",
			state = "disabled",
			textvariable = self.assigned_raffle
		)
		self.entry_assigned_raffle.grid(row = 3, column = 1)

		self.entry_payed_raffle = ttk.Entry(
			label_frame_movements,
			width = 15,
			style = "Entry.TEntry",
			state = "disabled",
			textvariable = self.payed_raffle
		)
		self.entry_payed_raffle.grid(row = 3, column = 2)

		self.entry_debt_raffle = ttk.Entry(
			label_frame_movements,
			width = 15,
			style = "Entry.TEntry",
			state = "disabled",
			textvariable = self.debt_raffle
		)
		self.entry_debt_raffle.grid(row = 3, column = 3)

		self.entry_pay_raffle = ttk.Entry(
			label_frame_movements,
			width = 15,
			state = "disabled",
			textvariable = self.pay_raffle
		)
		self.entry_pay_raffle.grid(row = 3, column = 4)
		self.entry_pay_raffle.bind(
			'<KeyRelease>',
			lambda event: self.calculate_totals(event, self.entry_pay_raffle)
		)
		self.entry_pay_raffle.bind(
			'<FocusIn>',
			lambda event: self.select_content(event, self.entry_pay_raffle)
		)

		self.label_totals = ttk.Label(
			label_frame_movements, text = "Totals", style = "Label.TLabel"
		)
		self.label_totals.grid(row = 4, column = 0, padx = 5, sticky = "e")

		self.entry_total_assigned = ttk.Entry(
			label_frame_movements,
			width = 15,
			style = "Entry.TEntry",
			state = "disabled",
			textvariable = self.total_assigned
		)
		self.entry_total_assigned.grid(row = 4, column = 1)

		self.entry_total_payed = ttk.Entry(
			label_frame_movements,
			width = 15,
			style = "Entry.TEntry",
			state = "disabled",
			textvariable = self.total_payed
		)
		self.entry_total_payed.grid(row = 4, column = 2)

		self.entry_total_debt = ttk.Entry(
			label_frame_movements,
			width = 15,
			style = "Entry.TEntry",
			state = "disabled",
			textvariable = self.total_debt
		)
		self.entry_total_debt.grid(row = 4, column = 3)

		self.entry_pay_total = ttk.Entry(
			label_frame_movements,
			width = 15,
			style = "Entry.TEntry",
			state = "disabled",
			textvariable = self.pay_total
		)
		self.entry_pay_total.grid(row = 4, column = 4)

		self.radio_button_cash = ttk.Radiobutton(
			label_frame_movements,
			text = "Caixa",
			style = "Radio.TRadiobutton",
			variable = self.way_to_pay,
			value = 1
		)
		self.radio_button_bank = ttk.Radiobutton(
			label_frame_movements,
			text = "Banc",
			style = "Radio.TRadiobutton",
			variable = self.way_to_pay,
			value = 2
		)
		self.radio_button_cash.grid(row = 5, column = 2)
		self.radio_button_bank.grid(row = 5, column = 3)

		self.button_pay = ttk.Button(
			label_frame_movements,
			width = 8,
			state = "disabled",
			text = "Pagar",
			style = "Button.TButton",
			command = self.pay
		)
		self.button_pay.grid(row = 5, column = 4, pady = 10, sticky = "e")

		# Frame "Moviments de la familia".
		self.label_family_assigned = ttk.Label(
			label_frame_family_movements,
			text="Assignat",
			style = "Label.TLabel"
		)
		self.label_family_assigned.grid(row = 0, column = 1, pady = 2)

		self.label_family_payed = ttk.Label(
			label_frame_family_movements,
			text = "Pagat",
			style = "Label.TLabel"
		)
		self.label_family_payed.grid(row = 0, column = 2)

		self.label_family_difference = ttk.Label(
			label_frame_family_movements,
			text = "Diferència",
			style = "Label.TLabel"
		)
		self.label_family_difference.grid(row = 0, column = 3)

		self.label_family_fee = ttk.Label(
			label_frame_family_movements,
			text = "Quota",
			style = "Label.TLabel"
		)
		self.label_family_fee.grid(row = 1, column = 0, padx = 5, sticky = "e")

		self.entry_family_assigned_fee = ttk.Entry(
			label_frame_family_movements,
			width = 15,
			style = "Entry.TEntry",
			state = "disabled",
			textvariable = self.family_assigned_fee
		)
		self.entry_family_assigned_fee.grid(row = 1, column = 1)

		self.entry_family_payed_fee = ttk.Entry(
			label_frame_family_movements,
			width = 15,
			style = "Entry.TEntry",
			state = "disabled",
			textvariable = self.family_payed_fee
		)
		self.entry_family_payed_fee.grid(row = 1, column = 2)

		self.entry_family_debt_fee = ttk.Entry(
			label_frame_family_movements,
			width = 15,
			style = "Entry.TEntry",
			state = "disabled",
			textvariable = self.family_debt_fee
		)
		self.entry_family_debt_fee.grid(row = 1, column = 3)

		self.entry_family_pay_fee = ttk.Entry(
			label_frame_family_movements,
			width = 15,
			state = "disabled",
			textvariable = self.family_pay_fee
		)
		self.entry_family_pay_fee.grid(row = 1, column = 4)
		self.entry_family_pay_fee.bind(
			'<KeyRelease>',
			lambda event: self.calculate_totals(
				event,
				self.entry_family_pay_fee
			)
		)
		self.entry_family_pay_fee.bind(
			'<FocusIn>',
			lambda event: self.select_content(event, self.entry_family_pay_fee)
		)

		self.label_family_lottery = ttk.Label(
			label_frame_family_movements,
			text = "Loteria",
			style = "Label.TLabel"
		)
		self.label_family_lottery.grid(
			row = 2, column = 0, padx = 5, sticky = "e"
		)

		self.entry_family_assigned_lottery = ttk.Entry(
			label_frame_family_movements,
			width = 15,
			style = "Entry.TEntry",
			state = "disabled",
			textvariable = self.family_assigned_lottery
		)
		self.entry_family_assigned_lottery.grid(row = 2, column = 1)

		self.entry_family_payed_lottery = ttk.Entry(
			label_frame_family_movements,
			width = 15,
			style = "Entry.TEntry",
			state = "disabled",
			textvariable = self.family_payed_lottery
		)
		self.entry_family_payed_lottery.grid(row = 2, column = 2)

		self.entry_family_debt_lottery = ttk.Entry(
			label_frame_family_movements,
			width = 15,
			style = "Entry.TEntry",
			state = "disabled",
			textvariable = self.family_debt_lottery
		)
		self.entry_family_debt_lottery.grid(row = 2, column = 3)

		self.entry_family_pay_lottery = ttk.Entry(
			label_frame_family_movements,
			width = 15,
			state = "disabled",
			textvariable=self.family_pay_lottery
		)
		self.entry_family_pay_lottery.grid(row = 2, column = 4)
		self.entry_family_pay_lottery.bind(
			'<KeyRelease>',
			lambda event: self.calculate_totals(
				event,
				self.entry_family_pay_lottery
			)
		)
		self.entry_family_pay_lottery.bind(
			'<FocusIn>',
			lambda event: self.select_content(
				event,
				self.entry_family_pay_lottery
			)
		)

		self.label_family_raffle = ttk.Label(
			label_frame_family_movements,
			text = "Rifa",
			style = "Label.TLabel"
		)
		self.label_family_raffle.grid(
			row = 3, column = 0, padx = 5, sticky = "e"
		)

		self.entry_family_assigned_raffle = ttk.Entry(
			label_frame_family_movements,
			width = 15,
			style = "Entry.TEntry",
			state = "disabled",
			textvariable = self.family_assigned_raffle
		)
		self.entry_family_assigned_raffle.grid(row = 3, column = 1)

		self.entry_family_payed_raffle = ttk.Entry(
			label_frame_family_movements,
			width = 15,
			style = "Entry.TEntry",
			state = "disabled",
			textvariable = self.family_payed_raffle
		)
		self.entry_family_payed_raffle.grid(row = 3, column = 2)

		self.entry_family_debt_raffle = ttk.Entry(
			label_frame_family_movements,
			width = 15,
			style = "Entry.TEntry",
			state = "disabled",
			textvariable = self.family_debt_raffle
		)
		self.entry_family_debt_raffle.grid(row = 3, column = 3)

		self.entry_family_pay_raffle = ttk.Entry(
			label_frame_family_movements,
			width = 15,
			state = "disabled",
			textvariable = self.family_pay_raffle
		)
		self.entry_family_pay_raffle.grid(row = 3, column = 4)
		self.entry_family_pay_raffle.bind(
			'<KeyRelease>',
			lambda event: self.calculate_totals(
				event,
				self.entry_family_pay_raffle
			)
		)
		self.entry_family_pay_raffle.bind(
			'<FocusIn>',
			lambda event: self.select_content(
				event,
				self.entry_family_pay_raffle
			)
		)

		self.label_total_family = ttk.Label(
			label_frame_family_movements,
			text = "Totals",
			style = "Label.TLabel"
		)
		self.label_total_family.grid(
			row = 4, column = 0, padx = 5, sticky = "e"
		)

		self.entry_family_total_assigned = ttk.Entry(
			label_frame_family_movements,
			width = 15,
			style = "Entry.TEntry",
			state = "disabled",
			textvariable = self.family_total_assigned
		)
		self.entry_family_total_assigned.grid(row = 4, column = 1)

		self.entry_family_total_payed = ttk.Entry(
			label_frame_family_movements,
			width = 15,
			style = "Entry.TEntry",
			state = "disabled",
			textvariable = self.family_total_payed
		)
		self.entry_family_total_payed.grid(row = 4, column = 2)

		self.entry_family_total_debt = ttk.Entry(
			label_frame_family_movements,
			width = 15,
			style = "Entry.TEntry",
			state = "disabled",
			textvariable = self.family_total_debt
		)
		self.entry_family_total_debt.grid(row = 4, column = 3)

		self.entry_family_pay_total = ttk.Entry(
			label_frame_family_movements,
			width = 15,
			style = "Entry.TEntry",
			state = "disabled",
			textvariable = self.family_pay_total
		)
		self.entry_family_pay_total.grid(row = 4, column = 4)

		self.radio_button_family_cash = ttk.Radiobutton(
			label_frame_family_movements,
			text = "Caixa",
			style = "Radio.TRadiobutton",
			variable = self.family_way_to_pay,
			value = 1
		)
		self.radio_button_family_bank = ttk.Radiobutton(
			label_frame_family_movements,
			text = "Banc",
			style = "Radio.TRadiobutton",
			variable = self.family_way_to_pay,
			value = 2
		)
		self.radio_button_family_cash.grid(row = 5, column = 2)
		self.radio_button_family_bank.grid(row = 5, column = 3)

		self.button_family_pay = ttk.Button(
			label_frame_family_movements,
			width = 8,
			state = "disabled",
			text = "Pagar",
			style = "Button.TButton",
			command = self.family_pay
		)
		self.button_family_pay.grid(
			row = 5, column = 4, pady = 10, sticky = "e"
		)

		# Frame "Assignar".
		self.label_description = ttk.Label(
			label_frame_assign,
			text = "Descripció",
			style = "Label.TLabel"
		)
		self.label_description.grid(
			row = 0, column = 0, padx = 5, pady = 2, sticky = "w"
		)

		self.entry_assignment_description = ttk.Entry(
			label_frame_assign,
			state = "disabled",
			textvariable = self.assignment_description
		)
		self.entry_assignment_description.grid(row = 1, column = 0, padx = 5)

		self.label_assign_amount = ttk.Label(
			label_frame_assign,
			text = "Quantitat",
			style = "Label.TLabel"
		)
		self.label_assign_amount.grid(
			row = 2, column = 0, padx = 5, pady = 2, sticky = "w"
		)

		self.entry_total_assignment = ttk.Entry(
			label_frame_assign,
			state = "disabled",
			textvariable = self.total_assignment
		)
		self.entry_total_assignment.grid(
			row = 3, column = 0, padx = 5, sticky = "n"
		)
		self.entry_total_assignment.bind(
			'<KeyRelease>',
			lambda event: self.calculate_totals(
				event,
				self.entry_total_assignment
			)
		)
		self.entry_total_assignment.bind(
			'<FocusIn>',
			lambda event: self.select_content(
				event,
				self.entry_total_assignment
			)
		)

		self.radio_button_fee = ttk.Radiobutton(
			label_frame_assign,
			text = "Quota",
			style = "Radio.TRadiobutton",
			variable = self.assignment_concept,
			value = 1
		)
		self.radio_button_lottery = ttk.Radiobutton(
			label_frame_assign,
			text = "Loteria",
			style = "Radio.TRadiobutton",
			variable = self.assignment_concept,
			value = 2
		)
		self.radio_button_raffle = ttk.Radiobutton(
			label_frame_assign,
			text = "Rifa",
			style = "Radio.TRadiobutton",
			variable = self.assignment_concept,
			value = 3
		)
		self.radio_button_fee.grid(row = 1, column = 1, padx = 5, sticky = "w")
		self.radio_button_lottery.grid(
			row = 1, column = 2, padx = 5, sticky = "w"
		)
		self.radio_button_raffle.grid(
			row = 1, column = 3, padx = 5, sticky = "w"
		)

		self.button_assign = ttk.Button(
			label_frame_assign,
			state = "disabled",
			text = "Assignar",
			style = "Button.TButton",
			command = self.assign
		)
		self.button_assign.grid(row = 3, column = 2, columnspan = 2, padx = 5)

		# Frame "Taula".
		self.tree_movements = ttk.Treeview(label_frame_history, height = 10)
		self.tree_movements.grid(row = 0, column = 0, padx = 10, pady = 5)
		self.tree_movements["columns"] = ("one","two","three","four","five")
		self.tree_movements.column("#0", width = 80)
		self.tree_movements.column("one", width = 80)
		self.tree_movements.column("two", width = 80)
		self.tree_movements.column("three", width = 80)
		self.tree_movements.column("four", width = 80)
		self.tree_movements.column("five", width = 160)
		self.tree_movements.heading("#0", text = "moviment")
		self.tree_movements.heading('one', text = "data")
		self.tree_movements.heading('two', text = "assignat")
		self.tree_movements.heading('three', text = "pagat")
		self.tree_movements.heading('four', text = "concepte")
		self.tree_movements.heading('five', text = "descripció")

		self.scroll_movements_table = ttk.Scrollbar(
			label_frame_history,
			command = self.tree_movements.yview
		)
		self.scroll_movements_table.grid(row = 0, column = 1, sticky = "nsew")

		self.tree_movements.config(
			yscrollcommand = self.scroll_movements_table.set
		)

		# Bindeig de la finestra per a que refresque quan pille
		# el foco al tancar la finestra "modificar".
		self.bind("<FocusIn>", self.handle_focus)

		# Paràmetres d'inici de la finestra.
		falla = Falla()
		falla.get_current_falla_year()
		self.falla_year.set(
			str(falla.falla_year-1) + "-" + str(falla.falla_year)
		)
		self.entry_id.focus()
		self.way_to_pay.set(1)
		self.family_way_to_pay.set(1)
		self.assignment_concept.set(1)
		self.grab_set()
		self.transient(self.master)


	def handle_focus(self, event):
		'''
		Controla el tancament de la finestra "Modificar" de forma que al tancar
		dita finestra, recupera el foco i torna a carregar totes
		les dades del faller ja actualitzades.
		'''
		if self.id.get() != "" and self.modify_member_window_opened == 1:
			self.entry_id.focus()
			self.search_by_id('<Return>')
			self.modify_member_window_opened = 0


	def open_modify_member_window(self):
		''' 
		Crea una nova instància de la classe ModifyMemberWindow
		que obri la finestra "Modificar" des del botó.
		'''
		modify = ModifyMemberWindow(self)
		self.modify_member_window_opened = 1
		modify.fill_in_fields(int(self.id.get()))
		

	def change_membership_status(self):
		'''
		Canvia l'estat del faller d'alta a baixa i al revés.
		Es modifica el seu estat en la base de dades
		i es canvia també l'historial.
		Després es recalcula el descompte familiar
		depenent dels fallers que queden actius.
		'''
		falla = Falla()
		falla.get_current_falla_year()
		result = Member.get_member(self.id.get())
		family = Family(result[12], result[13], result[14])
		category = Category(result[15], result[16], result[17], result[18])
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
			family,
			category
		)

		if member.is_registered == 1:
			value = messagebox.askquestion(
				"Baixa","Estàs segur que vols donar de baixa al faller?"
			)
			if value == "yes":
				member.is_registered = 0
				member.modify_member(
					member.id,
					member.name,
					member.surname,
					member.birthdate,
					member.gender,
					member.dni,
					member.address,
					member.phone_number,
					member.is_registered,
					member.email,
					family.id,
					category.id
				)
		elif member.is_registered == 0:
			value = messagebox.askquestion(
				"Alta","Estàs segur que vols donar d'alta al faller?"
			)
			if value == "yes":
				member.is_registered = 1
				member.modify_member(
					member.id,
					member.name,
					member.surname,
					member.birthdate,
					member.gender,
					member.dni,
					member.address,
					member.phone_number,
					member.is_registered,
					member.email,
					family.id,
					category.id
				)
		result = family.get_members(family.id)
		for values in result:
			category = Category(values[15], values[16], values[17], values[18])
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
		self.entry_id.focus()
		self.search_by_id('<Return>')

	
	def search_by_id(self, event):
		'''
		Comprova que el faller amb l'id indicat està a la base de dades i,
		si es així llença la funció que ompli el formulari complet.
		En cas de no ser així mostra un error.
		Utilitza l'atribut "self.previous_id" per a guardar l'identificador
		de l'últim faller mostrat per a tornar-lo a mostrar en cas d'error.
		Va associat a l'event de pulsar la tecla "Enter" dins del camp "id".
		'''
		id = self.id.get()
		result = Member.get_member(0)
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
		try:
			if member.id < int(self.id.get()):
				messagebox.showwarning(
					"Error", "No existeix un faller amb eixa id"
				)
				if self.previous_id == 0:
					self.id.set("")
				else:
					self.id.set(self.previous_id)
			else:
				self.previous_id = id
				self.fill_in_fields(id)
		except:
			messagebox.showinfo(
				"Info", "No hi ha fallers amb id = 0"
			)
		

	def display_member(self):
		'''
		Controla el combobox comparant la cadena escrita amb la base de dades
		i mostrant els resultats en el combobox.
		Utilitza l'atribut "self.member_ids" per a passar l'identificador
		de faller a la funció "select_member".
		'''
		falla = Falla()
		surname = self.combo_box_member.get()
		falla.get_members("surname", surname)
		members_list = []
		self.member_ids = []
		for member in falla.members_list:
			self.member_ids = self.member_ids + [member.id]
			members_list = members_list + [(
				member.surname + ", " + member.name
			)]
		self.combo_box_member["values"] = members_list

	
	def select_member(self, event):
		'''
		Controla la selecció del combobox per a guardar l'identificador
		del faller i omplir les dades a partir d'aquest.
		'''
		index = self.combo_box_member.current()
		self.id.set(self.member_ids[index])
		self.member_ids = []
		self.previous_id = self.id.get()
		self.fill_in_fields(self.id.get())
		

	def display_family(self):
		'''
		Ompli el combobox amb tots els familiars del faller.
		'''
		result = Member.get_member(self.id.get())
		family = Family(result[12], result[13], result[14])
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
				values[11]
			)
			family.members_list.append(family_member)
		members_list = []
		self.member_ids = []
		for member in family.members_list:
			self.member_ids = self.member_ids + [member.id]
			members_list = members_list + [(
				member.surname + ", " + member.name
			)]
		self.combo_box_family["values"] = members_list


	def select_family(self, event):
		'''
		Controla la selecció del combobox per a guardar l'identificador
		del familiar del faller
		i ompli les dades a partir d'aquest.
		'''
		index = self.combo_box_family.current()
		self.id.set(self.member_ids[index])
		self.member_ids = []
		self.previous_id = self.id.get()
		self.fill_in_fields(self.id.get())
		self.combo_box_family.set("")


	def fill_in_fields(self, id):
		'''
		Ompli el formulari complet (dades, pagaments, familia...)
		a partir de l'id del faller.

		Paràmetres:
		-----------
		id : int
			Identificador del faller.
		'''
		falla = Falla()
		falla.get_current_falla_year()
		result = Member.get_member(id)
		family = Family(result[12], result[13], result[14])
		category = Category(result[15], result[16], result[17], result[18])
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
			family,
			category
		)
		
		self.combo_box_member.set(member.surname + ", " + member.name)
		utils = Utils()
		birthdate = utils.convert_to_spanish_date(member.birthdate)
		self.birthdate.set(birthdate)
		self.dni.set(member.dni)
		self.address.set(member.address)
		self.phone_number.set(member.phone_number)
		self.email.set(member.email)
		self.button_modify.config(state = "normal")

		if member.is_registered == 0:
			self.button_register.config(
				state = "normal",
				text = "Donar d'alta"
			)
			self.pay_fee.set("")
			self.entry_pay_fee.config(state = "disabled")
			self.pay_lottery.set("")
			self.entry_pay_lottery.config(state = "disabled")
			self.pay_raffle.set("")
			self.entry_pay_raffle.config(state = "disabled")
			self.pay_total.set("")
			self.button_pay.config(state = "disabled")
			self.entry_assignment_description.config(state = "disabled")
			self.total_assignment.set("")
			self.entry_total_assignment.config(state = "disabled")
			self.button_assign.config(state = "disabled")
		else:
			self.button_register.config(
				state = "normal",
				text = "Donar de baixa"
			)
			self.pay_fee.set(0)
			self.entry_pay_fee.config(state = "normal")
			self.pay_lottery.set(0)
			self.entry_pay_lottery.config(state = "normal")
			self.pay_raffle.set(0)
			self.entry_pay_raffle.config(state = "normal")
			self.pay_total.set(0)
			self.button_pay.config(state="normal")
			self.entry_assignment_description.config(state = "normal")
			self.total_assignment.set(0)
			self.entry_total_assignment.config(state = "normal")
			self.button_assign.config(state = "normal")

		if member.is_registered == 1:
			balance = falla.get_balance(member.id)
			assigned_fee = balance[0]
			payed_fee = balance[1]
			assigned_lottery = balance[2]
			payed_lottery = balance[3]
			assigned_raffle = balance[4]
			payed_raffle = balance[5]
		else:
			assigned_fee = falla.calculate_assigned_fee(
				member.id,falla.falla_year
			)
			payed_fee = falla.calculate_payed_fee(member.id, falla.falla_year)
			assigned_lottery = falla.calculate_assigned_lottery(
				member.id, falla.falla_year
			)
			payed_lottery = falla.calculate_payed_lottery(
				member.id, falla.falla_year
			)
			assigned_raffle = falla.calculate_assigned_raffle(
				member.id, falla.falla_year
			)
			payed_raffle = falla.calculate_payed_raffle(
				member.id, falla.falla_year
			)

		self.assigned_fee.set("{0:.2f}".format(assigned_fee) + " €")
		self.payed_fee.set("{0:.2f}".format(payed_fee) + " €")
		self.debt_fee.set("{0:.2f}".format(assigned_fee-payed_fee) + " €")
		self.assigned_lottery.set("{0:.2f}".format(assigned_lottery) + " €")
		self.payed_lottery.set("{0:.2f}".format(payed_lottery) + " €")
		self.debt_lottery.set(
			"{0:.2f}".format(assigned_lottery-payed_lottery) + " €"
		)
		self.assigned_raffle.set("{0:.2f}".format(assigned_raffle) + " €")
		self.payed_raffle.set("{0:.2f}".format(payed_raffle) + " €")
		self.debt_raffle.set(
			"{0:.2f}".format(assigned_raffle - payed_raffle) + " €"
		)
		self.total_assigned.set(
			"{0:.2f}".format(
				assigned_fee + assigned_lottery + assigned_raffle
			) + " €"
		)
		self.total_payed.set(
			"{0:.2f}".format(payed_fee + payed_lottery + payed_raffle) + " €"
		)
		self.total_debt.set("{0:.2f}".format(
			(assigned_fee + assigned_lottery + assigned_raffle) -
			(payed_fee + payed_lottery + payed_raffle)
		) + " €")

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
				values[11]
			)
			family.members_list.append(family_member)
		number_family_members = family.calculate_family_members(
			family.members_list
		)
		self.family_members.set(number_family_members)
		if member.is_registered == 1 and number_family_members > 1:
			self.family_pay_fee.set(0)
			self.entry_family_pay_fee.config(state = "normal")
			self.family_pay_lottery.set(0)
			self.entry_family_pay_lottery.config(state = "normal")
			self.family_pay_raffle.set(0)
			self.entry_family_pay_raffle.config(state = "normal")
			self.family_pay_total.set(0)
			self.button_family_pay.config(state = "normal")
		else:
			self.family_pay_fee.set("")
			self.entry_family_pay_fee.config(state = "disabled")
			self.family_pay_lottery.set("")
			self.entry_family_pay_lottery.config(state = "disabled")
			self.family_pay_raffle.set("")
			self.entry_family_pay_raffle.config(state = "disabled")
			self.family_pay_total.set("")
			self.button_family_pay.config(state = "disabled")

		family_assigned_fee = 0
		family_payed_fee = 0
		family_assigned_lottery = 0
		family_payed_lottery = 0
		family_assigned_raffle = 0
		family_payed_raffle = 0
		
		for family_member in family.members_list:
			if family_member.is_registered == 1:
				balance = falla.get_balance(family_member.id)
				assigned_fee = balance[0]
				payed_fee = balance[1]
				assigned_lottery = balance[2]
				payed_lottery = balance[3]
				assigned_raffle = balance[4]
				payed_raffle = balance[5]

				family_assigned_fee = family_assigned_fee + assigned_fee
				family_payed_fee = family_payed_fee + payed_fee
				family_assigned_lottery = family_assigned_lottery + assigned_lottery
				family_payed_lottery = family_payed_lottery + payed_lottery
				family_assigned_raffle = family_assigned_raffle + assigned_raffle
				family_payed_raffle = family_payed_raffle + payed_raffle

		self.family_assigned_fee.set(
			"{0:.2f}".format(family_assigned_fee) + " €"
		)
		self.family_payed_fee.set("{0:.2f}".format(family_payed_fee) + " €")
		self.family_debt_fee.set(
			"{0:.2f}".format(family_assigned_fee - family_payed_fee) + " €"
		)
		self.family_assigned_lottery.set(
			"{0:.2f}".format(family_assigned_lottery) + " €"
		)
		self.family_payed_lottery.set(
			"{0:.2f}".format(family_payed_lottery) + " €"
		)
		self.family_debt_lottery.set(
			"{0:.2f}".format(
				family_assigned_lottery - family_payed_lottery
			) + " €"
		)
		self.family_assigned_raffle.set(
			"{0:.2f}".format(family_assigned_raffle) + " €"
		)
		self.family_payed_raffle.set(
			"{0:.2f}".format(family_payed_raffle) + " €"
		)
		self.family_debt_raffle.set(
			"{0:.2f}".format(
				family_assigned_raffle - family_payed_raffle
			) + " €"
		)
		self.family_total_assigned.set(
			"{0:.2f}".format(
				family_assigned_fee + family_assigned_lottery + \
					family_assigned_raffle
			) + " €"
		)
		self.family_total_payed.set(
			"{0:.2f}".format(
				family_payed_fee + family_payed_lottery+family_payed_raffle
			) + " €"
		)
		self.family_total_debt.set(
			"{0:.2f}".format(
				(family_assigned_fee - family_payed_fee) + \
					(family_assigned_lottery - family_payed_lottery) + \
						(family_assigned_raffle - family_payed_raffle)
			) + " €"
		)

		self.assignment_description.set("")

		self.tree_movements.delete(*self.tree_movements.get_children())
		falla.get_movements(member.id, falla.falla_year)
		for movement in falla.movements_list:
			if movement.id_concept == 1:
				concepte = "quota"
			elif movement.id_concept == 2:
				concepte = "loteria"
			elif movement.id_concept == 3:
				concepte = "rifa"
			if movement.id_type == 1:
				self.tree_movements.insert(
					"",
					"end",
					text = movement.id,
					values = (
						movement.transaction_date,
						"{0:.2f}".format(movement.amount) + " €",
						"",
						concepte,
						movement.description
					)
				)
			elif movement.id_type == 2:
				self.tree_movements.insert(
					"",
					"end",
					text = movement.id,
					values = (
						movement.transaction_date,
						"",
						"{0:.2f}".format(movement.amount) + " €",
						concepte,
						movement.description
					)
				)

		
	def select_content(self, event, entry):
		'''
		Es bindeja a un camp de forma que al fer "FocusIn" en ell
		es selecciona el contingut del camp i es pot sobreescriure
		sense haver de borrar.

		Paràmetres:
		-----------
		entry : tkinter.Entry
			Camp en el que es fa el foco.
		'''
		entry.select_range(0, tk.END)

	
	def calculate_totals(self, event, entry):
		'''
		Es bindeja a un camp de forma que al fer "KeyRelease" en ell
		es comprova el contingut del camp per veure si es un valor correcte.
		En cas de ser així mostra la suma dels 3 camps en el camp total
		i en cas de que no ho siga el fica a 0, manté el foco per a poder
		canviar el valor i fa la suma però amb el valor del camp a 0.

		Paràmetres:
		-----------
		entry : tkinter.Entry
			Camp en el que es fa el foco.
		'''
		pay_fee = 0
		pay_lottery = 0
		pay_raffle = 0
		family_pay_fee = 0
		family_pay_lottery = 0
		family_pay_raffle = 0
		# Camp "pagar_quota".
		if entry == self.entry_pay_fee:
			pay_lottery = float(self.entry_pay_lottery.get())
			pay_raffle = float(self.entry_pay_raffle.get())
			try:
				pay_fee = float(self.entry_pay_fee.get())
			except ValueError:
				if self.entry_pay_fee.get() == '' or \
					self.entry_pay_fee.get() == '-' or (
						self.entry_pay_fee.get() != '' and \
							self.entry_pay_fee.get()[0] == '-' and \
								self.entry_pay_fee.get()[1:].replace(
									'.', '', 1
								).isdigit()
					):
					pass
				else:
					pay_fee = 0
					self.pay_fee.set(0)
					messagebox.showwarning(
						"Error", "Has d'escriure un valor vàlid"
					)
					self.entry_pay_fee.focus()
			self.pay_total.set(
				"{0:.2f}".format(pay_fee + pay_lottery + pay_raffle) + " €"
			)
		# Camp "pagar_loteria".
		elif entry == self.entry_pay_lottery:
			pay_fee = float(self.entry_pay_fee.get())
			pay_raffle = float(self.entry_pay_raffle.get())
			try:
				pay_lottery = float(self.entry_pay_lottery.get())
			except ValueError:
				if self.entry_pay_lottery.get() == '' or \
					self.entry_pay_lottery.get() == '-' or (
						self.entry_pay_lottery.get() != '' and \
							self.entry_pay_lottery.get()[0] == '-' and \
								self.entry_pay_lottery.get()[1:].replace(
									'.', '', 1
								).isdigit()
					):
					pass
				else:
					pay_lottery = 0
					self.pay_lottery.set(0)
					messagebox.showwarning(
						"Error", "Has d'escriure un valor vàlid"
					)
					self.entry_pay_lottery.focus()
			self.pay_total.set(
				"{0:.2f}".format(pay_fee + pay_lottery + pay_raffle) + " €"
			)
		# Camp "pagar_rifa".
		elif entry == self.entry_pay_raffle:
			pay_fee = float(self.entry_pay_fee.get())
			pay_lottery = float(self.entry_pay_lottery.get())
			try:
				pay_raffle = float(self.entry_pay_raffle.get())
			except ValueError:
				if self.entry_pay_raffle.get() == '' or \
					self.entry_pay_raffle.get() == '-' or (
						self.entry_pay_raffle.get() != '' and \
							self.entry_pay_raffle.get()[0] == '-' and \
								self.entry_pay_raffle.get()[1:].replace(
									'.', '', 1
								).isdigit()
					):
					pass
				else:
					pay_raffle = 0
					self.pay_raffle.set(0)
					messagebox.showwarning(
						"Error", "Has d'escriure un valor vàlid"
					)
					self.entry_pay_raffle.focus()
			self.pay_total.set(
				"{0:.2f}".format(pay_fee + pay_lottery + pay_raffle) + " €"
			)
		# Camp "pagar_quota_familia".
		elif entry == self.entry_family_pay_fee:
			family_pay_lottery = float(self.entry_family_pay_lottery.get())
			family_pay_raffle = float(self.entry_family_pay_raffle.get())
			try:
				family_pay_fee = float(self.entry_family_pay_fee.get())
			except ValueError:
				if self.entry_family_pay_fee.get() == '' or (
					self.entry_family_pay_fee.get() != '' and \
						self.entry_family_pay_fee.get()[0] == '-' and \
							self.entry_family_pay_fee.get()[1:].replace(
								'.', '', 1
							).isdigit()
				):
					pass
				else:
					family_pay_fee = 0
					self.family_pay_fee.set(0)
					messagebox.showwarning(
						"Error", "Has d'escriure un valor vàlid"
					)
					self.entry_family_pay_fee.focus()
			if float(self.family_pay_fee.get()) < 0:
				family_pay_fee = 0
				self.family_pay_fee.set(0)
				messagebox.showwarning(
					"Error",
					"Els abonos només es poden fer als fallers per separat"
				)
				self.entry_family_pay_fee.focus()
			self.family_pay_total.set(
				"{0:.2f}".format(
					family_pay_fee + family_pay_lottery + family_pay_raffle
				) + " €"
			)
		# Camp "pagar_loteria_familia".
		elif entry == self.entry_family_pay_lottery:
			family_pay_fee = float(self.entry_family_pay_fee.get())
			family_pay_raffle = float(self.entry_family_pay_raffle.get())
			try:
				family_pay_lottery = float(self.entry_family_pay_lottery.get())
			except ValueError:
				if self.entry_family_pay_lottery.get() == '' or (
					self.entry_family_pay_lottery.get() != '' and \
						self.entry_family_pay_lottery.get()[0] == '-' and \
							self.entry_family_pay_lottery.get()[1:].replace(
								'.', '', 1
							).isdigit()
				):
					pass
				else:
					family_pay_lottery = 0
					self.family_pay_lottery.set(0)
					messagebox.showwarning(
						"Error", "Has d'escriure un valor vàlid"
					)
					self.entry_family_pay_lottery.focus()
			if float(self.family_pay_lottery.get()) < 0:
				family_pay_lottery = 0
				self.family_pay_lottery.set(0)
				messagebox.showwarning(
					"Error",
					"Els abonos només es poden fer als fallers per separat"
				)
				self.entry_family_pay_lottery.focus()
			self.family_pay_total.set(
				"{0:.2f}".format(
					family_pay_fee + family_pay_lottery + family_pay_raffle
				) + " €"
			)
		# Camp "pagar_rifa_familia".
		elif entry == self.entry_family_pay_raffle:
			family_pay_fee = float(self.entry_family_pay_fee.get())
			family_pay_lottery = float(self.entry_family_pay_lottery.get())
			try:
				family_pay_raffle = float(self.entry_family_pay_raffle.get())
			except ValueError:
				if self.entry_family_pay_raffle.get() == '' or (
					self.entry_family_pay_raffle.get() != '' and \
						self.entry_family_pay_raffle.get()[0] == '-' and \
							self.entry_family_pay_raffle.get()[1:].replace(
								'.', '', 1
							).isdigit()):
					pass
				else:
					family_pay_raffle = 0
					self.family_pay_raffle.set(0)
					messagebox.showwarning(
						"Error", "Has d'escriure un valor vàlid"
					)
					self.entry_family_pay_raffle.focus()
			if float(self.family_pay_raffle.get()) < 0:
				family_pay_raffle = 0
				self.family_pay_raffle.set(0)
				messagebox.showwarning(
					"Error",
					"Els abonos només es poden fer als fallers per separat"
				)
				self.entry_family_pay_raffle.focus()
			self.family_pay_total.set(
				"{0:.2f}".format(
					family_pay_fee + family_pay_lottery + family_pay_raffle
				) + " €"
			)
		# Camp "assignar".
		elif entry == self.entry_total_assignment:
			try:
				float(self.entry_total_assignment.get())
			except ValueError:
				if self.entry_total_assignment.get() == '' or \
					self.entry_total_assignment.get() == '-' or (
						self.entry_total_assignment.get() != '' and \
							self.entry_total_assignment.get()[0] == '-' and \
								self.entry_total_assignment.get()[1:].replace(
									'.', '', 1
								).isdigit()
					):
					pass
				else:
					self.total_assignment.set(0)
					messagebox.showwarning(
						"Error", "Has d'escriure un valor vàlid"
					)
					self.entry_total_assignment.focus()
		
		
	
	def pay(self):
		'''
		A partir de les quantitats indicades s'efectua el pagament de forma que
		es crea un moviment que es guarda a la base de dades i es crea un rebut
		en cas de que aquest moviment s'efectue per caixa.
		'''
		falla = Falla()
		fee_payment = 0
		lottery_payment = 0
		raffle_payment = 0
		if self.pay_fee.get() == "":
			self.pay_fee.set(0)
		if self.pay_lottery.get() == "":
			self.pay_lottery.set(0)
		if self.pay_raffle.get() == "":
			self.pay_raffle.set(0)
		fee_payment = float(self.pay_fee.get()) 
		lottery_payment = float(self.pay_lottery.get())
		raffle_payment = float(self.pay_raffle.get())
		option = self.way_to_pay.get() 
		description = ""
		if option == 1:
			description = "pagat en caixa"
		if option == 2:
			description = "pagat pel banc"
		value = messagebox.askquestion(
			"Pagar","Estàs segur que vols fer el pagament?"
		)
		if value == "yes":
			if float(self.pay_fee.get()) == 0 and \
				float(self.pay_lottery.get()) == 0 and \
					float(self.pay_raffle.get()) == 0:
				messagebox.showwarning(
					"Error", "No es pot fer un pagament de 0 euros"
				)
			else:
				receipt_number = 0
				receipt = Report()
				if option == 1:
					receipt_number = receipt.assign_receipt_number()
				result = Member.get_member(self.id.get())
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
				if float(self.pay_fee.get()) != 0:
					falla.pay_fee(
						None,
						float(self.pay_fee.get()),
						None,
						description,
						receipt_number,
						member.id
					)
				if float(self.pay_lottery.get()) != 0:
					falla.pay_lottery(
						None,
						float(self.pay_lottery.get()),
						None,
						description,
						receipt_number,
						member.id
					)
				if float(self.pay_raffle.get()) != 0:
					falla.pay_raffle(
						None,
						float(self.pay_raffle.get()),
						None,
						description,
						receipt_number,
						member.id
					)
				self.entry_id.focus()
				self.search_by_id('<Return>')
				if option == 1:
					receipt.create_receipt(
						0,
						self.combo_box_member.get(),
						fee_payment,
						lottery_payment,
						raffle_payment,
						self.assigned_fee.get()[:-2],
						self.payed_fee.get()[:-2],
						self.assigned_lottery.get()[:-2],
						self.payed_lottery.get()[:-2],
						self.assigned_raffle.get()[:-2],
						self.payed_raffle.get()[:-2]
					)

	
	def family_pay(self):
		'''
		A partir de les quantitats indicades s'efectua el pagament de forma que
		es crea un moviment per cada membre actiu de la familia fins que
		s'esgota la quantitat a pagar.
		Aquest moviment es guarda a la base de dades i es crea un rebut en cas
		de que aquest moviment s'efectue per caixa.
		'''
		falla = Falla()
		family_fee_payment = 0
		family_lottery_payment = 0
		family_raffle_payment = 0
		if self.family_pay_fee.get() == "":
			self.family_pay_fee.set(0)
		if self.family_pay_lottery.get() == "":
			self.family_pay_lottery.set(0)
		if self.family_pay_raffle.get() == "":
			self.family_pay_raffle.set(0)
		try:
			family_fee_payment = float(self.family_pay_fee.get())
			if float(self.family_pay_fee.get()) < 0:
				family_fee_payment = 0
		except ValueError:
			family_fee_payment = 0
			self.family_pay_fee.set(0)
			self.family_pay_total.set(
				"{0:.2f}".format(
					family_lottery_payment + family_raffle_payment
				) + " €"
			)
			messagebox.showwarning("Error", "Has d'escriure un valor vàlid")
		try:
			family_lottery_payment = float(self.family_pay_lottery.get())
			if float(self.family_pay_lottery.get()) < 0:
				family_lottery_payment = 0
		except ValueError:
			family_lottery_payment = 0
			self.family_pay_lottery.set(0)
			self.family_pay_total.set(
				"{0:.2f}".format(
					family_fee_payment+family_raffle_payment
				) + " €"
			)
			messagebox.showwarning("Error", "Has d'escriure un valor vàlid")
		try:
			family_raffle_payment = float(self.family_pay_raffle.get())
			if float(self.family_pay_raffle.get()) < 0:
				family_raffle_payment = 0
		except ValueError:
			family_raffle_payment = 0
			self.family_pay_raffle.set(0)
			self.family_pay_total.set(
				"{0:.2f}".format(
					family_fee_payment + family_lottery_payment
				) + " €"
			)
			messagebox.showwarning("Error", "Has d'escriure un valor vàlid")
		option = self.family_way_to_pay.get()
		description = ""
		if option == 1:
			description = "pagat en caixa"
		if option == 2:
			description = "pagat pel banc"
		value = messagebox.askquestion(
			"Pagar","Estàs segur que vols fer el pagament?"
		)
		if value == "yes":
			if float(self.family_pay_fee.get()) == 0 and \
				float(self.family_pay_lottery.get()) == 0 and \
					float(self.family_pay_raffle.get()) == 0:
				messagebox.showwarning(
					"Error", "No es pot fer un pagament de 0 euros"
				)
			else:
				result = Member.get_member(self.id.get())
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
						values[11]
					)
					family.members_list.append(family_member)
				registered_members_list = []
				for member in family.members_list:
					if member.is_registered == 1:
						registered_members_list.append(member)
				total_registered_members = len(registered_members_list)
				assigned_fee = 0
				payed_fee = 0
				assigned_lottery = 0
				payed_lottery = 0
				assigned_raffle = 0
				payed_raffle = 0
				pending_fee = 0
				pending_lottery = 0
				pending_raffle = 0
				fee_payment = float(self.family_pay_fee.get())
				lottery_payment = float(self.family_pay_lottery.get())
				raffle_payment = float(self.family_pay_raffle.get())
				receipt_number = 0
				receipt = Report()
				if option == "1":
					receipt_number = receipt.assign_receipt_number()
				falla.get_current_falla_year()
				for member in registered_members_list:
					assigned_fee = assigned_fee + falla.calculate_assigned_fee(
						member.id, falla.falla_year
					)
					payed_fee = payed_fee + falla.calculate_payed_fee(
						member.id, falla.falla_year
					)
					assigned_lottery = assigned_lottery + \
						falla.calculate_assigned_lottery(
							member.id, falla.falla_year
						)
					payed_lottery = payed_lottery + \
						falla.calculate_payed_lottery(
							member.id, falla.falla_year
						)
					assigned_raffle = assigned_raffle + \
						falla.calculate_assigned_raffle(
							member.id, falla.falla_year
						)
					payed_raffle = payed_raffle + falla.calculate_payed_raffle(
						member.id, falla.falla_year
					)

					pending_fee = assigned_fee - payed_fee
					if fee_payment != 0 and total_registered_members == 1:
						falla.pay_fee(
							None,
							fee_payment,
							None,
							description,
							receipt_number,
							member.id
						)
					if fee_payment != 0 and \
						fee_payment <= pending_fee and \
							total_registered_members != 1:
						falla.pay_fee(
							None,
							fee_payment,
							None, description,
							receipt_number,
							member.id
						)
						fee_payment = 0
					if fee_payment != 0 and \
						fee_payment > pending_fee \
							and total_registered_members != 1:
						if pending_fee != 0:
							falla.pay_fee(
								None,
								pending_fee,
								None,
								description,
								receipt_number,
								member.id
							)
						fee_payment = Decimal(fee_payment) - pending_fee

					pending_lottery = assigned_lottery - payed_lottery
					if lottery_payment != 0 and total_registered_members == 1:
						falla.pay_lottery(
							None,
							lottery_payment,
							None,
							description,
							receipt_number,
							member.id
						)
					if lottery_payment != 0 and \
						lottery_payment <= pending_lottery and \
							total_registered_members != 1:
						falla.pay_lottery(
							None,
							lottery_payment,
							None,
							description,
							receipt_number,
							member.id
						)
						lottery_payment = 0
					if lottery_payment != 0 and \
						lottery_payment > pending_lottery and \
							total_registered_members != 1:
						if pending_lottery != 0:
							lottery_payment = 0
							falla.pay_lottery(
								None,
								pending_lottery,
								None,
								description,
								receipt_number,
								member.id
							)
						lottery_payment = Decimal(lottery_payment) - pending_lottery

					pending_raffle = assigned_raffle - payed_raffle
					if raffle_payment != 0 and total_registered_members == 1:
						falla.pay_raffle(
							None,
							raffle_payment,
							None,
							description,
							receipt_number,
							member.id
						)
					if raffle_payment != 0 and \
						raffle_payment <= pending_raffle and \
							total_registered_members != 1:
						falla.pay_raffle(
							None,
							raffle_payment,
							None,
							description,
							receipt_number,
							member.id
						)
						raffle_payment = 0
					if raffle_payment != 0 and \
						raffle_payment > pending_raffle and \
							total_registered_members != 1:
						if pending_raffle != 0:
							falla.pay_raffle(
								None,
								pending_raffle,
								None,
								description,
								receipt_number,
								member.id
							)
						raffle_payment = Decimal(raffle_payment) - pending_raffle

					total_registered_members = total_registered_members - 1

				self.entry_id.focus()
				self.search_by_id('<Return>')
				if option == 1:
					receipt.create_receipt(
						1,
						self.combo_box_member.get(),
						family_fee_payment,
						family_lottery_payment,
						family_raffle_payment,
						self.family_assigned_fee.get()[:-2],
						self.family_payed_fee.get()[:-2],
						self.family_assigned_lottery.get()[:-2],
						self.family_payed_lottery.get()[:-2],
						self.family_assigned_raffle.get()[:-2],
						self.family_payed_raffle.get()[:-2]
					)
	
	
	def assign(self):
		'''
		Crea un moviment d'assignació de quota, loteria o rifa
		amb la descripció que li fiquem.
		'''
		value = messagebox.askquestion(
			"Asignar","Estàs segur que vols fer l'assignació?"
		)
		if value == "yes":
			try:
				if float(self.total_assignment.get()) == 0:
					messagebox.showwarning(
						"Error", "No es pot fer una assignació de 0 euros"
					)
				else:
					result = Member.get_member(self.id.get())
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
					if self.assignment_concept.get() == 1:
						falla.assign_fee(
							None,
							self.total_assignment.get(),
							None,
							member.id,
							self.assignment_description.get()
						)
					elif self.assignment_concept.get() == 2:
						falla.assign_lottery(
							None,
							self.total_assignment.get(),
							None,
							member.id,
							self.assignment_description.get()
						)
					elif self.assignment_concept.get() == 3:
						falla.assign_raffle(
							None,
							self.total_assignment.get(),
							None,
							member.id,
							self.assignment_description.get()
						)
					self.entry_id.focus()
					self.search_by_id('<Return>')
			except ValueError:
				messagebox.showwarning(
					"Error", "Has d'escriure un valor vàlid"
				)
				self.total_assignment.set(0)