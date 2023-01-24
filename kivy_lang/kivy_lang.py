KV = """
WindowManager:
    LoginScreen:
    RegisterScreen:

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
            
            MDTextField:
                id: user_password
                hint_text: "Jelszó"
                password: True
                pos_hint: {'center_x': 0.5}
                size_hint_x: None
                width: "300dp"
                icon_left: "key-variant"
                
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
    
    MDBoxLayout:
        orientation: "vertical"
        spacing: 10
        size_hint: None, None
        pos_hint: {'center_x': 0.5}
        adaptive_height: True
        adaptive_width: True
        
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
            pos_hint: {'center_x': 0.5}
            size_hint_x: None
            width: "300dp"
            icon_left: "email"
        
        MDTextField:
            id: user_password
            hint_text: "Jelszó"
            pos_hint: {'center_x': 0.5}
            size_hint_x: None
            width: "300dp"
            icon_left: "key-variant"
            password: True
            
        MDTextField:
            id: user_password_again
            hint_text: "Jelszó újra"
            pos_hint: {'center_x': 0.5}
            size_hint_x: None
            width: "300dp"
            icon_left: "key-variant"
            password: True
        
        MDTextField:
            id: date_of_birth
            hint_text: "Születési dátum"
            pos_hint: {'center_x': 0.5}
            size_hint_x: None
            width: "300dp"
            icon_left: "calendar"
        
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