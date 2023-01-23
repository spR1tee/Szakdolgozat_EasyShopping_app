KV = """
MDScreen:
    md_bg_color: "white"
    
    FitImage:
        source: "img/logo.png"
        size_hint: None, None
        pos_hint: {'center_x': 0.5, 'center_y': 0.85}
        width: "200dp"
        height: "200dp"
    
    MDBoxLayout:
        orientation: "vertical"
        spacing: 12
        size_hint: None, None
        pos_hint: {'center_x': 0.5, 'center_y': 0.40}
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
                width: root.width*0.4
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
            width: root.width*0.4
        
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
            width: root.width*0.4
"""