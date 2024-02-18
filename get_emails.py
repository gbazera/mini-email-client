import imaplib
import email
import email.header
from bs4 import BeautifulSoup

def get_emails(email_address, password, number_of_msgs):
    imap_server = 'imap.gmail.com' #:993

    imap = imaplib.IMAP4_SSL(imap_server)
    imap.login(email_address, password)

    imap.select('Inbox')

    response, data = imap.search(None, 'ALL')

    msgs = []
    msg_contents = []

    if response == 'OK':
        email_ids = data[0].split()
        for id in email_ids[-number_of_msgs:]:
            response, data = imap.fetch(id, '(RFC822)')
            if response == 'OK':
                msg = email.message_from_bytes(data[0][1])

                msg_from = msg.get('From')

                msg_subject = msg.get('Subject')
                msg_subject = email.header.decode_header(msg_subject)
                msg_subject = email.header.make_header(msg_subject)

                msg_date = msg.get('Date')

                msg_full = (msg_from, msg_subject, msg_date)
                msgs.append(msg_full)

                msg_content = []
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain':
                        txt = part.get_payload(decode=True).decode('utf-8')
                        msg_content.append(txt)
                msg_content = "\n".join(msg_content)
                soup = BeautifulSoup(msg_content, "html.parser")
                msg_content = soup.get_text(separator="\n")
                        
                msg_contents.append(msg_content)

    imap.logout()
    return msgs[::-1], msg_contents[::-1]