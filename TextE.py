from os import stat
import tkinter as tk
import os
from tkinter import END, Label, Menu, ttk
from tkinter import font,filedialog,messagebox,colorchooser



main_app = tk.Tk()
main_app.geometry('1200x800')
main_app.title("Text Editor")

#                                         main menu start
main_menu=tk.Menu()
file=tk.Menu(main_menu,tearoff=False)
#adding icons and file
new_icon=tk.PhotoImage(file='icons/add.png')
open_icon=tk.PhotoImage(file='icons/open.png')
save_icon=tk.PhotoImage(file='icons/save.png')
save_as_icon=tk.PhotoImage(file='icons/save as.png')
exit_icon=tk.PhotoImage(file='icons/exit.png')

#edit
edit=tk.Menu(main_menu,tearoff=False)

#view
view=tk.Menu(main_menu,tearoff=False)
# view_select=tk.StringVar()

#color theme
color_theme=tk.Menu(main_menu,tearoff=False)
theme_choice=tk.StringVar()

color_dict={
    'Dark':('#474747','#e0e0e0'),
    'Light plus':('#c4c4c4','#2d2d2d')
}

#cascade
main_menu.add_cascade(label='File',menu=file)
main_menu.add_cascade(label='Edit',menu=edit)
main_menu.add_cascade(label='View',menu=view)
main_menu.add_cascade(label='Color theme',menu=color_theme)

#                                             main menu end

#                                             toolbar start 
tool_bar=ttk.Label(main_app)
tool_bar.pack(side=tk.TOP,fill=tk.X)

fonts=tk.StringVar()
font_tuples = tk.font.families()
font_box=ttk.Combobox(tool_bar,width=30,textvariable=fonts,stat='readonly')
font_box['values']=font_tuples
font_box.current(font_tuples.index('Arial'))
font_box.grid(row=0,column=0)
#sizebar
size_bar=tk.StringVar()
size=ttk.Combobox(tool_bar,width=10,textvariable=size_bar,stat='readonly')
size['value']=tuple(range(8,82,2))
size.current(2)
size.grid(row=0,column=1)

bold=tk.PhotoImage(file="icons/bold.png")
bold_button=ttk.Button(tool_bar,image=bold)
bold_button.grid(row=0,column=2)

italic=tk.PhotoImage(file='icons/italic.png')
italic_button=ttk.Button(tool_bar,image=italic)
italic_button.grid(row=0,column=3)

underlined=tk.PhotoImage(file='icons/underlined.png')
underlined_button=ttk.Button(tool_bar,image=underlined)
underlined_button.grid(row=0,column=4)

font_color=tk.PhotoImage(file="icons/fontcolor.png")
fontcolor_button=ttk.Button(tool_bar,image=font_color)
fontcolor_button.grid(row=0,column=5)

align_left=tk.PhotoImage(file="icons/alignleft.png")
left_button=ttk.Button(tool_bar,image=align_left)
left_button.grid(row=0,column=6)

align_center=tk.PhotoImage(file="icons/aligncenter.png")
center_button=ttk.Button(tool_bar,image=align_center)
center_button.grid(row=0,column=7 )

align_right=tk.PhotoImage(file="icons/alignright.png")
right_button=ttk.Button(tool_bar,image=align_right)
right_button.grid(row=0,column=8)

#                                             toolbar end

#                                   text editor start 

text_editor=tk.Text(main_app)
text_editor.config(wrap='word',relief=tk.FLAT)
text_editor.focus_set()
scroll_bar=tk.Scrollbar(main_app)
scroll_bar.pack(side=tk.RIGHT,fill=tk.Y)
text_editor.pack(fill=tk.BOTH,expand=True)
scroll_bar.config(command=text_editor.yview)
text_editor.config(yscrollcommand=scroll_bar.set)
#font family and font size
current_font='Arial'
current_size=12

def fontchange(main_app):
    global current_font
    current_font=fonts.get()
    text_editor.configure(font=(current_font,current_size))

def fontsizechange(main_app):
    global current_size
    current_size=size_bar.get()
    text_editor.configure(font=(current_font,current_size))

font_box.bind("<<ComboboxSelected>>", fontchange)
size.bind("<<ComboboxSelected>>",fontsizechange)
#button functionality
# print(tk.font.Font(font=text_editor['font']).actual())
def change_bold():
    bold_btn=tk.font.Font(font=text_editor['font'])
    # print(bold_btn.actual())
    if bold_btn.actual()['weight'] == 'normal':
        text_editor.configure(font=(current_font,current_size,'bold'))
    if bold_btn.actual()['weight']=='bold':
        text_editor.configure(font=(current_font,current_size,'normal'))
