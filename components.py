from kivy.core.text.markup import MarkupLabel
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.list import OneLineAvatarIconListItem, ILeftBodyTouch, ThreeLineListItem
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.selectioncontrol import MDCheckbox


class PicListItem(OneLineAvatarIconListItem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def delete_item(self, item):
        app = MDApp.get_running_app()
        app.database.remove_cards(item.text)
        db_path = "images/" + app.database.userId + "/" + item.text + ".jpg"
        app.database.remove_from_storage(db_path)
        self.parent.remove_widget(item)
        toast("Kártya törölve!")


class ListItemWithCheckbox(OneLineAvatarIconListItem):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def mark(self, check, the_list_item):
        app = MDApp.get_running_app()
        if check.active:
            the_list_item.text = "[s]" + the_list_item.text + "[/s]"
            data = {MarkupLabel(the_list_item.text).markup[1]: 1}
            app.database.update_shopping_list(data)
        else:
            the_list_item.text = MarkupLabel(the_list_item.text).markup[1]
            data = {the_list_item.text: 0}
            app.database.update_shopping_list(data)

    def delete_item(self, check, the_list_item):
        app = MDApp.get_running_app()
        text = MarkupLabel(the_list_item.text).markup[1] if check.active else MarkupLabel(the_list_item.text).markup[0]
        app.database.remove_shopping_list_item(text)
        self.parent.remove_widget(the_list_item)


class ClickableTextFieldRound(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()


class ClickableTextFieldRoundPasswordAgain(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()


class ShopCard(MDCard):
    text = StringProperty()
    image = StringProperty()
    shop_name = StringProperty()
    icon = StringProperty()


class ForgottenPwContent(MDBoxLayout):
    pass


class DialogContent(MDBoxLayout):
    pass


class PicDialogContent(MDBoxLayout):
    pass


class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    pass


class ExpansionContent(MDBoxLayout):
    pass


class ThreeLineItem(ThreeLineListItem):
    lat = StringProperty()
    lon = StringProperty()
