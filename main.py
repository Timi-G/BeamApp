from datetime import date, datetime
from multiprocessing import pool

from kivy.core.window import Window
from kivy.app import App
from kivy.animation import Animation
from kivy.base import runTouchApp
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import BooleanProperty, ColorProperty, ListProperty, \
    NumericProperty, ObjectProperty, StringProperty
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button, ButtonBehavior

from AppCustomWidget import Balrem_date_picker, CustomAccountNumbersTI, \
    CustomCheckBoxLabel, CustomPropBubble, \
    DatePicker, EntryDate, TimeTI, CustomSpinner

kivyfiles = ['proplogin.kv']
for k in kivyfiles:
    Builder.load_file(k)


"""Login, Signup & ForgotPassword Screen"""
class LoginScreen(Screen):
    pass

class SignUpScreen(Screen):
    pass

class ForgotPasswordScreen(Screen):
    pass


class DataBooks_Create_Screen(Screen):

    def __init__(self, **kwargs):
        super(DataBooks_Create_Screen, self).__init__(**kwargs)
        self.screen_organizer()

    def screen_organizer(self):
        if self.children:
            self.clear_widgets()

        self.dat_zero_ent_page()

    def dat_zero_ent_page(self):
        dat_zeroentpage = DataBooks_ZeroEntryPage()
        self.add_widget(dat_zeroentpage)


class MainLabels(ButtonBehavior, GridLayout):
    pass

class DataBooks_ZeroEntryPage(FloatLayout):
    pass


class DateCheckBoxLabel(CustomCheckBoxLabel):
    pass

class BalanceCheckBoxLabel(CustomCheckBoxLabel):
    pass

class ReceivedCheckBoxLabel(CustomCheckBoxLabel):
    pass

class SentCheckBoxLabel(CustomCheckBoxLabel):
    pass

class ErrorAlerts(Label):
    pass

class BaseEntryScreen(Screen):
    pass


# MV for balance reminder
class BalReminderModalview(ModalView):
    # find out how to accept the complete date and time chosen by user and store in a variable
    # string is proposed, which will be converted to datetime format
    dismiss_choice = StringProperty()

    def show_no_time_input_error_alert(self):
        anim = Animation(opacity=1, duration=2) + Animation(opacity=0, duration=1.5)
        anim2 = Animation(foreground_color=[0.8, 0.2, 0.2, 0.5], border_width=1, duration=2) \
                + Animation(foreground_color=[0, 0, 0, 1], border_width=0.1, duration=1.5)
        anim3 = Animation(foreground_color=[0.8, 0.2, 0.2, 0.5], border_width=1, duration=2) \
                + Animation(foreground_color=[0, 0, 0, 1], border_width=0.1, duration=1.5)
        anim.start(self.ids.no_time_input_error_alert)
        anim2.start(self.ids.hh)
        anim3.start(self.ids.mins)

    def show_time_error_alert(self):
        anim = Animation(opacity=1, duration=2) + Animation(opacity=0, duration=1.5)
        anim2 = Animation(foreground_color=[0.8, 0.2, 0.2, 0.5], border_width=1, duration=2) \
                + Animation(foreground_color=[0, 0, 0, 1], border_width=0.1, duration=1.5)
        anim3 = Animation(border_color=[0.8, 0.2, 0.2, 0.5], border_width=1, duration=2) \
                + Animation(border_color=[0, 0, 0, 0.5], border_width=0.1, duration=1.5)
        anim.start(self.ids.time_error_alert)
        anim2.start(self.ids.hh)
        anim3.start(self.ids.timespinner)

    def show_pastdate_error_alert(self):
        anim = Animation(opacity=1, duration=2) + Animation(opacity=0, duration=1.5)
        anim2 = Animation(foreground_color=[0.8, 0.2, 0.2, 0.5], border_width=1, duration=2) \
                + Animation(foreground_color=[0, 0, 0, 1], border_width=0.1, duration=1.5)
        anim.start(self.ids.past_error_alert)
        anim2.start(self.ids.rem_date_picker)

    def show_pasttime_error_alert(self):
        anim = Animation(opacity=1, duration=2) + Animation(opacity=0, duration=1.5)
        anim2 = Animation(foreground_color=[0.8, 0.2, 0.2, 0.5], border_width=1, duration=2) \
                + Animation(foreground_color=[0, 0, 0, 1], border_width=0.1, duration=1.5)
        anim3 = Animation(foreground_color=[0.8, 0.2, 0.2, 0.5], border_width=1, duration=2) \
                + Animation(foreground_color=[0, 0, 0, 1], border_width=0.1, duration=1.5)
        anim.start(self.ids.past_error_alert)
        anim2.start(self.ids.hh)
        anim3.start(self.ids.mins)

    def update_reminder_datetime(self):
        date_dmy = datetime.strptime(self.ids.rem_date_picker.text, '%d %b, %Y')
        date_y = int(date_dmy.strftime("%Y"))
        date_m = int(date_dmy.strftime("%m"))
        date_d = int(date_dmy.strftime("%d"))
        time_hh = self.ids.hh.text
        time_mm = self.ids.mins.text
        if time_hh == '':
            time_hh = 0
        else:
            time_hh = int(self.ids.hh.text)
        if time_mm == '':
            time_mm = 0
        else:
            time_mm = int(self.ids.mins.text)

        ndate_dmyhm = datetime(date_y, date_m, date_d, time_hh, time_mm)
        ndate_dmy = date(date_y, date_m, date_d)
        self.reminder_datetime = ndate_dmyhm
        self.reminder_date = ndate_dmy

    def cancel_button(self):
        self.dismiss_choice = 'Cancel'
        dc = self.dismiss_choice
        self.ids.hh.text = ''
        self.ids.mins.text = ''
        self.dismiss()
        return dc

    def save_ok_button(self):
        time_hh = self.ids.hh.text
        time_mm = self.ids.mins.text
        self.update_reminder_datetime()
        print(self.reminder_datetime)
        if time_hh == '' or time_mm == '':
            self.show_no_time_input_error_alert()
            return
        if self.ids.balremmodFL.time_spin_text != 'GMT' and int(time_hh) > 12:
            self.show_time_error_alert()
            return

        # return if date or time set by user is in the past
        current_datetime = datetime.now()
        current_date = date.today()
        if self.reminder_date < current_date:
            self.show_pastdate_error_alert()
            return
        if self.reminder_datetime <= current_datetime:
            self.show_pasttime_error_alert()
            return
        self.dismiss()
        BaseEntry().Balance_reminder_types.close_container_wid()
        App.get_running_app().bal_reminder_text = 'Custom Reminder Set'