bold_button.configure(command=change_bold)

def change_italic():
    italic_btn=tk.font.Font(font=text_editor['font'])
    if italic_btn.actual()['slant']=='roman':
        text_editor.configure(font=(current_font,current_size,'italic'))
    else:
        text_editor.configure(font=(current_font,current_size,'roman'))
italic_button.configure(command=change_italic)


def change_underline():
    underline_btn=tk.font.Font(font=text_editor['font'])
    # print(bold_btn.actual())
    if underline_btn.actual()['underline'] == 0:
        text_editor.configure(font=(current_font,current_size,'underline'))
    if underline_btn.actual()['underline']==1:
        text_editor.configure(font=(current_font,current_size,'normal'))
underlined_button.configure(command=change_underline)

def change_color():
    color_var=tk.colorchooser.askcolor()
    text_editor.configure(fg=color_var[1])
fontcolor_button.configure(command=change_color)

def leftalign():
    contents=text_editor.get(1.0,'end')
    text_editor.tag_config('left',justify=tk.LEFT)
    text_editor.delete(1.0,tk.END)
    text_editor.insert(tk.INSERT,contents,'left')
left_button.configure(command=leftalign)

def centeralign():
    contents=text_editor.get(1.0,tk.END)
    text_editor.tag_config('center',justify=tk.CENTER)
    text_editor.delete(1.0,tk.END)
    text_editor.insert(tk.INSERT,contents,'center')

center_button.configure(command=centeralign)

def rightalign():
    contents=text_editor.get(1.0,tk.END)
    text_editor.tag_config('right',justify=tk.RIGHT)
    text_editor.delete(1.0,tk.END)
    text_editor.insert(tk.INSERT,contents,'right')
    
right_button.configure(command=rightalign)

text_change=False
def statusbar(event=None):
    if text_editor.edit_modified():
        global text_change
        text_change=True
        # print(text_change)
        words=len(text_editor.get(1.0,'end-1c').split())
        chars=len(text_editor.get(1.0,'end-1c'))
        status_bar.config(text=f'words : {words} characters : {chars}')
    text_editor.edit_modified(False)
text_editor.bind('<<Modified>>',statusbar)


text_editor.configure(font=('Arial',12))
#                                   text editor end

#                                   status bar start
status_bar=ttk.Label(main_app,text="Status bar")
status_bar.pack(side=tk.BOTTOM)
#                                    status bar end

#                            main menu functionality start

url=''
#new file
def newfile(event=None):
    # global url
    # url=""
    text_editor.delete(1.0,tk.END)

file.add_command(label='New',image=new_icon,compound=tk.LEFT, accelerator='ctrl+n',command=newfile)

#open file
def openfile(event=None):
    global url
    url=filedialog.askopenfilename(initialdir=os.getcwd(),title='Select file',filetypes=(('text file','*.txt'),("All file","*.*")))
    try:
        with open(url,'r') as f:
            text_editor.delete(1.0,tk.END)
            text_editor.insert(1.0,f.read())
    except:
        return
    main_app.title(os.path.basename(url))

file.add_command(label='Open',image=open_icon,compound=tk.LEFT, accelerator='ctrl+o',command=openfile)

#save file
def save_file(event=None):
    global url
    try: 
        if url:
            with open(url,'w') as f:
                content=text_editor.get(1.0,tk.END)
                f.write(content)
        else:
            url=filedialog.asksaveasfile(mode='w',defaultextension='.txt',filetypes=(('text file','*.txt'),("All file","*.*")))
            contents= text_editor.get(1.0,tk.END)
            url.write(contents)
            url.close()
    except:
        return

file.add_command(label='Save',image=save_icon,compound=tk.LEFT, accelerator='ctrl+s',command=save_file)

#save as file
def saveas(event=None):
    global url
    try:
        content=text_editor.get(1.0,tk.END)
        url=filedialog.asksaveasfile(mode='w',defaultextension='.txt',filetypes=(('text file','*.txt'),("All file","*.*")))
        url.write(content)
        url.close()
    except:
        return

file.add_command(label='Save as',image=save_as_icon,compound=tk.LEFT, accelerator='ctrl+s',command=saveas)

#exit file
def exit_func(event=None):
    global url,text_change
    # print(text_change)
    try:
        if text_change:
            msgbox=messagebox.askyesnocancel("Warning" , "Do you want to save the file ?")
            if msgbox is True:
                # print(text_change)
                save_file()
                main_app.destroy()
            elif msgbox is False:
                main_app.destroy()
        else:
            main_app.destroy()
    except:
        return

