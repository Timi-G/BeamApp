from datetime import date, datetime
import locale
import re

from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.bubble import Bubble
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput

from kivycalendar3 import DatePicker


class CustomAccountNumbersTI(TextInput):
    locale.setlocale(locale.LC_ALL, '')

    def insert_text(self, substring, from_undo=False):
        '''get thousand seperator and decimal char. used by system #update this to global variables'''
        number_toget_locale = '1000.1'
        format_number_toget_locale = locale.format_string("%f", locale.atof(number_toget_locale), grouping=True)
        system_setthou = format_number_toget_locale[1]
        system_setdec = format_number_toget_locale[5]
        # float regex(no thousand seperator)>>> (u'^-?[0-9]*\\.?[0-9]*$')
        # float regex(thousand seperator(',')) >>> re.match((u'^-?[0-9]{,3},([0-9]{3,3},)*[0-9]{3,3}\\.?[0-9]{6,6}$') and
        # >>> re.match((u'^-?[0-9]{,3}\\.?[0-9]{6,6}$')
        # Ensure only numbers and dot can be entered to textinput
        if re.match((u'^[0-9.]*$'), substring):
            cc, cr = self.cursor
            # return, if first textinput is '0' and entered figure has '0' as well
            if self._lines[cr]=='0' and substring=='0':
                return
            # return, if textinput has a decimal point and entered figure as a decimal point as well
            if '.' in self._lines[cr] and '.' in substring:
                print('the dot place')
                return

            # (incase of paste) return, if entered figure is not a float with maximum of 6d.p
            '''#to be updated so user can paste float or integer with thousand seperator up to 6d.p'''
            if not re.match((u'^[0-9]*\\.?[0-9]{,6}$'), substring):
                '''#proposed update below'''
                # or not re.match((u'^-?[0-9]{,3},([0-9]{3,3},)*[0-9]{3,3}\\.?[0-9]{,6}$'), substring) \
                # or not re.match((u'^-?[0-9]{,3}\\.?[0-9]{,6}$'), substring):
                return

            # return if textinput has 6d.p and user tries to enter another number in decimal place
            if re.match((u"^-?[0-9]{,3}[\s,.]([0-9]{3,3}[\s,.])*[0-9]{3,3}\\.[0-9]{6,6}$"),self._lines[cr]) or re.match((u'^-?[0-9]{,3}\\.[0-9]{6,6}$'), self._lines[cr]):
                # checks if cursor position is around the filled 6d.p
                if cc in range(len(self._lines[cr])-6,len(self._lines[cr])+1):
                    return
            super(CustomAccountNumbersTI, self).insert_text(substring, from_undo=from_undo)
            cc, cr = self.cursor
            print(cc)
            print(locale.format_string("%f",locale.atof(self._lines[cr]),grouping=True))

            # convert self._lines to float and
            # format resulting numeric text to include thousand seperator
            new_text=locale.format_string("%f",locale.atof(self._lines[cr]), grouping=True)
            new_text_fmt=new_text

            # if user inputs '.', strip only trailing zeros
            if system_setdec in substring:
                 new_text=new_text.rstrip('0')
            else:
                 new_text=new_text.rstrip('0').rstrip(system_setdec)
            print(cc,cr,len(new_text),len(self._lines[cr]))

            # increase cursor column position to account for
            # thousand seperator included automatically in text
            ntext_thou=new_text.count(system_setthou)
            lines_thou=self._lines[cr].count(system_setthou)
            curs_adjus=ntext_thou-lines_thou
            if len(new_text)>len(self._lines[cr]):
                if ntext_thou>lines_thou:
                    new_cursor=list(self._cursor)
                    new_cursor[0]=new_cursor[0]+curs_adjus
                    self._cursor=tuple(new_cursor)
                    print('current2', cc)

            # so user can input '0' after decimal sign with no glitches
            # if user inputs tenth placed zero or decimal place zero greater than tenth
            finddecipos_lines=self._lines[cr].find(system_setdec)
            finddecipos_ntext= new_text_fmt.find(system_setdec)
            if '0' in substring and cc == len(new_text) + 2 and system_setdec in self._lines[cr] and cc == finddecipos_lines+2:
                    new_text = new_text + system_setdec + '0'
            elif '0' in substring and cc>finddecipos_lines+1 and system_setdec in self._lines[cr]:
                 new_text=new_text_fmt[:finddecipos_ntext]+self._lines[cr][finddecipos_lines:]


            # set line text with new_text
            self._set_line_text(cr, new_text)
            print('newest', cc)


