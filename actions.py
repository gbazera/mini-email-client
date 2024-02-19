from imap_tools import MailBox
import smtplib

def get_emails(email_address, password, number_of_msgs):
    imap_server = 'imap.gmail.com' #:993

    headers = []
    contents = []

    with MailBox(imap_server).login(email_address, password) as mailbox:
        for msg in mailbox.fetch(limit=number_of_msgs, reverse=True):
            header = (msg.from_, msg.subject, msg.date_str)
            headers.append(header)
            contents.append(msg.text)
    
    return headers, contents

def send_email(email_address, password, receiver_address, subject, message):
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(email_address, password)

        message = 'Subject: ' + subject + '\n\n' + message

        server.sendmail(email_address, receiver_address, message)
        server.quit()
        return True
    return False
