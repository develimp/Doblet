from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from tkinter import messagebox
import os
import errno
import os.path as path
import subprocess
import platform
import pickle
from pathlib import Path

from utils import Utils

from falla import Falla
from member import Member


class Report():

	def __init__(self):
		pass


	def assign_receipt_number(self):
		'''
		Busca a la carpeta "rebuts" quin és l'últim rebut creat
		i retorna el número següent.

		Retorna:
		--------
		index : int
			Número de rebut disponible per a ser assignat.
		'''
		base_path = Path(__file__).parent.resolve()
		try:
			os.mkdir(base_path / 'reports' / 'rebuts')
		except OSError as e:
			if e.errno != errno.EEXIST:
				raise

		index = 1
		file = base_path / 'reports' / 'rebuts' / (str(index) + ".pdf")
		while path.exists(file):
			index = index + 1
			file = base_path / 'reports' / 'rebuts' / (str(index) + ".pdf")
		return(index)


	def create_receipt(
			self,
			individualized,
			name,
			pay_fee,
			pay_lottery,
			pay_raffle,
			assigned_fee,
			payed_fee,
			assigned_lottery,
			payed_lottery,
			assigned_raffle,
			payed_raffle
		):
		'''
		Crea un .pdf amb la informació de pagament del faller en format rebut.

		Paràmetres:
		-----------
		individualized : boolean
			Indica si el pagament ha segut personal o familiar.
		name : string
			Nom complet del faller.
		pay_fee : float
			Quantitat pagada pel faller en concepte de quota
			en el moviment actual.
		pay_lottery : float
			Quantitat pagada pel faller en concepte de loteria
			en el moviment actual.
		pay_raffle : float
			Quantitat pagada pel faller en concepte de rifa
			en el moviment actual.
		assigned_fee : float
			Quantitat total assignada al faller en concepte de quota.
		payed_fee : float
			Quantitat total pagada pel faller en concepte de quota.
		assigned_lottery : float
			Quantitat total assignada al faller en concepte de loteria.
		payed_lottery : float
			Quantitat total pagada pel faller en concepte de loteria.
		assigned_raffle : float
			Quantitat total assignada al faller en concepte de rifa.
		payed_raffle : float
			Quantitat total pagada pel faller en concepte de rifa.
		'''
		base_path = Path(__file__).parent.resolve()
		utils = Utils()
		date = utils.calculate_current_date()
		current_date = date[0] + "-" + date[1] + "-" + date[2]

		total_pay = pay_fee + pay_lottery + pay_raffle

		fee_debt = float(assigned_fee) - float(payed_fee)
		lottery_debt = float(assigned_lottery) - float(payed_lottery)
		raffle_debt = float(assigned_raffle) - float(payed_raffle)

		total_assigned = float(assigned_fee) + \
			float(assigned_lottery) + float(assigned_raffle)
		total_payed = float(payed_fee) + \
			float(payed_lottery) + float(payed_raffle)
		total_debt = fee_debt + lottery_debt + raffle_debt

		try:
			os.mkdir(base_path / 'reports' / 'rebuts')
		except OSError as e:
			if e.errno != errno.EEXIST:
				raise

		index = self.assign_receipt_number()
		file = base_path / 'reports' / 'rebuts' / (str(index) + ".pdf")

		w, h = A4
		c = canvas.Canvas(str(file), pagesize = A4)

		c.line(0, h - (h / 3), w, h - (h / 3))
		c.line(0, h / 3, w, h / 3)
		c.drawString(w - 100, h - 30, current_date)

		c.drawString(
			50,
			h - 50,
			name + " abona la quantitat de " + \
				"{0:.2f}".format(total_pay) + " €"
		)
		c.drawString(
			70,
			h - 80,
			"{0:.2f}".format(pay_fee) + " € en concepte de quota"
		)
		c.drawString(
			70,
			h - 100,
			"{0:.2f}".format(pay_lottery) + " € en concepte de loteria"
		)
		c.drawString(
			70,
			h - 120,
			"{0:.2f}".format(pay_raffle) + " € en concepte de rifa"
		)

		if individualized == 0:
			c.drawString(50, h - 150, "RESUM DEL PENDENT DE PAGAMENT:")
		else:
			c.drawString(
				50,
				h - 150,
				"RESUM DEL PENDENT DE PAGAMENT DE LA FAMILIA COMPLETA:"
			)
		xlist = [50, 120, 190, 260, 330]
		ylist = [h - 165, h - 185, h - 205, h - 225, h - 245, h - 265]
		c.grid(xlist, ylist)
		c.drawString(130, h - 180, "Assignat")
		c.drawString(208, h - 180, "Pagat")
		c.drawString(272, h - 180, "Pendent")
		c.drawString(55, h - 200, "Quota:")
		c.drawString(130, h - 200, assigned_fee + " €")
		c.drawString(200, h - 200, payed_fee + " €")
		c.drawString(270, h - 200, "{0:.2f}".format(fee_debt) + " €")
		c.drawString(55, h - 220, "Loteria:")
		c.drawString(130, h - 220, assigned_lottery + " €")
		c.drawString(200, h - 220, payed_lottery + " €")
		c.drawString(270, h - 220, "{0:.2f}".format(lottery_debt) + " €")
		c.drawString(55, h - 240, "Rifa:")
		c.drawString(130, h - 240, assigned_raffle + " €")
		c.drawString(200, h - 240, payed_raffle + " €")
		c.drawString(270, h - 240, "{0:.2f}".format(raffle_debt) + " €")
		c.drawString(55, h - 260, "Totals:")
		c.drawString(130, h - 260, "{0:.2f}".format(total_assigned) + " €")
		c.drawString(200, h - 260, "{0:.2f}".format(total_payed) + " €")
		c.drawString(270, h - 260, "{0:.2f}".format(total_debt) + " €")
		c.drawImage(base_path / 'images' / 'escut.jpg', 360, h - 260, height = 150, width = 200)
		c.showPage()
		c.save()

		operating_system = platform.system()
		if operating_system == 'Windows':
			os.startfile(file)
		elif operating_system == 'Linux':
			subprocess.run(["xdg-open", str(file)])


	def movements_report(self, date, cash, bank):
		'''
		Crea un .pdf amb un llistat de tots els moviments
		de la data indicada segons el tipus de pagament.

		Paràmetres:
		-----------
		date : string
			Data en la que volem llistar els moviments.
		cash : boolean
			Marca si volem traure els moviments fets en efectiu.
		bank : boolean
			Marca si volem traure els moviments fets pel banc.
		'''
		falla = Falla()
		utils = Utils()
		base_path = Path(__file__).parent.resolve()
		mariadb_date = utils.convert_to_mariadb_date(date)
		page = 0		
		try:
			os.mkdir(base_path / 'reports' / 'moviments dia')
		except OSError as e:
			if e.errno != errno.EEXIST:
				raise
		file = base_path / 'reports' / 'moviments dia' / (date + ".pdf")

		w, h = A4
		c = canvas.Canvas(str(file), pagesize=A4)
		if cash == 1 and bank == 1:
			falla.get_daily_payments(mariadb_date, "pagat en caixa")
			falla.get_daily_payments(mariadb_date, "pagat pel banc")
		elif cash == 1 and bank == 0:
			falla.get_daily_payments(mariadb_date, "pagat en caixa")
		else:
			falla.get_daily_payments(mariadb_date, "pagat pel banc")
		i = 0
		total = 0
		c.drawString(50, h - 30, "FALLER")
		c.drawString(300, h - 30, "CONCEPTE")
		c.drawString(w - 100, h - 30, "QUANTITAT")
		for movement in falla.movements_list:
			c.drawString(
				50,
				h - i - 60,
				movement.member.name + " " + movement.member.surname
			)
			if movement.id_concept == 1:
				concept = "quota"
			if movement.id_concept == 2:
				concept = "loteria"
			if movement.id_concept == 3:
				concept = "rifa"
			c.drawString(300, h - i - 60, concept)
			c.drawString(
				w - 100,
				h - i - 60,
				"{0:.2f}".format(movement.amount) + " €"
			)
			i = i + 20
			total = total + movement.amount
			if i == 700:
				page = page + 1
				c.drawString(20, 20, "moviments del dia")
				c.drawString((w / 2) - 30, 20, "pàgina " + str(page))
				c.drawString(w - 80, 20, date)
				c.showPage()

				c.drawString(50, h - 30, "FALLER")
				c.drawString(300, h - 30, "CONCEPTE")
				c.drawString(w - 100, h - 30, "QUANTITAT")
				i = 0
		c.drawString(300, h - i - 80, "TOTAL")
		c.drawString(w - 100, h - i - 80, "{0:.2f}".format(total) + " €")
		c.drawString(20, 20, "moviments del dia")
		c.drawString((w / 2) - 30, 20, "pàgina " + str(page + 1))
		c.drawString(w - 80, 20, date)
		c.showPage()
		c.save()

		operating_system = platform.system()
		if operating_system == 'Windows':
			os.startfile(file)
		elif operating_system == 'Linux':
			subprocess.run(["xdg-open", str(file)])


	def general_report(self):
		'''
		Crea un .pdf amb un llistat amb l'estat actual de comptes
		de tots els fallers actius i, en conseqüència, de la falla al complet.
		'''
		utils = Utils()
		base_path = Path(__file__).parent.resolve()
		date = utils.calculate_current_date()
		current_date = date[0] + "-" + date[1] + "-" + date[2]
		falla = Falla()
		falla.get_current_falla_year()
		falla.get_members("is_registered", 1)
		assigned_fee_sum = 0
		payed_fee_sum = 0
		assigned_lottery_sum = 0
		payed_lottery_sum = 0
		assigned_raffle_sum = 0
		payed_raffle_sum = 0
		page = 0

		try:
			os.mkdir(base_path / 'reports' / 'llistat general')
		except OSError as e:
			if e.errno != errno.EEXIST:
				raise
		file = base_path / 'reports' / 'llistat general' / (current_date + ".pdf")

		w, h = A4
		c = canvas.Canvas(str(file), pagesize = landscape(A4))
		c.setFont("Helvetica", 11)
		i = 0
		total_members = 0
		c.drawString(20, w - 30, "ID")
		c.drawString(50, w - 30, "FALLER")
		c.drawRightString(295, w - 30, "QUOTA A.")
		c.drawRightString(365, w - 30, "QUOTA P.")
		c.drawRightString(435, w - 30, "LOTER. A.")
		c.drawRightString(505, w - 30, "LOTER. P.")
		c.drawRightString(565, w - 30, "RIFA A.")
		c.drawRightString(625, w - 30, "RIFA P.")
		c.drawRightString(695, w - 30, "TOTAL A.")
		c.drawRightString(765, w - 30, "TOTAL P.")
		c.drawRightString(835, w - 30, "DIFERÈNC.")
		c.line(0, w - 35, h, w - 35)
		for member in falla.members_list:
			assigned_fee = 0
			payed_fee = 0
			assigned_lottery = 0
			payed_lottery = 0
			assigned_raffle = 0
			payed_raffle = 0
			c.drawString(20, w - i - 60, str(member.id))
			c.drawString(50, w - i - 60, member.surname + ", " + member.name)
			balance = falla.get_balance(member.id)
			assigned_fee = assigned_fee + balance[0]
			payed_fee = payed_fee + balance[1]
			assigned_lottery = assigned_lottery + balance[2]
			payed_lottery = payed_lottery + balance[3]
			assigned_raffle = assigned_raffle + balance[4]
			payed_raffle = payed_raffle + balance[5]
			total_assigned = assigned_fee + assigned_lottery + assigned_raffle
			total_payed = payed_fee + payed_lottery + payed_raffle
			c.drawRightString(
				295,
				w - i - 60,
				"{0:.2f}".format(assigned_fee) + " €"
			)
			assigned_fee_sum = assigned_fee_sum + assigned_fee
			c.drawRightString(
				365,
				w - i - 60,
				"{0:.2f}".format(payed_fee) + " €"
			)
			payed_fee_sum = payed_fee_sum + payed_fee
			c.drawRightString(
				435,
				w - i - 60,
				"{0:.2f}".format(assigned_lottery) + " €"
			)
			assigned_lottery_sum = assigned_lottery_sum + assigned_lottery
			c.drawRightString(
				505,
				w - i - 60,
				"{0:.2f}".format(payed_lottery) + " €"
			)
			payed_lottery_sum = payed_lottery_sum + payed_lottery
			c.drawRightString(
				565,
				w - i - 60,
				"{0:.2f}".format(assigned_raffle) + " €"
			)
			assigned_raffle_sum = assigned_raffle_sum + assigned_raffle
			c.drawRightString(
				625,
				w - i - 60,
				"{0:.2f}".format(payed_raffle) + " €"
			)
			payed_raffle_sum = payed_raffle_sum + payed_raffle
			c.drawRightString(
				695,
				w - i - 60,
				"{0:.2f}".format(total_assigned) + " €"
			)
			c.drawRightString(
				765,
				w - i - 60,
				"{0:.2f}".format(total_payed) + " €"
			)
			c.drawRightString(
				835,
				w - i - 60,
				"{0:.2f}".format(total_assigned - total_payed) + " €"
			)
			i = i + 20
			total_members = total_members + 1
			if i == 500:
				page = page + 1
				c.drawString(20, 20, "llistat general")
				c.drawString(( h/2 ) - 30, 20, "pàgina " + str(page))
				c.drawString(h - 80, 20, current_date)
				c.showPage()

				c.setFont("Helvetica", 11)
				c.drawString(20, w - 30, "ID")
				c.drawString(50, w - 30, "FALLER")
				c.drawRightString(295, w - 30, "QUOTA A.")
				c.drawRightString(365, w - 30, "QUOTA P.")
				c.drawRightString(435, w - 30, "LOTER. A.")
				c.drawRightString(505, w - 30, "LOTER. P.")
				c.drawRightString(565, w - 30, "RIFA A.")
				c.drawRightString(625, w - 30, "RIFA P.")
				c.drawRightString(695, w - 30, "TOTAL A.")
				c.drawRightString(765, w - 30, "TOTAL P.")
				c.drawRightString(835, w - 30, "DIFERÈNC.")
				c.line(0, w - 35, h, w - 35)
				i = 0
		c.line(0, w - i - 60, h, w - i - 60)
		c.drawRightString(50, w - i - 80, "TOTALS")
		c.drawRightString(200, w - i - 80, "FALLERS = " + str(total_members))
		c.drawRightString(
			295,
			w - i - 80,
			"{0:.2f}".format(assigned_fee_sum) + " €"
		)
		c.drawRightString(
			365,
			w - i - 80,
			"{0:.2f}".format(payed_fee_sum) + " €"
		)
		c.drawRightString(
			435,
			w - i - 80,
			"{0:.2f}".format(assigned_lottery_sum) + " €"
		)
		c.drawRightString(
			505,
			w - i - 80,
			"{0:.2f}".format(payed_lottery_sum) + " €"
		)
		c.drawRightString(
			565,
			w - i - 80,
			"{0:.2f}".format(assigned_raffle_sum) + " €"
		)
		c.drawRightString(
			625,
			w - i - 80,
			"{0:.2f}".format(payed_raffle_sum) + " €"
		)
		total_assignments = assigned_fee_sum + \
			assigned_lottery_sum + assigned_raffle_sum
		c.drawRightString(
			695,
			w - i - 80,
			"{0:.2f}".format(total_assignments) + " €"
		)
		total_payments = payed_fee_sum + payed_lottery_sum + payed_raffle_sum
		c.drawRightString(
			765,
			w - i - 80,
			"{0:.2f}".format(total_payments) + " €"
		)
		c.drawRightString(
			835,
			w - i - 80,
			"{0:.2f}".format(total_assignments-total_payments) + " €"
		)
		page = page + 1
		c.drawString(20, 20, "llistat general")
		c.drawString((h / 2) - 30, 20, "pàgina " + str(page))
		c.drawString(h - 80, 20, current_date)
		c.showPage()
		c.save()

		operating_system = platform.system()
		if operating_system == 'Windows':
			os.startfile(file)
		elif operating_system == 'Linux':
			subprocess.run(["xdg-open", str(file)])


	def general_report_by_families(self):
		'''
		Crea un .pdf amb un llistat amb l'estat actual de comptes
		de tots els fallers actius organitzats per famílies.
		'''
		utils = Utils()
		base_path = Path(__file__).parent.resolve()
		date = utils.calculate_current_date()
		current_date = date[0] + "-" + date[1] + "-" + date[2]
		falla = Falla()
		falla.get_current_falla_year()
		falla.get_families()
		total_assignments = 0
		total_payments = 0
		page = 0

		try:
			os.mkdir(base_path / 'reports' / 'llistat general familiar')
		except OSError as e:
			if e.errno != errno.EEXIST:
				raise
		file = base_path / 'reports' / 'llistat general familiar' / (current_date + ".pdf")

		w, h = A4
		c = canvas.Canvas(str(file), pagesize = landscape(A4))
		c.setFont("Helvetica", 11)
		i = 0
		total_families = 0
		c.drawRightString(70, w - 30, "MEMBRES")
		c.drawString(100, w - 30, "FAMILIAR REFERENT")
		c.drawString(300, w - 30, "ADREÇA")
		c.drawRightString(590, w - 30, "TOTAL ASSIGNACIONS")
		c.drawRightString(715, w - 30, "TOTAL PAGAMENTS")
		c.drawRightString(810, w - 30, "DIFERÈNCIA")
		c.line(0, w - 35, h, w - 35)
		head_family_list = []
		for family in falla.families_list:
			head_family_list.clear()
			total_family_assigned = 0
			total_family_payed = 0
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
				if family_member.is_registered == 1:
					family.members_list.append(family_member)
			for member in family.members_list:
				assigned_fee = 0
				payed_fee = 0
				assigned_lottery = 0
				payed_lottery = 0
				assigned_raffle = 0
				payed_raffle = 0
				head_family_list.append(member)
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
				total_assigned = assigned_fee + \
					assigned_lottery + assigned_raffle
				total_payed = payed_fee + payed_lottery + payed_raffle
				total_family_assigned = total_family_assigned + total_assigned
				total_family_payed = total_family_payed + total_payed
			if len(head_family_list) > 0:
				member = head_family_list[0]
				c.drawRightString(50, w - i - 60, str(len(head_family_list)))
				c.drawString(
					100,
					w - i - 60,
					member.surname + ", " + member.name
				)
				c.drawString(275, w - i - 60, member.address)
				c.drawRightString(
					550,
					w - i - 60,
					"{0:.2f}".format(total_family_assigned) + " €"
				)
				total_assignments = total_assignments + total_family_assigned
				c.drawRightString(
					675,
					w - i - 60,
					"{0:.2f}".format(total_family_payed) + " €"
				)
				total_payments = total_payments + total_family_payed
				c.drawRightString(
					800,
					w - i - 60,
					"{0:.2f}".format(
						total_family_assigned - total_family_payed
					) + " €"
				)
				i = i + 20
			total_families = total_families + 1
			if i == 500:
				page = page + 1
				c.drawString(20, 20, "llistat general familiar")
				c.drawString((h / 2) - 30, 20, "pàgina " + str(page))
				c.drawString(h - 80, 20, current_date)
				c.showPage()
				c.setFont("Helvetica", 11)
				c.drawRightString(70, w - 30, "MEMBRES")
				c.drawString(100, w - 30, "FAMILIAR REFERENT")
				c.drawString(300, w - 30, "ADREÇA")
				c.drawRightString(590, w - 30, "TOTAL ASSIGNACIONS")
				c.drawRightString(715, w - 30, "TOTAL PAGAMENTS")
				c.drawRightString(810, w - 30, "DIFERÈNCIA.")
				c.line(0, w - 35, h, w - 35)
				i = 0
		c.line(0, w - i - 60, h, w - i - 60)
		c.drawRightString(50, w - i - 80, "TOTALS")
		c.drawRightString(200, w - i -80, "FAMILIES = " + str(total_families))
		c.drawRightString(
			450,
			w - i - 80,
			"{0:.2f}".format(total_assignments) + " €"
		)
		c.drawRightString(
			625,
			w - i - 80,
			"{0:.2f}".format(total_payments) + " €"
		)
		c.drawRightString(
			800,
			w - i - 80,
			"{0:.2f}".format(total_assignments-total_payments) + " €"
		)
		page = page + 1
		c.drawString(20, 20, "llistat general familiar")
		c.drawString((h / 2) - 30, 20, "pàgina " + str(page))
		c.drawString(h - 80, 20, current_date)
		c.showPage()
		c.save()

		operating_system = platform.system()
		if operating_system == 'Windows':
			os.startfile(file)
		elif operating_system == 'Linux':
			subprocess.run(["xdg-open", str(file)])


	def inactive_members_fees_report(self):
		'''
		Crea un .pdf amb un llistat dels fallers que s'han donat de baixa
		però han aportat quotes mentre han segut fallers.
		'''
		utils = Utils()
		base_path = Path(__file__).parent.resolve()
		date = utils.calculate_current_date()
		current_date = date[0] + "-" + date[1] + "-" + date[2]
		falla = Falla()
		falla.get_current_falla_year()
		falla.get_members("is_registered", 0)
		payed_fee_sum = 0
		page = 0

		try:
			os.mkdir(base_path / 'reports' / 'llistat quotes no fallers')
		except OSError as e:
			if e.errno != errno.EEXIST:
				raise
		file = base_path / 'reports' / 'llistat quotes no fallers' / (current_date + ".pdf")

		w, h = A4
		c = canvas.Canvas(str(file), pagesize = A4)
		c.setFont("Helvetica", 11)
		i = 0
		total_members = 0
		c.drawString(20, h - 30, "ID")
		c.drawString(50, h - 30, "FALLER")
		c.drawString(295, h - 30, "QUOTA PAGADA")
		c.line(0, h - 35, w, h - 35)
		for member in falla.members_list:
			payed_fee = 0
			payed_fee = payed_fee + falla.calculate_payed_fee(
					member.id, falla.falla_year
				)
			if payed_fee > 0:
				c.drawString(20, h - i - 60, str(member.id))
				c.drawString(
					50,
					h - i - 60,
					member.surname + ", " + member.name
				)
				c.drawString(
					295,
					h - i - 60,
					"{0:.2f}".format(payed_fee) + " €"
				)
				payed_fee_sum = payed_fee_sum + payed_fee
				i = i + 20
				total_members = total_members + 1
			if i == 700:
				page = page + 1
				c.drawString(20, 20, "llistat quotes no fallers")
				c.drawString((w / 2) - 30, 20, "pàgina " + str(page))
				c.drawString(w - 80, 20, current_date)
				c.showPage()
				c.setFont("Helvetica", 11)
				c.drawString(20, h - 30, "ID")
				c.drawString(50, h - 30, "FALLER")
				c.drawString(295, h - 30, "QUOTA PAGADA")
				c.line(0, h - 35, w, h - 35)
				i = 0
		c.line(0, h - i - 60, w, h - i - 60)
		c.drawRightString(50, h - i - 80, "TOTALS")
		c.drawRightString(200, h - i - 80, "FALLERS = " + str(total_members))
		c.drawString(295, h - i - 80, "{0:.2f}".format(payed_fee_sum) + " €")
		page = page + 1
		c.drawString(20, 20, "llistat quotes no fallers")
		c.drawString((w / 2) - 30, 20, "pàgina " + str(page))
		c.drawString(w - 80, 20, current_date)
		c.showPage()
		c.save()

		operating_system = platform.system()
		if operating_system == 'Windows':
			os.startfile(file)
		elif operating_system == 'Linux':
			subprocess.run(["xdg-open", str(file)])


	def members_with_raffle_list(self):
		'''
		Crea un .pdf amb un llistat dels fallers amb obligació de rifa.
		'''
		utils = Utils()
		base_path = Path(__file__).parent.resolve()
		date = utils.calculate_current_date()
		current_date = date[0] + "-" + date[1] + "-" + date[2]
		falla = Falla()
		falla.get_members("adult")
		page = 0

		try:
			os.mkdir(base_path / 'reports' / 'llistat rifes')
		except OSError as e:
			if e.errno != errno.EEXIST:
				raise
		file = base_path / 'reports' / 'llistat rifes' / (current_date + ".pdf")

		w, h = A4
		c = canvas.Canvas(str(file), pagesize = A4)
		c.drawString(20, h - 30, "ID")
		c.drawString(50, h - 30, "FALLER")
		c.drawString(300, h - 30, "ID")
		c.drawString(330, h - 30, "FALLER")
		c.line(0, h - 35, w, h - 35)
		row = 0
		column = 0
		for member in falla.members_list:
			if row < 34 and column == 0:
				c.drawString(20, h - (row * 20) - 60, str(member.id))
				c.drawString(
					50,
					h - (row * 20) - 60,
					member.surname + ", " + member.name
				)
				row = row + 1
			elif row == 34 and column == 0:
				c.drawString(20, h - (row * 20) - 60, str(member.id))
				c.drawString(
					50,
					h - (row * 20) - 60,
					member.surname + ", " + member.name
				)
				column = 1
				row = 0
			elif row < 34 and column == 1:
				c.drawString(300, h - (row * 20) - 60, str(member.id))
				c.drawString(
					330,
					h - (row * 20) - 60,
					member.surname + ", " + member.name
				)
				row = row + 1
			elif row == 34 and column == 1:
				c.drawString(300, h - (row * 20) - 60, str(member.id))
				c.drawString(
					330,
					h - (row * 20) - 60,
					member.surname + ", " + member.name
				)
				page = page + 1
				c.drawString(20, 20, "llistat rifes")
				c.drawString((w / 2) - 30, 20, "pàgina " + str(page))
				c.drawString(w - 80, 20, current_date)
				c.showPage()
				c.drawString(20, h - 30, "ID")
				c.drawString(50, h - 30, "FALLER")
				c.drawString(300, h - 30, "ID")
				c.drawString(330, h - 30, "FALLER")
				c.line(0, h - 35, w, h - 35)
				column = 0
				row = 0
		page = page + 1
		c.drawString(20, 20, "llistat rifes")
		c.drawString((w / 2) - 30, 20, "pàgina " + str(page))
		c.drawString(w - 80, 20, current_date)
		c.showPage()
		c.save()

		operating_system = platform.system()
		if operating_system == 'Windows':
			os.startfile(file)
		elif operating_system == 'Linux':
			subprocess.run(["xdg-open", str(file)])
		

	def members_list(self, data_list):
		'''
		Crea un .pdf amb el llistat de dades dels fallers actius.

		Paràmetres:
		-----------
		data_list : list
			Llistat de dades a mostrar a l'informe.
		'''
		utils = Utils()
		base_path = Path(__file__).parent.resolve()
		date = utils.calculate_current_date()
		current_date = date[0] + "-" + date[1] + "-" + date[2]
		falla = Falla()
		falla.get_current_falla_year()
		falla.get_members("is_registered", 1)
		page = 0

		try:
			os.mkdir(base_path / 'reports' / 'llistat fallers')
		except OSError as e:
			if e.errno != errno.EEXIST:
				raise
		file = base_path / 'reports' / 'llistat fallers' / (current_date + ".pdf")

		w, h = A4
		c = canvas.Canvas(str(file), pagesize = landscape(A4))
		i = 0
		j = 20
		c.drawString(j, w - 30, "ID")
		j = j + 30
		if "nom" in data_list:
			c.drawString(j, w - 30, "FALLER")
			j = j + 200
		if "dni" in data_list:
			c.drawString(j, w - 30, "DNI")
			j = j + 75
		if "adreça" in data_list:
			c.drawString(j, w - 30, "ADREÇA")
			j = j + 250
		if "telefon" in data_list:
			c.drawString(j, w - 30, "TELÈFON")
			j = j + 75
		if "naixement" in data_list:
			c.drawString(j, w - 30, "NAIXEMENT")
			j = j + 75
		if "correu" in data_list:
			c.drawString(j, w - 30, "E-MAIL")
		c.line(0, w - 35, h, w - 35)
		for member in falla.members_list:
			j = 20
			c.drawString(j, w - i - 60, str(member.id))
			j = j + 30
			if "nom" in data_list:
				c.drawString(
					j,
					w - i - 60,
					member.surname + ", " + member.name
				)
				j = j + 200
			if "dni" in data_list:
				c.drawString(j, w - i - 60, member.dni)
				j = j + 75
			if "adreça" in data_list:
				c.drawString(j, w - i - 60, member.address)
				j = j + 250
			if "telefon" in data_list:
				c.drawString(j, w - i - 60, member.phone_number)
				j = j + 75
			if "naixement" in data_list:
				spanish_birthdate = utils.convert_to_spanish_date(
					member.birthdate
				)
				c.drawString(j, w - i - 60, spanish_birthdate)
				j = j + 75
			if "correu" in data_list:
				c.drawString(j, w - i - 60, member.email)
			i = i + 20
			if i == 500:
				page = page + 1
				c.drawString(20, 20, "llistat de fallers")
				c.drawString((h / 2) - 30, 20, "pàgina " + str(page))
				c.drawString(h - 80, 20, current_date)
				c.showPage()

				j = 20
				c.drawString(j, w - 30, "ID")
				j = j + 30
				if "nom" in data_list:
					c.drawString(j, w - 30, "FALLER")
					j = j + 200
				if "dni" in data_list:
					c.drawString(j, w - 30, "DNI")
					j = j + 75
				if "adreça" in data_list:
					c.drawString(j, w - 30, "ADREÇA")
					j = j + 250
				if "telefon" in data_list:
					c.drawString(j, w - 30, "TELÈFON")
					j = j + 75
				if "naixement" in data_list:
					c.drawString(j, w - 30, "NAIXEMENT")
					j = j + 75
				if "correu" in data_list:
					c.drawString(j, w - 30, "E-MAIL")
				c.line(0, w - 35, h, w - 35)
				i = 0
		page = page + 1
		c.drawString(20, 20, "llistat de fallers")
		c.drawString((h / 2) - 30, 20, "pàgina " + str(page))
		c.drawString(h-80, 20, current_date)
		c.showPage()
		c.save()

		operating_system = platform.system()
		if operating_system == 'Windows':
			os.startfile(file)
		elif operating_system == 'Linux':
			subprocess.run(["xdg-open", str(file)])


	def reduced_members_list(self, data_list):
		'''
		Crea un .pdf amb el llistat de dades dels fallers actius.

		Paràmetres:
		-----------
		data_list : list
			Llistat de dades a mostrar a l'informe.
		'''
		utils = Utils()
		base_path = Path(__file__).parent.resolve()
		date = utils.calculate_current_date()
		current_date = date[0] + "-" + date[1] + "-" + date[2]
		falla = Falla()
		falla.get_current_falla_year()
		falla.get_members("is_registered", 1)
		page = 0

		try:
			os.mkdir(base_path / 'reports' / 'llistat fallers')
		except OSError as e:
			if e.errno != errno.EEXIST:
				raise
		file = base_path / 'reports' / 'llistat fallers' / (current_date + ".pdf")

		w, h = A4
		c = canvas.Canvas(str(file), pagesize = A4)
		i = 0
		j = 20
		c.drawString(j, h - 30, "ID")
		j = j + 30
		if "nom" in data_list:
			c.drawString(j, h - 30, "FALLER")
			j = j + 200
		if "dni" in data_list:
			c.drawString(j, h - 30, "DNI")
			j = j + 75
		if "adreça" in data_list:
			c.drawString(j, h - 30, "ADREÇA")
			j = j + 250
		if "telefon" in data_list:
			c.drawString(j, h - 30, "TELÈFON")
			j = j + 75
		if "naixement" in data_list:
			c.drawString(j, h - 30, "NAIXEMENT")
			j = j + 75
		if "correu" in data_list:
			c.drawString(j, h - 30, "E-MAIL")
		c.line(0, h - 35, w, h - 35)
		for member in falla.members_list:
			j = 20
			c.drawString(j, h - i - 60, str(member.id))
			j = j + 30
			if "nom" in data_list:
				c.drawString(
					j,
					h - i - 60,
					member.surname + ", " + member.name
				)
				j = j + 200
			if "dni" in data_list:
				c.drawString(j, h - i - 60, member.dni)
				j = j + 75
			if "adreça" in data_list:
				c.drawString(j, h - i - 60, member.address)
				j = j + 250
			if "telefon" in data_list:
				c.drawString(j, h - i - 60, member.phone_number)
				j = j + 75
			if "naixement" in data_list:
				spanish_birthdate = utils.convert_to_spanish_date(
					member.birthdate
				)
				c.drawString(j, h - i - 60, spanish_birthdate)
				j = j + 75
			if "correu" in data_list:
				c.drawString(j, h - i - 60, member.email)
			i = i + 20
			if i == 700:
				page = page + 1
				c.drawString(20, 20, "llistat de fallers")
				c.drawString((w / 2) - 30, 20, "pàgina " + str(page))
				c.drawString(w - 80, 20, current_date)
				c.showPage()

				j = 20
				c.drawString(j, h - 30, "ID")
				j = j + 30
				if "nom" in data_list:
					c.drawString(j, h - 30, "FALLER")
					j = j + 200
				if "dni" in data_list:
					c.drawString(j, h - 30, "DNI")
					j = j + 75
				if "adreça" in data_list:
					c.drawString(j, h - 30, "ADREÇA")
					j = j + 250
				if "telefon" in data_list:
					c.drawString(j, h - 30, "TELÈFON")
					j = j + 75
				if "naixement" in data_list:
					c.drawString(j, h-30, "NAIXEMENT")
					j = j + 75
				if "correu" in data_list:
					c.drawString(j, h - 30, "E-MAIL")
				c.line(0, h - 35, w, h - 35)
				i = 0
		page = page + 1
		c.drawString(20, 20, "llistat de fallers")
		c.drawString((w / 2) - 30, 20, "pàgina " + str(page))
		c.drawString(w - 80, 20, current_date)
		c.showPage()
		c.save()

		operating_system = platform.system()
		if operating_system == 'Windows':
			os.startfile(file)
		elif operating_system == 'Linux':
			subprocess.run(["xdg-open", str(file)])


	def members_list_by_categories(self, categories_list, data_list):
		'''
		Crea un .pdf amb el llistat de dades dels fallers actius
		de les categories passades.

		Paràmetres:
		-----------
		categories_list : list
			Llistat de categories per a les quals volem treure el llistat.
		data_list : list
			Llistat de dades a mostrar a l'informe.
		'''
		utils = Utils()
		base_path = Path(__file__).parent.resolve()
		date = utils.calculate_current_date()
		current_date = date[0] + "-" + date[1] + "-" + date[2]
		falla = Falla()
		sorted_members_list = []
		for category in categories_list:
			falla.get_members("category", category)
		sorted_members_list = sorted(
			falla.members_list,
			key = lambda member:member.surname
		)
		page = 0

		try:
			os.mkdir(base_path / 'reports' / 'llistat fallers')
		except OSError as e:
			if e.errno != errno.EEXIST:
				raise
		file = base_path / 'reports' / 'llistat fallers' / ("categories " + current_date + ".pdf")

		w, h = A4
		c = canvas.Canvas(str(file), pagesize = landscape(A4))
		i = 0
		j = 20
		c.drawString(j, w - 30, "ID")
		j = j + 30
		if "nom" in data_list:
			c.drawString(j, w - 30, "FALLER")
			j = j + 200
		if "dni" in data_list:
			c.drawString(j, w - 30, "DNI")
			j = j + 75
		if "adreça" in data_list:
			c.drawString(j, w - 30, "ADREÇA")
			j = j + 250
		if "telefon" in data_list:
			c.drawString(j, w - 30, "TELÈFON")
			j = j + 75
		if "naixement" in data_list:
			c.drawString(j, w - 30, "NAIXEMENT")
			j = j + 75
		if "correu" in data_list:
			c.drawString(j, w - 30, "E-MAIL")
		c.line(0, w - 35, h, w - 35)
		for member in sorted_members_list:
			j = 20
			c.drawString(j, w - i - 60, str(member.id))
			j = j + 30
			if "nom" in data_list:
				c.drawString(
					j,
					w - i - 60,
					member.surname + ", " + member.name
				)
				j = j + 200
			if "dni" in data_list:
				c.drawString(j, w - i - 60, member.dni)
				j = j + 75
			if "adreça" in data_list:
				c.drawString(j, w - i - 60, member.address)
				j = j + 250
			if "telefon" in data_list:
				c.drawString(j, w - i - 60, member.phone_number)
				j = j + 75
			if "naixement" in data_list:
				spanish_birthdate = utils.convert_to_spanish_date(
					member.birthdate
				)
				c.drawString(j, w - i - 60, spanish_birthdate)
				j = j + 75
			if "correu" in data_list:
				c.drawString(j, w - i - 60, member.email)
			i = i + 20
			if i == 500:
				page = page + 1
				c.drawString(20, 20, "llistat de fallers per categories")
				c.drawString((h / 2) - 30, 20, "pàgina " + str(page))
				c.drawString(h - 80, 20, current_date)
				c.showPage()

				j = 20
				c.drawString(j, w - 30, "ID")
				j = j + 30
				if "nom" in data_list:
					c.drawString(j, w - 30, "FALLER")
					j = j + 200
				if "dni" in data_list:
					c.drawString(j, w - 30, "DNI")
					j = j + 75
				if "adreça" in data_list:
					c.drawString(j, w - 30, "ADREÇA")
					j = j + 250
				if "telefon" in data_list:
					c.drawString(j, w - 30, "TELÈFON")
					j = j + 75
				if "naixement" in data_list:
					c.drawString(j, w - 30, "NAIXEMENT")
					j = j + 75
				if "correu" in data_list:
					c.drawString(j, w - 30, "E-MAIL")
				c.line(0, w - 35, h, w - 35)
				i = 0
		page = page + 1
		c.drawString(20, 20, "llistat de fallers per categories")
		c.drawString((h / 2) - 30, 20, "pàgina " + str(page))
		c.drawString(h - 80, 20, current_date)
		c.showPage()
		c.save()

		operating_system = platform.system()
		if operating_system == 'Windows':
			os.startfile(file)
		elif operating_system == 'Linux':
			subprocess.run(["xdg-open", str(file)])


	def reduced_members_list_by_categories(self, categories_list, data_list):
		'''
		Crea un .pdf amb el llistat de dades dels fallers actius
		de les categories passades.

		Paràmetres:
		-----------
		categories_list : list
			Llistat de categories per a les quals volem treure el llistat.
		data_list : list
			Llistat de dades a mostrar a l'informe.
		'''
		utils = Utils()
		base_path = Path(__file__).parent.resolve()
		date = utils.calculate_current_date()
		current_date = date[0] + "-" + date[1] + "-" + date[2]
		falla = Falla()
		sorted_members_list = []
		for category in categories_list:
			falla.get_members("category", category)
		sorted_members_list = sorted(
			falla.members_list,
			key = lambda member:member.surname
		)
		page = 0

		try:
			os.mkdir(base_path / 'reports' / 'llistat fallers')
		except OSError as e:
			if e.errno != errno.EEXIST:
				raise
		file = base_path / 'reports' / 'llistat fallers' / ("categories " + current_date + ".pdf")
		w, h = A4
		c = canvas.Canvas(str(file), pagesize = A4)
		i = 0
		j = 20
		c.drawString(j, h - 30, "ID")
		j = j + 30
		if "nom" in data_list:
			c.drawString(j, h - 30, "FALLER")
			j = j + 200
		if "dni" in data_list:
			c.drawString(j, h - 30, "DNI")
			j = j + 75
		if "adreça" in data_list:
			c.drawString(j, h - 30, "ADREÇA")
			j = j + 250
		if "telefon" in data_list:
			c.drawString(j, h - 30, "TELÈFON")
			j = j + 75
		if "naixement" in data_list:
			c.drawString(j, h - 30, "NAIXEMENT")
			j = j + 75
		if "correu" in data_list:
			c.drawString(j, h - 30, "E-MAIL")
		c.line(0, h - 35, w, h - 35)
		for member in sorted_members_list:
			j = 20
			c.drawString(j, h - i - 60, str(member.id))
			j = j + 30
			if "nom" in data_list:
				c.drawString(
					j,
					h - i - 60,
					member.surname + ", " + member.name
				)
				j = j + 200
			if "dni" in data_list:
				c.drawString(j, h - i - 60, member.dni)
				j = j + 75
			if "adreça" in data_list:
				c.drawString(j, h - i - 60, member.address)
				j = j + 250
			if "telefon" in data_list:
				c.drawString(j, h - i - 60, member.phone_number)
				j = j + 75
			if "naixement" in data_list:
				spanish_birthdate = utils.convert_to_spanish_date(
					member.birthdate
				)
				c.drawString(j, h - i - 60, spanish_birthdate)
				j = j + 75
			if "correu" in data_list:
				c.drawString(j, h - i - 60, member.email)
			i = i + 20
			if i == 700:
				page = page + 1
				c.drawString(20, 20, "llistat de fallers per categories")
				c.drawString((w / 2) - 30, 20, "pàgina " + str(page))
				c.drawString(w - 80, 20, current_date)
				c.showPage()

				j = 20
				c.drawString(j, h - 30, "ID")
				j = j + 30
				if "nom" in data_list:
					c.drawString(j, h - 30, "FALLER")
					j = j + 200
				if "dni" in data_list:
					c.drawString(j, h - 30, "DNI")
					j = j + 75
				if "adreça" in data_list:
					c.drawString(j, h - 30, "ADREÇA")
					j = j + 250
				if "telefon" in data_list:
					c.drawString(j, h - 30, "TELÈFON")
					j = j + 75
				if "naixement" in data_list:
					c.drawString(j, h - 30, "NAIXEMENT")
					j = j + 75
				if "correu" in data_list:
					c.drawString(j, h - 30, "E-MAIL")
				c.line(0, h - 35, w, h - 35)
				i = 0
		page = page + 1
		c.drawString(20, 20, "llistat de fallers per categories")
		c.drawString((w / 2) - 30, 20, "pàgina " + str(page))
		c.drawString(w - 80, 20, current_date)
		c.showPage()
		c.save()

		operating_system = platform.system()
		if operating_system == 'Windows':
			os.startfile(file)
		elif operating_system == 'Linux':
			subprocess.run(["xdg-open", str(file)])


	def members_list_by_age(self, initial_age, final_age, data_list):
		'''
		Crea un .pdf amb el llistat de dades dels fallers actiu
		amb edats compreses entre els paràmetres d'entrada.

		Paràmetres:
		-----------
		initial_age : int
			Mínima edat dels fallers del llistat.
		final_age : int
			Màxima edat dels fallers del llistat.
		data_list : list
			Llistat de dades a mostrar a l'informe.
		'''
		utils = Utils()
		base_path = Path(__file__).parent.resolve()
		date = utils.calculate_current_date()
		current_date = date[0] + "-" + date[1] + "-" + date[2]
		falla = Falla()
		falla.get_current_falla_year()
		falla.get_members("is_registered", 1)
		members_list_by_age = []
		for member in falla.members_list:
			age = member.calculate_age(member.birthdate, falla.falla_year)
			if (age >= initial_age) and (age <= final_age):
				members_list_by_age.append(member)
		page = 0

		try:
			os.mkdir(base_path / 'reports' / 'llistat fallers')
		except OSError as e:
			if e.errno != errno.EEXIST:
				raise
		file = base_path / 'reports' / 'llistat fallers' / ("edat " + current_date + ".pdf")

		w, h = A4
		c = canvas.Canvas(str(file), pagesize = landscape(A4))
		i = 0
		j = 20
		c.drawString(j, w - 30, "ID")
		j = j + 30
		if "nom" in data_list:
			c.drawString(j, w - 30, "FALLER")
			j = j + 200
		if "dni" in data_list:
			c.drawString(j, w - 30, "DNI")
			j = j + 75
		if "adreça" in data_list:
			c.drawString(j, w - 30, "ADREÇA")
			j = j + 250
		if "telefon" in data_list:
			c.drawString(j, w - 30, "TELÈFON")
			j = j + 75
		if "naixement" in data_list:
			c.drawString(j, w - 30, "NAIXEMENT")
			j = j + 75
		if "correu" in data_list:
			c.drawString(j, w - 30, "E-MAIL")
		c.line(0, w - 35, h, w - 35)
		for member in members_list_by_age:
			j = 20
			c.drawString(j, w - i - 60, str(member.id))
			j = j + 30
			if "nom" in data_list:
				c.drawString(
					j,
					w - i - 60,
					member.surname + ", " + member.name
				)
				j = j + 200
			if "dni" in data_list:
				c.drawString(j, w - i - 60, member.dni)
				j = j + 75
			if "adreça" in data_list:
				c.drawString(j, w - i - 60, member.address)
				j = j + 250
			if "telefon" in data_list:
				c.drawString(j, w - i - 60, member.phone_number)
				j = j + 75
			if "naixement" in data_list:
				spanish_birthdate = utils.convert_to_spanish_date(
					member.birthdate
				)
				c.drawString(j, w - i - 60, spanish_birthdate)
				j = j + 75
			if "correu" in data_list:
				c.drawString(j, w - i - 60, member.email)
			i = i + 20
			if i == 500:
				page = page + 1
				c.drawString(20, 20, "llistat de fallers per edat")
				c.drawString((h / 2) - 30, 20, "pàgina " + str(page))
				c.drawString(h - 80, 20, current_date)
				c.showPage()

				j = 20
				c.drawString(j, w - 30, "ID")
				j = j + 30
				if "nom" in data_list:
					c.drawString(j, w - 30, "FALLER")
					j = j + 200
				if "dni" in data_list:
					c.drawString(j, w - 30, "DNI")
					j = j + 75
				if "adreça" in data_list:
					c.drawString(j, w - 30, "ADREÇA")
					j = j + 250
				if "telefon" in data_list:
					c.drawString(j, w - 30, "TELÈFON")
					j = j + 75
				if "naixement" in data_list:
					c.drawString(j, w - 30, "NAIXEMENT")
					j = j + 75
				if "correu" in data_list:
					c.drawString(j, w - 30, "E-MAIL")
				c.line(0, w - 35, h, w - 35)
				i = 0
		page = page + 1
		c.drawString(20, 20, "llistat de fallers per edat")
		c.drawString((h / 2) - 30, 20, "pàgina " + str(page))
		c.drawString(h - 80, 20, current_date)
		c.showPage()
		c.save()

		operating_system = platform.system()
		if operating_system == 'Windows':
			os.startfile(file)
		elif operating_system == 'Linux':
			subprocess.run(["xdg-open", str(file)])


	def reduced_members_list_by_age(self, initial_age, final_age, data_list):
		'''
		Crea un .pdf amb el llistat de dades dels fallers actius
		amb edats compreses entre els paràmetres d'entrada.

		Paràmetres:
		-----------
		initial_age : int
			Mínima edat dels fallers del llistat.
		final_age : int
			Màxima edat dels fallers del llistat.
		data_list : list
			Llistat de dades a mostrar a l'informe.
		'''
		utils = Utils()
		base_path = Path(__file__).parent.resolve()
		date = utils.calculate_current_date()
		current_date = date[0] + "-" + date[1] + "-" + date[2]
		falla = Falla()
		falla.get_current_falla_year()
		falla.get_members("is_registered", 1)
		members_list_by_age = []
		for member in falla.members_list:
			age = member.calculate_age(member.birthdate, falla.falla_year)
			if (age >= initial_age) and (age <= final_age):
				members_list_by_age.append(member)
		page = 0

		try:
			os.mkdir(base_path / 'reports' / 'llistat fallers')
		except OSError as e:
			if e.errno != errno.EEXIST:
				raise
		file = base_path / 'reports' / 'llistat fallers' / ("edat " + current_date + ".pdf")

		w, h = A4
		c = canvas.Canvas(str(file), pagesize = A4)
		i = 0
		j = 20
		c.drawString(j, h - 30, "ID")
		j = j + 30
		if "nom" in data_list:
			c.drawString(j, h - 30, "FALLER")
			j = j + 200
		if "dni" in data_list:
			c.drawString(j, h - 30, "DNI")
			j = j + 75
		if "adreça" in data_list:
			c.drawString(j, h - 30, "ADREÇA")
			j = j + 250
		if "telefon" in data_list:
			c.drawString(j, h - 30, "TELÈFON")
			j = j + 75
		if "naixement" in data_list:
			c.drawString(j, h - 30, "NAIXEMENT")
			j = j + 75
		if "correu" in data_list:
			c.drawString(j, h - 30, "E-MAIL")
		c.line(0, h - 35, w, h - 35)
		for member in members_list_by_age:
			j = 20
			c.drawString(j, h - i - 60, str(member.id))
			j = j + 30
			if "nom" in data_list:
				c.drawString(
					j,
					h - i - 60,
					member.surname + ", " + member.name
				)
				j = j + 200
			if "dni" in data_list:
				c.drawString(j, h - i - 60, member.dni)
				j = j + 75
			if "adreça" in data_list:
				c.drawString(j, h - i - 60, member.address)
				j = j + 250
			if "telefon" in data_list:
				c.drawString(j, h - i - 60, member.phone_number)
				j = j + 75
			if "naixement" in data_list:
				spanish_birthdate = utils.convert_to_spanish_date(
					member.birthdate
				)
				c.drawString(j, h - i - 60, spanish_birthdate)
				j = j + 75
			if "correu" in data_list:
				c.drawString(j, h - i - 60, member.email)
			i = i + 20
			if i == 700:
				page = page + 1
				c.drawString(20, 20, "llistat de fallers per edat")
				c.drawString((w / 2) - 30, 20, "pàgina " + str(page))
				c.drawString(w - 80, 20, current_date)
				c.showPage()

				j = 20
				c.drawString(j, h - 30, "ID")
				j = j + 30
				if "nom" in data_list:
					c.drawString(j, h - 30, "FALLER")
					j = j + 200
				if "dni" in data_list:
					c.drawString(j, h - 30, "DNI")
					j = j + 75
				if "adreça" in data_list:
					c.drawString(j, h - 30, "ADREÇA")
					j = j + 250
				if "telefon" in data_list:
					c.drawString(j, h - 30, "TELÈFON")
					j = j + 75
				if "naixement" in data_list:
					c.drawString(j, h - 30, "NAIXEMENT")
					j = j + 75
				if "correu" in data_list:
					c.drawString(j, h - 30, "E-MAIL")
				c.line(0, h - 35, w, h - 35)
				i = 0
		page = page + 1
		c.drawString(20, 20, "llistat de fallers per edat")
		c.drawString((w / 2) - 30, 20, "pàgina " + str(page))
		c.drawString(w - 80, 20, current_date)
		c.showPage()
		c.save()

		operating_system = platform.system()
		if operating_system == 'Windows':
			os.startfile(file)
		elif operating_system == 'Linux':
			subprocess.run(["xdg-open", str(file)])