import tkinter as tk
from tkinter import *
import tkinter.font as tkFont
import tkinter.ttk as ttk
# from tkinter.ttk  import *

import sys
sys.setrecursionlimit(5000) 
# print(sys.getrecursionlimit())  

import os
os.environ["PATH"] += os.pathsep + 'C:\\Program Files (x86)\\Graphviz2.38\\bin\\'
os.environ["PATH"] += os.pathsep + 'C:\\Program Files (x86)\\Graphviz2.38\\bin'
os.environ["PATH"] += os.pathsep + 'C:\\ProgramData\\Anaconda3\\Library\\bin\\graphviz\\'



import sys
main_f='D:\\OneDriveNew\\OneDrive\\Έγγραφα\\ΕΑΠ\\Team Project\\geneology_tree\\'
sys.path.append(f'{main_f}')
import backend
import importlib
# import pandas as pd
from pandas import DataFrame as pddf
from pandas import isnull as isnull
from pandas import to_numeric as to_numeric
from pandas import notnull as notnull
import numpy as np


importlib.reload(backend)

class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self,master=master,relief=tk.FLAT, bg='SlateGray2',font="calibri 12" , **kw)
        
        # self.defaultBackground = self["background"]
        self.defaultBackground = 'SlateGray2'
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        
    def on_enter(self, e):
        self['background'] = self['activebackground']

    def on_leave(self, e):
        self['background'] = self.defaultBackground
        
class BorderedEntry(ttk.Entry):
    def __init__(self, root, *args, bordercolor, borderthickness=1,
                 background='white', foreground='black', **kwargs):
        super().__init__(root, *args, **kwargs)
        # Styles must have unique image, element, and style names to create
        # multiple instances. winfo_id() is good enough
        e_id = self.winfo_id()
        img_name = 'entryBorder{}'.format(e_id)
        element_name = 'bordercolor{}'.format(e_id)
        style_name = 'bcEntry{}.TEntry'.format(e_id)
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()
        self.img = tk.PhotoImage(img_name, width=width, height=height)
        self.img.put(bordercolor, to=(0, 0, width, height))
        self.img.put(background, to=(borderthickness, borderthickness, width -
                     borderthickness, height - borderthickness))

        style = ttk.Style()
        style.element_create(element_name, 'image', img_name, sticky='nsew',
                             border=borderthickness)
        style.layout(style_name,
                     [('Entry.{}'.format(element_name), {'children': [(
                      'Entry.padding', {'children': [(
                          'Entry.textarea', {'sticky': 'nsew'})],
                          'sticky': 'nsew'})], 'sticky': 'nsew'})])
        style.configure(style_name, background=background,
                        foreground=foreground)
        self.config(style=style_name) 
        
