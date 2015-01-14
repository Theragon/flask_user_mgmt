from flask import request

def get_from_request_form(*args):
	results = []
	for arg in args:
		try:
			results.append(request.form[arg])
		except KeyError:
			results.append(None)

	if len(results) > 1:
		result = tuple(results)
	else:
		result = results[0]
	return result