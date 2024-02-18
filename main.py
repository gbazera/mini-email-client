from rich.text import Text
from textual.app import App, ComposeResult
from textual.widgets import Footer, DataTable, RichLog, Label
from textual.events import Key

from get_emails import get_emails

email_address = 'giorgigamer27@gmail.com'
password = 'eqzm mscc lhqh lpnd'

messages, message_contents = get_emails(email_address, password, 10)

ROWS = [('From', 'Subject', 'Date')] + messages

class MiniEmailClient(App):
    CSS_PATH = './style/message_display.tcss'
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def compose(self) -> ComposeResult:
        yield Footer()
        yield DataTable(zebra_stripes=True)
        yield Label()
        yield RichLog(auto_scroll=False)
    
    def on_mount(self) -> None:
        # Table
        table = self.query_one(DataTable)
        table.cursor_type = 'row'
        table.add_columns(*ROWS[0])
        for number, row in enumerate(ROWS[1:], start=1):
            label = Text(str(number), style="#fff")
            table.add_row(*row, label=label)
        
        # Log
        log = self.query_one(RichLog)
        log.write(message_contents[0])
    
    def on_data_table_row_selected(self) -> None:
        table = self.query_one(DataTable)
        log = self.query_one(RichLog)
        log.clear()
        log.write(message_contents[table.cursor_coordinate[0]])

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark

if __name__ == "__main__":
    app = MiniEmailClient()
    app.run()