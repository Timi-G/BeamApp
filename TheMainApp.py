from datetime import date, datetime
from multiprocessing import pool

from kivy.core.window import Window
from kivy.app import App
from kivy.animation import Animation
from kivy.base import runTouchApp
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import BooleanProperty,ColorProperty,ListProperty,\
                            NumericProperty,ObjectProperty,StringProperty
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
    CustomCheckBoxLabel,CustomPropBubble, \
    DatePicker, EntryDate, TimeTI, CustomSpinner

import DBEnd as de


kivyfiles= ['proplogin.kv']
for k in kivyfiles:
    Builder.load_file(k)


databooknames = []
con = de.con_db('Databook.db')

# func's arg is a list containing 2_dim array sublist of data_name & data_category
def ui_dbl_names(dblist):
    # unpack list & seperate date, data_names from data_category
    dbl= list(zip(*dblist))
    if dbl != []:
        dbnames = list(dbl[1])
    else:
        dbnames = []
    return dbnames

def add_databookname(dbn_mem,add_db):
    dbn_mem.append(add_db)
    print('this is', databooknames)

def remove_databookname(dblist_mem, rem_db):
    dblist_mem.remove(rem_db)

# databooknames derived from sql database
def f_databooknames(con):
    de.create_databookdb(con)
    return

# update databooknames in sql database
def update_dbnames(dbn):
    global con

    print('got to update',dbn)
    de.clear_dbdb(con)
    de.insert_in_dbdb(con,dbn)
    de.com_db(con,'DataBooks')
    con.close()
    return


"""Login, Signup & ForgotPassword Screen"""
class LoginScreen(Screen):
    pass

class SignUpScreen(Screen):
    pass

class ForgotPasswordScreen(Screen):
    pass

class BaseEntryScreen(Screen):
    pass
    # bal_reminder_text = App.get_running_app().bal_reminder_text
    #
    # def __init__(self, **kwargs):
    #     Clock.schedule_once(App.get_running_app().sm.bal_reminder_text)
    #     super(BaseEntryScreen, self).__init__(**kwargs)
    #     self.bal_reminder_text = App.get_running_app().bal_reminder_text

class AddEntrySign(ButtonBehavior, Image):
    pass

class MainLabels(ButtonBehavior,GridLayout):
    pass

class MainOptionsPage(Screen):
    pass

class DataBooks_ZeroEntryPage(FloatLayout):

    def create_first_databook(self):
        create_databook= DataBook_Create_MV()
        create_databook.open()

    def remove_zero_self(self):
        self.parent.remove_widget(self)

