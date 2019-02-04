#!/usr/bin/python
# -*- coding: utf-8 -*-

import email, imaplib, os, sys, re
from email.parser import HeaderParser
import datetime

from blog.models import Blog, Category

#wypelnic odpowiednio
user = "****@gmail.com"
pwd = "****"

m = imaplib.IMAP4_SSL("imap.gmail.com")
m.login(user,pwd)

def sprawdzPoczte():
	from_folder = "przetwarzane"
	to_folder = "historia"

	m.select(from_folder, readonly = False)

	response, emailids = m.search(None, 'All')
	assert response == 'OK'

	emailids = emailids[0].split()

	errors = []
	labeled = []
		
	for emailid in emailids:
		result = m.fetch(emailid, '(X-GM-MSGID)')

		if result[0] != 'OK':
			errors.append(emailid)
			continue

		#temat
		r, subject = m.fetch(emailid, '(BODY[HEADER.FIELDS (SUBJECT)])')
		subject = subject[0][1]
		subject = email.message_from_string(subject)
		subject = email.header.decode_header(subject['Subject'])[0]
		subject = unicode(subject[0], 'utf-8')
		title = subject
		
		#tresc
		r, email_data = m.fetch(emailid, '(RFC822)')
		raw_email = email_data[0][1]
		raw_email_string = raw_email.decode('utf-8')
		email_message = email.message_from_string(raw_email_string)
		
		text = ""
		
		for part in email_message.walk():
			if part.get_content_type() == "text/plain": # ignore attachments/html
				body = part.get_payload(decode=True)
				text = text + body.decode('utf-8')
			else:
				continue

		text = text.replace('#djangodyskusyjna', '')		
		
		#autor
		r, author = m.fetch(emailid, '(BODY[HEADER.FIELDS (FROM)])')
		author = author[0][1]
		author = email.message_from_string(author)
		author = email.header.decode_header(author['From'])[0]
		author = unicode(author[0], 'utf-8')
		
		#zapisz do bazy
		now = datetime.datetime.now()
		Blog.objects.create(author = author, title = title, body = text, category = Category.objects.get_or_create(title=now.strftime("%B %Y"))[0])

		gm_msgid = re.findall(r"X-GM-MSGID (\d+)", result[1][0])[0]

		result = m.store(emailid, '+X-GM-LABELS', to_folder)

		if result[0] != 'OK':
			errors.append(emailid)
			continue

		labeled.append(gm_msgid)

	m.close()
	m.select(to_folder, readonly = False)

	errors2 = []

	for gm_msgid in labeled:
		result = m.search(None, '(X-GM-MSGID "%s")' % gm_msgid)

		if result[0] != 'OK':
			errors2.append(gm_msgid)
			continue

		emailid = result[1][0]
		result = m.store(emailid, '-X-GM-LABELS', from_folder)

		if result[0] != 'OK':
			errors2.append(gm_msgid)
			continue

	m.close()
	#m.logout()

	if errors: print >>sys.stderr, len(errors), "failed to add label", to_folder
	if errors2: print >>sys.stderr, len(errors2), "failed to remove label", from_folder