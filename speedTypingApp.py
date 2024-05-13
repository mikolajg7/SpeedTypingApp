# importuje biblioteki
import tkinter as tk # gui
import time # odliczanie czasu w wpm
import random # randomizacja słów

class WPMApp: # klasa dla liczenia predkosci pisania
    def __init__(self, root, callback):
        self.root = root
        self.callback = callback
        self.root.title("WPM Calculator")

        self.target_words = self.load_words()
        self.curr_text = []
        self.words_typed = 0
        self.wpm = 0
        self.start_time = 0
        self.timer_seconds = 60

        self.create_widgets()
        self.display_text()

        self.root.bind("<Key>", self.key_pressed)

    def create_widgets(self):
        self.label = tk.Label(self.root, text="Press any key to start", font=("Helvetica", 14))
        self.label.pack(pady=20)

        self.timer_label = tk.Label(self.root, text=f"Time left: {self.timer_seconds}", font=("Helvetica", 14))
        self.timer_label.pack(anchor='e', side='top')

        self.wpm_label = tk.Label(self.root, text="WPM: 0", font=("Helvetica", 14))
        self.wpm_label.pack(anchor='w', side='top')

        self.white_bar = tk.Text(self.root, font=("Helvetica", 18), bg="white", fg="black", wrap="word")
        self.white_bar.pack(pady=20)

    def load_words(self): # zaladowanie slow z txt
        with open("data.txt", "r") as f:
            content = f.read()
            words = content.split('\n')
            random.shuffle(words) # wymieszanie ich
            print(words)
            return words

    def update_timer(self): # odliczanie czasu
        if self.timer_seconds > 0:
            self.timer_seconds -= 1
            self.timer_label.config(text=f"Time left: {self.timer_seconds}")
            self.root.after(1000, self.update_timer)
        elif self.timer_seconds <= 0:
            self.show_completion_dialog()

    def update_wpm(self): # liczenie wpm na bierzaco
        time_elapsed = max(time.time() - self.start_time, 1)
        self.wpm = round(self.words_typed / (time_elapsed / 60))
        self.wpm_label.config(text=f"WPM: {self.wpm}")

    def display_text(self): # wyswietlanie tekstu
        self.white_bar.delete('1.0', tk.END)
        if self.target_words:
            target_word = self.target_words[0]
            for i, char in enumerate(target_word):
                color = "black"
                if i < len(self.curr_text):
                    entered_char = self.curr_text[i]
                    color = "green" if entered_char == char else "red"
                self.white_bar.insert(tk.END, char, color)
            self.white_bar.tag_config("green", foreground="green")
            self.white_bar.tag_config("red", foreground="red")
            self.white_bar.tag_config("black", foreground="black")

    def key_pressed(self, event): # reakcje na wcisniety klawisz
        if not self.start_time:
            self.start_time = time.time()
            self.root.after(1000, self.update_timer)

        if "".join(self.curr_text) == self.target_words[0] or len(self.curr_text) > len(self.target_words[0]):
            self.target_words.pop(0)
            self.curr_text = []

        key = event.char
        keysym = event.keysym

        if keysym == 'Escape':
            self.root.destroy()
            return
        elif keysym == 'BackSpace':
            if len(self.curr_text) > 0:
                self.curr_text.pop()
        elif len(self.curr_text) < len(self.target_words[0]) and key != ' ':
            self.curr_text.append(key)
        elif key == ' ':
            self.words_typed += 1

        self.display_text()
        self.update_wpm()

    def create_custom_dialog(self, title, message, button1_text, button1_command, button2_text, button2_command):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)

        # Wyswietlanie okienka na srodku wczesniejszego
        parent_x = self.root.winfo_rootx()
        parent_y = self.root.winfo_rooty()
        parent_height = self.root.winfo_height()
        parent_width = self.root.winfo_width()

        # ustawienie wielkosci
        dialog_width = 350
        dialog_height = 100

        pos_x = parent_x + (parent_width / 2) - (dialog_width / 2)
        pos_y = parent_y + (parent_height / 2) - (dialog_height / 2)

        dialog.geometry(f"{dialog_width}x{dialog_height}+{int(pos_x)}+{int(pos_y)}")

        tk.Label(dialog, text=message).pack(pady=10)
        tk.Button(dialog, text=button1_text, command=button1_command).pack(side='left', padx=10)
        tk.Button(dialog, text=button2_text, command=button2_command).pack(side='right', padx=10)

    def show_completion_dialog(self): # okienko wyskakujace po wykonaniu testu
        message = f"You typed {self.words_typed} words in 60 seconds"
        self.create_custom_dialog("Completed", message, "Go to Main Page", self.show_main_page, "Try Again", self.try_again)

    def try_again(self): # co powinno sie wydarzyc po kliknieciu try agian
        self.root.withdraw() #ukrywa okno
        self.new_window = tk.Toplevel(self.root) #nowe okno
        self.new_window.geometry(self.root.geometry()) # ustawia nowe oknow w tym samym miejscu
        self.new_window.title("WPM Calculator")
        self.new_window.protocol("WM_DELETE_WINDOW", lambda: self.show_main_page())  # gdbybysmy zamknetli to okno wrcamy do main page
        wpm_app = WPMApp(self.new_window, self.show_main_page)  # tworzy instancje
    def show_main_page(self): # metoda to powrotu do manu glownego
        self.root.destroy()
        self.callback()