class DataBooks_AddEntry(FloatLayout):
    wid_con_names=ListProperty()

    def __init__(self):
        super(DataBooks_AddEntry, self).__init__()

    def widget_as_list(self, **kwargs):
        self.wid_con_names = ui_dbl_names(databooknames)
        wcnames=self.wid_con_names
        self.dbooklayout= GridLayout(rows= 5, size_hint=(0.8, None))

        # change MainLabels to more appropriate widget for a list menu
        for databookname in wcnames:
            self.dbooklayout.add_widget(MainLabels(text=databookname,img= 'App Images/Data Book Image.jpeg',
                                                   size_hint= (0.6,0.25)))
        self.dbooklayout.add_widget(MainLabels(text='Add New DataBook', img= 'App Images/Green add.jpg',
                                               size_hint= (0.2,0.25)))

    def widget_as_grid(self, **kwargs):
        self.wid_con_names = ui_dbl_names(databooknames)
        wcnames = self.wid_con_names
        print('got here at grid', wcnames)
        wcimages = ['App Images/Data Book Image.jpeg']
        scroll_view_width= Window.width*(1-2/5)
        scroll_view_height= Window.height*(1-2/6)
        cont_wid_width= Window.height*(1/6)
        cont_wid_height= Window.height*(1/5)
        self.scroll_view= ScrollView(size_hint=(0.8,None), pos_hint= {'x':0.2,'y':0.15}, size=(scroll_view_width,scroll_view_height))
        # self.dbooklayout= SubMainOptionsPage(cols=3, size_hint_y=None, spacing=[40,40], col_default_width=cont_wid_width,
        #                               row_default_height= cont_wid_height,row_force_default=True,col_force_default= True,
        #                               items_name=wcnames,items_image=wcimages,add_new_opt_image='App Images/Green add.jpg',
        #                             add_new_opt_text='Add New DataBook',add_new_opt_color=(0,0.5,0,0.8))
        self.dbooklayout_less = GridLayout(cols=3, size_hint_y=None, spacing=[40,40], col_default_width=cont_wid_width,
                                      row_default_height= cont_wid_height,row_force_default=True,col_force_default= True)
        dbl= self.dbooklayout_less
        scrlv= self.scroll_view
        dbll=Button(text='Wheel',size_hint=(0.5,0.5),pos_hint={'x':0.2,'y':0.1})

        # dbl.adding_new_widgets()
        for (wcname, image) in zip(wcnames, wcimages*len(wcnames)):
            dbl.add_widget(MainLabels(text=wcname, img=image,img_size=(1,0.75),lbl_size=(1,0.25), lbl_font_size=13,
                                      lbl_padding=(5,5),width=cont_wid_width, height=cont_wid_height))
        dbl.add_widget(MainLabels(text='Add New DataBook', img='App Images/Green add.jpg',text_color=(0,0.5,0,0.8),img_size=(1,0.75),
                                  lbl_size=(1,0.25), lbl_font_size=13,lbl_padding=(5,5),width=cont_wid_width, height=cont_wid_height))
        # dbl.bind(minimum_height= dbl.setter('height'))
        # dbl._trigger_layout()
        self.add_widget(dbll)
        # scrlv.add_widget(dbl)
        # self.add_widget(scrlv)

class DataBooks_Create_Screen(Screen):
    # swe= []
    display_format_options= ['List', 'Grid']
    display_format= 'Grid'
    dat_zeroentpage = DataBooks_ZeroEntryPage()
    dat_addentry = DataBooks_AddEntry()

    def __init__(self,**kwargs):
        self.dbns = ui_dbl_names(databooknames)
        super(DataBooks_Create_Screen, self).__init__(**kwargs)

    def screen_organizer(self):
        if len(self.dbns) == 0:
            print('zero place')
            self.dat_zero_ent_page()
        if len(self.dbns) > 0:
            if self.dat_zeroentpage:
                self.dat_zeroentpage.remove_zero_self()
            self.dat_ent_page()

    def dat_zero_ent_page(self):
        self.add_widget(self.dat_zeroentpage)

    def dat_ent_page(self):
        if self.display_format=='Grid':
            self.dat_addentry.widget_as_grid()
            self.add_widget(self.dat_addentry)

        elif self.display_format=='List':
            self.add_widget(self.dat_addentry)
            self.dat_addentry.widget_as_list()


# Scrollable Editable Grid/List Option_icons layout
class SubMainOptionsPage(GridLayout):
    # items_name = ListProperty()
    # items_images = ListProperty()
    # icon_img_size = ListProperty([1, 0.75])
    # icon_lbl_size = ListProperty([1, 0.25])
    # icon_lbl_font_size = NumericProperty(13)
    # add_new_opt_image = StringProperty()
    # add_new_opt_text = StringProperty()
    # add_new_opt_color = ColorProperty()

    def __init__(self,**kwargs):
        self.cols = 2
        self.items_name = ['']
        self.items_images = ['']
        self.icon_img_size = [1, 0.75]
        self.icon_lbl_size = [1, 0.25]
        self.icon_lbl_font_size = 13
        self.add_new_opt_image = ''
        self.add_new_opt_text = ''
        self.add_new_opt_color = [None,None,None,None]
        super(SubMainOptionsPage, self).__init__()

    def adding_new_widgets(self):
        inames=self.items_name
        iimgs= self.items_images
        ilbl_size= self.icon_lbl_size
        iimg_size=self.icon_img_size
        ilbl_font_size=self.icon_lbl_font_size

        # loop for adding each option_icon to layout
        for (name, img) in zip(inames, iimgs*len(inames)):
            self.add_widget(MainLabels(text=name, img=img,img_size=iimg_size,lbl_size=ilbl_size,lbl_font_size=ilbl_font_size,
                                      lbl_padding=(5,5)))
        self.add_widget(MainLabels(text=self.add_new_opt_text, img=self.add_new_opt_image,text_color=self.add_new_opt_color,
                                   img_size=iimg_size,lbl_size=ilbl_size, lbl_font_size=ilbl_font_size,lbl_padding=(5,5)))


