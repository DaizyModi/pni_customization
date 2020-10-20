
def validate_customer(doc, method):
	for user in doc.daily_payment_report:
		doc.last_commitment_date = user.commitment_date
		doc.last_commitment_amt = user.commitment_amt
		doc.last_remark = user.remark