#--------------------------------------------Imports-------------------------------------------------------------------#
from tkinter import *
import tkinter.filedialog
from tkinter import messagebox as t

from xml_validation import validate
from xml_get_type import get_type_
from xml_show_error import showError




root = Tk()
root.geometry('1200x700')
root.title('XML EDITOR')

#-------------------------------------------------Variables Declerations-----------------------------------------------#
global source
global lines
global types
global stack
global errors
global prettify
global close_stack
global remove_new_lines
global open_stack
global file_name
close_stack =[]
open_stack=[]
prettify = []
source = []
lines = []
types = []
stack = []
errors = []
close_stack = []
remove_new_lines = []

#-----------------------------------------------------Node Decleration-------------------------------------------------#
class Node:
    def __init__(self, data):
        self.children = []
        #super(Node, self).__init__()
        self.data = data

    def insert(self, data, baba):  # Compare the new value with the parent node
        if self.data == baba:
            self.children.append(Node(data))
        else:
            for l in self.children:
                l.insert(data, baba)

    def synset_count(self):
        if not self.children :return 1
        for z in self.children:
            if z.children:
                return 0
        return 1
    def synset_no(self):
        if not self.children:return 0
        count =0
        for a in self.children:
            count+= a.synset_no()
        if not count : return 1
        #for b in self.children:
        #    b.synset_no()
        return count


    def definition(self,word):
        found=False
        for l in self.children:
            if l.data['tag_name'].strip()=='word' and  "".join(l.data['body'])==word:
                found =True
            if found and l.data['tag_name'].strip() =='def':
                errorText.delete(1.0,END)
                errorText.insert(INSERT,word+'  :  '+"".join(l.data['body']))
                print("".join(l.data['body']))
                return
        for l in self.children:
            l.definition(word)
    # Print the tree
    def PrintTree(self):
        global root
        global num_spaces
        if self.data == root.data :
            text.insert(INSERT,'  "' + self.data['tag_name'] + '": {\n')
            num_spaces += 1
        elif self.children or self.data['attr']:
           arr=False
           if prettify[self.data['line_number']] == -1 :
                num_spaces -= 1
           if not self.children:
               dum =num_spaces
               num_spaces=3
           if self.children:  # self.synset_no()==1:
               for h in range(len(self.children) - 1):
                   #if h != 0:
                   #    if self.children[h].data['tag_name'] != '0' + self.children[h - 1].data['tag_name']:
                           if self.children[h].data['tag_name'] == self.children[h + 1].data['tag_name']:
                               u = self.children[h].data['tag_name']
                               self.children[h].data['tag_name'] = '1' + self.children[h].data['tag_name']
                               for j, g in enumerate(range(len(self.children) - (h + 1)), start=h):
                                   y = self.children[j + 1].data['tag_name']
                                   if y == u:
                                       self.children[j + 1].data['tag_name'] = '0' + self.children[h].data[
                                           'tag_name']
                                   else:
                                       break
           if self.children or self.synset_no()==1:
               k='['
               arr=True
           else:
               k='{'
               arr=False
           if not self.children:
               if self.data['tag_name'][0] == '1' and self.data['tag_name'][1] != '0' and self.data['tag_name'][1] != '1' :
                   text.insert(INSERT,num_space()+'      "'+self.data['tag_name'][1:]+'":  [ \n')
                   text.insert(INSERT,num_space()+'             {\n')
               elif self.data['tag_name'][0] =='0' or self.data['tag_name'][0] == '1':text.insert(INSERT,num_space()+'            {'+'\n')
               else :text.insert(INSERT,num_space()+'      "'+self.data['tag_name']+'":  {\n')
           else :
               if self.data['tag_name'][0] == '1' and self.data['tag_name'][1] != '0' and self.data['tag_name'][1] != '1' :
                   text.insert(INSERT,num_space()+'      "'+self.data['tag_name'][1:]+'":  \n')
                 #  text.insert(INSERT, num_space() + '             {\n')
               elif self.data['tag_name'][0] == '0':
                   text.insert(INSERT, num_space() + '            {' + '\n')
               elif self.data['tag_name'][0] != '0' and self.data['tag_name'][0] != '1' : text.insert(INSERT, num_space() + '      "' + self.data['tag_name'] + '": [   \n')
           if arr :  text.insert(INSERT,num_space()+'           {\n')
           if prettify[self.data['line_number']] == 1 and num_spaces<=4:
                num_spaces += 1
           sec =False
           thi =False
           if self.data['attr'] and self.data['attr'].find('=') !=-1:
               r=self.data['attr'].split("=",1)
               if r[1].find('" ') != -1:
                   sec=True
                   second=r[1].find('" ')+1
                   s=r[1][second+1:]
                   r[1] = r[1][: second]
                   s = s.split("=", 1)
                   if s[1].find('" ') != -1:
                       thi = True
                       third = s[1].find('" ') + 1
                       t = s[1][third + 1:]
                       s[1] = s[1][: third]
                       t = t.split("=", 1)
               if not self.children:
                   dum=num_spaces
                   num_spaces=4
                   k=',' if self.data['body'] else ''
                   text.insert(INSERT,num_space()+'      "__'+r[0]+'" : '+r[1]+'' +k+'\n')
                   if sec :
                       text.insert(INSERT, num_space() + '      "__' + s[0] + '" : ' + s[1] + '' + k + '\n')
                       if thi :
                           text.insert(INSERT, num_space() + '      "__' + t[0] + '" : ' + t[1] + '' + k + '\n')
                   if self.data['body']:
                       bod = "".join(self.data['body'])
                       text.insert(INSERT, num_space() + '      "__text" : ' +'"' +bod + '"\n')
        else:
            dum=num_spaces
            num_spaces =4
            bod="".join(self.data['body'])
            if self.data['tag_name'][0] == '1' and self.data['tag_name'][1] != '0' :
                text.insert(INSERT, num_space() + '     "' + self.data['tag_name'][1:] + '":  [\n')
                text.insert(INSERT, num_space() + '                   "' + bod + '",\n')
            elif self.data['tag_name'][0] == '1'and self.data['tag_name'][1] == '0':
                #text.insert(INSERT, num_space() + '     "' + self.data['tag_name'][1:] + '":  [\n')
                text.insert(INSERT, num_space() + '                   "' + bod + '",\n')
            elif self.data['tag_name'][0] == '0':
                text.insert(INSERT, num_space() + '                   "' + bod + '",\n')
            else:
                text.insert(INSERT, num_space() + '   "' + self.data['tag_name'] + '": "' + bod + '",\n')
            #text.insert(INSERT,num_space() + '     "' + self.data['tag_name'] + '": "' + bod + '",\n')
            num_spaces=dum
            num_spaces-=1

        if self.children:
          for l in range(len(self.children)):
             self.children[l].PrintTree()
          if self.data==root.data :
              if self.data['attr']:
                  r = self.data['attr'].split("=")
                  if r[1].find(' ') !=-1 : r[1]=r[1][ : r[1].find(' ')]
                  text.insert(INSERT,  '      "__' + r[0] + '" : ' + r[1] + '\n')
              text.insert(INSERT, '  }\n')
          else:
              if self.data['attr'] and self.data['attr'].find('=') != -1:
                  if self.children:
                      text.insert(INSERT, num_space() + '      "__' + r[0] + '" : ' + r[1] + ',\n')
                      if sec:
                          text.insert(INSERT, num_space() + '      "__' + s[0] + '" : ' + s[1] + ',\n')
                          if thi:
                              text.insert(INSERT, num_space() + '      "__' + t[0] + '" : ' + t[1] + ',\n')
                  if self.data['body']:
                      bod = "".join(self.data['body'])
                      if self.children:text.insert(INSERT, num_space() + '      "__text" : ' + '"' + bod + '"\n')
              if arr:
                  text.insert(INSERT,num_space() + '       }\n')
                  text.insert(INSERT,num_space() + '    ],\n')

        elif self.data['attr']:    text.insert(INSERT,num_space() + '     },\n')


