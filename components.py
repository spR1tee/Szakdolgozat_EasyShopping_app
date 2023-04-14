from kivy.core.text.markup import MarkupLabel
from kivy.properties import StringProperty, ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.list import OneLineAvatarIconListItem, ILeftBodyTouch
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.selectioncontrol import MDCheckbox


class ClickableTextFieldRound(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()
    pass


class ClickableTextFieldRoundPasswordAgain(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()
    pass


class ForgottenPwContent(MDBoxLayout):
    pass


class ShopCard(MDCard):
    text = StringProperty()
    image = StringProperty()
    shop_name = StringProperty()
    icon = StringProperty()
    pass


class DialogContent(MDBoxLayout):
    pass


class ListItemWithCheckbox(OneLineAvatarIconListItem):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def mark(self, check, the_list_item):
        app = MDApp.get_running_app()
        if check.active:
            the_list_item.text = "[s]" + the_list_item.text + "[/s]"
            print(MarkupLabel(the_list_item.text).markup)
            data = {MarkupLabel(the_list_item.text).markup[1]: 1}
            app.controller.db.child("users").child(app.controller.currently_logged_in_email).child(
                "shopping_list").update(data)
        else:
            the_list_item.text = MarkupLabel(the_list_item.text).markup[1]
            data = {the_list_item.text: 0}
            app.controller.db.child("users").child(app.controller.currently_logged_in_email).child(
                "shopping_list").update(data)

    def delete_item(self, check, the_list_item):
        app = MDApp.get_running_app()
        text = MarkupLabel(the_list_item.text).markup[1] if check.active else MarkupLabel(the_list_item.text).markup[0]
        app.controller.db.child("users").child(app.controller.currently_logged_in_email).child(
            "shopping_list").child(text).remove()
        self.parent.remove_widget(the_list_item)


class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    pass

class ExpansionContent(MDBoxLayout):
    pass