KV = """

WindowManager:
    LoginScreen:
    RegisterScreen:
    NavigationScreen:

<NavigationScreen>:
    name: "nav"
    
    MDBottomNavigation:
        id: bottom_nav
        selected_color_background: "red"
        use_text: False
            
        MDBottomNavigationItem:
            name: "home"
            icon: "home"
            
            MDBoxLayout:
                adaptive_size: True
                pos_hint: {"center_x": .5, "center_y": .5}
                
                MDTextField:
                    size_hint_x: None
                    width: "300dp"
                    pos_hint: {"center_x": .5, "center_y": .5}
            
        MDBottomNavigationItem:
            name: "shops"
            icon: "shopping"
            
            MDBoxLayout:
                adaptive_size: True
                md_bg_color: "blue"
                pos_hint: {"center_x": .5, "center_y": .5}
                
                MDFlatButton:
                    text: "helloszevasz"
                    pos_hint: {"center_x": 0.5, "center_y": 0.5}
                    on_release: app.notification_test()
            
        MDBottomNavigationItem:
            name: "profile"
            icon: "account"
            on_tab_press: app.check_if_registered()
            
            MDBoxLayout:
                adaptive_size: True
                md_bg_color: "green"
                pos_hint: {"center_x": .5, "center_y": .5}
                
                MDFlatButton:
                    text: "helloszia"
                    pos_hint: {"center_x": 0.5, "center_y": 0.5}
                    
        MDBottomNavigationItem:
            name: "cards"
            icon: "credit-card"
            # on_tab_press: app.check_if_registered()
            
            MDBoxLayout:
                adaptive_size: True
                md_bg_color: "green"
                pos_hint: {"center_x": .5, "center_y": .5}
                
                MDFlatButton:
                    text: "hellocsá"
                    pos_hint: {"center_x": 0.5, "center_y": 0.5}
        
        MDBottomNavigationItem:
            name: "favorites"
            icon: "heart"
            # on_tab_press: app.check_if_registered()
            
            MDBoxLayout:
                adaptive_size: True
                md_bg_color: "green"
                pos_hint: {"center_x": .5, "center_y": .5}
                
                MDFlatButton:
                    text: "hellocsákedvencek"
                    pos_hint: {"center_x": 0.5, "center_y": 0.5}
                    on_release: app.view_google()
                    
<ForgottenPwContent>
    spacing: "20dp"
    size_hint_y: None
    text: forgotten_pw_email.text
    height: "120dp"
    
    MDTextField:
        id: forgotten_pw_email
        pos_hint: {'center_x': 0.5}
        pos_hint: {'center_y': 0.5}
        size_hint: None, None
        width: "300dp"
        hint_text: "Add meg az e-mail címed"
        helper_text: "Erre az e-mail címre fogunk küldeni egy e-mailt"
        helper_text_mode: "on_focus"
              
                
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
                    on_release: app.login()
                
                MDTextButton:
                    text: "Elfelejtett jelszó"
                    underline: True
                    font_name: "fonts/Comfortaa-Regular.ttf"
                    font_size: 12
                    size_hint: None, None
                    on_release: app.forgotten_password()
                
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
                on_release:
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
                on_release: app.join_as_guest()
    
<RegisterScreen>:
    name: "register"
    
    ScrollView:
        bar_width: 0
        do_scroll_y: True
        
        MDBoxLayout:
            orientation: "vertical"
            size: root.width, root.height
            spacing: 10
            padding: 15
            elevation: 10
            md_bg_color: "white"
                
            MDBoxLayout:
                orientation: "horizontal"
                size_hint: None, None
                pos_hint: {'center_x': 0.4}
                spacing: 15
                adaptive_height: True
                adaptive_width: True
                
                MDIconButton:
                    icon: "arrow-left"
                    size_hint: None, None
                    pos_hint: {'center_x': 0.5}
                    on_release: 
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
                
            MDTextField:
                id: username
                hint_text: "Felhasználónév"
                pos_hint: {'center_x': 0.5}
                size_hint_x: None
                width: "300dp"
                icon_left: "account"
                
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
                    
            MDFillRoundFlatIconButton:
                text: "Születési dátum"
                icon: "calendar"
                font_name: "fonts/Comfortaa-Regular.ttf"
                pos_hint: {'center_x': 0.5}
                size_hint: None, None
                width: root.width*0.5
                on_release: app.show_date_picker()
                    
            MDBoxLayout:
                id: dob_box
                orientation: "vertical"
                size_hint: None, None
                adaptive_height: True
                adaptive_width: True
                pos_hint: {'center_x': 0.5}
                
            Widget:
                height: "100dp"
                
            MDFillRoundFlatIconButton:
                text: "Regisztráció"
                icon: "note"
                font_name: "fonts/Comfortaa-Regular.ttf"
                pos_hint: {'center_x': 0.5}
                size_hint: None, None
                width: "300dp"
                on_release:
                    app.sign_up()
                    root.manager.transition.direction = "left"
"""