import random
from src.player import Player
import tkinter as tk
from tkinter import font
from tkinter import messagebox
from src.services import collect_word, createSecret

class QuizApp:
    def __init__(self, root):
        
        self.root = root
        self.root.title("Bilgi Yarişmasi")
        self.root.geometry("600x400")
        self.root.config(bg="#ffe6f0")

        self.player = Player()
        self.wrong_attempts = 0
        self.score = 0

        self.questions = [
            ("Türkiye Cumhuriyeti'nin kurucusu kimdir?", "Mustafa Kemal Atatürk"),
            ("Türkiye'nin en uzun nehri hangisidir?", "Kizilirmak"),
            ("Türkiye'nin yüz ölçümü bakimindan en büyük ili hangisidir?", "Konya"),
            ("İstanbul Boğazi'nin iki kitasini bağlayan ilk köprünün adi nedir?", "Boğaziçi Köprüsü"),
            ("Mevlana Celaleddin Rumi'nin türbesi hangi şehirde bulunmaktadir?", "Konya"),
            ("Türkiye'nin en çok şampiyonluk kazanan basketbol takimi hangisidir?", "Anadolu Efes"),
            ("Türkiye'nin ilk ve tek Formula 1 pilotu kimdir?", "Cem Bölükbaşi"),
            ("Türkiye'nin ilk yerli uydusu hangisidir?", "Bilsat"),
            ("Türkiye'nin ilk milli gözlemevi hangi ilde kurulmuştur?", "Antalya"),
            ("Türk pop müziğinin 'Kraliçesi' olarak bilinen sanatçi kimdir?", "Sezen Aksu")
            ("Türk rock müziğinin 'Deli Kizin Türküsü' olarak bilinen grubu kimdir?", "Duman")
            ("Türkiye'nin ilk uluslararasi müzik yarişmasinda birinci olan sanatçi kimdir?", "Sertab Erener")
            ("Türkiye'nin ilk 'Metal' müzik grubu hangisidir?", "Pentagram")
            ("Hangi Türk şarkici, 'Unutamadim' şarkisiyla ün kazanmiştir?", "Ferdi Tayfur")
            ("Türkiye'nin ilk kadin pilotu olan ve 'Türk Hava Yollari'nin ilk kadin pilotu olan kişi kimdir?", "Sabiha Gökçen")
            ("MSKU'de Algoritmalar ve Programlama dersini kim vermektedir?", "Güncel Sariman")
            ("Türk mitolojisinde 'Asena' kimdir ve hangi Türk halkinin efsanesinde yer alir?", "Göktürkler")
            ("Türk bilim insani Aziz Sancar hangi alanda Nobel Ödülü kazanmiştir?", "Kimya")
        ]

        random.shuffle(self.questions)
        self.question_index = 0
        self.frame()

    def frame(self):

        self.font_large = font.Font(family="Helvetica", size=16, weight="bold")
        self.font_medium = font.Font(family="Helvetica", size=12)
        self.font_small = font.Font(family="Helvetica", size=10, slant="italic")

        self.label_question = tk.Label(self.root, text=self.questions[self.question_index][0], wraplength=500, bg="#ffe6f0", fg="#ff66b2", font=self.font_large)
        self.label_question.pack(pady=20)

        self.entry_answer = tk.Entry(self.root, width=50, font=self.font_medium, bg="#ffb3d9", fg="#ffffff", insertbackground="#ff66b2")
        self.entry_answer.pack(pady=10)

        self.button_submit = tk.Button(self.root, text="Cevabi Gönder", command=self.check_answer, bg="#ff66b2", fg="white", font=self.font_medium, activebackground="#45a049")
        self.button_submit.pack(pady=10)

        self.label_feedback = tk.Label(self.root, text=" ", bg="#ffe6f0", fg="#ff66b2", font=self.font_small)
        self.label_feedback.pack(pady=10)

        self.label_score = tk.Label(self.root, text=f"Skor: {self.score}", bg="#ffe6f0", fg="#ff66b2", font=self.font_medium)
        self.label_score.pack(pady=10)

        self.label_remaining_attempts = tk.Label(self.root, text=f"Kalan Haklar: {self.player.hp}", bg="#ffe6f0", fg="#ff66b2", font=self.font_medium)
        self.label_remaining_attempts.pack(pady=10)
    
 
    def check_answer(self):
        answer = self.entry_answer.get().strip()
        if self.question_index < len(self.questions):
            correct_answer = self.questions[self.question_index][1]

            if answer.lower() == correct_answer.lower():
                self.score += 1
                self.label_feedback.config(text="Doğru!", fg="green")
            else:
                self.player.lose_hp()
                self.wrong_attempts += 1
                self.label_feedback.config(text=f"Yanliş! Doğru cevap: {correct_answer}", fg="red")
                self.label_remaining_attempts.config(text=f"Kalan Haklar: {self.player.hp}")

            self.entry_answer.delete(0, tk.END)
            self.question_index += 1
            self.label_score.config(text=f"Skor: {self.score}")

            if self.question_index < len(self.questions) and self.player.hp > 0 and self.wrong_attempts < 3:
                self.label_question.config(text=self.questions[self.question_index][0])
            else:
                self.ask_city_question()
        else:
            self.ask_city_question()

    def ask_city_question(self):
        word = collect_word()
        correct_answer = word
        self.city_secret = createSecret(word, 2)
        self.city_attempts_left = 3
        self.label_question.config(text=f"Harika ilerlediniz! İşte final sorumuz:\n Güzel ülkemizdeki gizli şehir: {self.city_secret}")
        self.button_submit.config(command=lambda: self.check_city_answer(correct_answer))  
        self.label_remaining_attempts.config(text=f"Kalan Haklar: {self.city_attempts_left}")

    def check_city_answer(self, correct_answer):
        answer = self.entry_answer.get().strip()
        if isinstance(answer, str) and isinstance(correct_answer, str):
            if answer.lower() == correct_answer.lower():
                self.score += 1
                self.label_feedback.config(text="Doğru!", fg="green")
                messagebox.showinfo("Tebrikler", f"Oyunu kazandiniz! Skorunuz: {self.score}")
                self.root.destroy()
            else:
                self.city_attempts_left -= 1
                self.label_feedback.config(text=f"Yanliş! Doğru cevap: {correct_answer}", fg="red")
                self.label_remaining_attempts.config(text=f"Kalan Haklar: {self.city_attempts_left}")
                
                if self.city_attempts_left == 0:
                    messagebox.showinfo("Oyun Bitti", f"Oyun bitti! Skorunuz: {self.score}")
                    self.root.destroy()
                self.entry_answer.delete(0, tk.END)

        else:
            messagebox.showerror("hata","beklenmedik hata")

    
    def end_game(self):
            messagebox.showinfo("Oyun Bitti", f"Oyun bitti! Skorunuz: {self.score}")
            self.root.destroy()

    

    