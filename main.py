from tkinter import *
from tkinter import messagebox as msg
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import json

def read_questions():
    with open('file.json', encoding='utf-8') as f:
        d = json.load(f)
    return d
        
class TestWindow():
    root = Tk()
    result = {}
    name = StringVar()
    def __init__(self):
        self.root.title('Определение темперамента')
        self.root.geometry("500x350")
        self.root.resizable(0, 0)
        self.root.option_add('*Font', 'Ubuntu 20 roman')
        self.root.option_add('*Button.Width', '7')
        
        self.main_frame = Frame(self.root)
        self.main_frame.pack(fill=BOTH, expand=1)
        self.result_frame = Frame(self.root)
        
        
        Label(self.main_frame, text='Вам будет необходимо ' + \
                                        'ответить на 80 вопросов ' + \
                                        'для выяснения Вашего ' + \
                                        'темперамента', 
                                        wraplengt=450).pack(side=TOP, pady=10)
                                        
        Label(self.main_frame, text='Отвечайте "ДА", если ' + \
                                        'качество для вас обычно, повседневно.\n' +\
                                        'Введите свое имя ниже.', 
                                        wraplengt=450,
                                        font='Ubuntu 10 roman').pack(side=TOP, pady=10)
        
        Entry(self.main_frame, textvariable=self.name).pack(pady=5)
        
        go_button = Button(self.main_frame, 
                                text='Начать', 
                                borderwidth=0,
                                command=self.start  
                                )
        go_button.pack(pady=10)
        
        exit_button = Button(self.main_frame, 
                                text='Выход', 
                                borderwidth=0,
                                command=self.exit
                                )
        exit_button.pack(pady=10)
        
        self.root.mainloop()
        
    def exit(self):
        self.root.destroy()

    def start(self):
        if self.name.get() == '':
            msg.showerror('Name Error!', 'Пожалуйста, введите свое имя!')
        else:
            self.main_frame.destroy()
            json_data = read_questions()
            
            asked = 0
            amount = sum([len(i) for i in json_data.values()])
            self.result = {key:0 for key in json_data.keys()}
            
            for temp, questions in json_data.items():
                for q in questions:
                    f = Frame(self.root)
                    Label(f, text=f'Вопрос {asked+1} из {amount}').pack(side=TOP)
                    Label(f, text=q, wraplengt=450).pack(side=TOP, expand=1)
                    
                    yes_button = Button(f, 
                                        text='ДА',
                                        borderwidth=0,
                                        command=lambda: self.answer_yes(f, temp)
                                        )
                    yes_button.pack(padx=50, pady=50, side=RIGHT)
                        
                    no_button = Button( f,
                                        text='НЕТ',
                                        borderwidth=0,
                                        command=lambda: self.answer(f)
                                        )
                    no_button.pack(padx=50, pady=50, side=LEFT)
                        
                    f.pack(fill=BOTH, side=LEFT, expand=1)
                    f.mainloop()
                    asked += 1
                    
            answers = sum(self.result.values())       
            for temp in self.result.keys():
                self.result[temp] /= answers
                    
            self.show_result()
                
    def answer(self, frame):
        frame.quit()
        frame.destroy()
        
    def answer_yes(self, frame, temp):
        self.result[temp] += 1
        self.answer(frame)
        
    def show_result(self):
        self.root.geometry("900x600")
        f = Figure(figsize=(90, 75))
        canvas = FigureCanvasTkAgg(f, self.result_frame)
        canvas.get_tk_widget().pack()
        scale = max(self.result.values())
        ax = f.add_subplot(111, polar=1)
        
        Choleric = f'Холерик {round(self.result["Холерик"]*100, 2)}%'
        Melancholic = f'Меланхолик {round(self.result["Меланхолик"]*100, 2)}%'
        Phlegmatic = f'Флегматик {round(self.result["Флегматик"]*100, 2)}%'
        Sanguine = f'Сангвиник {round(self.result["Сангвиник"]*100, 2)}%'

        labels = (  Choleric, 'Нестабильность',
                    Melancholic, 'Интроверсия',
                    Phlegmatic, 'Стабильность',
                    Sanguine, 'Экстраверсия')
     
        rad = 0.0174533
        x = [i*rad for i in (0, 270, 180, 90)]
        y = [value for value in self.result.values()]
        ax.fill(x, y,  "#2277ff",)
        x1 = [180*rad, 270*rad, 0, 90*rad, 180*rad]
        y1 = [.3, .3, .3, .3, .3]
        ax.plot(x1, y1,  "r")

        ax.set_rticks([scale])
        #ax.set_yticklabels([round(scale*100), 2], ha='center')
        ax.set_rmax(1)

        ax.set_rlim(0)
        ax.set_thetagrids(range(0, 361, 45), labels=[])
        xtext = [1.1, .9, .5, .1, -.1, .1, .5, .9]
        ytext = [.5, .9, 1.1, .9, .5, .1, -.1, .1]
        rot_angles = ['vertical', -45, 0, 45, 'vertical', -45, 0, 45]
        
        for i in range(8):
            ax.text(xtext[i],
                    ytext[i], 
                    labels[i], 
                    ha='center', 
                    va='center',
                    rotation=rot_angles[i],
                    transform=ax.transAxes)
        
        description = '\nРезультат\nВаш темперамент:\n'         
        for key, val in sorted(self.result.items(), key=lambda res: res[1], reverse=True):
            description += f'на {round(val*100, 2)}% {key}\n'
        description +=  '\n*Внутри красного четырехугольника' +\
                        '\nнаходятся слабо выраженные' +\
                        '\nтипы темперамента (<30%)'
        f.suptitle(description, y=0.98, x=0.01, fontsize=8, ha='left')
        
        self.result_frame.pack(fill=BOTH, expand=1)

if __name__ == '__main__':
    test = TestWindow()
    if test.name.get() != '':
        with open(f'{test.name.get()}.json', 'a+', encoding='utf-8') as res_file:
            json.dump(test.result, res_file, indent=3, ensure_ascii=False)
