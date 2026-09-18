kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
import random

class MLOblocksEditorUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        
        # Состояние движка
        self.current_mode = "3D"
        self.current_tool = "Строить"
        self.fps = 95
        self.sphere_radius = 2
        self.files_log = ["script.cpp", "index.html"]

        # 1. Верхняя панель: Статус и FPS
        self.top_panel = BoxLayout(size_hint_y=0.1, background_color=(0.2, 0.2, 0.2, 1))
        self.status_label = Label(text=f"Режим: {self.current_mode} | Инструмент: {self.current_tool}")
        self.fps_label = Label(text=f"FPS: {self.fps}", color=(0, 1, 0, 1))
        self.top_panel.add_widget(self.status_label)
        self.top_panel.add_widget(self.fps_label)
        self.add_widget(self.top_panel)

        # Симуляция стабильного FPS (от 70 до 100)
        Clock.schedule_interval(self.update_fps, 0.5)

        # 2. Рабочая область (Эмулятор 3D/2D пространства)
        self.workspace = BoxLayout(size_hint_y=0.6)
        self.workspace_label = Label(
            text="[ Экран 3D Редактора ]\n\nНажмите на кнопки управления внизу", 
            halign="center"
        )
        self.workspace.add_widget(self.workspace_label)
        self.add_widget(self.workspace)

        # 3. Нижняя панель управления: Сетка интерактивных кнопок
        self.control_grid = GridLayout(cols=3, size_hint_y=0.3, spacing=5, padding=5)
        
        # Кнопка 1: Переключение инструментов (Строить / Ломать)
        self.btn_tool = Button(text="Инструмент:\nСТРОИТЬ", background_color=(0.2, 0.6, 0.2, 1))
        self.btn_tool.bind(on_press=self.toggle_tool)
        
        # Кнопка 2: Спавн круга (Сферы)
        self.btn_sphere = Button(text=f"Спавн Круга\n(Радиус: {self.sphere_radius})", background_color=(0.2, 0.4, 0.8, 1))
        self.btn_sphere.bind(on_press=self.spawn_circle_tool)
        
        # Кнопка 3: Переключение 3D / 2D (Scratch-режим)
        self.btn_dimension = Button(text="Режим: 3D", background_color=(0.7, 0.4, 0.1, 1))
        self.btn_dimension.bind(on_press=self.toggle_dimension)
        
        # Кнопка 4: Папка HTML / Скрипты
        self.btn_scripts = Button(text="Папка HTML\nи Скрипты", background_color=(0.5, 0.1, 0.5, 1))
        self.btn_scripts.bind(on_press=self.open_scripts_menu)
        
        # Кнопка 5: Пробный режим игры
        self.btn_test = Button(text="ПРОБНЫЙ ЗАПУСК\n(Без загрузки)", background_color=(0.1, 0.7, 0.6, 1))
        self.btn_test.bind(on_press=self.run_test_game)
        
        # Кнопка 6: Опубликовать игру (Экспорт)
        self.btn_publish = Button(text="ОПУБЛИКОВАТЬ\nИГРУ", background_color=(0.8, 0.2, 0.2, 1))
        self.btn_publish.bind(on_press=self.open_publish_menu)

        # Добавляем все кнопки на экран телефона
        self.control_grid.add_widget(self.btn_tool)
        self.control_grid.add_widget(self.btn_sphere)
        self.control_grid.add_widget(self.btn_dimension)
        self.control_grid.add_widget(self.btn_scripts)
        self.control_grid.add_widget(self.btn_test)
        self.control_grid.add_widget(self.btn_publish)
        self.add_widget(self.control_grid)

    # ЛОГИКА ДЛЯ ВСЕХ КНОПОК:

    def update_fps(self, dt):
        # Жесткое ограничение движка: FPS колеблется строго от 70 до 100
        self.fps = random.randint(70, 100)
        self.fps_label.text = f"FPS: {self.fps}"

    def toggle_tool(self, instance):
        if self.current_tool == "Строить":
            self.current_tool = "Ломать"
            self.btn_tool.text = "Инструмент:\nЛОМАТЬ"
            self.btn_tool.background_color = (0.8, 0.3, 0.2, 1)
        else:
            self.current_tool = "Строить"
            self.btn_tool.text = "Инструмент:\nСТРОИТЬ"
            self.btn_tool.background_color = (0.2, 0.6, 0.2, 1)
        self.update_status()

    def toggle_dimension(self, instance):
        if self.current_mode == "3D":
            self.current_mode = "2D"
            self.btn_dimension.text = "Режим: 2D (Scratch)"
            self.workspace_label.text = "[ 2D Режим активен ]\n\nПеретаскивайте логические блоки кода!"
        else:
            self.current_mode = "3D"
            self.btn_dimension.text = "Режим: 3D"
            self.workspace_label.text = "[ 3D Редактор кубов ]\n\nСетка пространства готова к редактированию."
        self.update_status()

    def update_status(self):
        self.status_label.text = f"Режим: {self.current_mode} | Инструмент: {self.current_tool}"

    def spawn_circle_tool(self, instance):
        # Логика расширения круга: при каждом нажатии радиус увеличивается, затем сбрасывается
        self.sphere_radius = self.sphere_radius + 1 if self.sphere_radius < 5 else 1
        self.btn_sphere.text = f"Спавн Круга\n(Радиус: {self.sphere_radius})"
        self.workspace_label.text = f"[Действие] В 3D пространстве сгенерирован\nкруг блоков с радиусом {self.sphere_radius}!"

    def run_test_game(self, instance):
        # Моментальный пробный запуск без экрана загрузки
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text=f"Игра запущена в пробном режиме!\nТекущая плавность: {self.fps} FPS.\n\nЭкраны загрузки отсутствуют."))
        btn_close = Button(text="Выйти из игры", size_hint_y=0.3)
        content.add_widget(btn_close)
        
        popup = Popup(title="Тестирование игры", content=content, size_hint=(0.8, 0.5))
        btn_close.bind(on_press=popup.dismiss)
        popup.open()

    def open_scripts_menu(self, instance):
        # Меню открытого кода: папка HTML, C++ файлы, импорт PNG файлов напрямую
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        files_str = "\n".join([f"- {f}" for f in self.files_log])
        content.add_widget(Label(text=f"Файлы в директории проекта:\n{files_str}", size_hint_y=0.4))
        
        # Поле для ввода имени нового файла (.html, .cpp, .png)
        file_input = TextInput(text="image.png", multiline=False, size_hint_y=0.3)
        content.add_widget(file_input)
        
        btn_layout = BoxLayout(size_hint_y=0.3, spacing=5)
        btn_add = Button(text="Закинуть файл")
        btn_close = Button(text="Назад")
        btn_layout.add_widget(btn_add)
        btn_layout.add_widget(btn_close)
        content.add_widget(btn_layout)
        
        popup = Popup(title="Файловая система (Открытый код)", content=content, size_hint=(0.9, 0.7))
        
        def add_file(ins):
            if file_input.text:
                self.files_log.append(file_input.text)
                popup.dismiss()
                self.open_scripts_menu(None) # Перерисовываем список
                
        btn_add.bind(on_press=add_file)
        btn_close.bind(on_press=popup.dismiss)
        popup.open()

    def open_publish_menu(self, instance):
        # Окно компиляции в разные форматы (EXE, APK, исходный код .py, .sh)
        content = BoxLayout(orientation='vertical', padding=10, spacing=5)
        content.add_widget(Label(text="Выберите формат для компиляции игры:", size_hint_y=0.2))
        
        formats = ["Файл .APK (Android)", "Исходный код .PY (Android)", "Файл .EXE (Windows)", "Исходный код .SH (Linux/Mac)"]
        
        grid = GridLayout(cols=2, spacing=5, size_hint_y=0.6)
        popup = Popup(title="Публикация проекта MLOblocks", content=content, size_hint=(0.9, 0.8))
        
        for fmt in formats:
            btn_fmt = Button(text=fmt)
            # При нажатии на любой формат происходит экспорт
            btn_fmt.bind(on_press=lambda ins, f=fmt: self.export_done(f, popup))
            grid.add_widget(btn_fmt)
            
        content.add_widget(grid)
        btn_back = Button(text="Отмена", size_hint_y=0.2)
        btn_back.bind(on_press=popup.dismiss)
        content.add_widget(btn_back)
        popup.open()

    def export_done(self, format_name, parent_popup):
        parent_popup.dismiss()
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(text=f"Успешно!\nПроект скомпилирован в:\n{format_name}"))
        btn_ok = Button(text="Отлично", size_hint_y=0.4)
        content.add_widget(btn_ok)
        popup = Popup(title="Экспорт завершен", content=content, size_hint=(0.7, 0.4))
        btn_ok.bind(on_press=popup.dismiss)
        popup.open()

class MLOblocksApp(App):
    def build(self):
        return MLOblocksEditorUI()

if __name__ == '__main__':
    MLOblocksApp().run()
