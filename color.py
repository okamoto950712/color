import tkinter as tk
from tkinter import font as tkfont
import random
import time


class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('文字色当てゲーム')
        self.geometry('1200x900')
        self.option_add('*font', ('Helvetica', 80, 'bold'))

        # 基盤となるフレーム
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # 結果準備のページ
        self.frames = []
        frame = ResultPage(parent=container, controller=self)
        frame.grid(row=0, column=0, sticky='nsew')
        self.frames.append(frame)

        # 問題のページ
        frame = QuestionPage(
            parent=container, controller=self, next_frame=self.frames[-1])
        frame.grid(row=0, column=0, sticky='nsew')
        self.frames.append(frame)

        # はじめのページ
        frame = StartPage(parent=container, controller=self,
                          next_frame=self.frames[-1])
        frame.grid(row=0, column=0, sticky='nsew')
        self.frames.append(frame)

        # はじめのページを表示する
        frame.tkraise()


class ResultPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.label = tk.Label(self, text='正解数はx問でした')
        self.label.pack(side='top', fill='x', pady=10)

        self.time_label = tk.Label(self, text='かかった時間はy分z秒です')
        self.time_label.pack(side='top', fill='x')

        button = tk.Button(self)
        button['text'] = 'スタートに戻る'
        button['command'] = lambda: self.controller.frames[-1].tkraise()
        button.pack(fill='x')

        quit_button = tk.Button(
            self, text='終了する', command=self.controller.destroy)
        quit_button.pack(fill='x')


class QuestionPage(tk.Frame):
    COLOR = ['あか', 'あお', 'みどり', 'きいろ']
    COLOR_CODE = {'あか': '#f80d00', 'あお': '#1f05f8',
                  'きいろ': '#fcde01', 'みどり': '#36dc21'}
    QUESTIONS = 5

    def __init__(self, parent, controller, next_frame):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.next_frame = next_frame

        self.select_color()
        self.questions_num = 0
        self.correct_answers = 0
        # ボタンを作る
        self.create_button()

    def select_color(self):
        # 問題の文字と色，選択肢の順番を決める
        self.choices_color = random.sample(self.COLOR, len(self.COLOR))
        self.question_char = self.COLOR[random.randint(
            0, len(self.choices_color)-1)]
        self.answer_color = self.choices_color[random.randint(
            0, len(self.choices_color)-1)]

    def create_button(self):
        self.question = tk.Label(self)
        self.question['text'] = self.question_char
        self.question['fg'] = self.COLOR_CODE[self.answer_color]
        self.question['bg'] = 'white'
        #question['font'] = self.controller.font
        self.question.grid(row=0, column=0, columnspan=2, sticky='nsew')

        button_row = [1, 1, 2, 2]
        button_col = [0, 1, 0, 1]
        self.choices = []
        for i in range(len(self.choices_color)):
            choice = tk.Button(self)
            choice['text'] = self.choices_color[i]
            choice['width'] = 10
            choice.bind('<1>', self.check_ans)
            choice.grid(row=button_row[i], column=button_col[i], sticky='nsew')
            self.choices.append(choice)

    def check_ans(self, event):
        choice = event.widget['text']
        if choice == self.answer_color:
            self.correct_answers += 1

        self.select_color()
        for i in range(len(self.choices_color)):
            self.question['text'] = self.question_char
            self.question['fg'] = self.COLOR_CODE[self.answer_color]
            self.choices[i]['text'] = self.choices_color[i]

        if self.questions_num < self.QUESTIONS-1:
            self.questions_num += 1
        else:
            self.questions_num = 0
            self.controller.frames[0].label['text'] = f'正解数: {self.correct_answers}/{self.QUESTIONS}'
            self.correct_answers = 0

            # かかった時間
            elasped_time = time.time() - self.controller.frames[-1].start_time
            m, s = divmod(int(elasped_time), 60)
            if m > 0:
                self.controller.frames[0].time_label['text'] = f'TIME: {m}分{s}秒'
            else:
                self.controller.frames[0].time_label['text'] = f'TIME: {s}秒'

            # 結果の表示
            self.next_frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller, next_frame):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.next_frame = next_frame
        self.start_time = 0.0

        label = tk.Label(self, text='文字の色を当ててくだい')
        label.pack(side='top', fill='x', pady=10)
        button = tk.Button(self, text='スタート', command=self.raise_next_frame)
        button.pack(fill='x')

    def raise_next_frame(self):
        self.start_time = time.time()
        self.next_frame.tkraise()


if __name__ == '__main__':
    app = Application()
    app.mainloop()
