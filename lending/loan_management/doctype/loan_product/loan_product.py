# Copyright (c) 2019, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import frappe
from frappe import _
from frappe.model.document import Document


class LoanProduct(Document):
	def validate(self):
		self.validate_accounts()
		self.validate_rates()

	def validate_accounts(self):
		for fieldname in [
			"payment_account",
			"loan_account",
			"interest_income_account",
			"penalty_income_account",
		]:
			company = frappe.get_value("Account", self.get(fieldname), "company")

			if company and company != self.company:
				frappe.throw(
					_("Account {0} does not belong to company {1}").format(
						frappe.bold(self.get(fieldname)), frappe.bold(self.company)
					)
				)

		if self.get("loan_account") == self.get("payment_account"):
			frappe.throw(_("Loan Account and Payment Account cannot be same"))

	def validate_rates(self):
		for field in ["rate_of_interest", "penalty_interest_rate"]:
			if self.get(field) and self.get(field) < 0:
				frappe.throw(_("{0} cannot be negative").format(frappe.unscrub(field)))