import sqlite3
from datetime import datetime
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button

# --- VERİTABANI İŞLEMLERİ ---
def init_db():
    conn = sqlite3.connect('health_monitor.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS medications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, category TEXT, 
                    description TEXT, is_active TEXT, notes TEXT, daily_dose TEXT, meal_type TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS bp_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, 
                    sys TEXT, dia TEXT, pulse TEXT, note TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS med_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, 
                    med_name TEXT, meal_type TEXT)''')
    
    c.execute("INSERT OR IGNORE INTO categories (name) VALUES ('Ağrı Kesici')")
    c.execute("INSERT OR IGNORE INTO categories (name) VALUES ('Antibiyotik')")
    conn.commit()
    conn.close()

# --- KIVY ARAYÜZ TASARIMI (KV dili) ---
KV = '''
ScreenManager:
    MainMenu:
    MedMenuScreen:
    MedicationScreen:
    MedListScreen:
    TrackingMenuScreen:
    BpTrackingScreen:
    MedTrackingScreen:
    LogMenuScreen:
    BpLogScreen:
    MedLogScreen:

<MainMenu>:
    name: 'main'
    BoxLayout:
        orientation: 'vertical'
        padding: 30
        spacing: 20
        Label:
            text: 'Sağlık Monitörü'
            font_size: '36sp'
        Button:
            text: '1. İlaç Yönetimi (Ekle/Düzenle)'
            font_size: '22sp'
            size_hint_y: None
            height: 120
            on_release: root.manager.current = 'med_menu'
        Button:
            text: '2. Veri Girişi (Tansiyon / İlaç)'
            font_size: '22sp'
            size_hint_y: None
            height: 120
            on_release: root.manager.current = 'tracking_menu'
        Button:
            text: '3. Kayıtları İzle (Loglar)'
            font_size: '22sp'
            size_hint_y: None
            height: 120
            on_release: root.manager.current = 'log_menu'

<MedMenuScreen>:
    name: 'med_menu'
    BoxLayout:
        orientation: 'vertical'
        padding: 40
        spacing: 30
        Label:
            text: 'İlaç Yönetimi'
            font_size: '32sp'
        Button:
            text: 'Yeni İlaç Ekle'
            font_size: '24sp'
            size_hint_y: None
            height: 120
            on_release: 
                root.manager.get_screen('medication').reset_form()
                root.manager.current = 'medication'
        Button:
            text: 'Kayıtlı İlaçları Düzenle'
            font_size: '24sp'
            size_hint_y: None
            height: 120
            on_release: root.manager.current = 'med_list'
        Button:
            text: 'Ana Menüye Dön'
            font_size: '24sp'
            size_hint_y: None
            height: 120
            on_release: root.manager.current = 'main'

<MedListScreen>:
    name: 'med_list'
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 10
        Label:
            text: 'Kayıtlı İlaçlar (Aktifler Üstte)'
            font_size: '26sp'
            size_hint_y: None
            height: 60
        GridLayout:
            cols: 4
            size_hint_y: None
            height: 60
            canvas.before:
                Color:
                    rgba: 0.2, 0.2, 0.2, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
            Label:
                text: 'İlaç Adı'
                bold: True
                font_size: '16sp'
            Label:
                text: 'Kategori'
                bold: True
                font_size: '16sp'
            Label:
                text: 'Durum'
                bold: True
                font_size: '16sp'
            Label:
                text: 'İşlem'
                bold: True
                font_size: '16sp'
        ScrollView:
            GridLayout:
                id: med_grid
                cols: 4
                size_hint_y: None
                height: self.minimum_height
                row_default_height: 80
                row_force_default: True
                spacing: 5
        Button:
            text: 'Geri Dön'
            font_size: '24sp'
            size_hint_y: None
            height: 100
            on_release: root.manager.current = 'med_menu'

