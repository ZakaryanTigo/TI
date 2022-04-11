from tkinter import *
from tkinter import messagebox
import viterbi_decoder
import re

root = Tk()
#функция перевода в бинарный вид информационного слова
def text_to_bits(txt, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(txt.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def f_1():
    global max
    #проверка на заполненность ячеек, ввод инф. слова и перевод его в двоичный вид
    if (entry1 != "") or (entry2 != "") or (entry3 != ""):
        fi1e = entry1.get()
        txt_bits = text_to_bits(fi1e)
        i = []
        #заполняем в список информационное слово
        for k, l in enumerate(txt_bits):
            if int(l) == 1:
                i.append(k)
        #получаем кол-во сумматоров и проверяем их на некорректные символы
        expression = entry2.get()
        regexp = r"([a-zA-Z])"
        regexp1 = r"([!@#$%^&*()+=/><.,'№;:?_])"
        match = re.search(regexp, expression)
        match1 = re.search(regexp1, expression)
        if (match is None) and (match1 is None):
            summators = int(expression)
            g = []
            m = []
            expression = ""
            #получаем позиции сумматоров и проверяем их на некорректные символы
            expression = entry3.get()
            regexp = r"([a-zA-Z])"
            regexp1 = "4567890"
            regexp2 = r"([!@#$%^&*()+=/><.,'№;:?_])"
            match = re.search(regexp, expression)
            match1 = re.search(regexp1, expression)
            match2 = re.search(regexp2, expression)
            if (match is None) and (match1 is None) and (match2 is None):
                #поочередно выписываем все позиции сумматоров
                #сравниваем кол-во позиций с тем, количеством сумматоров, которое ввели ранее
                while expression != '':
                    if expression.find(" ") != -1:
                        m.append(expression[:expression.find(" ")])
                        expression = expression[expression.find(" ") + 1:]
                    else:
                        regexp = r"(\d+)"
                        a = re.search(regexp, expression)
                        m.append(a[0])
                        expression = ''
                #создаем двумерный список с сумматорами
                count = 0
                for j in range(len(m)):
                    count += 1
                    t = list(m[j])
                    g.append(t)
                if count != summators:
                    messagebox.showerror('error', 'Something went wrong!')
                    return
            else:
                messagebox.showerror('error', 'Something went wrong!')
            for k, m in enumerate(g):
                for l, n in enumerate(g[k]):
                    g[k][l] = int(g[k][l]) - 1
            c = []
            txt_l = '10'
            #складываем поочередно элементы из каждого подсписка с информационным словом, формируя полином
            for k, m in enumerate(g):
                a = []
                for l, n in enumerate(g[k]):
                    for p, q in enumerate(i):
                        d = int(n) + int(q)
                        a.append(d)
                        a.sort()
                c.append(a)
            count = -1
            code_word = []
            #походим все повторяющиеся элементы и приравниваем их -1
            for o in range(len(c)):
                for k in range(len(c[o]) - 1):
                    if (c[o][k] == c[o][k + 1]) or (c[o][k] == count):
                        count = c[o][k]
                        c[o][k] = -1
                        c[o][k] = -1
            #удаляем все элементы, равные -1
            for o in range(len(c)):
                while c[o].count(-1) != 0:
                    c[o].remove(-1)
            max = max(map(max, c))
            #находим максимальный элемент в полученном полиноме и делаем проверку от 0 до него
            #если есть элемент, выводим в список кодового слова 1, если такого нет - 0
            for k, m in enumerate(c):
                min = 0
                while min != max:
                    if min in c[k]:
                        code_word.append(1)
                    else:
                        code_word.append(0)
                    min += 1
            #список преобразуем в строчку и выводим
            txt_1 = "".join(map(str, code_word))
            entry4.insert(END, txt_1)
            #применяем декодирование и выводим результат
            vd = viterbi_decoder.ViterbiDecoder()
            file = vd.decode(txt_l)
            entry5.insert(END, fi1e)
        else:
            messagebox.showerror('error', 'Something went wrong!')
    else:
        messagebox.showerror('error', 'Something went wrong!')

#построение графического интерфейса
root.title("Сверточный код")
root.geometry('427x230')

label1=Label(root, text="Слово:", fg="#000000", width = 15)
label1.grid(row=0, column = 0, columnspan=1)
label2=Label(root, text="Kол-во сумматоров:", fg="#000000", width = 15)
label2.grid(row=2, column = 0, columnspan=1)
label3=Label(root, text="Позиции сумматоров:", fg="#000000", width = 17)
label3.grid(row=4, column = 0, columnspan=1)
label4=Label(root, text="Закодированное слово:", fg="#000000", width = 25)
label4.grid(row=7, column = 0, columnspan=1)
label5=Label(root, text="Декодированное слово:", fg="#000000", width = 25)
label5.grid(row=9, column = 0, columnspan=1)

entry1 = Entry(root, width = 70)
entry1.grid(row=1, column=0, columnspan=5)
entry2 = Entry(root, width = 70)
entry2.grid(row=3, column=0, columnspan=5)
entry3 = Entry(root, width = 70)
entry3.grid(row=5, column = 0, columnspan=5)
entry4 = Entry(root, width = 70)
entry4.grid(row=8, column=0, columnspan=5)
entry5 = Entry(root, width = 70)
entry5.grid(row=10, column = 0, columnspan=5)

bttn1 = Button(root, text="начало", width = 30, command = f_1)
bttn1.grid(row=6, column = 0, columnspan=5)


root.mainloop()