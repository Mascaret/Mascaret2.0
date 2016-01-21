# Kivy libs import
from kivy.uix.textinput import TextInput

# Python libs import

# Personal libs import

class CenteredTextInput(TextInput):

    def __init__(self, text = "input", **kwargs):
        super(CenteredTextInput, self).__init__(**kwargs)
        self.bind(text=self.on_text)

        self.text = text
        self.padding = [10, ( self.height - self.line_height ) / 2]
        self.center_text()


    def on_text(self, instance, value):
        self.center_text()


    def center_text(self):
        cursor_index_save = self.cursor_index
        self.padding = [10,self.padding[1]]

        if self.get_end_x() != (self.x + self.width):
            i = 0
            while self.get_end_x() + self.get_begining_x() != 2 * self.x + self.width  and i < 100:
                print("end: " + str(self.get_end_x()))
                print("begining: " + str(self.get_begining_x()))
                self.padding = [self.padding[0] + 1 ,self.padding[1]]
                i = i + 1


    def get_begining_x(self):
        self.do_cursor_movement('cursor_home')
        return self.cursor_pos[0]


    def get_end_x(self):
        self.do_cursor_movement('cursor_end')
        return self.cursor_pos[0]