class MultiColumnListbox:
    
    """use a ttk.TreeView as a multicolumn ListBox"""

    def __init__(self, c_header, c_list):
        self.c_header=c_header
        self.c_list=c_list
        self.tree = None
        self._setup_widgets(c_header)
        self._build_tree(c_header, c_list)
        # self._selectItem()
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def _setup_widgets(self, c_header):
        s = """click on header to sort by that column
to change width of column drag boundary
        """
        msg = ttk.Label(wraplength="4i", justify="left", anchor="n",
            padding=(10, 2, 10, 6), text=s)
        msg.pack(fill='x')
        container = ttk.Frame()
        container.pack(fill='both', expand=True)
        # create a treeview with dual scrollbars
        self.tree = ttk.Treeview(columns=c_header, show="headings")
        vsb = ttk.Scrollbar(orient="vertical",
            command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal",
            command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,
            xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
        vsb.grid(column=1, row=0, sticky='ns', in_=container)
        hsb.grid(column=0, row=1, sticky='ew', in_=container)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

    def _build_tree(self, c_header, c_list):
        
        for col in c_header:
            self.tree.heading(col, text=col.title(),
                command=lambda c=col: sortby(self.tree, c, 0))
            # adjust the column's width to the header string
            self.tree.column(col,
                width=tkFont.Font().measure(col.title()))

        for i in range(0,c_list.shape[0]):
            # i=1
            self.tree.insert('', 'end', values=tuple(['' if (x in ['nan', np.nan, None, "NaN", ''] or isnull(x)) else x for x in c_list.loc[i].values]))
            # adjust column's width if necessary to fit each value
            for ix in range(len(c_header)):
                col_w = tkFont.Font().measure(c_header[ix])
                if self.tree.column(c_header[ix],width=None)<col_w:
                    self.tree.column(c_header[ix], width=col_w)
            

    def on_tree_select(self, event):
        import numpy as np
        curItem = self.tree.item(self.tree.focus())
        # col = self.tree.identify_column(event.x)
        # print ('curItem = ', curItem['values'])
        # global selected_tuple
        selected_tuple=curItem['values']
        selected_tuple=[x if str(x)!='None' and notnull(x) else "" for x in selected_tuple ]

        clear_command()
        #0 'id',   
        #1             'name', 
        #2             'surname',                                   
        #3             'date_birth',
        #4             'date_death',
        #5             'mother_id',
        #6             'father_id',
        #7             'spouse_id',                                   
        #8             'generation',
        #9             'cluster', 
        #10             'gender',
        #11             'place_birth',
        #12             'country_birth',
        #13             'country',
        #14            'comments'
            
        def to_num(a):
            return to_numeric(a, errors='coerce', downcast='integer')
        
        nones=['nan', np.nan, None, "NaN", '']
        # name
        if notnull(selected_tuple[1]):
            val_name.insert(END,selected_tuple[1])
        #surname
        if notnull(selected_tuple[2]):
            val_sur.insert(END,selected_tuple[2])
        #id
        if notnull(selected_tuple[0]):
            val_id.insert(END,selected_tuple[0])
        # 
        if notnull(selected_tuple[3]):
            val_year.insert(END,selected_tuple[3])
        
        #
        v=selected_tuple[4]
        if not (isnull(v) or v in nones):
            val_death.insert(END,v)
            
        v=selected_tuple[5]
        if not (isnull(v) or v in nones):
            val_mom.insert(END, to_num(v))
        

        v=selected_tuple[6]
        if not (isnull(v) or v in nones):
            val_fat.insert(END, to_num(v))
        
        v=selected_tuple[7]
        if not (isnull(v) or v in nones):    
            val_spo.insert(END, to_num(v))
        
        v=selected_tuple[8]
        if not (isnull(v) or v in nones):    
            val_gen.insert(END, to_num(v))

        v=selected_tuple[9]
        if not (isnull(v) or v in nones):    
            val_clu.insert(END, to_num(v))


        if selected_tuple[10]==0:
            rad1.deselect()
            rad2.select()      
        else:
            rad1.select()
            rad2.deselect()     

        val_place.insert(END,selected_tuple[11])

        val_countryB.insert(END,selected_tuple[12])

        val_country.insert(END,selected_tuple[13])

        val_comment.insert(END,selected_tuple[14])
             
def sortby(tree, col, descending):
    """sort tree contents when a column header is clicked on"""
    # grab values to sort
    data = [(tree.set(child, col), child) \
        for child in tree.get_children('')]
    # if the data to be sorted is numeric change to float
    #data =  change_numeric(data)
    # now sort the data in place
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
    # switch the heading so it will sort in the opposite direction
    tree.heading(col, command=lambda col=col: sortby(tree, col, \
        int(not descending)))



# https://likegeeks.com/python-gui-examples-tkinter-tutorial/
def new_command():
    backend.insert(id_text.get(),name_text.get(), surname_text.get(),
                   year_text.get(),
                   yearDeath_text.get(),
                   mom_id.get(),
                   fath_id.get(),
                   spouse_id.get(),
                   gen_text.get(), cluster_text.get(),  gender.get(),
                   place_text.get(),
                   country_birth.get(),
                   country_text.get(),
                   comment_text.get()
                   
                   
                   
                   )
    clear_command()
    view_command()
    



def view_command():
    for i in list1.tree.get_children():
        list1.tree.delete(i)
    list1._build_tree(c_header, pddf(columns=c_header))
    df=pddf(backend.view(), columns=c_header)
    for c in ['id',   
            'mother_id',
            'father_id',
            'spouse_id',                                   
            'generation',
            'cluster', 
            'gender'       ]:
        df[c]=to_numeric(df[c], downcast='integer',errors='coerce')
    list1._build_tree(c_header, df)
    
    

def search_command():
    for i in list1.tree.get_children():
        list1.tree.delete(i)
    # list1._build_tree(c_header, pddf(columns=c_header))
    c_list=pddf(backend.search(name_text.get(),surname_text.get(),year_text.get(),gen_text.get()), columns=c_header)
    list1._build_tree(c_header, c_list)        


def delete_command():
    backend.delete(id_text.get())
    clear_command()
    view_command()

def update_command():
    backend.update( id_text.get(),name_text.get(), surname_text.get(),
                   year_text.get(), yearDeath_text.get(),
                   mom_id.get(),fath_id.get(),spouse_id.get(),
                   gen_text.get(), cluster_text.get(), gender.get(),
                   place_text.get(),
                   country_birth.get(),
                   country_text.get(),
                   comment_text.get()
                   )
    clear_command()
    view_command()

def clear_command():
    val_name.delete(0,END)
    val_sur.delete(0,END)
    val_id.delete(0,END)
    val_year.delete(0,END)
    val_death.delete(0,END)
    val_mom.delete(0,END)
    val_fat.delete(0,END)
    val_spo.delete(0,END)
    val_gen.delete(0,END)
    
    val_clu.delete(0,END)

    
    rad1.select()
    rad2.deselect()      

    val_place.delete(0,END)
    val_countryB.delete(0,END)
    val_country.delete(0,END)

    val_comment.delete(0,END)

    
def draw_tree():
    from PIL import ImageTk, Image as Image_PIL
    
    class ResizingCanvas(Canvas):
        def __init__(self,parent,**kwargs):
            Canvas.__init__(self,parent,**kwargs)
            self.bind("<Configure>", self.on_resize)
            self.height = self.winfo_reqheight()
            self.width = self.winfo_reqwidth()
            # self.bind_all("<MouseWheel>", self.on_mousewheel)
    
        def on_resize(self,event):     
            new_width = self.master.winfo_width()
            new_height = self.master.winfo_height()
    
        #colors
    col_f='#ff4e5c'
    col_m='#1c3144'
    col_w='#9d7a7d'
    #
                   
    top = tk.Tk()
    top.iconbitmap(f'{main_f}2683232.ico')
    Grid.rowconfigure(top, 0, weight=1)
    Grid.columnconfigure(top, 0, weight=1)
    top.geometry("900x480")
    top.wm_title("Tree")
    
    frame = tk.Frame(top)
    frame.grid(row=0, column=0, sticky=N+S+E+W)
    
    #scrollbars
    xscrollbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
    xscrollbar.grid(row=1, column=0, sticky="EW")
    yscrollbar = tk.Scrollbar(frame)
    yscrollbar.grid(row=0, column=1, sticky="NS")
    
    
    canvas = ResizingCanvas(frame,  xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)
    canvas.grid(row=0, column=0, sticky="EWNS")
    canvas.configure(bg='white')
    
    # Image
        
    import pydotplus as pdt
    import time

    df=pddf(backend_app.view(), columns=c_header)
    
    for c in ['id',   
            'mother_id',
            'father_id',
            'spouse_id',                                   
            'generation',
            'cluster', 
            'gender'       ]:
        df[c]=to_numeric(df[c], downcast='integer',errors='coerce')
    
    min_level=int(df['generation'].min())
    max_level=int(df['generation'].max())
    
    g = pdt.Dot(graph_type='digraph', compound='true', rankdir='TB',newrank = 'true')
    
    i=0
    edges = []
    nodes=[]
    # create all edges
    
    from ast import literal_eval as make_tuple
    nl=max_level-min_level+1
    s=[None]*(max_level+1)
    
    
    for i in range(min_level,max_level+1):
        s = pdt.Subgraph(i,rank='same')
        for j in df.loc[df['generation']==i, 'id'].values :
            s.add_node(pdt.Node(f"{df.loc[df['id']==j, 'id'].values[0]}"))
        g.add_subgraph(s)
       
    
    min_cl=int(df['cluster'].min())
    max_cl=int(df['cluster'].max())
    nl=max_cl-min_cl+1
    ss=[None]*(max_cl+1)
    for i in range(min_cl,max_cl+1):
        ss = pdt.Cluster(f'c1_{i}', color="white",rankdir="TB")
        for j in df.loc[df['cluster']==i, 'id'].values :
            ss.add_node(pdt.Node(f"{df.loc[df['id']==j, 'id'].values[0]}"))
        g.add_subgraph(ss)
      
     
        
    for i in range(df.shape[0]):
        m=df.loc[i, 'mother_id']
        f=df.loc[i, 'father_id']
        nod=pdt.Node(f"{df.loc[i, 'id']}",  shape='record', color=col_m, style='rounded')
        if m in df['id'].values:        g.add_edge(pdt.Edge(pdt.Node(f"{df.loc[df['id']==m, 'id'].values[0]}"), nod, color=col_f))
        if f in df['id'].values:        g.add_edge(pdt.Edge(pdt.Node(f"{df.loc[df['id']==f, 'id'].values[0]}"), nod, color=col_m))
    
    
        if notnull(df.loc[i, 'spouse_id']):
            who=to_numeric(df.loc[i, 'spouse_id'], downcast='integer', errors='coerce')
            if who in df['id'].values:
                g.add_edge(pdt.Edge(pdt.Node(f"{df.loc[df['id']==who, 'id'].values[0]}"), nod,  dir='none',color=col_w)) #label='m',
    
    
    
    for i in  range(df.shape[0]):
        cc=col_f
        if df.loc[i, 'gender']==1: cc=col_m
        sstr=f"{df.loc[i, 'name']}"
        if notnull(df.loc[i, 'surname']): sstr=f"{sstr} {df.loc[i, 'surname']}"
        if notnull(df.loc[i, 'date_birth']): 
            if isinstance(df.loc[i, 'date_birth'], int) or isinstance(df.loc[i, 'date_birth'], str): 
                sstr=f"{sstr}\nB: {df.loc[i, 'date_birth']}"
            else: 
                sstr=f"{sstr}\nB: {df.loc[i, 'date_birth'].strftime('%d %b %Y') }" # %H:%M:%S
        
        d=df.loc[i, 'date_death']
        # import numpy as np
        if notnull(d): 
            # print("ddd" , isna(d), isnull(d), d, type(d) )
            sstr=f"{sstr}\nD: {d}"
        
        if notnull(df.loc[i, 'place_birth']): 
            sstr=f"{sstr}\nPoB: {df.loc[i, 'place_birth']} ({df.loc[i, 'country_birth']})"
        
        if not (isnull(df.loc[i, 'comments']) or df.loc[i, 'comments']==''): 
            sstr=f"{sstr}\nComments: {df.loc[i, 'comments']}"
                
        nod=pdt.Node(f"{df.loc[i, 'id']}", label=sstr, shape='box', color=cc, style='rounded')
    
        g.add_node(nod)
    
    
    import io
    buf = io.BytesIO()
    g.write_png(buf)
    # plt.savefig(buf, format='png')
    buf.seek(0)
    img_g = Image_PIL.open(buf)
    img = ImageTk.PhotoImage(img_g, master=frame)
    canvas.create_image(0, 0, image=img)
    
    #scrollconfig
    canvas.config(scrollregion=canvas.bbox(tk.ALL))
    
    xscrollbar.config(command=canvas.xview)
    yscrollbar.config(command=canvas.yview)
    
    
    
    frame.grid(row=0, column=0)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    
    #menu
    menubar = Menu(top)
    top.config(menu=menubar)
    menu = Menu(menubar)
    
    def file_save():

        from tkinter.filedialog import asksaveasfilename
        f =  asksaveasfilename(title = "Select file",filetypes = (("png files","*.png"),("all files","*.*")), defaultextension='.png')
        if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return
        img_g.save(f)


    menu.add_command(label='Save',command=file_save)
    
    menu.add_command(label='Close',command=top.destroy)
    # menu.add_command(label="Exit", command=window.quit)
    menubar.add_cascade(label="File", menu=menu)

    top.mainloop()


window=Tk()
window.iconbitmap(f'{main_f}2683232.ico')
# https://www.flaticon.com/free-icon/tree_2683232?term=tree&page=1&position=7
 
window.geometry('1000x600') #size
window.wm_title("GenTree")

#menu
menubar = Menu(window)
window.config(menu=menubar)

menu = Menu(menubar)

def file_save_csv():

    from tkinter.filedialog import asksaveasfilename
    f =  asksaveasfilename(title = "Select file",filetypes = (("CSV files","*.csv"),("all files","*.*")), defaultextension='.png')
    if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return
    df=pddf(backend.view(), columns=c_header)
    
    df.to_csv(f, index = False)

def file_save_xls():
    from tkinter.filedialog import asksaveasfilename
    f =  asksaveasfilename(title = "Select file",filetypes = (("Excel files","*.xlsx"),("all files","*.*")), defaultextension='.png')
    if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return
    df=pddf(backend.view(), columns=c_header)
    import io
    df.to_excel(f, index = False)
  
menu.add_command(label='Save As CSV',command=file_save_csv)
menu.add_command(label='Save As Excel',command=file_save_xls)
menu.add_command(label='Close',command=window.destroy)

# menu.add_command(label="Exit", command=window.quit)
menubar.add_cascade(label="File", menu=menu)



''' first raw'''
fr1 = Frame(window)
fr1.pack(fill=X, side=TOP)

l1=Label(fr1,text="Name          ")
l1.pack(side=tk.LEFT, padx=10, pady=10)

name_text=StringVar()
val_name=BorderedEntry(fr1,bordercolor='tomato', textvariable=name_text)
val_name.pack(side=tk.LEFT, padx=10, pady=10)


l2=Label(fr1,text="Surname   ")
l2.pack(side=tk.LEFT, padx=10, pady=10)


surname_text=StringVar()
val_sur=Entry(fr1,textvariable=surname_text)
val_sur.pack(side=tk.LEFT, padx=10, pady=10)

l4=Label(fr1,text="Date of Birth")
l4.pack(side=tk.LEFT, padx=10, pady=10)

year_text=StringVar()
val_year=Entry(fr1,textvariable=year_text)
val_year.pack(side=tk.LEFT, padx=10, pady=10)


l3=Label(fr1,text="ID", width=5)
l3.pack(side=tk.LEFT, padx=10, pady=10)

id_text=StringVar()
val_id=BorderedEntry(fr1 ,bordercolor='tomato' ,textvariable=id_text)
val_id.pack(side=tk.LEFT, padx=10, pady=10)

''' second row '''
fr2 = Frame(window)
fr2.pack(fill=X, side=TOP)

l5=Label(fr2,text="Mother (ID)") #, style="BW.TLabel"
l5.pack(side=tk.LEFT, padx=10, pady=10)


mom_id=StringVar()
val_mom=Entry(fr2,textvariable=mom_id)
val_mom.pack(side=tk.LEFT, padx=10, pady=10)

l6=Label(fr2,text="Father (ID)")
l6.pack(side=tk.LEFT, padx=10, pady=10)


fath_id=StringVar()
val_fat=Entry(fr2,textvariable=fath_id)
val_fat.pack(side=tk.LEFT, padx=10, pady=10)

l7=Label(fr2,text="Generation   ")
l7.pack(side=tk.LEFT, padx=10, pady=10)

gen_text=StringVar()
val_gen=BorderedEntry(fr2, bordercolor='tomato',textvariable=gen_text)
val_gen.pack(side=tk.LEFT, padx=10, pady=10)

l8=Label(fr2,text="Cluster", width=5)
l8.pack(side=tk.LEFT, padx=10, pady=10)

cluster_text=StringVar()
val_clu=BorderedEntry(fr2,bordercolor='tomato',textvariable=cluster_text)
val_clu.pack(side=tk.LEFT, padx=10, pady=10)

''' third row '''
fr3 = Frame(window)
fr3.pack(fill=X, side=TOP)

l9=Label(fr3,text="Spouse (ID)")
l9.pack(side=tk.LEFT, padx=10, pady=10)

spouse_id=StringVar()
val_spo=Entry(fr3,textvariable=spouse_id)
val_spo.pack(side=tk.LEFT, padx=10, pady=10)


#male 

gender = tk.IntVar()
gender.set(0)
def clicked():
    print(gender.get())
rad1 = Radiobutton(fr3,text='Male', value=1, variable=gender)
rad2 = Radiobutton(fr3,text='Female', value=0, variable=gender)
rad1.select()
rad1.pack(side=tk.LEFT, padx=10, pady=10)
rad2.pack(side=tk.LEFT, padx=10, pady=10)

l10=Label(fr3,text="Place of Birth") #, style="BW.TLabel"
l10.pack(side=tk.LEFT, padx=10, pady=10)


place_text=StringVar()
val_place=Entry(fr3,textvariable=place_text)
val_place.pack(side=tk.LEFT, padx=10, pady=10)

l11=Label(fr3,text="Country of Birth")
l11.pack(side=tk.LEFT, padx=10, pady=10)


country_birth=StringVar()
val_countryB=Entry(fr3,textvariable=country_birth)

val_countryB.pack(side=tk.LEFT, padx=10, pady=10)

''' extra row '''
fr5 = Frame(window)
fr5.pack(fill=X, side=TOP)


l12=Label(fr5,text="Country      ")
l12.pack(side=tk.LEFT, padx=10, pady=10)

country_text=StringVar()
val_country=Entry(fr5,textvariable=country_text)
val_country.pack(side=tk.LEFT, padx=10, pady=10)


l14=Label(fr5,text="Date of Death")
l14.pack(side=tk.LEFT, padx=10, pady=10)

yearDeath_text=StringVar()
val_death=Entry(fr5,textvariable=yearDeath_text)
val_death.pack(side=tk.LEFT, padx=10, pady=10)


l15=Label(fr5,text="Comment")
l15.pack(side=tk.LEFT, padx=10, pady=10)

comment_text=StringVar()
val_comment=Entry(fr5,textvariable=comment_text)
val_comment.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill='both')