<MedicationScreen>:
    name: 'medication'
    ScrollView:
        BoxLayout:
            orientation: 'vertical'
            padding: 15
            spacing: 15
            size_hint_y: None
            height: self.minimum_height
            
            Label:
                id: screen_title
                text: 'Yeni İlaç Ekle'
                font_size: '28sp'
                size_hint_y: None
                height: 60
            TextInput:
                id: med_name
                hint_text: 'İlaç Adı'
                font_size: '22sp'
                multiline: False
                size_hint_y: None
                height: 120
            BoxLayout:
                spacing: 10
                size_hint_y: None
                height: 120
                Spinner:
                    id: category_spinner
                    text: 'Kategori Seç'
                    font_size: '20sp'
                    values: root.get_categories()
                Spinner:
                    id: status_spinner
                    text: 'Aktif'
                    font_size: '20sp'
                    values: ['Aktif', 'Pasif']
                Spinner:
                    id: meal_spinner
                    text: 'Aç'
                    font_size: '20sp'
                    values: ['Aç', 'Tok', 'Farketmez']
            TextInput:
                id: new_category
                hint_text: 'Veya Yeni Kategori Yaz'
                font_size: '22sp'
                multiline: False
                size_hint_y: None
                height: 120
            TextInput:
                id: daily_dose
                hint_text: 'Günlük Doz (Örn: 2)'
                font_size: '22sp'
                input_filter: 'int'
                multiline: False
                size_hint_y: None
                height: 120
            TextInput:
                id: notes
                hint_text: 'Özel Notlar'
                font_size: '22sp'
                multiline: False
                size_hint_y: None
                height: 120
            TextInput:
                id: description
                hint_text: 'Açıklama (Ne işe yarar?)'
                font_size: '22sp'
                multiline: True
                size_hint_y: None
                height: 180
            BoxLayout:
                spacing: 10
                size_hint_y: None
                height: 120
                Button:
                    id: save_btn
                    text: 'Kaydet'
                    font_size: '24sp'
                    background_color: (0.2, 0.7, 0.3, 1)
                    on_release: root.save_medication()
                Button:
                    text: 'İptal / Geri'
                    font_size: '24sp'
                    on_release: root.manager.current = 'med_menu'

<TrackingMenuScreen>:
    name: 'tracking_menu'
    BoxLayout:
        orientation: 'vertical'
        padding: 40
        spacing: 30
        Label:
            text: 'Ne girmek istersiniz?'
            font_size: '28sp'
        Button:
            text: 'Tansiyon Değeri Gir'
            font_size: '24sp'
            size_hint_y: None
            height: 120
            on_release: root.manager.current = 'bp_tracking'
        Button:
            text: 'İlaç Kullanımı Gir'
            font_size: '24sp'
            size_hint_y: None
            height: 120
            on_release: root.manager.current = 'med_tracking'
        Button:
            text: 'Ana Menüye Dön'
            font_size: '24sp'
            size_hint_y: None
            height: 120
            on_release: root.manager.current = 'main'

<BpTrackingScreen>:
    name: 'bp_tracking'
    ScrollView:
        BoxLayout:
            orientation: 'vertical'
            padding: 20
            spacing: 15
            size_hint_y: None
            height: self.minimum_height
            
            Label:
                text: 'Tansiyon Ekle'
                font_size: '32sp'
                size_hint_y: None
                height: 80
            TextInput:
                id: sys_input
                hint_text: 'Büyük Tansiyon (Örn: 120)'
                font_size: '24sp'
                input_filter: 'int'
                size_hint_y: None
                height: 120
            TextInput:
                id: dia_input
                hint_text: 'Küçük Tansiyon (Örn: 80)'
                font_size: '24sp'
                input_filter: 'int'
                size_hint_y: None
                height: 120
            TextInput:
                id: pulse_input
                hint_text: 'Nabız'
                font_size: '24sp'
                input_filter: 'int'
                size_hint_y: None
                height: 120
            TextInput:
                id: bp_note
                hint_text: 'Açıklama / Notunuz'
                font_size: '24sp'
                size_hint_y: None
                height: 120
            Button:
                text: 'KAYDET'
                font_size: '28sp'
                background_color: (0.2, 0.7, 0.3, 1)
                size_hint_y: None
                height: 120
                on_release: root.save_bp()
            Button:
                text: 'Geri Dön'
                font_size: '24sp'
                size_hint_y: None
                height: 120
                on_release: root.manager.current = 'tracking_menu'