class Learning(WPMApp): #klasa do uczenia sie pisania bezwzrokowego
    finger_mapping = {
        'a': 'Mały palec lewej ręki', 's': 'Palec serdeczny lewej ręki', 'd': 'Środkowy palec lewej ręki',
        'f': 'Palec wskazujący lewej ręki', 'g': 'Palec wskazujący lewej ręki', 'h': 'Palec wskazujący prawej ręki',
        'j': 'Palec wskazujący prawej ręki', 'k': 'Środkowy palec prawej ręki', 'l': 'Palec serdeczny prawej ręki',
        ';': 'Mały palec prawej ręki', 'q': 'Mały palec lewej ręki', 'w': 'Palec serdeczny lewej ręki',
        'e': 'Środkowy palec lewej ręki', 'r': 'Palec wskazujący lewej ręki', 't': 'Palec wskazujący lewej ręki',
        'y': 'Palec wskazujący prawej ręki', 'u': 'Palec wskazujący prawej ręki', 'i': 'Środkowy palec prawej ręki',
        'o': 'Palec serdeczny prawej ręki', 'p': 'Mały palec prawej ręki', 'z': 'Mały palec lewej ręki',
        'x': 'Palec serdeczny lewej ręki', 'c': 'Środkowy palec lewej ręki', 'v': 'Palec wskazujący lewej ręki',
        'b': 'Palec wskazujący lewej ręki', 'n': 'Palec wskazujący prawej ręki', 'm': 'Palec wskazujący prawej ręki',
    }

    def create_widgets(self): # zastepowanie metody create_widets aby w tym oknie nie pojawial sie wpm i odliczanie czasu
        self.label = tk.Label(self.root, text="Press any key to start", font=("Helvetica", 14))
        self.label.pack(pady=20)

        self.white_bar = tk.Text(self.root, font=("Helvetica", 18), bg="white", fg="black", wrap="word")
        self.white_bar.pack(pady=20)

    def display_text(self): #wyswietlanie tekstu
        self.white_bar.delete('1.0', tk.END)
        if self.target_words:
            for word_index, word in enumerate(self.target_words):
                for i, char in enumerate(word):
                    color = "black"
                    if word_index == 0 and i < len(self.curr_text):
                        entered_char = self.curr_text[i]
                        color = "green" if entered_char == char else "red"
                    self.white_bar.insert(tk.END, char, color)
                self.white_bar.insert(tk.END, ' ', 'black')
            self.white_bar.tag_config("green", foreground="green")
            self.white_bar.tag_config("red", foreground="red")
            self.white_bar.tag_config("black", foreground="black")
        if self.target_words and len(self.curr_text) < len(self.target_words[0]):
            next_char = self.target_words[0][len(self.curr_text)]
            finger = self.finger_mapping.get(next_char.lower(), 'Unknown')
            self.label.config(text=f"Kliknij {next_char} palcem: {finger}")

    def key_pressed(self, event): #reakcja na nacisniecie klawisza
        if "".join(self.curr_text) == self.target_words[0] or len(self.curr_text) > len(self.target_words[0]):
            self.target_words.pop(0)
            self.curr_text = []
            if not self.target_words:
                self.show_completion_dialog()
                self.root.destroy()
                return
        key = event.char
        keysym = event.keysym
        if keysym == 'Escape':
            self.root.destroy()
            return
        elif keysym == 'BackSpace':
            if len(self.curr_text) > 0:
                self.curr_text.pop()
        elif len(self.curr_text) < len(self.target_words[0]) and key != ' ':
            self.curr_text.append(key)
        self.display_text()