''' forth row '''
fr4 = Frame(window)
fr4.pack(fill=X, side=TOP)

c_header=['id',   
            'name', 
            'surname',                                   
            'date_birth',
            'date_death',
            'mother_id',
            'father_id',
            'spouse_id',                                   
            'generation',
            'cluster', 
            'gender',
            'place_birth',
            'country_birth',
            'country',
            'comments'
                                                            ]
c_list=pddf(backend.view(), columns=c_header)

list1 = MultiColumnListbox(c_header, c_list)

''' fifth row '''
fr5 = Frame(window)
fr5.pack(fill=X, side=TOP)

# '''Buttons'''

b_clear=HoverButton(fr5,text="Clear Fields", width=12,command=clear_command,  activebackground='SlateGray3')
b_clear.pack(side=tk.LEFT, pady=15, padx=10)

b3=HoverButton(fr5,text="Add entry", width=12,command=new_command,  activebackground='SlateGray3') 
b3.pack(side=tk.LEFT, pady=15, padx=10)


b4=HoverButton(fr5,text="Update selected", width=12,command=update_command,  activebackground='SlateGray3')
b4.pack(side=tk.LEFT, pady=15, padx=10)

b5=HoverButton(fr5,text="Delete selected", width=12,command=delete_command,  activebackground='SlateGray3')
b5.pack(side=tk.LEFT, pady=15, padx=10)

