from tkinter import *
from tkinter import Tk,filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import webbrowser

import Lexico
import Sintactico
import ok

class prinicipal:

    def __init__(self):
        self.window = Tk()
        self.txt = ScrolledText(self.window,height=27,width=78,foreground='white')
        self.input = Entry(self.window,border=5,width=63,bg='gray',fg='black',font='Arial 13 bold')
        self.input.place(x=20,y=520)
        self.obj = Lexico.AnalizadorLexico()

    def limpiar(self):
        self.input.delete("0","end")

    def insertarTexto(self,mensaje):
        self.txt.config(state='normal')
        self.txt.insert("end", mensaje+ '\n', ("LEFT",))
        self.txt.tag_configure("left", justify="left")
        self.txt.config(state='disabled')

    def getText(self):
        cadena = 'bro?'
        cadena = self.input.get()
        print(cadena)
        return cadena

    def principio(self):
        res = self.getText()
        # res = obj.imprimirTokens()
        self.txt.config(state='normal')
        self.txt.insert("end", res+' \n', ("right",))
        self.txt.tag_configure("right", justify="right")
        self.txt.config(state='disabled')
        ####
        self.obj.analizar(res)
        sint = Sintactico.AnalizadorSintactico(self.obj.listaTokens)
        sint.analizar()
        
        res = ok.callme()
        sint.imprimirErrores()
        sint.imprimirErroresNone()
        self.insertarTexto(res.mensaje)

    def manualU(self):
        path = 'Proyecto2/archivos/Manual_usuario.pdf'
        webbrowser.open_new(path)
    def manualT(self):
        path = 'Proyecto2/archivos/Manual_Tecnico.pdf'
        webbrowser.open_new(path)

    def INICIO(self):
        self.window.geometry('850x590')
        self.window.title("Proyecto 2 LFP")
        self.window.config(bg='DarkSlateGrey')
        
        DIVISION = '*----------------------------------------------------------------------------*'
        btn_errores = Button(self.window,text='Reporte de Errores',command=self.obj.crearTErrores,bg='#f39c12',width=16,borderwidth=4,relief='raised',foreground='black',font='Arial 11 bold',height=1,).place(x=680,y=36)
        btn_limpiar1 = Button(self.window,text='Clean log de Errores',command=self.obj.limpiarErrores,bg='#f39c12',width=16,borderwidth=4,relief='raised',foreground='black',font='Arial 11 bold',height=1).place(x=680,y=83)
        btn_tokens = Button(self.window,text='Reporte de Tokens',command=self.obj.crearTTokens,bg='#f39c12',width=16,borderwidth=4,relief='raised',foreground='black',font='Arial 11 bold',height=1).place(x=680,y=130)
        btn_limpiar2 = Button(self.window,text='Clean log de Tokens',command=self.obj.limpiarTokens,bg='#f39c12',width=16,borderwidth=4,relief='raised',foreground='black',font='Arial 11 bold',height=1).place(x=680,y=177)
        btn_manualU = Button(self.window,text='Manual de Usuario',command=self.manualU,bg='#f39c12',width=16,borderwidth=4,relief='raised',foreground='black',font='Arial 11 bold',height=1).place(x=680,y=224)
        btn_manualT = Button(self.window,text='Manual Tecnico',command=self.manualT,bg='#f39c12',width=16,borderwidth=4,relief='raised',foreground='black',font='Arial 11 bold',height=1).place(x=680,y=271)
        lbl= Label(self.window,text='La Liga BOT',width=95,bg='#d4ac0d',foreground='black',font='Arial 12 bold',anchor='w',height=1).place(x=0,y=0)
        lbl2= Label(self.window,text='',width=95,bg='#d4ac0d',foreground='black',font='Arial 12 bold',anchor='w',height=1).place(x=0,y=567)
        btn = Button(self.window, text="ENVIAR",bg='SeaGreen',borderwidth=4,width=16,fg='white',font='Arial 10 bold',command=self.principio,height=1)
        btn.place(x=680,y=520)

        btnExit = Button(self.window, text="EXIT",bg='red',borderwidth=5,fg='white',font='Arial 10 bold',command=self.window.destroy,height=2,width=7)
        btnExit.place(x=720,y=320)
        btnLimp = Button(self.window, text="Limpiar texto",bg='blue',borderwidth=5,fg='white',font='Arial 10 bold',command=self.limpiar,height=1,width=10)
        btnLimp.place(x=700,y=470)
        # txt = ScrolledText(window,height=27,width=78,foreground='white')
        # txt = Text(window,height=26,width=80,font='Arial 11',foreground='white')
        self.txt.config(bg='#2E2E2E')
        self.txt.place(x=20,y=36)
        self.txt.insert('insert',DIVISION+'\t\t      Bienvenido a La Liga Bot, ingrese un comando\n'+DIVISION)
        self.txt.config(state='disabled')
        
        self.window.mainloop()

if __name__ == '__main__':
    
    obj = prinicipal()
    obj.INICIO()