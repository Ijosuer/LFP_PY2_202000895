from tkinter import *
from tkinter import Tk,filedialog, messagebox

from matplotlib.pyplot import text


def clearTextInput():
    txt.delete("1.0","end")

def leerForm():
    Tk().withdraw() #Pido Archivo
    archivo = filedialog.askopenfile(
        title= "Seleccione un archivo",
        initialdir='./Practica1',
        filetypes=(('Archivos de data','*.form*'),)
    )  
    if archivo is not None: #Comienza analisis
        lectura = archivo.read()

        txt.insert('insert',lectura)
    else:
        messagebox.showinfo(message='Error al escoger el archivo',title='ARCHIVO .Form')

def getText():
    texto = ''
    texto = input.get()
    if texto != "":
        txt.insert('insert','\t'+texto+'\n')
    else:
        txt.insert('insert','BRUUUUH\n')    
# Aqui esta toda la app grafica.
if __name__ == '__main__':

    window = Tk()
    window.geometry('850x590')
    window.title("Proyecto 2 LFP")
    window.config(bg='DarkSlateGrey')
    btn_errores = Button(window,text='Reporte de Errores',command='reports',bg='#f39c12',width=16,borderwidth=4,relief='raised',foreground='black',font='Arial 11 bold',height=1).place(x=680,y=36)
    btn_limpiar1 = Button(window,text='Clean log de Errores',command='reports',bg='#f39c12',width=16,borderwidth=4,relief='raised',foreground='black',font='Arial 11 bold',height=1).place(x=680,y=83)
    btn_tokens = Button(window,text='Reporte de Tokens',command='reports',bg='#f39c12',width=16,borderwidth=4,relief='raised',foreground='black',font='Arial 11 bold',height=1).place(x=680,y=130)
    btn_limpiar2 = Button(window,text='Clean log de Tokens',command='reports',bg='#f39c12',width=16,borderwidth=4,relief='raised',foreground='black',font='Arial 11 bold',height=1).place(x=680,y=177)
    btn_manualU = Button(window,text='Manual de Usuario',command='reports',bg='#f39c12',width=16,borderwidth=4,relief='raised',foreground='black',font='Arial 11 bold',height=1).place(x=680,y=224)
    btn_manualT = Button(window,text='Manual Tecnico',command='reports',bg='#f39c12',width=16,borderwidth=4,relief='raised',foreground='black',font='Arial 11 bold',height=1).place(x=680,y=271)
    lbl= Label(window,text='La Liga BOT',width=95,bg='#d4ac0d',foreground='black',font='Arial 12 bold',anchor='w',height=1).place(x=0,y=0)
    lbl2= Label(window,text='',width=95,bg='#d4ac0d',foreground='black',font='Arial 12 bold',anchor='w',height=1).place(x=0,y=567)
    btn = Button(window, text="ENVIAR",bg='SeaGreen',borderwidth=4,width=16,fg='white',font='Arial 10 bold',command=getText,height=1)
    btn.place(x=680,y=520)

    input = Entry(window,border=5,width=63, text="LIMPIAR",bg='gray',fg='BLACK',font='Arial 13 bold')
    input.place(x=20,y=520)

    btnExit = Button(window, text="EXIT",bg='red',borderwidth=5,fg='white',font='Arial 10 bold',command=window.destroy,height=2,width=7)
    btnExit.place(x=720,y=320)

    txt = Text(window,height=26,width=80,font='Arial 11',foreground='white')
    txt.config(bg='#2E2E2E')
    txt.place(x=20,y=36)
    window.mainloop()