b2=HoverButton(fr5,text="Search entry", width=12,command=search_command,  activebackground='SlateGray3')
b2.pack(side=tk.LEFT, pady=15, padx=10)


b1=HoverButton(fr5,text="View all", width=12,command=view_command,  activebackground='SlateGray3')
b1.pack(side=tk.LEFT, pady=15, padx=10)

b7=HoverButton(fr5,text="Grow a Tree", width=12,command=draw_tree,  activebackground='SlateGray3')
b7.pack(side=tk.LEFT, pady=15, padx=10)

window.mainloop()

'''settings'''
# https://stackoverflow.com/questions/45729624/graphvizs-executables-not-found-anaconda-3
# https://stackoverflow.com/questions/35064304/runtimeerror-make-sure-the-graphviz-executables-are-on-your-systems-path-aft
# conda install python-graphviz
# conda install pydotplus 
# conda install pandas
# conda install pillow
# conda install -c anaconda ipython
# conda install pyinstaller
# pip install pypiwin32
# conda install cython

#or 
# pip install graphviz
# pip install pydotplus 
# pip install numpy
# pip install pandas
# pip install pillow
# pip install ipython
# pip install pyinstaller

# Settings
# Now you should be on the "advanced" tab of the System properties menu. Click the "Environment variables" button at the bottom of this menu -> Select path in the new menu -> Click "Edit" -> Click "New" -> In this box paste the link from your Python warning box. For me this was "C:\Users\David\Anaconda3\Library\bin\graphviz" but it may be different. Hit enter.
# Close all programs and restart your PC. This is necessary for the new path to take effect.

'''MAKE EXE file via pyistaller'''
# https://stackoverflow.com/questions/43886822/pyinstaller-with-pandas-creates-over-500-mb-exe/48846546#48846546

#1 Create virtual env
# conda create -n pip_gentree
# activate pip_gentree
# cd c:\a_tree\app

# run
# python frontend_multi_g.py


# in terminal go to folder by cd PATH
# in terminal run
# pyinstaller --onefile --windowed frontend_multi_g.py
# pyinstaller --onefile frontend_multi_g.spec