# MV to create a new DataBook
class DataBook_Create_MV(ModalView):
    data_category=['Business','Medical','Personal']

# databooks are created by name and category
    def save_ok_button(self):
        self.dbook_name= self.ids.dbcreateti.text
        self.dbook_cat= self.ids.dbcreatespinner.text

        dbd= datetime.now()
        dbn= self.dbook_name
        dbc= self.dbook_cat
        new_databook=  [f'{dbd}',dbn,dbc]
        dbns= databooknames

        print(new_databook)
        add_databookname(dbns,new_databook)

        # for first entry
        if len(dbns) == 1:
            f_databooknames(con)
        update_dbnames(dbns)
        self.dismiss()
        DataBooks_Create_Screen().screen_organizer()

    def cancel_button(self):
        self.dismiss()

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


# MV for balance reminder
class BalReminderModalview(ModalView):
    # find out how to accept the complete date and time chosen by user and store in a variable
    # string is proposed, which will be converted to datetime format
    dismiss_choice = StringProperty()

    def show_no_time_input_error_alert(self):
        anim= Animation(opacity=1, duration=2)+Animation(opacity=0, duration=1.5)
        anim2= Animation(foreground_color = [0.8,0.2,0.2,0.5], border_width=1,duration=2)\
               +Animation(foreground_color = [0,0,0,1], border_width=0.1,duration=1.5)
        anim3= Animation(foreground_color = [0.8,0.2,0.2,0.5],border_width=1 ,duration=2)\
               +Animation(foreground_color = [0,0,0,1],border_width=0.1 ,duration=1.5)
        anim.start(self.ids.no_time_input_error_alert)
        anim2.start(self.ids.hh)
        anim3.start(self.ids.mins)

    def show_time_error_alert(self):
        anim= Animation(opacity=1, duration=2)+Animation(opacity=0, duration=1.5)
        anim2= Animation(foreground_color = [0.8,0.2,0.2,0.5], border_width=1,duration=2)\
               +Animation(foreground_color = [0,0,0,1], border_width=0.1,duration=1.5)
        anim3= Animation(border_color = [0.8,0.2,0.2,0.5],border_width=1 ,duration=2)\
               +Animation(border_color = [0,0,0,0.5],border_width=0.1 ,duration=1.5)
        anim.start(self.ids.time_error_alert)
        anim2.start(self.ids.hh)
        anim3.start(self.ids.timespinner)

    def show_pastdate_error_alert(self):
        anim= Animation(opacity=1, duration=2)+Animation(opacity=0, duration=1.5)
        anim2= Animation(foreground_color = [0.8,0.2,0.2,0.5], border_width=1,duration=2)\
               +Animation(foreground_color = [0,0,0,1], border_width=0.1,duration=1.5)
        anim.start(self.ids.past_error_alert)
        anim2.start(self.ids.rem_date_picker)

    def show_pasttime_error_alert(self):
        anim= Animation(opacity=1, duration=2)+Animation(opacity=0, duration=1.5)
        anim2= Animation(foreground_color = [0.8,0.2,0.2,0.5], border_width=1,duration=2)\
               +Animation(foreground_color = [0,0,0,1], border_width=0.1,duration=1.5)
        anim3= Animation(foreground_color = [0.8,0.2,0.2,0.5],border_width=1 ,duration=2)\
               +Animation(foreground_color = [0,0,0,1],border_width=0.1 ,duration=1.5)
        anim.start(self.ids.past_error_alert)
        anim2.start(self.ids.hh)
        anim3.start(self.ids.mins)

    def update_reminder_datetime(self):
        date_dmy= datetime.strptime(self.ids.rem_date_picker.text, '%d %b, %Y')
        date_y= int(date_dmy.strftime("%Y"))
        date_m= int(date_dmy.strftime("%m"))
        date_d= int(date_dmy.strftime("%d"))
        time_hh= self.ids.hh.text
        time_mm= self.ids.mins.text
        if time_hh == '':
            time_hh=0
        else:
            time_hh = int(self.ids.hh.text)
        if time_mm == '':
            time_mm=0
        else:
            time_mm = int(self.ids.mins.text)

        # if self.ids.timespinner.text == 'PM':
        #     time_hh = time_hh+12

        # reminder_time= str(time_hh) + ':' + str(time_mm)
        # reminder_date= self.ids.rem_date_picker.text
        # reminder_datetime= reminder_date + ' ' + reminder_time
        # self.reminder_date=reminder_date
        # self.reminder_datetime=reminder_datetime
        ndate_dmyhm= datetime(date_y, date_m, date_d, time_hh, time_mm)
        ndate_dmy= date(date_y, date_m, date_d)
        self.reminder_datetime= ndate_dmyhm
        self.reminder_date= ndate_dmy

    def cancel_button(self):
        self.dismiss_choice = 'Cancel'
        dc = self.dismiss_choice
        self.ids.hh.text= ''
        self.ids.mins.text= ''
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
        current_datetime= datetime.now()
        current_date= date.today()
        if self.reminder_date < current_date:
            self.show_pastdate_error_alert()
            return
        if self.reminder_datetime <= current_datetime:
            self.show_pasttime_error_alert()
            return
        self.dismiss()
        BaseEntry().Balance_reminder_types.close_container_wid()
        App.get_running_app().bal_reminder_text= 'Custom Reminder Set'


