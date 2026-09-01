import customtkinter as ctk
from fisica import somar_valores

#configutação da aparência
ctk.set_appearance_mode('dark')

#criação da janela principal
app = ctk.CTk()
app.title("Lançamento de Projétil")
app.geometry("1280x800")

#criação dos campos
#label
label_num1 = ctk.CTkLabel(app,text='NUMERO 1')
label_num1.pack(pady=10)
#entry
campo_num1 = ctk.CTkEntry(app,placeholder_text='Digite seu número')
campo_num1.pack()

#label
label_num2 = ctk.CTkLabel(app,text='NUM 2')
label_num2.pack()
#entry
campo_num2 = ctk.CTkEntry(app,placeholder_text='Digite seu segundo número')
campo_num2.pack()

#button
somar_button = ctk.CTkButton(app,text='SOMAR',command=lambda: resultado.configure(
    text=f'Soma: {somar_valores(campo_num1.get(),campo_num2.get())}'
))
somar_button.pack(pady=10)


#campo de resultado
resultado = ctk.CTkLabel(app, text='')
resultado.pack(pady=10)
#iniciar a aplicação
app.mainloop()