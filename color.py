import random
import time
import tkinter as tk


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

        level = ['易しい', '難しい']
        moji = ['ひらがな', '漢字']

        # 問題のページ
        # 色を答える 易しい 難しい
        for i in range(2):
            frame = QuestionPage(parent=container, controller=self,
                                 next_frame=self.frames[0], level=level[i], moji=moji[0])
            frame.grid(row=0, column=0, sticky='nsew')
            self.frames.append(frame)

        # 文字と色を答える 易しいor難しい ひらがなor漢字
        for i in range(4):
            frame = QuestionPage2(parent=container, controller=self,
                                  next_frame=self.frames[0], level=level[i % 2], moji=moji[i // 2])
            frame.grid(row=0, column=0, sticky='nsew')
            self.frames.append(frame)

        # はじめのページ
        frame = StartPage(parent=container, controller=self,
                          frames=self.frames)
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
    NUM = [0, 1, 2, 3]
    # COLOR = ['あか', 'あお', 'みどり', 'きいろ']
    COLOR_CODE = ['#f80d00', '#00bfff', '#36dc21', '#fcde01']
    ACTIVE_COLOR_CODE = ['#ff635b', '#66d8ff', '#83e976', '#fee961']
    QUESTIONS = 5

    def __init__(self, parent, controller, next_frame, level, moji):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.next_frame = next_frame
        self.level = level
        if moji == 'ひらがな':
            self.COLOR = ['あか', 'あお', 'みどり', 'きいろ']
        else:
            self.COLOR = ['赤', '青', '緑', '黃']
        self.COLOR_CHOICES = ['あか', 'あお', 'みどり', 'きいろ']

        self.select_color()
        self.questions_num = 0
        self.correct_answers = 0
        # ボタンを作る
        self.create_button()

    def select_color(self):
        # 問題の文字と色，選択肢の順番を決める
        num = [0, 1, 2, 3]
        self.choices_color = random.sample(self.COLOR_CHOICES, len(self.COLOR))
        temp_num = list(range(0, len(self.choices_color)))
        self.question_char = random.choice(temp_num)
        del temp_num[self.question_char]
        self.answer_color = random.choice(temp_num)
        self.choices_bg = random.sample(num, len(num))

    def create_button(self):
        self.question_pre = tk.Label(self)
        self.question_pre['text'] = '色を答えてください'
        # question['font'] = self.controller.font
        self.question_pre.grid(row=0, column=0, columnspan=2, sticky='nsew')

        self.question = tk.Label(self)
        self.question['text'] = self.COLOR[self.question_char]
        self.question['fg'] = self.COLOR_CODE[self.answer_color]
        self.question['bg'] = 'white'
        # question['font'] = self.controller.font
        self.question.grid(row=1, column=0, columnspan=2, sticky='nsew')

        button_row = [2, 2, 3, 3]
        button_col = [0, 1, 0, 1]
        self.choices = []
        if self.level == '易しい':
            for i in range(len(self.choices_color)):
                choice = tk.Button(self)
                choice['text'] = self.choices_color[i]
                choice['width'] = 10
                choice.bind('<1>', self.check_ans)
                choice.grid(row=button_row[i],
                            column=button_col[i], sticky='nsew')
                self.choices.append(choice)
        else:
            for i in range(len(self.choices_color)):
                choice = tk.Button(self)
                choice['text'] = self.choices_color[i]
                choice['width'] = 10
                choice['fg'] = 'white'
                choice['activeforeground'] = 'white'
                choice['bg'] = self.COLOR_CODE[self.choices_bg[i]]
                choice['activebackground'] = self.ACTIVE_COLOR_CODE[self.choices_bg[i]]
                choice.bind('<1>', self.check_ans)
                choice.grid(row=button_row[i],
                            column=button_col[i], sticky='nsew')
                self.choices.append(choice)

    def check_ans(self, event):
        choice = event.widget['text']
        if choice == self.COLOR_CHOICES[self.answer_color]:
            self.correct_answers += 1

        self.select_color()
        self.question['text'] = self.COLOR[self.question_char]
        self.question['fg'] = self.COLOR_CODE[self.answer_color]
        for i in range(len(self.choices_color)):
            self.choices[i]['text'] = self.choices_color[i]
        if self.level == '難しい':
            for i in range(len(self.choices_color)):
                self.choices[i]['bg'] = self.COLOR_CODE[self.choices_bg[i]]
                self.choices[i]['activebackground'] = self.ACTIVE_COLOR_CODE[self.choices_bg[i]]

        if self.questions_num < self.QUESTIONS - 1:
            self.questions_num += 1
        else:
            self.questions_num = 0
            self.controller.frames[0].label['text'] = '正解数: {}/{}'.format(
                self.correct_answers, self.QUESTIONS)
            self.correct_answers = 0

            # かかった時間
            elasped_time = time.time() - self.controller.frames[-1].start_time
            m, s = divmod(int(elasped_time), 60)
            if m > 0:
                self.controller.frames[0].time_label['text'] = 'TIME: {}分{}秒'.format(
                    m, s)
            else:
                self.controller.frames[0].time_label['text'] = 'TIME: {}秒'.format(
                    s)

            # 結果の表示
            self.next_frame.tkraise()


class QuestionPage2(tk.Frame):
    NUM = [0, 1, 2, 3]
    # COLOR = ['あか', 'あお', 'みどり', 'きいろ']
    COLOR_CODE = ['#f80d00', '#00bfff', '#36dc21', '#fcde01']
    ACTIVE_COLOR_CODE = ['#ff635b', '#66d8ff', '#83e976', '#fee961']
    QUESTIONS = 5

    def __init__(self, parent, controller, next_frame, level, moji):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.next_frame = next_frame
        self.level = level
        if moji == 'ひらがな':
            self.COLOR = ['あか', 'あお', 'みどり', 'きいろ']
        else:
            self.COLOR = ['赤', '青', '緑', '黃']
        self.COLOR_CHOICES = ['あか', 'あお', 'みどり', 'きいろ']

        self.select_color()
        self.questions_num = 0
        self.correct_answers = 0
        # ボタンを作る
        self.create_button()

    def select_color(self):
        # 問題の文字と色，選択肢の順番を決める
        num = [0, 1, 2, 3]
        self.choices_color = random.sample(self.COLOR_CHOICES, len(self.COLOR))
        temp_num = list(range(0, len(self.choices_color)))
        self.question_char = random.choice(temp_num)
        del temp_num[self.question_char]
        self.answer_color = random.choice(temp_num)
        self.choices_bg = random.sample(num, len(num))
        # 0なら色を答える 1なら文字を答える
        self.color_or_moji = random.randint(0, 1)

    def create_button(self):
        self.question_pre = tk.Label(self)
        if self.color_or_moji == 0:
            self.question_pre['text'] = '色を答える'
        else:
            self.question_pre['text'] = '文字を答える'
        # question['font'] = self.controller.font
        self.question_pre.grid(row=0, column=0, columnspan=2, sticky='nsew')

        self.question = tk.Label(self)
        self.question['text'] = self.COLOR[self.question_char]
        self.question['fg'] = self.COLOR_CODE[self.answer_color]
        self.question['bg'] = 'white'
        # question['font'] = self.controller.font
        self.question.grid(row=1, column=0, columnspan=2, sticky='nsew')

        button_row = [2, 2, 3, 3]
        button_col = [0, 1, 0, 1]
        self.choices = []
        if self.level == '易しい':
            for i in range(len(self.choices_color)):
                choice = tk.Button(self)
                choice['text'] = self.choices_color[i]
                choice['width'] = 10
                choice.bind('<1>', self.check_ans)
                choice.grid(row=button_row[i],
                            column=button_col[i], sticky='nsew')
                self.choices.append(choice)
        else:
            for i in range(len(self.choices_color)):
                choice = tk.Button(self)
                choice['text'] = self.choices_color[i]
                choice['width'] = 10
                choice['fg'] = 'white'
                choice['activeforeground'] = 'white'
                choice['bg'] = self.COLOR_CODE[self.choices_bg[i]]
                choice['activebackground'] = self.ACTIVE_COLOR_CODE[self.choices_bg[i]]
                choice.bind('<1>', self.check_ans)
                choice.grid(row=button_row[i],
                            column=button_col[i], sticky='nsew')
                self.choices.append(choice)

    def check_ans(self, event):
        # 正解を判定する
        choice = event.widget['text']
        if self.color_or_moji == 0:  # 色の場合
            if choice == self.COLOR_CHOICES[self.answer_color]:
                self.correct_answers += 1
        else:  # 文字の場合
            if choice == self.COLOR_CHOICES[self.question_char]:
                self.correct_answers += 1

        # 問題の更新
        self.select_color()
        if self.color_or_moji == 0:
            self.question_pre['text'] = '色を答える'
        else:
            self.question_pre['text'] = '文字を答える'
        self.question['text'] = self.COLOR[self.question_char]
        self.question['fg'] = self.COLOR_CODE[self.answer_color]
        for i in range(len(self.choices_color)):
            self.choices[i]['text'] = self.choices_color[i]
        if self.level == '難しい':
            for i in range(len(self.choices_color)):
                self.choices[i]['bg'] = self.COLOR_CODE[self.choices_bg[i]]
                self.choices[i]['activebackground'] = self.ACTIVE_COLOR_CODE[self.choices_bg[i]]

        if self.questions_num < self.QUESTIONS - 1:
            self.questions_num += 1
        else:
            self.questions_num = 0
            self.controller.frames[0].label['text'] = '正解数: {}/{}'.format(
                self.correct_answers, self.QUESTIONS)
            self.correct_answers = 0

            # かかった時間
            elasped_time = time.time() - self.controller.frames[-1].start_time
            m, s = divmod(int(elasped_time), 60)
            if m > 0:
                self.controller.frames[0].time_label['text'] = 'TIME: {}分{}秒'.format(
                    m, s)
            else:
                self.controller.frames[0].time_label['text'] = 'TIME: {}秒'.format(
                    s)

            # 結果の表示
            self.next_frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller, frames):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.frames = frames
        self.start_time = 0.0

        self.t = [
            '色を答える\n易しい',
            '色を答える\n難しい',
            '文字と色を答える\n易しい',
            '文字と色を答える\n難しい',
            '文字と色を答える\n易しい 漢字',
            '文字と色を答える\n難しい 漢字'
        ]

        for i in range(len(self.t)):
            button = tk.Button(self, text=self.t[i], font=("", 50))
            button.bind('<1>', self.raise_next_frame)
            button.grid(row=i // 2, column=i % 2, sticky='nsew')

    def raise_next_frame(self, event):
        self.start_time = time.time()
        event_text = event.widget['text']
        next_frame = self.frames[self.t.index(event_text) + 1]
        next_frame.tkraise()


if __name__ == '__main__':
    app = Application()
    app.mainloop()