<MedTrackingScreen>:
    name: 'med_tracking'
    ScrollView:
        BoxLayout:
            orientation: 'vertical'
            padding: 20
            spacing: 15
            size_hint_y: None
            height: self.minimum_height
            
            Label:
                text: 'İlaç İçildi Kaydı'
                font_size: '32sp'
                size_hint_y: None
                height: 80
            Spinner:
                id: med_select_spinner
                text: 'İlaç Seç (Sadece Aktifler)'
                font_size: '24sp'
                values: root.get_active_meds()
                size_hint_y: None
                height: 120
            Spinner:
                id: usage_meal_spinner
                text: 'Aç'
                font_size: '24sp'
                values: ['Aç', 'Tok']
                size_hint_y: None
                height: 120
            Button:
                text: 'İÇİLDİ OLARAK KAYDET'
                font_size: '28sp'
                background_color: (0.2, 0.7, 0.3, 1)
                size_hint_y: None
                height: 120
                on_release: root.save_med_log()
            Button:
                text: 'Geri Dön'
                font_size: '24sp'
                size_hint_y: None
                height: 120
                on_release: root.manager.current = 'tracking_menu'

<LogMenuScreen>:
    name: 'log_menu'
    BoxLayout:
        orientation: 'vertical'
        padding: 40
        spacing: 30
        Label:
            text: 'Hangi kayıtları görmek istersiniz?'
            font_size: '28sp'
        Button:
            text: 'Tansiyon Kayıtları'
            font_size: '24sp'
            size_hint_y: None
            height: 120
            on_release: root.manager.current = 'bp_logs'
        Button:
            text: 'İlaç Kullanım Kayıtları'
            font_size: '24sp'
            size_hint_y: None
            height: 120
            on_release: root.manager.current = 'med_logs'
        Button:
            text: 'Ana Menüye Dön'
            font_size: '24sp'
            size_hint_y: None
            height: 120
            on_release: root.manager.current = 'main'

<BpLogScreen>:
    name: 'bp_logs'
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 10
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: 270
            spacing: 5
            Label:
                text: 'Başlangıç Tarihi:'
                font_size: '18sp'
                bold: True
                size_hint_y: None
                height: 35
                text_size: self.size
                halign: 'left'
                valign: 'middle'
            BoxLayout:
                spacing: 5
                size_hint_y: None
                height: 60
                Spinner:
                    id: start_y
                    values: root.get_years()
                Spinner:
                    id: start_m
                    values: root.get_months()
                Spinner:
                    id: start_d
                    values: root.get_days()
            Label:
                text: 'Bitiş Tarihi:'
                font_size: '18sp'
                bold: True
                size_hint_y: None
                height: 35
                text_size: self.size
                halign: 'left'
                valign: 'middle'
            BoxLayout:
                spacing: 5
                size_hint_y: None
                height: 60
                Spinner:
                    id: end_y
                    values: root.get_years()
                Spinner:
                    id: end_m
                    values: root.get_months()
                Spinner:
                    id: end_d
                    values: root.get_days()
            Button:
                text: 'FİLTREYİ UYGULA'
                font_size: '22sp'
                background_color: (0.1, 0.5, 0.8, 1)
                size_hint_y: None
                height: 70
                on_release: root.load_logs()
        GridLayout:
            cols: 5
            size_hint_y: None
            height: 60
            canvas.before:
                Color:
                    rgba: 0.2, 0.2, 0.2, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
            Label: 
                text: 'Tarih'
                bold: True
            Label: 
                text: 'Büyük'
                bold: True
            Label: 
                text: 'Küçük'
                bold: True
            Label: 
                text: 'Nabız'
                bold: True
            Label: 
                text: 'Not'
                bold: True
        ScrollView:
            GridLayout:
                id: bp_grid
                cols: 5
                size_hint_y: None
                height: self.minimum_height
                row_default_height: 60
                row_force_default: True
                spacing: 2
        Button:
            text: 'Geri Dön'
            font_size: '24sp'
            size_hint_y: None
            height: 100
            on_release: root.manager.current = 'log_menu'

