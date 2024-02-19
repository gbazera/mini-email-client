import re
from time import sleep
from rich.text import Text
from textual.app import App, ComposeResult
from textual.widgets import Footer, DataTable, Log, Label, Tabs, TabbedContent, Static, Input, TextArea, Button

from actions import get_emails, send_email

email_address = 'giorgigamer27@gmail.com'
password = 'eqzm mscc lhqh lpnd'

messages, message_contents = get_emails(email_address, password, 5)

ROWS = [('From', 'Subject', 'Date')] + messages

email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

def is_valid(address):
    if re.fullmatch(email_regex, address):
        return True
    return False

class MiniEmailClient(App):
    CSS_PATH = './style/main.tcss'
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def compose(self) -> ComposeResult:
        with TabbedContent('Inbox', 'Compose'):
            with Static(classes='inbox'):
                yield DataTable(zebra_stripes=True)
                yield Log(auto_scroll=False)
            with Static(classes='compose'):
                yield Input(placeholder='To', classes='input_to')
                yield Input(placeholder='Subject', classes='input_subject')
                yield TextArea()
                yield Button('Send', classes='button_send')
        yield Footer()
    
    def on_mount(self) -> None:
        # Table
        table = self.query_one(DataTable)
        table.cursor_type = 'row'
        table.add_columns(*ROWS[0])
        for number, row in enumerate(ROWS[1:], start=1):
            label = Text(str(number), style="#fff")
            table.add_row(*row, label=label)
        
        # Log
        log = self.query_one(Log)
        log.write(message_contents[0])
        log.border_title = messages[0][1]

        # TextArea
        textarea = self.query_one(TextArea)
        textarea.border_title = 'Message'
    
    def on_data_table_row_selected(self) -> None:
        table = self.query_one(DataTable)
        id = table.cursor_coordinate[0]
        log = self.query_one(Log)
        log.clear()
        log.write(message_contents[id])
        log.border_title = messages[id][1]

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark
    
    def on_button_pressed(self):
        input_to = self.query_one('.input_to')
        input_subject = self.query_one('.input_subject')
        textarea = self.query_one(TextArea)
        btn = self.query_one(Button)

        if not is_valid(input_to.value):
            input_to.value = 'Invalid email address.'
        else:
            if send_email(email_address, password, input_to.value, input_subject.value, textarea.text):
                btn.variant = 'success'
                input_to.value = ''
                input_subject.value = ''
                textarea.text = ''
            else:
                btn.variant = 'error'
                input_to.value = 'Email not sent.'

if __name__ == "__main__":
    app = MiniEmailClient()
    app.run()