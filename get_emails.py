from imap_tools import MailBox

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

    # imap = imaplib.IMAP4_SSL(imap_server)
    # imap.login(email_address, password)

    # imap.select('Inbox')

    # response, data = imap.search(None, 'ALL')

    # msgs = []
    # msg_contents = []

    # if response == 'OK':
    #     email_ids = data[0].split()
    #     for id in email_ids[-number_of_msgs:]:
    #         response, data = imap.fetch(id, '(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])')
    #         if response == 'OK':
    #             msg = email.message_from_bytes(data[0][1])

    #             msg_from = msg.get('From')
    #             msg_from = email.header.decode_header(msg_from)
    #             msg_from = email.header.make_header(msg_from)

    #             msg_subject = msg.get('Subject')
    #             msg_subject = email.header.decode_header(msg_subject)
    #             msg_subject = email.header.make_header(msg_subject)

    #             msg_date = msg.get('Date')

    #             msg_full = (msg_from, msg_subject, msg_date)
    #             msgs.append(msg_full)

    #         response, data = imap.fetch(id, '(UID BODY[TEXT])')
    #         if response == 'OK':
    #             msg_content = []
    #             for part in msg.walk():
    #                 if part.get_content_type() == 'text/plain':
    #                     txt = part.get_payload(decode=True).decode('utf-8')
    #                     msg_content.append(txt)
    #             msg_content = "\n".join(msg_content)
    #             soup = BeautifulSoup(msg_content, "html.parser")
    #             msg_content = soup.get_text(separator="\n")
                        
    #             msg_contents.append(msg_content)

    # imap.logout()