class MainApp: #glowna klasa
    def __init__(self):
        self.root = tk.Tk() #nowa instancja
        self.root.title("Main Application")
        self.center_and_resize_window(800, 600)
        self.root.bind("<Escape>", self.close_app)
        self.root.protocol("WM_DELETE_WINDOW", self.close_app)


        self.canvas = tk.Canvas(self.root)
        self.image = tk.PhotoImage(file="pisanie.jpg")
        self.image = self.image.subsample(2, 2)


        self.image_label = tk.Label(self.canvas, image=self.image)
        self.canvas.create_window(0, 0, anchor='nw', window=self.image_label)


        self.text = "Pisanie bezwzrokowe to cenna umiejętność, szczególnie przydatna w pracy, nauce i korzystaniu z urządzeń mobilnych. Nauka tej techniki przynosi kilka kluczowych korzyści.\n\nPierwsza to zwiększenie prędkości pisania. Dzięki pisaniu bez patrzenia na klawiaturę, poprawiasz swoją wydajność i płynność pracy.\n\nPo drugie, korzystasz z lepszej postawy ciała, co przekłada się na komfort i zdrowie w miejscu pracy. Unikasz schylania się nad klawiaturą, co może obciążać kręgosłup i plecy."
        self.text_label = tk.Label(self.root, text=self.text, font=("Helvetica", 14), wraplength=700)
        self.text_label.pack(pady=10)

        button1 = tk.Button(self.root, text="Otwórz Test Prędkości Pisania!", command=self.open_wpm_calculator)
        button1.pack(pady=10)

        button2 = tk.Button(self.root, text="Ucz się pisania bezwzrokowego!", command=self.open_learning_app)
        button2.pack(pady=10)


        self.canvas.pack(side='left', fill='both', expand=True)

        self.root.mainloop()

    def close_app(self, event=None): #metoda do zamkniecia okna
        self.root.quit()

    def center_and_resize_window(self, width, height): # ustawienie odpowiedniego miejsca okna
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.root.geometry('%dx%d+%d+%d' % (width, height, x, y)) #ustawnienie odpowiednich wielksci

    def open_learning_app(self): # otworzenie uczenia
        self.root.withdraw() #schowanie glownego okna apki
        self.new_window = tk.Toplevel(self.root) # otworzenie nowej aplikacji
        self.new_window.title("Learning App")
        self.new_window.geometry(self.root.geometry())  # wielkosc taka sama jak okna glownego
        self.new_window.protocol("WM_DELETE_WINDOW", lambda: self.show_main_page())  # co sie stanie po zamknieciu okna
        learning_app = Learning(self.new_window, self.show_main_page) # tworzenie instancji

    def open_wpm_calculator(self): #otworzenie testu
        self.root.withdraw()
        self.new_window = tk.Toplevel(self.root)
        self.new_window.title("WPM Calculator")
        self.new_window.geometry(self.root.geometry())
        self.new_window.protocol("WM_DELETE_WINDOW", lambda: self.show_main_page())
        wpm_app = WPMApp(self.new_window, self.show_main_page)  # tworzenie instancji

    def show_main_page(self): # metoda do tworzenia strony glownej
        self.root.deiconify()


app = MainApp() # tworzenie instancji