"""Layout for user to make entries to Database"""
class BaseEntry(FloatLayout):
    reminder_text= 'Remind me'
    # bal_reminder_text = StringProperty(defaultvalue=reminder_text)
    bal_reminder_fontsize = NumericProperty(defaultvalue=15)
    device_date = StringProperty()
    current_date = date.today()
    Balance_reminder_types = CustomPropBubble(orientation='vertical', arrow_pos='left_mid',
                                              pos_hint={'right': 0.87, 'top': 0.68}, size_hint= (0.15, 0.2))
    bal_rem_types = ['Hourly', 'Daily', 'Weekly', 'Monthly', 'Custom']
    Remindermodalview = BalReminderModalview()

    def on_touch_down(self, touch):
        '''Dealing with Balance Reminder Type Selection Bubble'''
        the_app= App.get_running_app()
        bal_rem_typ= self.Balance_reminder_types
        bub_act_text= self.Balance_reminder_types.bubble_active_text(touch)

        # Return 'Remind me' to inactive and close bubble when bubble is up,
        # user touches outside bubble and bubble has no active text
        if bal_rem_typ in self.children and not\
            bal_rem_typ.collide_point(*touch.pos) and \
            (the_app.bal_reminder_text==self.reminder_text or the_app.bal_reminder_text=='Custom reminder'):
            self.parent.ids.balance_checkboxlabel.ids.checkbx.active = False
            return self.close_balremtypebubble()

        if bal_rem_typ in self.children and \
            bal_rem_typ.collide_point(*touch.pos):
            # Return 'Remind me' to inactive and close bubble when bubble is up,
            # user touches bubble arrow and bubble has no active text
            if bal_rem_typ._arrow_layout.collide_point(*touch.pos) and \
                (the_app.bal_reminder_text==self.reminder_text or the_app.bal_reminder_text=='Custom reminder'):
                self.parent.ids.balance_checkboxlabel.ids.checkbx.active = False
                return bal_rem_typ.close_ontouch_arrow(touch)
            # Close bubble when user touches bubble arrow
            if bal_rem_typ._arrow_layout.collide_point(*touch.pos):
                return bal_rem_typ.close_ontouch_arrow(touch)

            if bub_act_text is None:
                self.parent.ids.balance_checkboxlabel.ids.checkbx.active= False
                # self.ids.balance_checkboxlabel.ids.checkbx._do_press()

            elif isinstance(bub_act_text,str):
                #Ensure BalanceCheckBox is active when 'Remind me' text updates chosen
                # bubble option to reminder type
                if not self.parent.ids.balance_checkboxlabel.ids.checkbx.active:
                    self.parent.ids.balance_checkboxlabel.ids.checkbx.active= True

                the_app.bal_reminder_text= bub_act_text +' reminder'
                self.bal_reminder_fontsize= 13

                if bub_act_text == 'Custom':
                    self.Remindermodalview.open()
                    # Balrem_date_picker().show_popup(self,val=True)
                    # self.bal_reminder_text= 'Reminder: ' + str(Balrem_date_picker().text)
                # print(self.Balance_reminder_types.bubble_active_text(touch) +' reminder')

        # if self.Balance_reminder_types.final_active_text_status=='unavailable':
        #     self.ids.balance_checkboxlabel.ids.checkbx.active = False
        #     self.Balance_reminder_types.final_active_text_status= 'available'

        super(BaseEntry, self).on_touch_down(touch)
    
    def usedevicedate(self, instance, value):
        if value:
            self.device_date= str(self.current_date.strftime("%d %B, %Y"))
        #     self.cal.active_date= str(self.current_date.strftime("%d %B, %Y"))
        elif not value:
            self.device_date = ""

    def original_reminder_text_value(self):
        App.get_running_app().bal_reminder_text = 'Remind me'
        self.bal_reminder_fontsize = 15

    def handle_balremtypebubble(self, *args):
        if self.parent.ids.balance_checkboxlabel.active:
            #check that bubble has not been previously created
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

    # def on_Balance_reminder_types(self, touch, **kwargs):
    #     self.bal_reminder_set_text=self.Balance_reminder_types.balance_active_text(touch)

    def save_entry(self):
        entry_date= self.parent.ids.date.text
        entry_amount= self.parent.ids.amount.text
        entry_balance= self.parent.ids.balance.text
        entry_reminder= self.parent.ids.balance_checkboxlabel.text
        entry_comment= self.parent.ids.comment.text
        entry_quantity= self.parent.ids.quantity.text

        if App.get_running_app().bal_reminder_text=='Custom Reminder Set':
            custom_reminder_date = self.Remindermodalview.reminder_datetime

        entry_type_sent= self.parent.ids.sent_checkboxlabel
        entry_type_received= self.parent.ids.received_checkboxlabel
        if entry_type_sent.active==True:
            entry_type_text= entry_type_sent.text
        elif entry_type_received.active==True:
            entry_type_text= entry_type_received.text

        if entry_date and entry_amount:
            if entry_type_sent.active== False and entry_type_received.active== False:
                print('it got here if')
                return
            else:
                print('it got here else')
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
        self.add_widget(MainOptionsPage(name='mainoptionsscreen'))
        self.add_widget(DataBooks_Create_Screen(name='databookscreatescreen'))
        self.add_widget(BaseEntryScreen(name='baseentryscreen'))
        self.add_widget(SavedEntryScreen(name='savedentryscreen'))


class AppMainWindow(FloatLayout):
    def __init__(self, **kwargs):
        super(AppMainWindow, self).__init__(**kwargs)
        self.sm= Sm()
        self.bsm= Bsm()
        self.add_widget(self.sm)

    def base_entry_screen(self):
        self.clear_widgets()
        print('now we are here')
        self.add_widget(self.bsm)


'''The Main App'''
class PropApp(App):
    bal_reminder_text= StringProperty(defaultvalue='Remind me')

    def build(self):
        self.appmainwindow= AppMainWindow()

        return self.appmainwindow


if __name__ == '__main__':
    PropApp().run()