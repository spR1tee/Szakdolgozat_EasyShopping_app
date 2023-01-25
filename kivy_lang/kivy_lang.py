KV = """
WindowManager:
    LoginScreen:
    RegisterScreen:
    HomeScreen:

<HomeScreen>:
    name: "home"

<ClickableTextFieldRound>
    size_hint_y: None
    height: user_password.height
    text: user_password.text
    
    MDTextField:
        id: user_password
        hint_text: root.hint_text
        password: True
        pos_hint: {'center_x': 0.5}
        size_hint_x: None
        width: "300dp"
        icon_left: "key-variant"
    
    MDIconButton:
        icon: "eye-off"
        pos_hint: {"center_y": .5}
        pos: user_password.width - self.width + dp(8), 0
        theme_text_color: "Hint"
        on_release:
            self.icon = "eye" if self.icon == "eye-off" else "eye-off"
            user_password.password = False if user_password.password is True else True

<ClickableTextFieldRoundPasswordAgain>
    size_hint_y: None
    height: user_password_again.height
    text: user_password_again.text
    
    MDTextField:
        id: user_password_again
        hint_text: root.hint_text
        password: True
        pos_hint: {'center_x': 0.5}
        size_hint_x: None
        width: "300dp"
        icon_left: "key-variant"
    
    MDIconButton:
        icon: "eye-off"
        pos_hint: {"center_y": .5}
        pos: user_password_again.width - self.width + dp(8), 0
        theme_text_color: "Hint"
        on_release:
            self.icon = "eye" if self.icon == "eye-off" else "eye-off"
            user_password_again.password = False if user_password_again.password is True else True

<LoginScreen>:
    name: "login"
    
    MDCard:
        orientation: "vertical"
        size: root.width, root.height
        spacing: 10
        padding: 15
        elevation: 10
        md_bg_color: "white"
    
        FitImage:
            source: "img/logo.png"
            size_hint: None, None
            pos_hint: {'center_x': 0.5, 'center_y': 0.9}
            width: "200dp"
            height: "200dp"
        
        MDBoxLayout:
            orientation: "vertical"
            spacing: 10
            size_hint: None, None
            pos_hint: {'center_x': 0.5, 'center_y': 0.50}
            adaptive_height: True
            adaptive_width: True
            
            MDTextField:
                id: user_email
                hint_text: "E-mail cím"
                pos_hint: {'center_x': 0.5}
                size_hint_x: None
                width: "300dp"
                icon_left: "email"
            
            ClickableTextFieldRound:
                id: login_pw
                size_hint_x: None
                hint_text: "Jelszó"
                width: "300dp"
                pos_hint: {"center_x": 0.5}
                
            MDBoxLayout:
                orientation: "horizontal"
                pos_hint: {'center_x': 0.5}
                size_hint_x: None
                adaptive_height: True
                adaptive_width: False
                width: "300dp"
                spacing: "48dp"
                
                MDFillRoundFlatIconButton:
                    text: "Bejelentkezés"
                    icon: "login"
                    font_name: "fonts/Comfortaa-Regular.ttf"
                    size_hint: None, None
                    width: "300dp"
                    on_press: app.login()
                
                MDTextButton:
                    text: "Elfelejtett jelszó"
                    underline: True
                    font_name: "fonts/Comfortaa-Regular.ttf"
                    font_size: 12
                    size_hint: None, None
                
            MDLabel:
                text: "Ha még nincs fiókod, itt regisztrálhatsz egyet:"
                font_name: "fonts/Comfortaa-Regular.ttf"
                adaptive_height: True
                adaptive_width: False
                width: "300dp"
                font_size: 10
                size_hint: None, None
                halign: "center"
            
            MDFillRoundFlatIconButton:
                text: "Regisztráció"
                icon: "note"
                font_name: "fonts/Comfortaa-Regular.ttf"
                pos_hint: {'center_x': 0.5}
                size_hint: None, None
                width: "300dp"
                on_press:
                    app.root.current = "register"
                    root.manager.transition.direction = "right"
            
            MDLabel:
                text: "vagy"
                font_name: "fonts/Comfortaa-Regular.ttf"
                adaptive_height: True
                adaptive_width: False
                width: "300dp"
                font_size: 10
                size_hint: None, None
                halign: "center"
            
            MDFillRoundFlatIconButton:
                text: "Folytatás vendégként"
                font_name: "fonts/Comfortaa-Regular.ttf"
                pos_hint: {'center_x': 0.5}
                size_hint: None, None
                width: "300dp"
                on_press: app.join_as_guest()
    
<RegisterScreen>:
    name: "register"
    
    MDCard:
        orientation: "vertical"
        size: root.width, root.height
        spacing: 10
        padding: 15
        elevation: 10
        md_bg_color: "white"
    
        MDBoxLayout:
            orientation: "vertical"
            spacing: 10
            size_hint: None, None
            pos_hint: {'center_x': 0.5}
            adaptive_height: True
            adaptive_width: True
            md_bg_color: "white"
            
            MDBoxLayout:
                orientation: "horizontal"
                spacing: 15
                adaptive_height: True
                adaptive_width: True
            
                MDIconButton:
                    icon: "arrow-left"
                    size_hint: None, None
                    pos_hint: {'center_x': 0.5}
                    on_press: 
                        app.root.current = "login"
                        root.manager.transition.direction = "left"
                
                MDLabel:
                    text: "Regisztráció"
                    font_name: "fonts/Comfortaa-Regular.ttf"
                    adaptive_width: True
                    font_size: 15
            
            Widget:
                height: "100dp"
            
            MDTextField:
                id: user_email
                hint_text: "E-mail cím"
                helper_text: "Ezzel az E-mail címmel tudsz majd bejelentkezni"
                helper_text_mode: "on_focus"
                pos_hint: {'center_x': 0.5}
                size_hint_x: None
                width: "300dp"
                icon_left: "email"
            
            ClickableTextFieldRound:
                id: register_pw
                size_hint_x: None
                hint_text: "Jelszó"
                width: "300dp"
                pos_hint: {"center_x": 0.5}
                
            ClickableTextFieldRoundPasswordAgain:
                id: register_pw_again
                size_hint_x: None
                hint_text: "Jelszó újra"
                width: "300dp"
                pos_hint: {"center_x": 0.5}
            
            MDTextField:
                id: date_of_birth
                hint_text: "Születési dátum"
                pos_hint: {'center_x': 0.5}
                size_hint_x: None
                width: "300dp"
                icon_left: "calendar"
            
            MDTextField:
                id: username
                hint_text: "Felhasználónév"
                pos_hint: {'center_x': 0.5}
                size_hint_x: None
                width: "300dp"
                icon_left: "account"
            
            MDFillRoundFlatIconButton:
                text: "Regisztráció"
                icon: "note"
                font_name: "fonts/Comfortaa-Regular.ttf"
                pos_hint: {'center_x': 0.5}
                size_hint: None, None
                width: "300dp"
                on_press:
                    app.sign_up()
                    root.manager.transition.direction = "left"
"""