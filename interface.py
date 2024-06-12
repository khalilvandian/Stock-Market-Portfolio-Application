from tkinter import *
import tkinter as tk
from tkinter.ttk import *
from estimate import LSTM_prediction
from svm import SVM_prediction
from crawlscrape import get_stocks, get_excel, crawl_scrape
import time

window = Tk()
window.resizable(False,False)
window.title("Stock Market Prediction")
window.geometry('600x900')

lbl1 = Label(window, text="enter the stock name you want:", font=("arail bold", 15))
lbl1.place(x=150, y=50)

txt1 = Entry(window, width=20)
txt1.place(x=220, y=100)

lbl2 = Label(window, text='Status',font=("arail bold",15))
lbl2.place(x=250, y=150)


def get_text():
    return txt1.get()


# to scraope stocks
def check():
    crawl_scrape(get_text())


# to call tarin and prediction
def predict():
    if combo.get() == 'LSTM':
        lstm_dict = LSTM_prediction(stock_name=get_text())
        lbl4.config(text=lstm_dict["prediction"])
        #lbl7.config(text=lstm_dict["error"])

    elif combo.get() == 'SVM':
        cj = SVM_prediction(stock_name=get_text())
        lbl4.config(text=cj.to_string())
        #lbl5.config(text=svm_dict["poly"])
        #lbl6.config(text=svm_dict["rbf"])

seprator = Separator(window, orient="horizontal")
seprator.place(relx=0, rely=0.30, relwidth=1, relheight=8)
btn1 = tk.Button(window, text="Statues Check", bg="silver", fg='black', command=lambda: check())
btn1.place(x=240, y=200)

combo = Combobox(window, width =25)
combo['values'] = ('Choose a training method','SVM','LSTM')
combo.current(0)
combo.place(x=400, y=300)

lbl3 = Label(window, text="total days",font=("arail bold",15))
lbl3.place(x=50, y=300)

btn2 = tk.Button(window, text="Predict", bg="silver", fg='black', command=predict)
btn2.place(x=255, y=400)


lbl4 = Label(window, text="results",font=("arail bold", 10))
lbl4.place(x=250, y=450)

#lbl7 = Label(window, text="error",font=("arail bold", 10))
#lbl7.place(x=200, y=500)

#lbl5 = Label(window,text="poly", font=("arail bold", 10))
#lbl5.place(x=10, y=600)

#lbl8 = Label(window,text="error",font=("arail bold", 10))
#lbl8.place(x=200, y=600)

#lbl6 = Label(window,text="rbf", font=("arail bold", 10))
#lbl6.place(x=10, y=700)

#lbl9 = Label(window,text="error", font=("arail bold", 10))
#lbl9.place(x=200, y=700)

frame = tk.LabelFrame(window,text="Excel data")
frame.place(x=45,y=600,width=500,height=250)

tv= Treeview(frame)
tv.place(relheight=1, relwidth=1)

treescrolly = tk.Scrollbar(frame, orient="vertical", command=tv.yview) # command means update the yaxis view of the widget
treescrollx = tk.Scrollbar(frame, orient="horizontal", command=tv.xview) # command means update the xaxis view of the widget
tv.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) # assign the scrollbars to the Treeview Widget
treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
treescrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget


def load():
    pass #https://gist.github.com/RamonWill/0686bd8c793e2e755761a8f20a42c762


btn3=tk.Button(window, text="save Excel", bg="silver", fg='black', command=get_excel(get_text()))
btn3.place(x=250,y=550)



window.mainloop()