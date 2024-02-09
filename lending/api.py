import frappe
import json

@frappe.whitelist()
def transfer_branch(**kwargs):
	response=[]
	body = json.loads(frappe.request.data)
	query_filters = {
		"hub": body.get("from_branch"),
	}
	
	if body.get('customer') != None:
		query_filters.update({'custom_individual_applicant':body.get('customer')})
	
	loans = frappe.get_all("Loan",filters=query_filters,fields=["name"])
	
	for loan in loans:
		frappe.db.set_value('Loan',loan.name,'hub',body.get('to_branch'))
		frappe.db.commit()
		result = frappe.db.sql("""select name,hub from `tabLoan` where name=%s""",(loan.name),as_dict=True)
		response.append(result)
	return response