#------------------------------------Show Errors-----------------------------------------------------------------------#
def errormessage(str,event=None):
   t.showerror("Error",str)

def infomessage(str,event=None):
   t.showinfo("Info",str)


#-------------------------------------------Make Indentations----------------------------------------------------------#

def num_space():
    spaces = ' '
    global num_spaces
    for l in range(num_spaces):
        spaces += spaces
    return spaces



#-------------------------------------------Print JSON In File --------------------------------------------------------#

def JSON():
    rootInit()
    valid = validate(source)
    if valid:
        global root
        global num_spaces
        text.delete(1.0, END)
        text.insert(INSERT, '{\n')
        root.PrintTree()
        text.insert(INSERT, '}\n')
        num_spaces = 0
    else:
        errormessage('Correct XML First')
#-------------------------------------Print Side Numbers---------------------------------------------------------------#

def update_line_numbers(event=None):
    line_numbers = get_line_numbers()
    line_number_bar.config(state='normal')
    line_number_bar.delete('1.0', 'end')
    line_number_bar.insert('1.0', line_numbers)
    line_number_bar.config(state='disabled')

def on_content_changed(event=None):
    update_line_numbers()

def get_line_numbers():
    output = ''
    if show_line_number.get():
        row, col = text.index("end").split('.')
        for i in range(1, int(row)):
            output += str(i) + '\n'
    return output


#---------------------------------
# ---------Get Synset Count and Word Definition----------------------------------------#

def syn_count():
    errorText.delete(1.0,END)

    errorText.insert(INSERT,('Number of synsets : '+ str(root.synset_no()) ))