<MedLogScreen>:
    name: 'med_logs'
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 10
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: 270
            spacing: 5
            Label:
                text: 'Başlangıç Tarihi:'
                font_size: '18sp'
                bold: True
                size_hint_y: None
                height: 35
                text_size: self.size
                halign: 'left'
                valign: 'middle'
            BoxLayout:
                spacing: 5
                size_hint_y: None
                height: 60
                Spinner:
                    id: start_y
                    values: root.get_years()
                Spinner:
                    id: start_m
                    values: root.get_months()
                Spinner:
                    id: start_d
                    values: root.get_days()
            Label:
                text: 'Bitiş Tarihi:'
                font_size: '18sp'
                bold: True
                size_hint_y: None
                height: 35
                text_size: self.size
                halign: 'left'
                valign: 'middle'
            BoxLayout:
                spacing: 5
                size_hint_y: None
                height: 60
                Spinner:
                    id: end_y
                    values: root.get_years()
                Spinner:
                    id: end_m
                    values: root.get_months()
                Spinner:
                    id: end_d
                    values: root.get_days()
            Button:
                text: 'FİLTREYİ UYGULA'
                font_size: '22sp'
                background_color: (0.1, 0.5, 0.8, 1)
                size_hint_y: None
                height: 70
                on_release: root.load_logs()
        GridLayout:
            cols: 3
            size_hint_y: None
            height: 60
            canvas.before:
                Color:
                    rgba: 0.2, 0.2, 0.2, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
            Label: 
                text: 'Tarih'
                bold: True
                font_size: '18sp'
            Label: 
                text: 'İlaç Adı'
                bold: True
                font_size: '18sp'
            Label: 
                text: 'Aç/Tok'
                bold: True
                font_size: '18sp'
        ScrollView:
            GridLayout:
                id: med_grid
                cols: 3
                size_hint_y: None
                height: self.minimum_height
                row_default_height: 60
                row_force_default: True
                spacing: 2
        Button:
            text: 'Geri Dön'
            font_size: '24sp'
            size_hint_y: None
            height: 100
            on_release: root.manager.current = 'log_menu'
