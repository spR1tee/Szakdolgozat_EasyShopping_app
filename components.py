from kivy.core.text.markup import MarkupLabel
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.list import OneLineAvatarIconListItem, ILeftBodyTouch
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.tab import MDTabsBase


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


class PicDialogContent(MDBoxLayout):
    pass


class PicListItem(OneLineAvatarIconListItem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def delete_item(self, item):
        app = MDApp.get_running_app()
        app.database.db.child("users").child(app.database.currently_logged_in_email).child(
            "cards").child(item.text).remove()
        db_path = "images/" + app.database.currently_logged_in_email + "/" + item.text + ".jpg"
        app.database.storage.delete(db_path)
        self.parent.remove_widget(item)


class ListItemWithCheckbox(OneLineAvatarIconListItem):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def mark(self, check, the_list_item):
        app = MDApp.get_running_app()
        if check.active:
            the_list_item.text = "[s]" + the_list_item.text + "[/s]"
            print(MarkupLabel(the_list_item.text).markup)
            data = {MarkupLabel(the_list_item.text).markup[1]: 1}
            app.database.db.child("users").child(app.database.currently_logged_in_email).child(
                "shopping_list").update(data)
        else:
            the_list_item.text = MarkupLabel(the_list_item.text).markup[1]
            data = {the_list_item.text: 0}
            app.database.db.child("users").child(app.database.currently_logged_in_email).child(
                "shopping_list").update(data)

    def delete_item(self, check, the_list_item):
        app = MDApp.get_running_app()
        text = MarkupLabel(the_list_item.text).markup[1] if check.active else MarkupLabel(the_list_item.text).markup[0]
        app.database.db.child("users").child(app.database.currently_logged_in_email).child(
            "shopping_list").child(text).remove()
        self.parent.remove_widget(the_list_item)


class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    pass


class ExpansionContent(MDBoxLayout):
    pass
