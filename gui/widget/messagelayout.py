# Kivy Libs import
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import (
                            ObjectProperty
                            )

# Python Lib import

# Personal Libs import


Builder.load_string('''
<MessageLayout>:
    message_label: message_label
    Label:
        id: message_label
''')

class MessageLayout(BoxLayout):
    message_label = ObjectProperty()

    def __init__(self, message, **kwargs):
        super(MessageLayout, self).__init__(**kwargs)

        self.message_label.text = message