file.add_command(label='Exit',image=exit_icon,compound=tk.LEFT, accelerator='alt+f4',command=exit_func)

#find functionality
def find(event=None):
    find_box=tk.Toplevel()
    find_box.geometry("400x300")
    find_box.title("Find")
    find_box.resizable(0,0)

    find_frame=ttk.LabelFrame(find_box,text="Find/Replace")
    find_frame.pack(pady=20)

    find_label=ttk.Label(find_frame,text='Find ')
    find_label.grid(row=0,column=0,pady=4,padx=4)
    replace_label=ttk.Label(find_frame,text="Replace")
    replace_label.grid(row=1,column=0,pady=4,padx=4)

    find_input=ttk.Entry(find_frame,width=30)
    find_input.grid(row=0,column=1,pady=4,padx=4)
    replace_input=ttk.Entry(find_frame,width=30)
    replace_input.grid(row=1,column=1,pady=4,padx=4)

    def finds():
        word=find_input.get()
        text_editor.tag_remove('match','1.0',tk.END)
        matches=0
        if word:
            start_pos='1.0'
            while True:
                start_pos=text_editor.search(word,start_pos,stopindex=tk.END)
                if not start_pos:
                    break
                end_pos=f'{start_pos}+{len(word)}c'
                text_editor.tag_add('match',start_pos,end_pos)
                matches+=1
                start_pos=end_pos
                text_editor.tag_config('match',foreground='red',background='yellow')

    def replace():
        word=find_input.get()
        replace_word=replace_input.get()
        contents=text_editor.get(1.0,tk.END)
        new_contents=contents.replace(word,replace_word)
        text_editor.delete(1.0,tk.END)
        text_editor.insert(1.0,new_contents)

    find_button=ttk.Button(find_frame,text="Find",command=finds)
    find_button.grid(row=2,column=1)
    replace_button=ttk.Button(find_frame,text="Replace",command=replace)
    replace_button.grid(row=2,column=2)




edit.add_command(label='copy', accelerator='ctrl+c',command=lambda:text_editor.event_generate('<Control c>'))
edit.add_command(label='paste', accelerator='ctrl+v',command=lambda:text_editor.event_generate('<Control v>'))
edit.add_command(label='cut', accelerator='ctrl+x',command=lambda:text_editor.event_generate('<Control x>'))
edit.add_command(label='clear all', accelerator='ctrl+alt+x',command=lambda:text_editor.delete(1.0,tk.END))
edit.add_command(label='find', accelerator='ctrl+f',command=find)

show_toolbar=tk.BooleanVar()
show_toolbar.set(True)
show_statusbar=tk.BooleanVar()
show_toolbar.set(True)

def toolbar():
    global show_toolbar
    if show_toolbar:
        tool_bar.pack_forget()
        show_toolbar=False
    else:
        text_editor.pack_forget()
        status_bar.pack_forget()
        tool_bar.pack(side=tk.TOP,fill=tk.X)
        text_editor.pack(fill=tk.BOTH,expand=True)
        status_bar.pack(side=tk.BOTTOM)
        show_toolbar=True

def statusbar():
    global show_statusbar
    if show_statusbar:
        status_bar.pack_forget()
        show_statusbar=False
    else:
        status_bar.pack(side=tk.BOTTOM)
        show_statusbar=True

view.add_checkbutton(label="Tool bar",onvalue=1,offvalue=0,compound=tk.LEFT,variable=show_toolbar,command=toolbar)
view.add_checkbutton(label="Status bar",onvalue=1,offvalue=0,compound=tk.LEFT,variable=show_statusbar,command=statusbar)

#color theme

def theme_change():
    chosen_theme=theme_choice.get()
    color=color_dict.get(chosen_theme)
    text_editor.config(background=color[0],fg=color[1])

color_theme.add_radiobutton(label="Light plus",variable=theme_choice,compound=tk.LEFT,command=theme_change)
color_theme.add_radiobutton(label="Dark",variable=theme_choice,compound=tk.LEFT,command=theme_change)

#                            main menu functionality end

main_app.config(menu=main_menu)
main_app.bind("<Control-n>",newfile)
main_app.bind("<Control-o>",openfile)
main_app.bind("<Control-s>",save_file)
main_app.bind("<Control-Alt-s>",saveas)
main_app.bind("<Control-q>",exit_func)
main_app.bind("<Control-f>",find)

main_app.mainloop()