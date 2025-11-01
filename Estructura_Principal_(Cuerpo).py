import tkinter as t

def saludar():
    entrada2 = entrada.get()
    etiqueta.config(text= f"hola, {entrada2}!" )
    
ventana = t.Tk()
ventana.title("Programa")
ventana.geometry("300x200") 

etiqueta= t.Label(ventana,text="Holaaa")
etiqueta.pack()

entrada = t.Entry(ventana)
entrada.pack()

boton = t.Button(ventana, text = "Saludar", command = saludar)
boton.pack()

ventana.mainloop()