def Define():
    try:
        rootInit()
        root.definition(str(entry.get()))
    except:
        print(0)


#----------------------------------------Open FIle---------------------------------------------------------------------#

def open_file(event=None):
    global source
    global errors
    source = []
    i=0
    file = tkinter.filedialog.askopenfilename(defaultextension=".xml",filetypes=[("All Files", "*.*"), ("XML Files", "*.xml")])
    if file:
        global file_name
        file_name = file
        text.delete(1.0, END)
        with open(file_name) as f:
            text.insert(1.0, f.read())
        with open(file_name, 'r') as f:
               source = f.readlines()
        start()
        start_pos1 = '1.0'
        start_pos2 = '1.0'
        x='<'

        while True:
            start_pos1 = text.search('<', start_pos1, stopindex=END)
            if not start_pos1: break
            end_pos1 = '{}+{}c'.format(start_pos1, len(x))
            text.tag_add('match', start_pos1, end_pos1)
            start_pos1 = end_pos1
            text.tag_config(
                'match', foreground='yellow')
        start_pos1 = '1.0'
        while True:
            start_pos1 = text.search('>', start_pos1, stopindex=END)
            if not start_pos1: break
            end_pos1 = '{}+{}c'.format(start_pos1, len(x))
            text.tag_add('match', start_pos1, end_pos1)
            start_pos1 = end_pos1
            text.tag_config(
                'match', foreground='yellow')

#-------------------------------------------Write In File--------------------------------------------------------------#
def write(file_name):
    try:
        content = text.get(1.0, 'end')
        with open(file_name, 'w') as the_file:
            the_file.write(content)
    except :
        print(0)

#------------------------------------------Save/Save As File-----------------------------------------------------------#
def save_as():
    file = tkinter.filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("All Files", "*.*"), ("XML Files", "*.xml")])
    if file:
        global file_name
        file_name = file
        write(file_name)
    return "break"

def save():
    global file_name
    global source
    write(file_name)
    source = []
    with open(file_name, 'r') as f:
        source = f.readlines()
    start()
    return "break"


#--------------------------------------------------Print XML File------------------------------------------------------#
def source_print():
    global so
    global errors
    
    text.delete(1.0, END)
    for s in so:
        text.insert(INSERT,s )

#----------------------------------------------Minify XML File --------------------------------------------------------#
def Minify():
    valid = validate(source)
    if valid:
        global so
        global errors
        global lines
        text.delete(1.0, END)
        s="".join(lines)
        text.insert(INSERT,s )
    else:
        errormessage('Correct XML First')


#---------------------------------------------Prettify XML FIle--------------------------------------------------------#

def pretty():
    rootInit()
    valid = validate(source)
    if valid:
        global prettify
        global num_spaces
        global lines
        flag=True
        num_spaces =0
        text.delete(1.0,END)
        for l,line in enumerate(lines):
            if l == len(lines)-1:flag=True
            if flag:
                text.insert(INSERT,lines[l]+'\n')
                if prettify[l]==1:
                    num_spaces+=1
                    flag=False
            elif prettify[l] == 0:
                text.insert(INSERT,num_space()+lines[l]+'\n')
            elif prettify[l] == 1:
                text.insert(INSERT,num_space()+lines[l]+'\n')
                if num_spaces<6:num_spaces+=1
            else:
                num_spaces-=1
                text.insert(INSERT,num_space()+lines[l]+'\n')
    else:
        errormessage('Correct XML First')

#-----------------------------------------------ShowErrors XML File----------------------------------------------------#

def showerror():
    result = showError(source)
    validate = result[0]
    errors = result[1]

    errorText.delete(1.0,END)
    if not validate and not errors:
        infomessage('XML is valid')
        return
    errormessage('XML is not valid')
    print(errors)
    print(validate)
    errorText.delete(1.0, END)
    for l in validate:
        errorText.insert(INSERT, l + '\n')
    for u in errors:
        errorText.insert(INSERT,'line '+str(u['line_number']+1)+' : ' + str(u['val'])+'\n')


#----------------------------------------------Validate XML------------------------------------------------------------#
def validate_x():
    valid = validate(source)
    print(valid)
    if valid:
        infomessage('XML is valid')
        return
    else:
        errormessage('XML is not valid')
