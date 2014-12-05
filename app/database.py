from app import db

def save(changes):
	try:
		print('saving changes')
		db.session.add(changes)
		db.session.commit()
		print('changes saved to database')
		return True
	except:
		print('could not save changes')
		db.session.rollback()
		return False