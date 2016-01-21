# Kivy libs import
from kivy.lang import Builder
from kivy.properties import ListProperty

# Python libs import

# Personal libs import
from gui.widget.centeredtextinput import CenteredTextInput

Builder.load_string('''
######################## Beginning of Colored TextInput #######################

<ColoredTextInput>:
    size_hint: (None, None)
    width: "120dp"
    height: "50dp"
    background_color: root.back_color
    foreground_color:
        ((1,1,1,1) if root.back_color[0] + root.back_color[1] +
        root.back_color[2] < 1.5 else (0,0,0,1))
    cursor_color:
        ((1,1,1,1) if root.back_color[0] + root.back_color[1] +
        root.back_color[2] < 1.5 else (0,0,0,1))
    write_tab: False
    multiline: False

########################## End of Colored TextInput ###########################
''')

class ColoredTextInput(CenteredTextInput):
    back_color = ListProperty([1,1,1,1])