"""Layout for user to make entries to Database"""
class BaseEntry(FloatLayout):
    reminder_text = 'Remind me'
    bal_reminder_fontsize = NumericProperty(defaultvalue=15)
    device_date = StringProperty()
    current_date = date.today()
    Balance_reminder_types = CustomPropBubble(orientation='vertical', arrow_pos='left_mid',
                                              pos_hint={'right': 0.87, 'top': 0.68}, size_hint=(0.15, 0.2))
    bal_rem_types = ['Hourly', 'Daily', 'Weekly', 'Monthly', 'Custom']
    Remindermodalview = BalReminderModalview()

    def on_touch_down(self, touch):
        '''Dealing with Balance Reminder Type Selection Bubble'''
        the_app = App.get_running_app()
        bal_rem_typ = self.Balance_reminder_types
        bub_act_text = self.Balance_reminder_types.bubble_active_text(touch)

        # Return 'Remind me' to inactive and close bubble when bubble is up,
        # user touches outside bubble and bubble has no active text
        if bal_rem_typ in self.children and not \
                bal_rem_typ.collide_point(*touch.pos) and \
                (the_app.bal_reminder_text == self.reminder_text or the_app.bal_reminder_text == 'Custom reminder'):
            self.parent.ids.balance_checkboxlabel.ids.checkbx.active = False
            return self.close_balremtypebubble()

        if bal_rem_typ in self.children and \
                bal_rem_typ.collide_point(*touch.pos):
            # Return 'Remind me' to inactive and close bubble when bubble is up,
            # user touches bubble arrow and bubble has no active text
            if bal_rem_typ._arrow_layout.collide_point(*touch.pos) and \
                    (the_app.bal_reminder_text == self.reminder_text or the_app.bal_reminder_text == 'Custom reminder'):
                self.parent.ids.balance_checkboxlabel.ids.checkbx.active = False
                return bal_rem_typ.close_ontouch_arrow(touch)
            # Close bubble when user touches bubble arrow
            if bal_rem_typ._arrow_layout.collide_point(*touch.pos):
                return bal_rem_typ.close_ontouch_arrow(touch)

            if bub_act_text is None:
                self.parent.ids.balance_checkboxlabel.ids.checkbx.active = False

            elif isinstance(bub_act_text, str):
                # Ensure BalanceCheckBox is active when 'Remind me' text updates chosen
                # bubble option to reminder type
                if not self.parent.ids.balance_checkboxlabel.ids.checkbx.active:
                    self.parent.ids.balance_checkboxlabel.ids.checkbx.active = True

                the_app.bal_reminder_text = bub_act_text + ' reminder'
                self.bal_reminder_fontsize = 13

                if bub_act_text == 'Custom':
                    self.Remindermodalview.open()

        super(BaseEntry, self).on_touch_down(touch)

    def usedevicedate(self, instance, value):
        if value:
            self.device_date = str(self.current_date.strftime("%d %B, %Y"))
        elif not value:
            self.device_date = ""

    def original_reminder_text_value(self):
        App.get_running_app().bal_reminder_text = 'Remind me'
        self.bal_reminder_fontsize = 15

    def handle_balremtypebubble(self, *args):
        if self.parent.ids.balance_checkboxlabel.active:
            # check that bubble has not been previously created
            if self.Balance_reminder_types not in self.children:
                # create bubble with CustomCheckBoxLabel
                self.create_balremtypebubble()
        if not self.parent.ids.balance_checkboxlabel.active:
            self.original_reminder_text_value()

    def create_balremtypebubble(self):
        for bal_rem_type in self.bal_rem_types:
            lbl = CustomCheckBoxLabel(text=bal_rem_type, group='bubble_group')
            self.Balance_reminder_types.add_widget(lbl)
        self.add_widget(self.Balance_reminder_types)

    def close_balremtypebubble(self):
        self.Balance_reminder_types.close_container_wid()

    def save_entry(self):
        entry_date = self.parent.ids.date.text
        entry_amount = self.parent.ids.amount.text
        entry_balance = self.parent.ids.balance.text
        entry_reminder = self.parent.ids.balance_checkboxlabel.text
        entry_comment = self.parent.ids.comment.text
        entry_quantity = self.parent.ids.quantity.text

        if App.get_running_app().bal_reminder_text == 'Custom Reminder Set':
            custom_reminder_date = self.Remindermodalview.reminder_datetime

        entry_type_sent = self.parent.ids.sent_checkboxlabel
        entry_type_received = self.parent.ids.received_checkboxlabel
        if entry_type_sent.active == True:
            entry_type_text = entry_type_sent.text
        elif entry_type_received.active == True:
            entry_type_text = entry_type_received.text

        if entry_date and entry_amount:
            if entry_type_sent.active == False and entry_type_received.active == False:
                return
            else:
                self.clear_widgets()
                self.parent.parent.current = 'savedentryscreen'

    def cancel_entry(self):
        self.parent.parent.current = 'databookscreatescreen'