#-------------------------------------solve errors----------------------------------------------------------------------
def solve_error():
    rootInit()
    result = showError(source)
    errors = result[1]
    text.delete(1.0, END)
    for z in range(len(errors)):
        line_num = errors[z]['line_number']
        if errors[z]['val'] == 'tags must end with >':
            so[line_num] = so[line_num].replace(lines[line_num], lines[line_num] + '>')
            # fix.append(lines[types[z]['line_number']] + '>')
            continue
        if errors[z]['val'] == '< is missing':
            if errors[z].get('solu') == 'replace/':
                so[line_num] = so[line_num].replace('/', '</')
                # fix.append(lines[types[z]['line_number']].replace('/', '</'))
                continue
            if errors[z].get('solu') == '< at begining':
                so[line_num] = so[line_num].replace(lines[line_num], '<' + lines[line_num])
                # fix.append('<' + lines[types[z]['line_number']])
                continue

            if errors[z].get('solu') == 'delete body before <':
                x = lines[line_num]
                so[line_num] = x[x.find('<'):]+'\n'
        if errors[z]['val'] == 'found extra / or <':
            l_num = lines[line_num]
            new = l_num[l_num.find('/') + 1: -1]
            so[line_num] = so[line_num].replace(new, new + '>', 1)



    for l in so:
        text.insert(INSERT, l )

#----------------------------------------------Root and Prettify Initialise--------------------------------------------#
def rootInit():
    global source
    global so
    global errors
    global lines
    global root
    global prettify
    global num_spaces
    num_spaces = 0
    prettify = []
    so = []
    lines = []
    stack = []

    types = get_type_(source)
    for line in source:
        x = line.strip()
        if len(x) > 0:
            so.append(line)
            lines.append(x)

    lines = [x for x in lines if x != '']
    for line in lines:
        prettify.append(0)

    root_check = True

    for i, tag in enumerate(types):
        if tag['type'] == 'selfClosingTag':
            if stack:
                root.insert(tag, stack[-1])

        if tag['type'] == 'openTag':
            prettify[tag['line_number']] += 1
            if root_check:
                root = Node(tag)
                root_check = False
                stack.append(tag)
            else:
                if stack:
                    root.insert(tag, stack[-1])
                stack.append(tag)
            continue
        if tag['type'] == 'closeTag':
            prettify[tag['line_number']] -= 1
            if stack:
                if stack[-1]['tag_name'] == tag['tag_name']:
                    stack.pop(-1)
                    continue

        if tag['type'] == 'body':
            if stack:
                continue

#-------------------------------------------------Start Function-------------------------------------------------------#
def start():
    pass


#--------------------------------------------------###############-----------------------------------------------------#


#---------------------------------------------Tkinter Declerations-----------------------------------------------------#


global num_spaces
num_spaces = 0
inputframe = Frame(root)
show_line_number = IntVar()
show_line_number.set(1)
menu_bar = Menu(root)
file_menu = Menu(menu_bar, tearoff=0)

file_menu.add_command(label='Open',  command=open_file)

file_menu.add_command(label='Save', underline=0, command=save)
file_menu.add_command(label='Save as', command=save_as)
file_menu.add_separator()
file_menu.add_command(label='Exit', accelerator='Alt+F4', command=exit)
menu_bar.add_cascade(label='File', menu=file_menu)
menu_bar.add_command(label='Show Errors',  command=showerror)
menu_bar.add_command(label='Validate',  command=validate_x)
menu_bar.add_command(label='JSON', command=JSON)
menu_bar.add_command(label='Minify', command=Minify)
menu_bar.add_command(label='Number of synsets', command=syn_count)
menu_bar.add_command(label='Prettify', command=pretty)
menu_bar.add_command(label='Show Original File',  command=source_print)
root.config(menu=menu_bar)
menu_bar.add_command(label='Solve Errors',  command=solve_error)
line_number_bar = Text(inputframe, width=4, padx=3, takefocus=0,  border=0,
                       background='grey40', state='disabled',  wrap='none', fg='grey80')
line_number_bar.pack(side='left',  fill='y')
text = Text(inputframe,bg='grey25',fg='white')


def viewall(*args):
    text.yview(*args)
    line_number_bar.yview(*args)


errort = Frame(root, height=10)
text.pack(expand='yes', fill='both')
errorText = Text(errort, height=10, takefocus=0, relief=RAISED, border=0,background='grey20', wrap='none',fg='grey95')
scroll_bar = Scrollbar(text)
scroll_bar1 = Scrollbar(errort)
scroll_bar1.config(command=errorText.yview())
text.configure(yscrollcommand=scroll_bar.set)
errorText.configure(yscrollcommand=scroll_bar1.set)
line_number_bar.configure(yscrollcommand=scroll_bar.set)
scroll_bar.config(command=viewall)
scroll_bar.pack(side='right', fill='y')
scroll_bar1.pack(side='right', fill='y')
text.bind('<Any-KeyPress>', on_content_changed)
inputframe.pack(expand='yes', fill='both')
errorText.pack( fill='x')
errort.pack(expand='no', fill='x')
lf = LabelFrame(root, text='Find Def', height=20,bg='grey19',fg='grey80')
lf.pack(fill='both')
entry = Entry(lf)
entry.pack(fill='both')
Button(lf, text='Find', width=20, command=Define).pack()
root.mainloop()
