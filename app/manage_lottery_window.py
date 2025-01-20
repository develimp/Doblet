import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import platform
from pathlib import Path

from utils import Utils

from falla import Falla
from lottery import Lottery
from movement import Movement
from member import Member
from family import Family
from category import Category


class ManageLotteryWindow(tk.Toplevel):
	'''
	Esta classe representa una nova finestra que depén de la finestra principal.

	Atributs:
	---------
	master : tk.Tk o tk.Toplevel
		La instància principal de l'aplicació o de la finestra que crea esta nova finestra.
	'''

	def __init__(self, master = None):
		'''
		Inicialitza una nova instància de la classe ManageLotteryWindow.

		Parametres:
		-----------
		master : tk.Tk o tk.Toplevel, opcional
			La instància principal de l'aplicació o de la finestra que crea esta nova finestra.
			Si no es proporciona, es creará una nueva instancia de tk.Tk().
		'''
		super().__init__(master)
		self.master = master
		operating_system = platform.system()
		base_path = Path(__file__).parent.resolve()
		if operating_system == 'Windows':
			self.iconbitmap(base_path / 'images' / 'escut.ico')
		self.resizable(0,0)
		self.title("Loteria")
		utils = Utils()
		utils.define_global_style()
		self.configure(bg = "#ffffff", pady = 5, padx = 5)

		self.lottery_id = tk.IntVar()
		self.member_id = tk.IntVar()
		self.tickets_male = tk.IntVar()
		self.tickets_female = tk.IntVar()
		self.tickets_childish = tk.IntVar()
		self.tenths_male = tk.IntVar()
		self.tenths_female = tk.IntVar()
		self.tenths_childish = tk.IntVar()
		self.price = tk.DoubleVar()
		self.benefit = tk.DoubleVar()
		self.total = tk.DoubleVar()
		self.total_tickets_male = tk.IntVar()
		self.total_tickets_female = tk.IntVar()
		self.total_tickets_childish = tk.IntVar()
		self.total_tenths_male = tk.IntVar()
		self.total_tenths_female = tk.IntVar()
		self.total_tenths_childish = tk.IntVar()
		self.total_price = tk.DoubleVar()
		self.total_benefit = tk.DoubleVar()
		self.total_sum = tk.DoubleVar()

		self.member_ids = []

		label_style_introduce = ttk.Label(self, text = "Introduir, modificar o eliminar fila", style = "Title.TLabel")
		label_frame_introduce = ttk.LabelFrame(self, style = "BorderLine.TFrame", labelwidget = label_style_introduce)
		label_frame_introduce.grid(row = 0, column = 0, ipadx = 2, ipady = 2)

		label_style_totals = ttk.Label(self, text = "Totals", style = "Title.TLabel")
		label_frame_totals = ttk.LabelFrame(self, style = "BorderLine.TFrame", labelwidget = label_style_totals)
		label_frame_totals.grid(row = 2, column = 0, ipadx = 2, ipady = 2)

		label_style_lottery_name = ttk.Label(self, text = "Sorteig", style = "Title.TLabel")
		label_frame_lottery_name = ttk.LabelFrame(self, style = "BorderLine.TFrame", labelwidget = label_style_lottery_name)
		label_frame_lottery_name.grid(row = 3, column = 0, ipadx = 2, ipady = 2)

		# Widgets per a cada frame.

		# Frame "Introduir".
		self.label_lottery_id = ttk.Label(label_frame_introduce, text = "Id sorteig", style = "Label.TLabel")
		self.label_lottery_id.grid(row = 0, column = 0, padx = 2)

		self.label_name = ttk.Label(label_frame_introduce, text = "Nom", style = "Label.TLabel")
		self.label_name.grid(row = 0, column = 1, padx = 2)

		self.label_member_id = ttk.Label(label_frame_introduce, text = "Id", style = "Label.TLabel")
		self.label_member_id.grid(row = 0, column = 2, padx = 2)

		self.label_tickets_male = ttk.Label(label_frame_introduce, text = "Paperetes Masc", style = "Label.TLabel")
		self.label_tickets_male.grid(row = 0, column = 3, padx = 2)

		self.label_tickets_female = ttk.Label(label_frame_introduce, text = "Paperetes Fem", style = "Label.TLabel")
		self.label_tickets_female.grid(row = 0, column = 4, padx = 2)

		self.label_tickets_childish = ttk.Label(label_frame_introduce, text = "Paperetes Inf", style = "Label.TLabel")
		self.label_tickets_childish.grid(row = 0, column = 5, padx = 2)

		self.label_tenths_male = ttk.Label(label_frame_introduce, text = "Dècims Masc", style = "Label.TLabel")
		self.label_tenths_male.grid(row = 0, column = 6, padx = 2)

		self.label_tenths_female = ttk.Label(label_frame_introduce, text = "Dècims Fem", style = "Label.TLabel")
		self.label_tenths_female.grid(row = 0, column = 7, padx = 2)

		self.label_tenths_childish = ttk.Label(label_frame_introduce, text = "Dècims Inf", style = "Label.TLabel")
		self.label_tenths_childish.grid(row = 0, column = 8, padx = 2)

		self.entry_lottery_id = ttk.Entry(label_frame_introduce, textvariable = self.lottery_id)
		self.entry_lottery_id.grid(row = 1, column = 0, padx = 2)

		self.combo_box_member = ttk.Combobox(label_frame_introduce, width = 30, postcommand = self.display_member)
		self.combo_box_member.grid(row = 1, column = 1)
		self.combo_box_member.bind("<<ComboboxSelected>>", self.select_member)

		self.entry_member_id = ttk.Entry(label_frame_introduce, state = "disabled", textvariable = self.member_id)
		self.entry_member_id.grid(row = 1, column = 2, padx = 2)

		self.entry_tickets_male = ttk.Entry(label_frame_introduce, textvariable = self.tickets_male)
		self.entry_tickets_male.grid(row = 1, column = 3, padx = 2)
		self.entry_tickets_male.bind('<FocusOut>', self.calculate_totals)

		self.entry_tickets_female = ttk.Entry(label_frame_introduce, textvariable = self.tickets_female)
		self.entry_tickets_female.grid(row = 1, column = 4, padx = 2)
		self.entry_tickets_female.bind('<FocusOut>', self.calculate_totals)

		self.entry_tickets_childish = ttk.Entry(label_frame_introduce, textvariable = self.tickets_childish)
		self.entry_tickets_childish.grid(row = 1, column = 5, padx = 2)
		self.entry_tickets_childish.bind('<FocusOut>', self.calculate_totals)

		self.entry_tenths_male = ttk.Entry(label_frame_introduce, textvariable = self.tenths_male)
		self.entry_tenths_male.grid(row = 1, column = 6, padx = 2)
		self.entry_tenths_male.bind('<FocusOut>', self.calculate_totals)

		self.entry_tenths_female = ttk.Entry(label_frame_introduce, textvariable = self.tenths_female)
		self.entry_tenths_female.grid(row = 1, column = 7, padx = 2)
		self.entry_tenths_female.bind('<FocusOut>', self.calculate_totals)

		self.entry_tenths_childish = ttk.Entry(label_frame_introduce, textvariable = self.tenths_childish)
		self.entry_tenths_childish.grid(row = 1, column = 8, padx = 2)
		self.entry_tenths_childish.bind('<FocusOut>', self.calculate_totals)

		self.label_price = ttk.Label(label_frame_introduce, text = "Diners", style = "Label.TLabel")
		self.label_price.grid(row = 2, column = 0, padx = 2)

		self.entry_price = ttk.Entry(label_frame_introduce, state = "disabled", textvariable = self.price)
		self.entry_price.grid(row = 2, column = 1, padx = 2)

		self.label_benefit = ttk.Label(label_frame_introduce, text = "Benefici", style = "Label.TLabel")
		self.label_benefit.grid(row = 2, column = 2, padx = 2)

		self.entry_benefit = ttk.Entry(label_frame_introduce, state = "disabled", textvariable = self.benefit)
		self.entry_benefit.grid(row = 2, column = 3, padx = 2)

		self.label_total = ttk.Label(label_frame_introduce, text = "Total", style = "Label.TLabel")
		self.label_total.grid(row = 2, column = 4, padx = 2)

		self.entry_total = ttk.Entry(label_frame_introduce, state = "disabled", textvariable = self.total)
		self.entry_total.grid(row = 2, column = 5, padx = 2)

		self.button_add = ttk.Button(label_frame_introduce, style = "Button.TButton", text = "Afegir", command = self.add_field)
		self.button_add.grid(row = 2, column = 6, padx = 2, pady = 4)

		self.button_modify = ttk.Button(label_frame_introduce, style = "Button.TButton", state = "disabled", text = "Modificar", command = self.modify_row)
		self.button_modify.grid(row = 2, column = 7, padx = 2)

		self.button_delete = ttk.Button(label_frame_introduce, style = "Button.TButton", state = "disabled", text = "Eliminar fila", command = self.delete_row)
		self.button_delete.grid(row = 2, column = 8, padx = 2)

		self.tree_lottery = ttk.Treeview(self, height = 20)
		self.tree_lottery["columns"] = ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve")
		self.tree_lottery.column("#0", width = 40)
		self.tree_lottery.column("one", width = 160)
		self.tree_lottery.column("two", width = 80)
		self.tree_lottery.column("three", width = 80)
		self.tree_lottery.column("four", width = 80)
		self.tree_lottery.column("five", width = 80)
		self.tree_lottery.column("six", width = 80)
		self.tree_lottery.column("seven", width = 80)
		self.tree_lottery.column("eight", width = 80)
		self.tree_lottery.column("nine", width = 80)
		self.tree_lottery.column("ten", width = 80)
		self.tree_lottery.column("eleven", width = 80)
		self.tree_lottery.column("twelve", width = 80)
		self.tree_lottery.heading("#0", text = "id")
		self.tree_lottery.heading("one", text = "nom")
		self.tree_lottery.heading("two", text = "pap. masc.")
		self.tree_lottery.heading("three", text = "pap. fem.")
		self.tree_lottery.heading("four", text = "pap. inf.")
		self.tree_lottery.heading("five", text = "dèc. masc.")
		self.tree_lottery.heading("six", text = "dèc. fem.")
		self.tree_lottery.heading("seven", text = "dèc. inf.")
		self.tree_lottery.heading("eight", text = "diners")
		self.tree_lottery.heading("nine", text = "benefici")
		self.tree_lottery.heading("ten", text = "total")
		self.tree_lottery.heading("eleven", text = "assignada")
		self.tree_lottery.heading("twelve", text = "id faller")
		self.tree_lottery.grid(row = 1, column = 0, padx = 10, pady = 5)
		self.tree_lottery.bind("<<TreeviewSelect>>", self.select_row)

		self.scroll_lottery_table = ttk.Scrollbar(self, command = self.tree_lottery.yview)
		self.scroll_lottery_table.grid(row = 1, column = 1, sticky = "nsew")

		self.tree_lottery.config(yscrollcommand = self.scroll_lottery_table.set)

		# Frame "Totals".
		self.label_total_tickets_male = ttk.Label(label_frame_totals, text = "Paperetes Masc", style = "Label.TLabel")
		self.label_total_tickets_male.grid(row = 0, column = 0, padx = 2)

		self.label_total_tickets_female = ttk.Label(label_frame_totals, text = "Paperetes Fem", style = "Label.TLabel")
		self.label_total_tickets_female.grid(row = 0, column = 1, padx = 2)

		self.label_total_tickets_childish = ttk.Label(label_frame_totals, text = "Paperetes Inf", style = "Label.TLabel")
		self.label_total_tickets_childish.grid(row = 0, column = 2, padx = 2)

		self.label_total_tenths_male = ttk.Label(label_frame_totals, text = "Dècims Masc", style = "Label.TLabel")
		self.label_total_tenths_male.grid(row = 0, column = 3, padx = 2)

		self.label_total_tenths_female = ttk.Label(label_frame_totals, text = "Dècims Fem", style = "Label.TLabel")
		self.label_total_tenths_female.grid(row = 0, column = 4, padx = 2)

		self.label_total_tenths_childish = ttk.Label(label_frame_totals, text = "Dècims Inf", style = "Label.TLabel")
		self.label_total_tenths_childish.grid(row = 0, column = 5, padx = 2)

		self.label_price = ttk.Label(label_frame_totals, text = "Diners", style = "Label.TLabel")
		self.label_price.grid(row = 0, column = 6, padx = 2)

		self.label_benefits = ttk.Label(label_frame_totals, text = "Benefici", style = "Label.TLabel")
		self.label_benefits.grid(row = 0, column = 7, padx = 2)

		self.label_total = ttk.Label(label_frame_totals, text = "Total", style = "Label.TLabel")
		self.label_total.grid(row = 0, column = 8, padx = 2)

		self.entry_total_tickets_male = ttk.Entry(label_frame_totals, state = "disabled", textvariable = self.total_tickets_male)
		self.entry_total_tickets_male.grid(row = 1, column = 0, padx = 2)
		self.total_tickets_male.set("0")

		self.entry_total_tickets_female = ttk.Entry(label_frame_totals, state = "disabled", textvariable = self.total_tickets_female)
		self.entry_total_tickets_female.grid(row = 1, column = 1, padx = 2)
		self.total_tickets_female.set("0")

		self.entry_total_tickets_childish = ttk.Entry(label_frame_totals, state = "disabled", textvariable = self.total_tickets_childish)
		self.entry_total_tickets_childish.grid(row = 1, column = 2, padx = 2)
		self.total_tickets_childish.set("0")

		self.entry_total_tenths_male = ttk.Entry(label_frame_totals, state = "disabled", textvariable = self.total_tenths_male)
		self.entry_total_tenths_male.grid(row = 1, column = 3, padx = 2)
		self.total_tenths_male.set("0")

		self.entry_total_tenths_female = ttk.Entry(label_frame_totals, state = "disabled", textvariable = self.total_tenths_female)
		self.entry_total_tenths_female.grid(row = 1, column = 4, padx = 2)
		self.total_tenths_female.set("0")

		self.entry_total_tenths_childish = ttk.Entry(label_frame_totals, state = "disabled", textvariable = self.total_tenths_childish)
		self.entry_total_tenths_childish.grid(row = 1, column = 5, padx = 2)
		self.total_tenths_childish.set("0")

		self.entry_price = ttk.Entry(label_frame_totals, state = "disabled", textvariable = self.total_price)
		self.entry_price.grid(row = 1, column = 6, padx = 2)
		self.total_price.set("0.00")

		self.entry_benefit = ttk.Entry(label_frame_totals, state = "disabled", textvariable = self.total_benefit)
		self.entry_benefit.grid(row = 1, column = 7, padx = 2)
		self.total_benefit.set("0.00")

		self.entry_total_sum = ttk.Entry(label_frame_totals, state = "disabled", textvariable = self.total_sum)
		self.entry_total_sum.grid(row = 1, column = 8, padx = 2)
		self.total_sum.set("0.00")

		# Frame "Sorteig".
		self.combo_box_lottery_name = ttk.Combobox(label_frame_lottery_name, width = 30, postcommand = self.display_lotteries)
		self.combo_box_lottery_name.grid(row = 0, column = 0, padx = 5)

		self.button_open = ttk.Button(label_frame_lottery_name, style = "Button.TButton", text = "Obrir", command = self.open)
		self.button_open.grid(row = 0, column = 2, padx = 2)

		self.button_save = ttk.Button(label_frame_lottery_name, style = "Button.TButton", text = "Guardar", command = self.save)
		self.button_save.grid(row = 0, column = 3, padx = 2)

		self.button_assign = ttk.Button(label_frame_lottery_name, style = "Button.TButton", text = "Assignar", command = self.assign)
		self.button_assign.grid(row = 0, column = 4, padx = 2)

		self.button_clean_form = ttk.Button(label_frame_lottery_name, style = "Button.TButton", text = "Netejar", command = self.clean_form)
		self.button_clean_form.grid(row = 0, column = 5, padx = 2)

		self.grab_set()
		self.transient(self.master)



	def reset_fields(self):

		self.entry_lottery_id.focus()
		self.tickets_male.set("0")
		self.tickets_female.set("0")
		self.tickets_childish.set("0")
		self.tenths_male.set("0")
		self.tenths_female.set("0")
		self.tenths_childish.set("0")
		self.price.set("0.00")
		self.benefit.set("0.00")
		self.total.set("0.00")

	
	def display_member(self):
		'''
		Controla el combobox comparant la cadena escrita amb la base de dades i mostrant els resultats en el combobox.
		Utilitza l'atribut "self.member_ids" per a passar el identificador de faller a la funció "select_member".
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
		Controla la selecció del combobox per a guardar el identificador del faller i omplir les dades a partir d'aquest.
		'''
		index = self.combo_box_member.current()
		self.member_id.set(self.member_ids[index])
		self.member_ids = []
		self.fill_name(self.member_id.get())


	def fill_name(self, id):
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


	def calculate_totals(self, event):
		self.price.set((self.tickets_male.get()*4) + (self.tickets_female.get()*4) + (self.tickets_childish.get()*4) + 
				(self.tenths_male.get()*20) + (self.tenths_female.get()*20) + (self.tenths_childish.get()*20))
		self.benefit.set(self.tickets_male.get() + self.tickets_female.get() + self.tickets_childish.get() +
				(self.tenths_male.get()*3) + (self.tenths_female.get()*3) + (self.tenths_childish.get()*3))
		self.total.set(self.price.get() + self.benefit.get())


	def add_field(self):
		self.calculate_totals('<FocusOut>')
		if self.lottery_id.get() == "":
			messagebox.showwarning("Error", "El id del sorteig ha de contindre un valor vàlid")
		if self.member_id.get() == "":
			messagebox.showwarning("Error", "El camp nom ha de contindre un nom de faller vàlid")
		else:
			self.tree_lottery.insert("", "end", text = self.lottery_id.get(),
				values = (self.combo_box_member.get(), self.tickets_male.get(), self.tickets_female.get(), self.tickets_childish.get(),
			   	self.tenths_male.get(), self.tenths_female.get(), self.tenths_childish.get(),
				self.price.get(), self.benefit.get(), self.total.get(), 0, self.member_id.get()))
			
			self.total_tickets_male.set(self.total_tickets_male.get() + self.tickets_male.get())
			self.total_tickets_female.set(self.total_tickets_female.get() + self.tickets_female.get())
			self.total_tickets_childish.set(self.total_tickets_childish.get() + self.tickets_childish.get())
			self.total_tenths_male.set(self.total_tenths_male.get() + self.tenths_male.get())
			self.total_tenths_female.set(self.total_tenths_female.get() + self.tenths_female.get())
			self.total_tenths_childish.set(self.total_tenths_childish.get() + self.tenths_childish.get())
			self.total_price.set(self.total_price.get() + self.price.get())
			self.total_benefit.set(self.total_benefit.get() + self.benefit.get())
			self.total_sum.set(self.total_sum.get() + self.total.get())

			self.lottery_id.set("")
			self.member_id.set("")
			self.combo_box_member.set("")
			self.reset_fields()


	def select_row(self, event):
		row = self.tree_lottery.selection()
		if not row:
			return
		self.combo_box_member.config(state = "disabled")
		self.button_modify.config(state = "normal")
		self.button_delete.config(state = "normal")
		lottery_id = self.tree_lottery.item(row, option = "text")
		data_list = self.tree_lottery.item(row, option = "values")
		if data_list[10] == "1":
			messagebox.showwarning("Error", "No es pot seleccionar una fila que ja ha segut assignada")
		else:
			self.lottery_id.set(lottery_id)
			self.combo_box_member.set(data_list[0])
			self.member_id.set(data_list[11])
			self.tickets_male.set(data_list[1])
			self.tickets_female.set(data_list[2])
			self.tickets_childish.set(data_list[3])
			self.tenths_male.set(data_list[4])
			self.tenths_female.set(data_list[5])
			self.tenths_childish.set(data_list[6])
			self.calculate_totals('<FocusOut>')


	def modify_row(self):
		self.calculate_totals('<FocusOut>')
		row = self.tree_lottery.selection()
		lottery_id = self.tree_lottery.item(row, option = "text")
		data_list = self.tree_lottery.item(row, option = "values")
		lottery_name_year = self.combo_box_lottery_name.get().split()
		lottery_name = lottery_name_year[0]
		falla_year = lottery_name_year[1]
		if data_list[10] == "1":
			messagebox.showerror("Error", "No es pot modificar una fila de loteria ja assignada")
		else:
			self.total_tickets_male.set(self.total_tickets_male.get() - int(data_list[1]))
			self.total_tickets_female.set(self.total_tickets_female.get() - int(data_list[2]))
			self.total_tickets_childish.set(self.total_tickets_childish.get() - int(data_list[3]))
			self.total_tenths_male.set(self.total_tenths_male.get() - int(data_list[4]))
			self.total_tenths_female.set(self.total_tenths_female.get() - int(data_list[5]))
			self.total_tenths_childish.set(self.total_tenths_childish.get() - int(data_list[6]))
			self.total_price.set(self.total_price.get() - float(data_list[7]))
			self.total_benefit.set(self.total_benefit.get() - float(data_list[8]))
			self.total_sum.set(self.total_sum.get() - float(data_list[9]))

			self.tree_lottery.item(row, text = self.lottery_id.get(), values = (self.combo_box_member.get(),
				self.tickets_male.get(), self.tickets_female.get(), self.tickets_childish.get(),
				self.tenths_male.get(), self.tenths_female.get(), self.tenths_childish.get(),
				self.price.get(), self.benefit.get(), self.total.get(), 0, self.member_id.get()))
			
			self.total_tickets_male.set(self.total_tickets_male.get() + self.tickets_male.get())
			self.total_tickets_female.set(self.total_tickets_female.get() + self.tickets_female.get())
			self.total_tickets_childish.set(self.total_tickets_childish.get() + self.tickets_childish.get())
			self.total_tenths_male.set(self.total_tenths_male.get() + self.tenths_male.get())
			self.total_tenths_female.set(self.total_tenths_female.get() + self.tenths_female.get())
			self.total_tenths_childish.set(self.total_tenths_childish.get() + self.tenths_childish.get())
			self.total_price.set(self.total_price.get() + self.price.get())
			self.total_benefit.set(self.total_benefit.get() + self.benefit.get())
			self.total_sum.set(self.total_sum.get() + self.total.get())

			Lottery.modify_lottery(lottery_id, lottery_name, falla_year, self.tickets_male.get(), self.tickets_female.get(), self.tickets_childish.get(),
				self.tenths_male.get(), self.tenths_female.get(), self.tenths_childish.get(), data_list[11])
			
		self.lottery_id.set("")
		self.member_id.set("")
		self.combo_box_member.set("")
		self.combo_box_member.config(state="normal")
		self.button_modify.config(state="disabled")
		self.button_delete.config(state="disabled")
		self.reset_fields()
		self.tree_lottery.selection_remove(self.tree_lottery.selection())


	def delete_row(self):
		row = self.tree_lottery.selection()
		lottery_id = self.tree_lottery.item(row, option = "text")
		data_list = self.tree_lottery.item(row, option = "values")
		lottery_name_year = self.combo_box_lottery_name.get().split()
		lottery_name = lottery_name_year[0]
		falla_year = lottery_name_year[1]
		if data_list[10] == "1":
			messagebox.showerror("Error", "No es pot eliminar una fila de loteria ja assignada")
		else:
			self.total_tickets_male.set(self.total_tickets_male.get() - int(data_list[1]))
			self.total_tickets_female.set(self.total_tickets_female.get() - int(data_list[2]))
			self.total_tickets_childish.set(self.total_tickets_childish.get() - int(data_list[3]))
			self.total_tenths_male.set(self.total_tenths_male.get() - int(data_list[4]))
			self.total_tenths_female.set(self.total_tenths_female.get() - int(data_list[5]))
			self.total_tenths_childish.set(self.total_tenths_childish.get() - int(data_list[6]))
			self.total_price.set(self.total_price.get() - float(data_list[7]))
			self.total_benefit.set(self.total_benefit.get() - float(data_list[8]))
			self.total_sum.set(self.total_sum.get() - float(data_list[9]))

			self.tree_lottery.delete(row)

			Lottery.delete_lottery(lottery_id, lottery_name, falla_year)

		self.lottery_id.set("")
		self.member_id.set("")
		self.combo_box_member.set("")
		self.combo_box_member.config(state="normal")
		self.button_modify.config(state="disabled")
		self.button_delete.config(state="disabled")
		self.reset_fields()
		self.tree_lottery.selection_remove(self.tree_lottery.selection())


	def display_lotteries(self):
		falla = Falla()
		lotteries_list = falla.get_lotteries_list()
		self.combo_box_lottery_name["values"] = lotteries_list


	def open(self):
		lottery_name = self.combo_box_lottery_name.get().split()
		name = lottery_name[0]
		falla_year = lottery_name[1]
		value = messagebox.askquestion(
			"Obrir","Al obrir un sorteig nou en borrarà tot el panell. Estàs segur?"
		)
		if value == "yes":
			self.reset_fields()
			self.tree_lottery.delete(*self.tree_lottery.get_children())
			self.lottery_id.set("")
			self.member_id.set("")
			self.combo_box_member.config(state="normal")
			self.combo_box_member.set("")
			self.total_tickets_male.set("0")
			self.total_tickets_female.set("0")
			self.total_tickets_childish.set("0")
			self.total_tenths_male.set("0")
			self.total_tenths_female.set("0")
			self.total_tenths_childish.set("0")
			self.total_price.set("0.00")
			self.total_benefit.set("0.00")
			self.total_sum.set("0.00")
			falla = Falla()
			falla.get_lotteries(name, falla_year)
			total_tickets_male = 0
			total_tickets_female = 0
			total_tickets_childish = 0
			total_tenths_male = 0
			total_tenths_female = 0
			total_tenths_childish = 0
			total_price = 0.00
			total_benefit = 0.00
			total_sum = 0.00
			for lottery in falla.lotteries_list:
				total_tickets_male = total_tickets_male + lottery.tickets_male
				total_tickets_female = total_tickets_female + lottery.tickets_female
				total_tickets_childish = total_tickets_childish + lottery.tickets_childish
				total_tenths_male = total_tenths_male + lottery.tenths_male
				total_tenths_female = total_tenths_female + lottery.tenths_female
				total_tenths_childish = total_tenths_childish + lottery.tenths_childish
				total_price = total_price + float(lottery.price[0])
				total_benefit = total_benefit + float(lottery.benefit[0])
				total = float(lottery.price[0]) + float(lottery.benefit[0])
				total_sum = total_sum + total
				member_name = lottery.member.surname + ", " + lottery.member.name
				data_list = [member_name, lottery.tickets_male, lottery.tickets_female, lottery.tickets_childish, lottery.tenths_male, lottery.tenths_female, lottery.tenths_childish, lottery.price, lottery.benefit, total, lottery.assigned, lottery.member.id]
				self.tree_lottery.insert("", "end", text = lottery.lottery_id, values = data_list)
			self.total_tickets_male.set(total_tickets_male)
			self.total_tickets_female.set(total_tickets_female)
			self.total_tickets_childish.set(total_tickets_childish)
			self.total_tenths_male.set(total_tenths_male)
			self.total_tenths_female.set(total_tenths_female)
			self.total_tenths_childish.set(total_tenths_childish)
			self.total_price.set(total_price)
			self.total_benefit.set(total_benefit)
			self.total_sum.set(total_sum)


	def save(self):
		lottery_name_year = self.combo_box_lottery_name.get().split()
		lottery_name = lottery_name_year[0]
		falla_year = lottery_name_year[1]
		row_list = self.tree_lottery.get_children()
		for row in row_list:
			lottery_id = self.tree_lottery.item(row, option = "text")
			data_list = self.tree_lottery.item(row, option = "values")
			result = Member.get_member(data_list[11])
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
			Lottery.set_lottery(lottery_id, lottery_name, falla_year, data_list[1], data_list[2], data_list[3], data_list[4], data_list[5], data_list[6], data_list[10], member.id)


	def assign(self):
		value = messagebox.askquestion("Assignar", "Es guardaran tots els registres pendents i s'assignaran els diners i beneficis. L'operació no es pot desfer")
		if value == "yes":
			self.save()
			row_list = self.tree_lottery.get_children()
			falla = Falla()
			for row in row_list:
				lottery_id = self.tree_lottery.item(row, option = "text")
				data_list = self.tree_lottery.item(row, option = "values")
				lottery_name_year = self.combo_box_lottery_name.get().split()
				lottery_name = lottery_name_year[0]
				falla_year = lottery_name_year[1]
				if data_list[10] == "0":
					falla.assign_lottery(None, data_list[9], falla_year, data_list[11], "assignació loteria " + lottery_name + " " + falla_year)
					falla.pay_fee(None, data_list[8], falla_year, "benefici " + lottery_name + " " + falla_year, None, data_list[11])
					Lottery.assign_lottery(lottery_id, lottery_name, falla_year)
			self.button_assign.config(state="disabled")


	def clean_form(self):

		self.reset_fields()
		self.tree_lottery.delete(*self.tree_lottery.get_children())
		self.member_id.set("")
		self.combo_box_member.config(state="normal")
		self.combo_box_member.set("")
		self.total_tickets_male.set("0")
		self.total_tickets_female.set("0")
		self.total_tickets_childish.set("0")
		self.total_tenths_male.set(0)
		self.total_tenths_female.set(0)
		self.total_tenths_childish.set(0)
		self.total_price.set(0)
		self.total_benefit-set(0)
		self.total_sum.set(0)
		self.combo_box_lottery_name.set("")
		self.button_add.config(state="normal")
		self.button_assign.config(state="normal")