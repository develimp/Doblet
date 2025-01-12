import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import platform
from pathlib import Path

from arxiu import Arxiu
from utils import Utils
from falla import Falla
from member import Member


class ModifyRecordWindow(tk.Toplevel):
	'''
	Esta classe representa una nova finestra que depén de la finestra principal.

	Atributs:
	---------
	master : tk.Tk o tk.Toplevel
		La instància principal de l'aplicació o de la finestra que crea esta nova finestra.
	'''


	def __init__(self, master = None):
		'''
		Inicialitza una nova instància de la classe FinestraHistorial.

		Parametres:
		-----------
		master : tk.Tk o tk.Toplevel, opcional
			La instància principal de l'aplicació o de la finestra que crea esta nova finestra.
			Si no es proporciona, es creará una nueva instancia de tk.Tk().
		'''
		super().__init__(master)
		self.master=master
		operating_system = platform.system()
		base_path = Path(__file__).parent.resolve()
		if operating_system == 'Windows':
			self.iconbitmap(base_path / 'images' / 'escut.ico')
		self.resizable(0, 0)
		self.title("Historial Faller")
		utils = Utils()
		utils.define_global_style()
		self.configure(bg = "#ffffff", pady = 5, padx = 5)

		self.id = tk.IntVar()
		self.childish = tk.IntVar()
		self.score = tk.IntVar()
		self.adult = tk.IntVar()
		self.falla = tk.StringVar()
		self.initial_year = tk.IntVar()
		self.final_year = tk.IntVar()

		self.member_ids = [] # Guarda els id_faller del llistat del combo.

		# Frames en els que dividim la finestra.
		label_style_search = ttk.Label(self, text = "Buscar faller", style = "Titol.TLabel")
		label_frame_search = ttk.LabelFrame(self, style = "Marc.TFrame", labelwidget = label_style_search)
		label_frame_search.grid(row = 0, column = 0, ipadx = 3, ipady = 5, pady = 5)

		label_frame_history = tk.LabelFrame(self, borderwidth = 0, background = "#ffffff")
		label_frame_history.grid(row = 1, column = 0, padx = 10, pady = 10)

		label_style_totals = ttk.Label(self, text = "Totals", style = "Titol.TLabel")
		label_frame_totals = ttk.LabelFrame(self, style = "Marc.TFrame", labelwidget = label_style_totals)
		label_frame_totals.grid(row = 2, column = 0, ipady = 5, pady = 5)

		label_style_modify = ttk.Label(self, text = "Modificar", style = "Titol.TLabel")
		label_frame_modify = ttk.LabelFrame(self, style = "Marc.TFrame", labelwidget = label_style_modify)
		label_frame_modify.grid(row = 3, column = 0, ipadx = 3, ipady = 5, pady = 5)

		# Widgets per a cada frame.

		# Frame "Buscar".
		self.label_name = ttk.Label(label_frame_search, text = "Nom", style = "Etiqueta.TLabel")
		self.label_name.grid(row = 0, column = 0, padx = 2)

		self.combo_box_member = ttk.Combobox(label_frame_search, width = 30, postcommand = self.display_member)
		self.combo_box_member.grid(row = 0, column = 1)
		self.combo_box_member.bind("<<ComboboxSelected>>", self.select_member)

		self.label_id = ttk.Label(label_frame_search, text = "Id", style = "Etiqueta.TLabel")
		self.label_id.grid(row = 0, column = 2, padx = 2)

		self.entry_id = ttk.Entry(label_frame_search, state = "disabled", textvariable = self.id)
		self.entry_id.grid(row = 0, column = 3, padx = 2)

		# Frame "Taula".
		self.tree_record = ttk.Treeview(label_frame_history, height = 10)
		self.tree_record["columns"] = ("one", "two", "three", "four")
		self.tree_record.column("#0", width = 80)
		self.tree_record.column("one", width = 80)
		self.tree_record.column("two", width = 80)
		self.tree_record.column("three", width = 80)
		self.tree_record.column("four", width = 120)
		self.tree_record.heading("#0", text = "exercici")
		self.tree_record.heading("one", text = "càrrec")
		self.tree_record.heading("two", text = "punts")
		self.tree_record.heading("three", text = "anys")
		self.tree_record.heading("four", text = "falla")
		self.tree_record.grid(row = 1, column = 0)

		self.scroll_record = ttk.Scrollbar(label_frame_history, command = self.tree_record.yview)
		self.scroll_record.grid(row = 1, column = 1, sticky = "nsew")

		self.tree_record.config(yscrollcommand = self.scroll_record.set)

		# Frame "Totals".
		self.label_childish = ttk.Label(label_frame_totals, text = "Anys d'infantil", style = "Etiqueta.TLabel")
		self.label_childish.grid(row = 0, column = 0, padx = 5, pady = 2, sticky = "w")

		self.entry_childish = ttk.Entry(label_frame_totals, style = "Entrada.TEntry", state = "disabled", textvariable = self.childish)
		self.entry_childish.grid(row = 1, column = 0, padx = 5, sticky = "w")

		self.label_score = ttk.Label(label_frame_totals, text = "Punts", style = "Etiqueta.TLabel")
		self.label_score.grid(row = 0, column = 1, padx = 5, pady = 2, sticky = "w")

		self.entry_score = ttk.Entry(label_frame_totals, style = "Entrada.TEntry", state = "disabled", textvariable = self.score)
		self.entry_score.grid(row = 1, column = 1, padx = 5, sticky = "w")

		self.label_adult = ttk.Label(label_frame_totals, text = "Anys d'adult", style = "Etiqueta.TLabel")
		self.label_adult.grid(row = 0, column = 2, padx = 5, pady = 2, sticky = "w")

		self.entry_adult = ttk.Entry(label_frame_totals, style = "Entrada.TEntry", state = "disabled", textvariable = self.adult)
		self.entry_adult.grid(row = 1, column = 2, padx = 5, sticky = "w")

		# Frame "Modificar".
		self.label_initial_year = ttk.Label(label_frame_modify, text = "Any inicial", style = "Etiqueta.TLabel")
		self.label_initial_year.grid(row = 0, column = 0, padx = 5, pady = 2, sticky = "w")

		self.entry_initial_year = ttk.Entry(label_frame_modify, state = "disabled", textvariable = self.initial_year)
		self.entry_initial_year.grid(row = 1, column = 0, padx = 5, sticky = "w")

		self.label_final_year = ttk.Label(label_frame_modify, text = "Any final", style = "Etiqueta.TLabel")
		self.label_final_year.grid(row = 2, column = 0, padx = 5, pady = 2, sticky = "w")

		self.entry_final_year = ttk.Entry(label_frame_modify, state = "disabled", textvariable = self.final_year)
		self.entry_final_year.grid(row = 3, column = 0, padx = 5, sticky = "w")

		self.label_position = ttk.Label(label_frame_modify, text = "Càrrec", style = "Etiqueta.TLabel")
		self.label_position.grid(row = 0, column = 1, padx = 5, pady = 2, sticky = "w")

		self.combo_box_position = ttk.Combobox(label_frame_modify, width = 20, state = "disabled", values = ["baixa", "vocal", "fallera major infantil", "president infantil", "directiu", "cort JFL", "fallera major", "president", "fallera major Alzira", "president JLF"])
		self.combo_box_position.current(1)
		self.combo_box_position.grid(row = 1, column = 1, padx = 5, sticky = "w")

		self.label_falla = ttk.Label(label_frame_modify, text = "Falla", style = "Etiqueta.TLabel")
		self.label_falla.grid(row = 2, column = 1, padx = 5, pady = 2, sticky = "w")

		self.entry_falla = ttk.Entry(label_frame_modify, state = "disabled", textvariable = self.falla)
		self.falla.set("Sants Patrons")
		self.entry_falla.grid(row = 3, column = 1, padx = 5, sticky = "w")

		self.button_modify = ttk.Button(label_frame_modify, state = "disabled", text = "Modificar historial", style = "Boto.TButton", command = self.modify_record)
		self.button_modify.grid(row = 2, column = 2, rowspan = 2, padx = 5, sticky = "s")

		# Paràmetres d'inici de la finestra.
		self.grab_set()
		self.transient(self.master)

	
	def display_member(self):
		
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
		
		index = self.combo_box_member.current()
		self.id.set(self.member_ids[index])
		self.member_ids = []
		self.fill_history(self.id.get())


	def fill_history(self, id):
		
		falla_obj = Falla()
		falla_obj.get_current_falla_year()
		result = Member.get_member(id)
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
		self.combo_box_member.set(member.surname + ", " + member.name)
		self.tree_record.delete(*self.tree_record.get_children())
		year = member.calculate_first_falla_year(member.birthdate)
		history_list = member.get_membership_history(member.id)
		sorted_history_list = sorted(history_list, key = lambda x: x[1])
		first_year_anoted = sorted_history_list[0][1]
		youth_years = year + 14 # Afegim 14 anys a l'any del primer exercici per a treure el primer any de cadet.
		while first_year_anoted > year:
			self.tree_record.insert("", "end", text = year, values = ("baixa", 0, 0, ""))
			year = year + 1
		score = 0
		childish_years = 0
		adult_years = 0
		for year_list in sorted_history_list:
			if (year_list[1] < youth_years) and (year_list[1] <= falla_obj.falla_year): # Calculem els anys d'infantil.
				position = year_list[2]
				falla = year_list[3]
				if position == "baixa":
					self.tree_record.insert("", "end", text = year_list[1], values = (position, 0, 0, ""))
				if position == "vocal":
					self.tree_record.insert("", "end", text = year_list[1], values = (position, 0, 1, falla))
					childish_years = childish_years + 1
				if position == "fallera major infantil" or position == "president infantil":
					self.tree_record.insert("", "end", text = year_list[1], values = (position, 0, 2, falla))
					childish_years = childish_years + 2
			elif year_list[1] <= falla_obj.falla_year: # Calculem els punts i anys d'adult.
				position = year_list[2]
				falla = year_list[3]
				if position == "baixa":
					self.tree_record.insert("", "end", text = year_list[1], values = (position, 0, 0, ""))
				if position == "vocal":
					if score >= 100:
						self.tree_record.insert("", "end", text = year_list[1], values = (position, 0, 1, falla))
						adult_years = adult_years + 1
					else:
						self.tree_record.insert("", "end", text = year_list[1], values = (position, 5, 0, falla))
						score = score + 5
				if position == "directiu" or position == "cort JLF":
					if score >= 100:
						self.tree_record.insert("", "end", text = year_list[1], values = (position, 0, 1, falla))
						adult_years = adult_years + 1
					else:
						self.tree_record.insert("", "end", text = year_list[1], values = (position, 8, 0, falla))
						score = score + 8
				if position == "fallera major" or position == "president":
					if score >= 100:
						self.tree_record.insert("", "end", text = year_list[1], values = (position, 0, 1, falla))
						adult_years = adult_years+1
					else:
						self.tree_record.insert("", "end", text = year_list[1], values = (position, 10, 0, falla))
						score = score + 10
				if position == "fallera major Alzira" or position == "president JLF":
					if score >= 100:
						self.tree_record.insert("", "end", text = year_list[1], values = (position, 0, 1, falla))
						adult_years = adult_years + 1
					else:
						self.tree_record.insert("", "end", text = year_list[1], values = (position, 12, 0, falla))
						score = score + 12
		# Omplim les dades finals calculades.
		self.childish.set(childish_years)
		self.score.set(score)
		self.adult.set(adult_years)
		# Fiquem en marxa els camps i botons per a poder modificar l'historial.
		self.entry_initial_year.config(state="normal")
		self.entry_final_year.config(state="normal")
		self.combo_box_position.config(state="readonly")
		self.entry_falla.config(state="normal")
		self.button_modify.config(state="normal")
		#bd.tancar_conexio()


	def modify_record(self):
		
		id = self.id.get()
		result = Member.get_member(id)
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
			initial_year = self.initial_year.get()
			final_year = self.final_year.get()
		except ValueError:
			messagebox.showwarning("Error", "Has d'escriure un any vàlid")
		else:
			position = self.combo_box_position.get()
			falla = self.falla.get()
			if final_year < initial_year:
				messagebox.showwarning("Error", "L'any inicial ha de ser menor o igual a l'any final")
			elif initial_year < member.calculate_first_falla_year(member.birthdate):
				messagebox.showwarning("Error", "L'any inicial ha de ser igual o superior a l'any del primer exercici")
			else:
				while initial_year <= final_year:
					member.modify_membership_history(id, position, falla, initial_year)
					initial_year = initial_year + 1
			self.fill_history(id)
		