class TimeTI(TextInput):
    # border_width= NumericProperty()

    def update_timeti_text(self, prev_text, entry, curs_pos):
        new_text = prev_text[:curs_pos] + entry + prev_text[curs_pos:]
        return new_text

    def time_hour_check(self, new_text, time_format):

        # am_pm_hr check
        if time_format != 'GMT':
            if int(new_text)>12:
                return False
        # GMT_hr check
        elif time_format == 'GMT':
            if int(new_text)>24:
                return False

    def time_mins_check(self, new_text):

        # minutes check
        if int(new_text)>59:
            return False

    def insert_text(self, substring, from_undo=False):
        cc, cr = self.cursor
        # Ensure only numbers 0-9 can be entered
        if not re.match((u'^[0-9]*$'), substring):
            return

        prev_text= self._lines[cr]
        latest_text= self.update_timeti_text(prev_text,substring,cc)
        # instantiating the spinner active text 'tfs' (TimeFormatSpin)
        # from FloatLayout used directly on Modal View
        '''Pending: to update how tfs is instantiated 
        as it comes from a seperate widget for better TimeTI future use'''
        tfs= self.parent.time_spin_text
        hr_bool_check= self.time_hour_check(latest_text, tfs)
        mins_bool_check= self.time_mins_check(latest_text)

        # for the 'hour text_input'
        if self.focus and self.hint_text=='hh':
            if hr_bool_check==False:
                return

        # for the 'minutes text_input'
        if self.focus and self.hint_text=='mm':
            if mins_bool_check==False:
                return
        return super(TimeTI, self).insert_text(substring, from_undo=from_undo)


class CustomSpinner(Spinner):

    def _update_dropdown_size(self, *largs):
        # set font_size of spinner options to that of main spinner button
        for item in self._dropdown.container.children[:]:
            item.font_size = self.font_size
        return super(CustomSpinner, self)._update_dropdown_size()


'''get thousand seperator and decimal char. used by system'''
# number_toget_locale= '1000.1'
# format_number_toget_locale=locale.format_string("%f", locale.atof(number_toget_locale), grouping=True)
# system_setthou= format_number_toget_locale[1]
# system_setdec= format_number_toget_locale[5]


class CustomCheckBoxLabel(ButtonBehavior, GridLayout):
    text= StringProperty()
    group= StringProperty()
    active_text= StringProperty()

    def on_active(self):
        if self.active:
            self.active_text= self.text
        else:
            self.active_text=''
        return super(CustomCheckBoxLabel, self).on_active(self)


'''A custom bubble that closes when touch is outside the bubble and
can give text of widget touched within the bubble using bubble_active_text'''
class CustomPropBubble(Bubble):

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            self.close_container_wid(touch)
        return super(CustomPropBubble, self).on_touch_down(touch)

    def bubble_active_text(self, touch):
        if self.collide_point(*touch.pos):
            for child in self.content.children:
                if child.collide_point(*touch.pos):
                    '''checkbox becomes active after touch event'''
                    if not child.active:
                        return child.text
                    elif child.active:
                        return None


    def close_ontouch_arrow(self, touch):
        if self._arrow_layout.collide_point(*touch.pos):
            self.clear_widgets()
            self.parent.remove_widget(self)

    def close_container_wid(self, *args, **kwargs):
        self.clear_widgets()
        self.parent.remove_widget(self)


class EntryDate(DatePicker):
    # change DatePicker original date format to custom date format
    def update_value(self, inst):
        super(EntryDate, self).update_value(self)
        ent_date = datetime.strptime(self.text, '%d.%m.%Y')
        self.text = str(ent_date.strftime("%d %B, %Y"))

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.parent.parent.ids.date_checkboxlabel.active:
                self.parent.parent.ids.date_checkboxlabel.ids.checkbx._do_press()
        return super(EntryDate, self).on_touch_down(touch)


class Balrem_date_picker(DatePicker):

    def init_ui(self):
        super(Balrem_date_picker, self).init_ui()
        # set the initial date format
        self.text = datetime.now().strftime("%d %b, %Y")

    # change DatePicker original date format to custom date format
    def update_value(self, inst):
        super(Balrem_date_picker, self).update_value(self)
        ent_date = datetime.strptime(self.text, '%d.%m.%Y')
        self.text = str(ent_date.strftime("%d %b, %Y"))