'''

# --- EKRAN SINIFLARI ---
class MainMenu(Screen): pass
class MedMenuScreen(Screen): pass
class TrackingMenuScreen(Screen): pass
class LogMenuScreen(Screen): pass

def get_popup(title, message):
    popup = Popup(title=title, content=Label(text=message, font_size='20sp'), size_hint=(0.8, 0.4))
    popup.open()

class MedListScreen(Screen):
    def on_enter(self, *args):
        self.load_table()

    def load_table(self):
        self.ids.med_grid.clear_widgets()
        conn = sqlite3.connect('health_monitor.db')
        c = conn.cursor()
        c.execute("SELECT id, name, category, is_active FROM medications ORDER BY is_active ASC, name ASC")
        rows = c.fetchall()
        conn.close()

        for row in rows:
            med_id, name, cat, status = row
            self.ids.med_grid.add_widget(Label(text=name, font_size='16sp'))
            self.ids.med_grid.add_widget(Label(text=cat, font_size='16sp'))
            self.ids.med_grid.add_widget(Label(text=status, font_size='16sp'))
            
            edit_btn = Button(text='Düzenle', font_size='16sp', background_color=(0.1, 0.5, 0.8, 1))
            edit_btn.bind(on_release=lambda instance, m_id=med_id: self.edit_medication(m_id))
            self.ids.med_grid.add_widget(edit_btn)

    def edit_medication(self, med_id):
        med_screen = self.manager.get_screen('medication')
        med_screen.load_medication_data(med_id)
        self.manager.current = 'medication'

class MedicationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.editing_id = None

    def on_enter(self, *args):
        self.ids.category_spinner.values = self.get_categories()

    def get_categories(self):
        conn = sqlite3.connect('health_monitor.db')
        c = conn.cursor()
        c.execute("SELECT name FROM categories")
        cats = [row[0] for row in c.fetchall()]
        conn.close()
        return cats

    def load_medication_data(self, med_id):
        self.editing_id = med_id
        self.ids.screen_title.text = "İlacı Düzenle"
        self.ids.save_btn.text = "Güncelle"
        
        conn = sqlite3.connect('health_monitor.db')
        c = conn.cursor()
        c.execute("SELECT name, category, description, is_active, notes, daily_dose, meal_type FROM medications WHERE id=?", (med_id,))
        row = c.fetchone()
        conn.close()

        if row:
            self.ids.med_name.text = row[0]
            self.ids.category_spinner.text = row[1]
            self.ids.description.text = row[2]
            self.ids.status_spinner.text = row[3]
            self.ids.notes.text = row[4]
            self.ids.daily_dose.text = str(row[5])
            self.ids.meal_spinner.text = row[6]
            self.ids.new_category.text = ''

    def reset_form(self):
        self.editing_id = None
        self.ids.screen_title.text = "Yeni İlaç Ekle"
        self.ids.save_btn.text = "Kaydet"
        self.ids.med_name.text = ''
        self.ids.category_spinner.text = 'Kategori Seç'
        self.ids.new_category.text = ''
        self.ids.description.text = ''
        self.ids.status_spinner.text = 'Aktif'
        self.ids.meal_spinner.text = 'Aç'
        self.ids.notes.text = ''
        self.ids.daily_dose.text = ''

    def save_medication(self):
        new_cat = self.ids.new_category.text.strip()
        selected_cat = self.ids.category_spinner.text
        category = new_cat if new_cat else selected_cat
        
        if category == 'Kategori Seç' and not new_cat:
            get_popup("Hata", "Lütfen bir kategori seçin veya yazın.")
            return

        name = self.ids.med_name.text.strip()
        if not name:
            get_popup("Hata", "İlaç adı boş olamaz.")
            return

        conn = sqlite3.connect('health_monitor.db')
        c = conn.cursor()
        if new_cat:
            c.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (new_cat,))
        
        if self.editing_id:
            c.execute('''UPDATE medications 
                         SET name=?, category=?, description=?, is_active=?, notes=?, daily_dose=?, meal_type=? 
                         WHERE id=?''',
                      (name, category, self.ids.description.text, self.ids.status_spinner.text,
                       self.ids.notes.text, self.ids.daily_dose.text, self.ids.meal_spinner.text, self.editing_id))
            conn.commit()
            conn.close()
            get_popup("Başarılı", f"{name} güncellendi.")
            self.reset_form()
            self.manager.current = 'med_list'
        else:
            c.execute('''INSERT INTO medications 
                         (name, category, description, is_active, notes, daily_dose, meal_type) 
                         VALUES (?, ?, ?, ?, ?, ?, ?)''',
                      (name, category, self.ids.description.text, self.ids.status_spinner.text,
                       self.ids.notes.text, self.ids.daily_dose.text, self.ids.meal_spinner.text))
            conn.commit()
            conn.close()
            get_popup("Başarılı", f"{name} başarıyla eklendi.")
            self.reset_form()
            self.manager.current = 'med_menu'

class BpTrackingScreen(Screen):
    def save_bp(self):
        sys = self.ids.sys_input.text
        dia = self.ids.dia_input.text
        pulse = self.ids.pulse_input.text
        note = self.ids.bp_note.text
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not sys or not dia:
            get_popup("Hata", "Büyük ve küçük tansiyon girilmelidir.")
            return

        conn = sqlite3.connect('health_monitor.db')
        c = conn.cursor()
        c.execute("INSERT INTO bp_logs (timestamp, sys, dia, pulse, note) VALUES (?, ?, ?, ?, ?)",
                  (now, sys, dia, pulse, note))
        conn.commit()
        conn.close()

        get_popup("Başarılı", "Tansiyon kaydı eklendi.")
        self.ids.sys_input.text = ''
        self.ids.dia_input.text = ''
        self.ids.pulse_input.text = ''
        self.ids.bp_note.text = ''
        self.manager.current = 'tracking_menu'

class MedTrackingScreen(Screen):
    def on_enter(self, *args):
        self.ids.med_select_spinner.values = self.get_active_meds()

    def get_active_meds(self):
        conn = sqlite3.connect('health_monitor.db')
        c = conn.cursor()
        c.execute("SELECT name FROM medications WHERE is_active='Aktif'")
        meds = [row[0] for row in c.fetchall()]
        conn.close()
        return meds

    def save_med_log(self):
        med = self.ids.med_select_spinner.text
        meal = self.ids.usage_meal_spinner.text
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if med == 'İlaç Seç' or med == 'İlaç Seç (Sadece Aktifler)':
            get_popup("Hata", "Lütfen bir ilaç seçin.")
            return

        conn = sqlite3.connect('health_monitor.db')
        c = conn.cursor()
        c.execute("INSERT INTO med_logs (timestamp, med_name, meal_type) VALUES (?, ?, ?)",
                  (now, med, meal))
        conn.commit()
        conn.close()

        get_popup("Başarılı", f"{med} içildi olarak kaydedildi.")
        self.manager.current = 'tracking_menu'

class DateFilterMixin:
    def get_years(self):
        return ['Tümü', '2024', '2025', '2026', '2027', '2028', '2029', '2030']
    
    def get_months(self):
        return ['Tümü'] + [str(i).zfill(2) for i in range(1, 13)]
    
    def get_days(self):
        return ['Tümü'] + [str(i).zfill(2) for i in range(1, 32)]

    def set_today(self):
        now = datetime.now()
        y = str(now.year)
        m = str(now.month).zfill(2)
        d = str(now.day).zfill(2)
        
        self.ids.start_y.text = y
        self.ids.start_m.text = m
        self.ids.start_d.text = d
        
        self.ids.end_y.text = y
        self.ids.end_m.text = m
        self.ids.end_d.text = d

class BpLogScreen(Screen, DateFilterMixin):
    def on_enter(self, *args):
        self.set_today()
        self.load_logs()

    def load_logs(self):
        self.ids.bp_grid.clear_widgets()
        
        start_y = self.ids.start_y.text
        start_m = self.ids.start_m.text
        start_d = self.ids.start_d.text
        
        end_y = self.ids.end_y.text
        end_m = self.ids.end_m.text
        end_d = self.ids.end_d.text
        
        query = "SELECT timestamp, sys, dia, pulse, note FROM bp_logs WHERE 1=1"
        params = []
        
        if start_y != 'Yıl' and start_y != 'Tümü':
            m = start_m if (start_m != 'Ay' and start_m != 'Tümü') else '01'
            d = start_d if (start_d != 'Gün' and start_d != 'Tümü') else '01'
            start_str = f"{start_y}-{m}-{d}"
            query += " AND date(timestamp) >= ?"
            params.append(start_str)
            
        if end_y != 'Yıl' and end_y != 'Tümü':
            m = end_m if (end_m != 'Ay' and end_m != 'Tümü') else '12'
            d = end_d if (end_d != 'Gün' and end_d != 'Tümü') else '31'
            end_str = f"{end_y}-{m}-{d}"
            query += " AND date(timestamp) <= ?"
            params.append(end_str)
            
        query += " ORDER BY timestamp DESC"
        
        conn = sqlite3.connect('health_monitor.db')
        c = conn.cursor()
        c.execute(query, params)
        records = c.fetchall()
        conn.close()
        
        for r in records:
            # \n kaldırıldı, tek satırda "08-25 14:30" formatında gösterilecek
            short_date = r[0][5:16]
            self.ids.bp_grid.add_widget(Label(text=short_date, font_size='14sp'))
            self.ids.bp_grid.add_widget(Label(text=str(r[1]), font_size='14sp'))
            self.ids.bp_grid.add_widget(Label(text=str(r[2]), font_size='14sp'))
            self.ids.bp_grid.add_widget(Label(text=str(r[3]), font_size='14sp'))
            
            note_text = str(r[4])
            if len(note_text) > 10: note_text = note_text[:10] + "..."
            self.ids.bp_grid.add_widget(Label(text=note_text, font_size='14sp'))
            
        if not records:
            self.ids.bp_grid.add_widget(Label(text="Kayıt Bulunamadı", font_size='14sp'))
            for _ in range(4): self.ids.bp_grid.add_widget(Label(text=""))

class MedLogScreen(Screen, DateFilterMixin):
    def on_enter(self, *args):
        self.set_today()
        self.load_logs()

    def load_logs(self):
        self.ids.med_grid.clear_widgets()
        
        start_y = self.ids.start_y.text
        start_m = self.ids.start_m.text
        start_d = self.ids.start_d.text
        
        end_y = self.ids.end_y.text
        end_m = self.ids.end_m.text
        end_d = self.ids.end_d.text
        
        query = "SELECT timestamp, med_name, meal_type FROM med_logs WHERE 1=1"
        params = []
        
        if start_y != 'Yıl' and start_y != 'Tümü':
            m = start_m if (start_m != 'Ay' and start_m != 'Tümü') else '01'
            d = start_d if (start_d != 'Gün' and start_d != 'Tümü') else '01'
            start_str = f"{start_y}-{m}-{d}"
            query += " AND date(timestamp) >= ?"
            params.append(start_str)
            
        if end_y != 'Yıl' and end_y != 'Tümü':
            m = end_m if (end_m != 'Ay' and end_m != 'Tümü') else '12'
            d = end_d if (end_d != 'Gün' and end_d != 'Tümü') else '31'
            end_str = f"{end_y}-{m}-{d}"
            query += " AND date(timestamp) <= ?"
            params.append(end_str)
            
        query += " ORDER BY timestamp DESC"
        
        conn = sqlite3.connect('health_monitor.db')
        c = conn.cursor()
        c.execute(query, params)
        records = c.fetchall()
        conn.close()
        
        for r in records:
            # \n kaldırıldı, tek satırda "08-25 14:30" formatında gösterilecek
            short_date = r[0][5:16]
            self.ids.med_grid.add_widget(Label(text=short_date, font_size='14sp'))
            
            med_name = str(r[1])
            if len(med_name) > 15: med_name = med_name[:15] + "..."
            self.ids.med_grid.add_widget(Label(text=med_name, font_size='14sp'))
            
            self.ids.med_grid.add_widget(Label(text=str(r[2]), font_size='14sp'))
            
        if not records:
            self.ids.med_grid.add_widget(Label(text="Kayıt Bulunamadı", font_size='14sp'))
            for _ in range(2): self.ids.med_grid.add_widget(Label(text=""))

class HealthMonitorApp(App):
    def build(self):
        init_db()
        return Builder.load_string(KV)

if __name__ == '__main__':
    HealthMonitorApp().run()
