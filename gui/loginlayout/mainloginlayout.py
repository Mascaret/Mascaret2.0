# Kivy Libs imports
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.properties import ObjectProperty
from kivy.animation import Animation

# # Python Libs imports
from data.db import MyDB

# Personnal Libs imports
from data.logicalobject.user import User
from data.logicalobject.users import Userd



Builder.load_string('''
############################### Login Screen ###############################

<MainLoginLayout>:
    login_box: login_input
    password_box: password_input
    error_box: error_label
    login_area: login_rect
    canvas:
        Rectangle:
            source: 'gui/loginlayout/login_screen-wallpaper.jpg'
            size: root.width if (root.width / root.height) > (1920 / 1080) else root.height * (1920 / 1080), root.height if (root.width / root.height) <= (1920 / 1080) else root.width / (1920 / 1080)
            pos: self.pos
    BoxLayout:
        id: login_rect
        BoxLayout:
            orientation: "vertical"
            canvas.before:
                Color:
                    rgba: (0,0,0,0.5)
                Rectangle:
                    source: 'gui/login_screen/login_screen_input_area.png'
                    size: (self.width + 120, self.height + 20)
                    pos: self.x - 100, self.y + 5
            size_hint: (None, None)
            width: "350dp"
            height: "120dp"
            pos_hint: {'x': .03,'y': .75}
            BoxLayout:
                BoxLayout:
                    size_hint: .7, 1
                    spacing: "15dp"
                    padding: "15dp"
                    orientation: "vertical"
                    Label:
                        text: "Login:"
                        font_size: '20dp'
                        text_size: self.size
                        halign: 'justify'
                        valign: 'top'
                        font_name: 'OCRAEXT.TTF'
                        italic: True
                    Label:
                        text: "Password:"
                        italic: True
                        font_size: '20dp'
                        text_size: self.size
                        halign: 'justify'
                        valign: 'top'
                        font_name: 'OCRAEXT.TTF'
                BoxLayout:
                    orientation: "vertical"
                    spacing: "5dp"
                    padding: "8dp"
                    TextInput:
                        text: "guichetcle"
                        focus: True
                        background_color: (1, 1, 1, 0)
                        foreground_color: (1,1,1,0.8)
                        write_tab: False
                        multiline: False
                        id: login_input
                        on_text_validate: password_input.focus = True
                        font_name: 'OCRAEXT.TTF'
                        font_size: '20dp'
                        cursor_color: 1,1,1,0.8
                    TextInput:
                        background_color: (1, 1, 1, 0)
                        foreground_color: (1,1,1,0.8)
                        write_tab: False
                        multiline: False
                        id: password_input
                        on_text_validate: root.login_animation()
                        password: True
                        font_name: 'OCRAEXT.TTF'
                        font_size: '20dp'
                        cursor_color: 1,1,1,0.8
                        text: "laptite"
            BoxLayout:
                size_hint: 1, 0.25
                Label:
                    text_size: self.size
                    id: error_label
                    font_name: 'OCRAEXT.TTF'
                    font_size: '16dp'
                    color: (1,0.5,0.5,0.8)
                    valign: 'top'
                    halign: 'right'

############################# End Login Screen #############################

''')

#Class creating the Login_screen
class MainLoginLayout(FloatLayout):
    # login testinput
    login_box = ObjectProperty()
    # Psswrd textinput
    password_box = ObjectProperty()
    # error message label
    error_box = ObjectProperty()
    # area containing the login objects
    login_area = ObjectProperty()

    def __init__(self, mainroot):
        super(MainLoginLayout, self).__init__()
        # we register the event "on right id" wich will be triggered
        # if the login and psswd match
        self.register_event_type('on_right_id')
        self.register_event_type('on_wrong_id')
        self.mainroot = mainroot

    def login_animation(self):
        # we create the animation triggered by the login action
        # it is a translation of the login area to disappear on the
        # left of the screen
        animation = Animation(
                        x=self.login_area.x - self.login_area.width,
                        duration=0.8
                             )
        # triggering of the anim
        animation.start(self.login_area)
        # creation of a background image during the login query
        self.pan_screen= Image(
                            source= "gui/loginlayout/loading.jpg",
                            keep_ratio= False,
                            allow_stretch= True,
                            color= (1, 1, 1, 0.1)
                              )
        # we add it
        self.add_widget(self.pan_screen)
        # we bind to the end of the animation the trigger of the check_login
        # method
        animation.bind(on_complete=self.login_check)

    def login_check(self, *args):
    # this methd checks if the login and psswd entered are correct

        # we get the login & psswrd entered
        user_login = self.login_box.text
        user_password = self.password_box.text

######################### Beginning of the CSV Method #########################

        # DB CONNECTION
        db = MyDB()

        # we get the users dtf
        users_dataframe = db.get_dataframe(objct = Userd)

        # We check that the login and the psswrd match
        temp_user = users_dataframe[users_dataframe.user_login == user_login]

        if not temp_user.empty:
            # print(temp_user.user_password)
            if temp_user.user_password.item() == user_password:
                # we save the user log in the singleton User()
                user_logged = User(
                                login = user_login,
                                index = temp_user.index.item()
                                  )
                # And launch the on_right_id method
                self.dispatch('on_right_id')
                # and stop the method
                return
        # if they are wrong
        # launch the on_wrong_id method
        self.dispatch('on_wrong_id')

############################ End of the CSV Method ############################


    def on_right_id(self):
    # Event triggered when the id is right
        self.mainroot.after_loginscreen(value = 1)

    def on_wrong_id(self):
        # if they are wrong
        # we put the focus back on the login textinput
        self.login_box.focus = True
        # we remove the background texture
        self.remove_widget(self.pan_screen)
        # we add an error message
        self.error_box.text = "Wrong credentials"
        # create an animation object. This object could be stored
        # and reused each call or reused across different widgets.
        # += is a sequential step, while &= is in parallel
        animation = Animation(x=(0), t='out_bounce')

        # apply the animation on the button, passed in the "instance"
        # argument Notice that default 'click' animation (changing the
        # button color while the mouse is down) is unchanged.
        animation.start(self.login_area)
