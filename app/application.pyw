'''

DOBLET (APP D'ESCRIPTORI)

Programa de gestió de l'oficina de la Falla Sants Patrons d'Alzira.
Control de fallers, families, quotes, pagaments, rifes, loteries, historials, etc.

Desenvolupat per Ivan Mas Presentación 2020.

'''

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import platform
from PIL import Image, ImageTk
from pathlib import Path

from insert_member_window import InsertMemberWindow
from manage_member_window import ManageMemberWindow
from modify_record_window import ModifyRecordWindow
from modify_categories_window import ModifyCategoriesWindow
from show_report_window import ShowReportWindow
from manage_lottery_window import ManageLotteryWindow

from utils import Utils
from database import Database

from falla import Falla


class Application(tk.Frame):
	"""
	Aquesta classe representa l'aplicació principal de la interfície gràfica d'usuari.

	Atributs:
	---------
	master : tk.Tk
		La instància principal de l'aplicació.
	"""
		
		
	def __init__(self, master = None):
		"""
		Inicialitza una nova instància de la classe Aplicacio.

		Paràmetres:
		-----------
		master : tk.Tk, opcional
			La instància principal de l'aplicació. Si no es proporciona,
			es crearà una nova instància de tk.Tk().
		"""
		super().__init__(master) # Heretem de la classe Frame.
		self.master = master
		self.operating_system = platform.system()
		base_path = Path(__file__).parent.resolve()
		if self.operating_system == 'Windows':
			self.master.state('zoomed') # La finestra s'obri maximitzada.
			self.master.iconbitmap(base_path / 'images' / 'escut.ico')
		elif self.operating_system == 'Linux':
			self.master.attributes('-zoomed', True)
		self.master.title("Falla Sants Patrons")
		utils = Utils()
		utils.define_global_style()
		self.master.configure(bg = "#ffffff", pady = 5, padx = 5)
		
		# Barra de menú.
		self.menu_bar = tk.Menu() # Guardem el menú en una variable.
		self.master.config(menu = self.menu_bar) # Construïm el menú.

		# Submenú Inici.
		self.start_menu = tk.Menu(self.menu_bar, tearoff = 0) # Creem els elements i subelements.
		self.start_menu.add_command(label = "Nou exercici", command = self.new_falla_year)
		self.start_menu.add_command(label = "Modificar categories", command = self.modify_categories)
		self.start_menu.add_command(label = "Eixir", command = self.exit)

		# Submenú Faller.
		self.member_menu = tk.Menu(self.menu_bar, tearoff = 0)
		self.member_menu.add_command(label = "Introduir", command = self.insert_member)
		self.member_menu.add_command(label = "Gestionar", command = self.manage_member)
		
		# Submenú Historial.
		self.record_menu = tk.Menu(self.menu_bar, tearoff = 0)
		self.record_menu.add_command(label = "Modificar", command = self.modify_record)

		# Submenú Sortejos.
		self.lotteries_menu = tk.Menu(self.menu_bar, tearoff = 0)
		self.lotteries_menu.add_command(label = "Assignar rifa", command = self.assign_raffle)
		self.lotteries_menu.add_command(label = "Assignar loteria", command = self.assign_lottery)

		# Submenú Imprimir.
		self.print_menu = tk.Menu(self.menu_bar, tearoff = 0)
		self.print_menu.add_command(label = "Llistats", command = self.show_lists)

		# Submenú Ajuda.
		self.help_menu = tk.Menu(self.menu_bar, tearoff = 0)
		self.help_menu.add_command(label = "Info", command = self.info)

		# Afegim tots els submenús a la barra.
		self.menu_bar.add_cascade(label = "Inici", menu = self.start_menu)
		self.menu_bar.add_cascade(label = "Faller", menu = self.member_menu)
		self.menu_bar.add_cascade(label = "Historial", menu = self.record_menu)
		self.menu_bar.add_cascade(label = "Sortejos", menu = self.lotteries_menu)
		self.menu_bar.add_cascade(label = "Imprimir", menu = self.print_menu)
		self.menu_bar.add_cascade(label = "Ajuda", menu = self.help_menu)

		# Frames en els que dividim la finestra.
		label_frame_cover = tk.LabelFrame(self.master, borderwidth = 0, background = "#ffffff")
		label_frame_cover.grid(row = 0, column = 0, padx = 20, pady = 10, ipady = 2, rowspan = 3)
		
		label_style_start = ttk.Label(self.master, text = "Inici", style = "Title.TLabel")
		label_frame_start = ttk.LabelFrame(self.master, style = "BorderLine.TFrame", labelwidget = label_style_start)
		label_frame_start.grid(row = 0, column = 1, padx = 20, pady = 10, ipady = 2, sticky = "n")

		label_style_member = ttk.Label(self.master, text = "Faller", style = "Title.TLabel")
		label_frame_member = ttk.LabelFrame(self.master, style = "BorderLine.TFrame", labelwidget = label_style_member)
		label_frame_member.grid(row = 1, column = 1, padx = 20, pady = 10, ipady = 2, sticky = "n")

		label_style_record = ttk.Label(self.master, text = "Historial", style = "Title.TLabel")
		label_frame_record = ttk.LabelFrame(self.master, style = "BorderLine.TFrame", labelwidget = label_style_record)
		label_frame_record.grid(row = 2, column = 1, padx = 20, pady = 10, ipady = 2, sticky = "n")

		label_style_lotteries = ttk.Label(self.master, text = "Sortejos", style = "Title.TLabel")
		label_frame_lotteries = ttk.LabelFrame(self.master, style = "BorderLine.TFrame", labelwidget = label_style_lotteries)
		label_frame_lotteries.grid(row = 0, column = 2, padx = 20, pady = 10, ipady = 2, sticky = "n")

		label_style_print = ttk.Label(self.master, text = "Imprimir", style = "Title.TLabel")
		label_frame_print = ttk.LabelFrame(self.master, style = "BorderLine.TFrame", labelwidget = label_style_print)
		label_frame_print.grid(row = 1, column = 2, padx = 20, pady = 10, ipady = 2, sticky = "n")

		# Widgets per a cada frame.

		# Frame portada.
		self.label_first_word = ttk.Label(label_frame_cover, text = "Falla", style = "FrontPage.TLabel")
		self.label_first_word.grid(row = 0, column = 0, padx = 2)

		self.label_second_word = ttk.Label(label_frame_cover, text = "Sants", style = "FrontPage.TLabel")
		self.label_second_word.grid(row = 1, column = 0, padx = 2)

		self.label_third_word = ttk.Label(label_frame_cover, text = "Patrons", style = "FrontPage.TLabel")
		self.label_third_word.grid(row = 2, column = 0, padx = 2)

		logo = Image.open(base_path / 'images' / 'escut.jpg')
		self.image = ImageTk.PhotoImage(logo)
		self.label_image = tk.Label(label_frame_cover, image = self.image, borderwidth = 0)
		self.label_image.grid(row = 3, column = 0)

		# Frame Inici.
		self.button_new_falla_year = ttk.Button(label_frame_start, width = 20, text = "Nou exercici", style = "Button.TButton", command = self.new_falla_year)
		self.button_new_falla_year.grid(row = 0, column = 0, padx = 5, pady = 5)
		
		self.button_modify_categories = ttk.Button(label_frame_start, width = 20, text = "Modificar categories", style = "Button.TButton", command = self.modify_categories)
		self.button_modify_categories.grid(row = 1, column = 0, padx = 5, pady = 5)

		# Frame Faller.
		self.button_insert_member = ttk.Button(label_frame_member, width = 20, text = "Introduir faller", style = "Button.TButton", command = self.insert_member)
		self.button_insert_member.grid(row = 0, column = 0, padx = 5, pady = 5)

		self.button_manage_member = ttk.Button(label_frame_member, width = 20, text = "Gestionar faller", style = "Button.TButton", command = self.manage_member)
		self.button_manage_member.grid(row = 1, column = 0, padx = 5, pady = 5)

		# Frame Sortejos.
		self.button_raffle = ttk.Button(label_frame_lotteries, width = 20, text = "Assignar rifa", style = "Button.TButton", command = self.assign_raffle)
		self.button_raffle.grid(row = 0, column = 0, padx = 5, pady = 5)

		self.button_lottery = ttk.Button(label_frame_lotteries, width = 20, text = "Assignar loteria", style = "Button.TButton", command = self.assign_lottery)
		self.button_lottery.grid(row = 1, column = 0, padx = 5, pady = 5)

		# Frame Historial.
		self.button_modify_record = ttk.Button(label_frame_record, width = 20, text = "Modificar historial", style = "Button.TButton", command = self.modify_record)
		self.button_modify_record.grid(row = 0, column = 0, padx = 5, pady = 5)

		#Frame Imprimir.
		self.button_lists = ttk.Button(label_frame_print, width = 20, text = "Llistats", style = "Button.TButton", command = self.show_lists)
		self.button_lists.grid(row = 0, column = 0, padx = 5, pady = 5)

		'''
		Comprova si existeixen els arxius necessaris per a que funcione el programa i en cas de que falten, els crea.
		Si es crea algún arxiu, avisa a l'usuari de que ho ha fet per a que prenga les mesures necessàries.
		'''
		db = Database('sp')
		db.close_connection()
	
	
	def modify_categories(self):
		''' 
		Crea una nova instància de la classe FinestraCategories
		que obri la finestra "Modificar" del menú "Categoria".
		'''
		ModifyCategoriesWindow(self)
	
	
	def manage_member(self):
		''' 
		Crea una nova instància de la classe FinestraGestionar
		que obri la finestra "Gestionar" del menú "Faller".
		'''
		db = Database('sp')
		total_members = db.count_members()
		if total_members > 0:
			ManageMemberWindow(self)
		else:
			messagebox.showwarning("Avís", "Primer has de donar d'alta algun faller")


	def insert_member(self):
		''' 
		Crea una nova instància de la classe FinestraIntroduir
		que obri la finestra "Introduir" del menú "Faller".
		'''
		InsertMemberWindow(self)


	def assign_lottery(self):
		''' 
		Crea una nova instància de la classe FinestraLoteria
		que obri la finestra "Loteria" del menú "Loteries".
		'''

		ManageLotteryWindow(self)


	def assign_raffle(self):
		'''
		Crea una nova instància de la classe Falla per que assigne la rifa corresponent als fallers.
		'''
		falla = Falla()
		falla.assign_massive_raffle()


	def modify_record(self):
		''' 
		Crea una nova instància de la classe FinestraHistorial
		que obri la finestra "Modificar" del menú "Historial".
		'''
		ModifyRecordWindow(self)


	def show_lists(self):
		''' 
		Crea una nova instància de la classe FinestraLlistats
		que obri la finestra "Llistats" del menú "Imprimir".
		'''
		ShowReportWindow(self)
		

	def new_falla_year(self):
		'''
		Crea una nova instància de la classe Falla per a que cree un exercici nou.
		'''
		falla = Falla()
		falla.new_falla_year()

	
	def exit(self):
		'''
		Tanca la finestra principal de l'aplicació.
		'''
		value = messagebox.askquestion("Eixir", "Vols eixir de l'aplicació?")
		if value == "yes":
			database = Database('sp')
			database.create_backup_database("root", "hamuclaulo07", "sp")
			self.master.destroy()


	def info(self):
		'''
		Mostra una finestra emergent amb informació del programa.
		'''
		messagebox.showinfo("Informació", "Aplicació creada per Ivan Mas")


if __name__ == '__main__':
	'''
	Inicia l'aplicació.
	'''
	root = tk.Tk()
	app = Application(root)
	app.mainloop()