class SavedEntry(FloatLayout):
    pass

class SavedEntryScreen(Screen):
    pass


class Sm(ScreenManager):
    def __init__(self):
        super(Sm, self).__init__()
        self.add_widget(LoginScreen(name='login'))
        self.add_widget(SignUpScreen(name='signup'))
        self.add_widget(ForgotPasswordScreen(name='forgotpassword'))


class Bsm(ScreenManager):
    def __init__(self):
        super(Bsm, self).__init__()
        self.add_widget(DataBooks_Create_Screen(name='databookscreatescreen'))
        self.add_widget(BaseEntryScreen(name='baseentryscreen'))
        self.add_widget(SavedEntryScreen(name='savedentryscreen'))


'''The Main App'''
class AppMainWindow(FloatLayout):
    def __init__(self, **kwargs):
        super(AppMainWindow, self).__init__(**kwargs)
        self.sm = Sm()
        self.bsm = Bsm()
        self.add_widget(self.sm)

    def base_entry_screen(self):
        self.clear_widgets()
        self.add_widget(self.bsm)


class PropApp(App):
    bal_reminder_text = StringProperty(defaultvalue='Remind me')

    def build(self):
        self.appmainwindow = AppMainWindow()

        return self.appmainwindow


if __name__ == '__main__':
    PropApp().run()