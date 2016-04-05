
import imaplib
import email
from datetime import datetime
from datetime import timedelta
import pytz
import tzlocal

def get_time_difference(mail_time):
	if(mail_time[24] == ' '):
		timediff = mail_time[25:][:5]
	elif(mail_time[25] == " "):
		timediff = mail_time[26:][:5]

	diff = timediff[0]
	hours = timediff[1:3]
	mins = timediff[3:5]

	return [diff, hours, mins]


mail = imaplib.IMAP4_SSL('imap.gmail.com', port = 993)
mail.login('abhyu195@gmail.com', 'cullingblade')
# mail.select('[Gmail]/Drafts')
# print(mail.list())

mail.select("[Gmail]/Important")

result, data = mail.search(None, "ALL")

ids = data[0]
id_list = ids.split()
latest_email_id = id_list[-1]

i = 1
for email_id in reversed(id_list):
	result, data = mail.fetch(email_id, "(RFC822)")
	raw_email = data[0][1]
	email_message = email.message_from_string(raw_email)
	local_timezone = tzlocal.get_localzone()
	date_format = "%a, %d %b %Y %H:%M:%S"
	current_date = datetime.now()

	# print("MAIL ", i)
	for item in email_message.items():
		if(item[0] == "Date"):
			mail_time = item[1][:24]
			utc_time = datetime.strptime(mail_time, date_format)
			timediff = get_time_difference(item[1])
			if(timediff[0] == '+'):
				utc_time = utc_time - timedelta(hours = int(timediff[1]), minutes = int(timediff[2]))
			else:
				utc_time = utc_time + timedelta(hours = int(timediff[1]), minutes = int(timediff[2]))
			local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)
			# print(item[1])
			# print(local_time, local_time.day, local_time.month)
			# print(current_date, current_date.day, current_date.month)
			if(current_date.day == local_time.day and current_date.month == local_time.month):
				read_mail = True
			else:
				read_mail = False
				break
		if(item[0] == "From"):
			mail_from = item[1]
			mail_from = mail_from[:mail_from.index('<')].strip()
		if(item[0] == "Subject"):
			mail_subject = item[1]
			
	if(read_mail):
		print("MAIL " + str(i))
		print(mail_from)
		print(mail_subject)
		i+=1
	else:
		break

# %a, %d %b %Y %H:%M:%S
# local_timezone = tzlocal.get_localzone()
# utc_time - timedelta(hours = 2)
# utc_time = datetime.strptime("2011-01-21 02:37:21", "%Y-%m-%d %H:%M:%S")
# local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)