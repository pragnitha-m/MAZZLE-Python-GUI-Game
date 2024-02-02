import random,datetime,csv,os
from tkinter import *
from enum import Enum
from collections import deque

class COLOR(Enum):
    ''' The first two objects (dark and light) are for theme and the two color
    The rest of the colors are for Agents. '''
    dark=('gray11','white')
    light=('white','black')
    black=('black','dim gray')
    red=('red3','tomato')
    cyan=('cyan4','cyan4')
    green=('green4','pale green')
    blue=('DeepSkyBlue4','DeepSkyBlue2')
    yellow=('yellow2','yellow2')
class agent:
    #The agents can be placed on the maze.They can have two shapes (square or arrow)
    def __init__(self,parentMaze,x=None,y=None,shape='square',goal=None,filled=False,footprints=False,color:COLOR=COLOR.blue):
        self._parentMaze=parentMaze
        self.color=color
        if(isinstance(color,str)):
            if(color in COLOR.__members__):
                self.color=COLOR[color]
            else:
                raise ValueError(f'{color} is not a valid COLOR!')
        self.filled=filled
        self.shape=shape
        self._orient=0
        if x is None:x=parentMaze.rows
        if y is None:y=parentMaze.cols
        self.x=x
        self.y=y
        self.footprints=footprints
        self._parentMaze._agents.append(self)
        if goal==None:
            self.goal=self._parentMaze._goal
        else:
            self.goal=goal
        self._body=[]
        self.position=(self.x,self.y)
        
    @property
    def x(self):
        return self._x
    @x.setter
    def x(self,newX):
        self._x=newX
    @property
    def y(self):
        return self._y
    @y.setter
    def y(self,newY):
        self._y=newY
        w=self._parentMaze._cell_width
        x=self.x*w-w+self._parentMaze._LabWidth
        y=self.y*w-w+self._parentMaze._LabWidth
        if self.shape=='square':
            if self.filled:
                self._coord=(y, x,y + w, x + w)
            else:
                self._coord=(y + w/2.5, x + w/2.5,y + w/2.5 +w/4, x + w/2.5 +w/4)
        else:
            self._coord=(y + w/2, x + 3*w/9,y + w/2, x + 3*w/9+w/4)

        if(hasattr(self,'_head')):
            if self.footprints is False:
                self._parentMaze._canvas.delete(self._head)
            else:
                if self.shape=='square':
                    self._parentMaze._canvas.itemconfig(self._head, fill=self.color.value[1],outline="")
                    self._parentMaze._canvas.tag_raise(self._head)
                    try:
                        self._parentMaze._canvas.tag_lower(self._head,'ov')
                    except:
                        pass
                    if self.filled:
                        lll=self._parentMaze._canvas.coords(self._head)
                        oldcell=(round(((lll[1]-26)/self._parentMaze._cell_width)+1),round(((lll[0]-26)/self._parentMaze._cell_width)+1))
                        self._parentMaze._redrawCell(*oldcell,self._parentMaze.theme)
                else:
                    self._parentMaze._canvas.itemconfig(self._head, fill=self.color.value[1])#,outline='gray70')
                    self._parentMaze._canvas.tag_raise(self._head)
                    try:
                        self._parentMaze._canvas.tag_lower(self._head,'ov')
                    except:
                        pass
                self._body.append(self._head)
            if not self.filled or self.shape=='arrow':
                if self.shape=='square':
                    self._head=self._parentMaze._canvas.create_rectangle(*self._coord,fill=self.color.value[0],outline='') #stipple='gray75'
                    try:
                        self._parentMaze._canvas.tag_lower(self._head,'ov')
                    except:
                        pass
                else:
                    self._head=self._parentMaze._canvas.create_line(*self._coord,fill=self.color.value[0],arrow=FIRST,arrowshape=(3/10*w,4/10*w,4/10*w))#,outline=self.color.name)
                    try:
                        self._parentMaze._canvas.tag_lower(self._head,'ov')
                    except:
                        pass
                    o=self._orient%4
                    if o==1:
                        self._RCW()
                        self._orient-=1
                    elif o==3:
                        self._RCCW()
                        self._orient+=1
                    elif o==2:
                        self._RCCW()
                        self._RCCW()
                        self._orient+=2
            else:
                self._head=self._parentMaze._canvas.create_rectangle(*self._coord,fill=self.color.value[0],outline='')#stipple='gray75'
                try:
                    self._parentMaze._canvas.tag_lower(self._head,'ov')
                except:
                        pass
                self._parentMaze._redrawCell(self.x,self.y,theme=self._parentMaze.theme)
        else:
            self._head=self._parentMaze._canvas.create_rectangle(*self._coord,fill=self.color.value[0],outline='')#stipple='gray75'
            try:
                self._parentMaze._canvas.tag_lower(self._head,'ov')
            except:
                pass
            self._parentMaze._redrawCell(self.x,self.y,theme=self._parentMaze.theme)
    @property
    def position(self):
        return (self.x,self.y)
    @position.setter
    def position(self,newpos):
        self.x=newpos[0]
        self.y=newpos[1]
        self._position=newpos
    def _RCCW(self):
        '''
        To Rotate the agent in Counter Clock Wise direction
        '''
        def pointNew(p,newOrigin):
            return (p[0]-newOrigin[0],p[1]-newOrigin[1])
        w=self._parentMaze._cell_width
        x=self.x*w-w+self._parentMaze._LabWidth
        y=self.y*w-w+self._parentMaze._LabWidth
        cent=(y+w/2,x+w/2)
        p1=pointNew((self._coord[0],self._coord[1]),cent)
        p2=pointNew((self._coord[2],self._coord[3]),cent)
        p1CW=(p1[1],-p1[0])
        p2CW=(p2[1],-p2[0])
        p1=p1CW[0]+cent[0],p1CW[1]+cent[1]
        p2=p2CW[0]+cent[0],p2CW[1]+cent[1]
        self._coord=(*p1,*p2)  
        self._parentMaze._canvas.coords(self._head,*self._coord)
        self._orient=(self._orient-1)%4
 
        
    def _RCW(self):
        '''
        To Rotate the agent in Clock Wise direction
        '''
        def pointNew(p,newOrigin):
            return (p[0]-newOrigin[0],p[1]-newOrigin[1])
        w=self._parentMaze._cell_width
        x=self.x*w-w+self._parentMaze._LabWidth
        y=self.y*w-w+self._parentMaze._LabWidth
        cent=(y+w/2,x+w/2)
        p1=pointNew((self._coord[0],self._coord[1]),cent)
        p2=pointNew((self._coord[2],self._coord[3]),cent)
        p1CW=(-p1[1],p1[0])
        p2CW=(-p2[1],p2[0])
        p1=p1CW[0]+cent[0],p1CW[1]+cent[1]
        p2=p2CW[0]+cent[0],p2CW[1]+cent[1]
        self._coord=(*p1,*p2)  
        self._parentMaze._canvas.coords(self._head,*self._coord)
        self._orient=(self._orient+1)%4


    def moveRight(self,event):
        if self._parentMaze.maze_map[self.x,self.y]['E']==True:
            self.y=self.y+1
    def moveLeft(self,event):
        if self._parentMaze.maze_map[self.x,self.y]['W']==True:
            self.y=self.y-1
    def moveUp(self,event):
        if self._parentMaze.maze_map[self.x,self.y]['N']==True:
            self.x=self.x-1
            self.y=self.y
    def moveDown(self,event):
        if self._parentMaze.maze_map[self.x,self.y]['S']==True:
            self.x=self.x+1
            self.y=self.y
class maze:
    #This is the main class to create maze.
    def __init__(self,rows=10,cols=10):
        #rows--> No. of rows of the maze, cols--> No. of columns of the maze
        self.rows=rows
        self.cols=cols
        self.maze_map={}
        self.grid=[]
        self.path={} 
        self._cell_width=50  
        self._win=None 
        self._canvas=None
        self._agents=[]
        self.markCells=[]

    @property
    def grid(self):
        return self._grid
    @grid.setter        
    def grid(self,n):
        self._grid=[]
        y=0
        for n in range(self.cols):
            x = 1
            y = 1+y
            for m in range(self.rows):
                self.grid.append((x,y))
                self.maze_map[x,y]={'E':0,'W':0,'N':0,'S':0}
                x = x + 1 
    def _Open_East(self,x, y):
        #To remove the East Wall of the cell
        self.maze_map[x,y]['E']=1
        if y+1<=self.cols:
            self.maze_map[x,y+1]['W']=1
    def _Open_West(self,x, y):
        self.maze_map[x,y]['W']=1
        if y-1>0:
            self.maze_map[x,y-1]['E']=1
    def _Open_North(self,x, y):
        self.maze_map[x,y]['N']=1
        if x-1>0:
            self.maze_map[x-1,y]['S']=1
    def _Open_South(self,x, y):
        self.maze_map[x,y]['S']=1
        if x+1<=self.rows:
            self.maze_map[x+1,y]['N']=1
    
    def CreateMaze(self,x=1,y=1,pattern=None,loopPercent=0,saveMaze=False,loadMaze=None,theme:COLOR=COLOR.dark):
        '''pattern-->  It can be 'v' for vertical or 'h' for horizontal
        loopPercent-->  0 means there will be just one path from start to goal (perfect maze)
        Higher value means there will be multiple paths (loops),Higher the value (max 100) more will be the loops
        saveMaze--> To save the generated Maze as CSV file for future reference.
        loadMaze--> Provide the CSV file to generate a desried maze, theme--> Dark or Light'''
        _stack=[]
        _closed=[]
        self.theme=theme
        self._goal=(x,y)
        if(isinstance(theme,str)):
            if(theme in COLOR.__members__):
                self.theme=COLOR[theme]
            else:
                raise ValueError(f'{theme} is not a valid theme COLOR!')
        def blockedNeighbours(cell):
            n=[]
            for d in self.maze_map[cell].keys():
                if self.maze_map[cell][d]==0:
                    if d=='E' and (cell[0],cell[1]+1) in self.grid:
                        n.append((cell[0],cell[1]+1))
                    elif d=='W' and (cell[0],cell[1]-1) in self.grid:
                        n.append((cell[0],cell[1]-1))
                    elif d=='N' and (cell[0]-1,cell[1]) in self.grid:
                        n.append((cell[0]-1,cell[1]))
                    elif d=='S' and (cell[0]+1,cell[1]) in self.grid:
                        n.append((cell[0]+1,cell[1]))
            return n
        def removeWallinBetween(cell1,cell2):
            '''
            To remove wall in between two cells
            '''
            if cell1[0]==cell2[0]:
                if cell1[1]==cell2[1]+1:
                    self.maze_map[cell1]['W']=1
                    self.maze_map[cell2]['E']=1
                else:
                    self.maze_map[cell1]['E']=1
                    self.maze_map[cell2]['W']=1
            else:
                if cell1[0]==cell2[0]+1:
                    self.maze_map[cell1]['N']=1
                    self.maze_map[cell2]['S']=1
                else:
                    self.maze_map[cell1]['S']=1
                    self.maze_map[cell2]['N']=1
        def isCyclic(cell1,cell2):
            '''
            To avoid too much blank(clear) path.
            '''
            ans=False
            if cell1[0]==cell2[0]:
                if cell1[1]>cell2[1]: cell1,cell2=cell2,cell1
                if self.maze_map[cell1]['S']==1 and self.maze_map[cell2]['S']==1:
                    if (cell1[0]+1,cell1[1]) in self.grid and self.maze_map[(cell1[0]+1,cell1[1])]['E']==1:
                        ans= True
                if self.maze_map[cell1]['N']==1 and self.maze_map[cell2]['N']==1:
                    if (cell1[0]-1,cell1[1]) in self.grid and self.maze_map[(cell1[0]-1,cell1[1])]['E']==1:
                        ans= True
            else:
                if cell1[0]>cell2[0]: cell1,cell2=cell2,cell1
                if self.maze_map[cell1]['E']==1 and self.maze_map[cell2]['E']==1:
                    if (cell1[0],cell1[1]+1) in self.grid and self.maze_map[(cell1[0],cell1[1]+1)]['S']==1:
                        ans= True
                if self.maze_map[cell1]['W']==1 and self.maze_map[cell2]['W']==1:
                    if (cell1[0],cell1[1]-1) in self.grid and self.maze_map[(cell1[0],cell1[1]-1)]['S']==1:
                        ans= True
            return ans
        # if maze is to be generated randomly
        if not loadMaze:
            _stack.append((x,y))
            _closed.append((x,y))
            biasLength=2 # if pattern is 'v' or 'h'
            if(pattern is not None and pattern.lower()=='h'):
                biasLength=max(self.cols//10,2)
            if(pattern is not None and pattern.lower()=='v'):
                biasLength=max(self.rows//10,2)
            bias=0

            while len(_stack) > 0:
                cell = []
                bias+=1
                if(x , y +1) not in _closed and (x , y+1) in self.grid:
                    cell.append("E")
                if (x , y-1) not in _closed and (x , y-1) in self.grid:
                    cell.append("W")
                if (x+1, y ) not in _closed and (x+1 , y ) in self.grid:
                    cell.append("S")
                if (x-1, y ) not in _closed and (x-1 , y) in self.grid:
                    cell.append("N") 
                if len(cell) > 0:    
                    if pattern is not None and pattern.lower()=='h' and bias<=biasLength:
                        if('E' in cell or 'W' in cell):
                            if 'S' in cell:cell.remove('S')
                            if 'N' in cell:cell.remove('N')
                    elif pattern is not None and pattern.lower()=='v' and bias<=biasLength:
                        if('N' in cell or 'S' in cell):
                            if 'E' in cell:cell.remove('E')
                            if 'W' in cell:cell.remove('W')
                    else:
                        bias=0
                    current_cell = (random.choice(cell))
                    if current_cell == "E":
                        self._Open_East(x,y)
                        self.path[x, y+1] = x, y
                        y = y + 1
                        _closed.append((x, y))
                        _stack.append((x, y))

                    elif current_cell == "W":
                        self._Open_West(x, y)
                        self.path[x , y-1] = x, y
                        y = y - 1
                        _closed.append((x, y))
                        _stack.append((x, y))

                    elif current_cell == "N":
                        self._Open_North(x, y)
                        self.path[(x-1 , y)] = x, y
                        x = x - 1
                        _closed.append((x, y))
                        _stack.append((x, y))

                    elif current_cell == "S":
                        self._Open_South(x, y)
                        self.path[(x+1 , y)] = x, y
                        x = x + 1
                        _closed.append((x, y))
                        _stack.append((x, y))

                else:
                    x, y = _stack.pop()

            ## Multiple Path Loops
            if loopPercent!=0:
                
                x,y=self.rows,self.cols
                pathCells=[(x,y)]
                while x!=self.rows or y!=self.cols:
                    x,y=self.path[(x,y)]
                    pathCells.append((x,y))
                notPathCells=[i for i in self.grid if i not in pathCells]
                random.shuffle(pathCells)
                random.shuffle(notPathCells)
                pathLength=len(pathCells)
                notPathLength=len(notPathCells)
                count1,count2=pathLength/3*loopPercent/100,notPathLength/3*loopPercent/100
                
                #remove blocks from shortest path cells
                count=0
                i=0
                while count<count1: #these many blocks to remove
                    if len(blockedNeighbours(pathCells[i]))>0:
                        cell=random.choice(blockedNeighbours(pathCells[i]))
                        if not isCyclic(cell,pathCells[i]):
                            removeWallinBetween(cell,pathCells[i])
                            count+=1
                        i+=1
                            
                    else:
                        i+=1
                    if i==len(pathCells):
                        break
                #remove blocks from outside shortest path cells
                if len(notPathCells)>0:
                    count=0
                    i=0
                    while count<count2: #these many blocks to remove
                        if len(blockedNeighbours(notPathCells[i]))>0:
                            cell=random.choice(blockedNeighbours(notPathCells[i]))
                            if not isCyclic(cell,notPathCells[i]):
                                removeWallinBetween(cell,notPathCells[i])
                                count+=1
                            i+=1
                                
                        else:
                            i+=1
                        if i==len(notPathCells):
                            break
        else:
            # Load maze from CSV file
            with open(loadMaze,'r') as f:
                last=list(f.readlines())[-1]
                c=last.split(',')
                c[0]=int(c[0].lstrip('"('))
                c[1]=int(c[1].rstrip(')"'))
                self.rows=c[0]
                self.cols=c[1]
                self.grid=[]

            with open(loadMaze,'r') as f:
                r=csv.reader(f)
                next(r)
                for i in r:
                    c=i[0].split(',')
                    c[0]=int(c[0].lstrip('('))
                    c[1]=int(c[1].rstrip(')'))
                    self.maze_map[tuple(c)]={'E':int(i[1]),'W':int(i[2]),'N':int(i[3]),'S':int(i[4])}
        self._drawMaze(self.theme)
        agent(self,*self._goal,shape='square',filled=True,color=COLOR.green)
        if saveMaze:
            dt_string = datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
            with open(f'maze--{dt_string}.csv','w',newline='') as f:
                writer=csv.writer(f)
                writer.writerow(['  cell  ','E','W','N','S'])
                for k,v in self.maze_map.items():
                    entry=[k]
                    for i in v.values():
                        entry.append(i)
                    writer.writerow(entry)
                f.seek(0, os.SEEK_END)
                f.seek(f.tell()-2, os.SEEK_SET)
                f.truncate()

    def _drawMaze(self,theme):
        #Creation of Tkinter window and maze lines   
        self._LabWidth=26 # Space from the top for Labels
        self._win=Tk()
        self._win.state('zoomed')
        self._win.title('MAZZLE')
        scr_width=self._win.winfo_screenwidth()
        scr_height=self._win.winfo_screenheight()
        self._win.geometry(f"{scr_width}x{scr_height}+0+0")
        self._canvas = Canvas(width=scr_width, height=scr_height, bg=theme.value[0]) # 0,0 is top left corner
        self._canvas.pack(expand=YES, fill=BOTH)
        # Some calculations for calculating the width of the maze cell
        k=3.25
        if self.rows>=95 and self.cols>=95:
            k=0
        elif self.rows>=80 and self.cols>=80:
            k=1
        elif self.rows>=70 and self.cols>=70:
            k=1.5
        elif self.rows>=50 and self.cols>=50:
            k=2
        elif self.rows>=35 and self.cols>=35:
            k=2.5
        elif self.rows>=22 and self.cols>=22:
            k=3
        self._cell_width=round(min(((scr_height-self.rows-k*self._LabWidth)/(self.rows)),((scr_width-self.cols-k*self._LabWidth)/(self.cols)),90),3)
        
        # Creating Maze lines
        if self._win is not None:
            if self.grid is not None:
                for cell in self.grid:
                    x,y=cell
                    w=self._cell_width
                    x=x*w-w+self._LabWidth
                    y=y*w-w+self._LabWidth
                    if self.maze_map[cell]['E']==False:
                        l=self._canvas.create_line(y + w, x, y + w, x + w,width=2,fill=theme.value[1],tag='line')
                    if self.maze_map[cell]['W']==False:
                        l=self._canvas.create_line(y, x, y, x + w,width=2,fill=theme.value[1],tag='line')
                    if self.maze_map[cell]['N']==False:
                        l=self._canvas.create_line(y, x, y + w, x,width=2,fill=theme.value[1],tag='line')
                    if self.maze_map[cell]['S']==False:
                        l=self._canvas.create_line(y, x + w, y + w, x + w,width=2,fill=theme.value[1],tag='line')

    def _redrawCell(self,x,y,theme):
        #With Full sized square agent, it can overlap with maze lines So the cell is redrawn
        w=self._cell_width
        cell=(x,y)
        x=x*w-w+self._LabWidth
        y=y*w-w+self._LabWidth
        if self.maze_map[cell]['E']==False:
            self._canvas.create_line(y + w, x, y + w, x + w,width=2,fill=theme.value[1])
        if self.maze_map[cell]['W']==False:
            self._canvas.create_line(y, x, y, x + w,width=2,fill=theme.value[1])
        if self.maze_map[cell]['N']==False:
            self._canvas.create_line(y, x, y + w, x,width=2,fill=theme.value[1])
        if self.maze_map[cell]['S']==False:
            self._canvas.create_line(y, x + w, y + w, x + w,width=2,fill=theme.value[1])
    def enableArrowKey(self,a):
        self._win.bind('<Left>',a.moveLeft)
        self._win.bind('<Right>',a.moveRight)
        self._win.bind('<Up>',a.moveUp)
        self._win.bind('<Down>',a.moveDown)
    def run(self):
        btna= Button(self._win, text = 'Exit',width=25,command = self._win.destroy)
        btna.place(relx=0.7,rely=0.6)
        def duster():
            self._win.destroy()
        btnb=Button(self._win, text = 'New Game',width=25,command=lambda: [duster(),start_window()])
        btnb.place(relx=0.7,rely=0.4)
        self._win.mainloop()
def fun_game(x:int,y:int,color_theme,agent_color):
    m=maze(x,y)
    m.CreateMaze(theme=color_theme)
    a=agent(m,footprints=True,color=agent_color)
    m.enableArrowKey(a)
    m.run()
def size_setting(color_theme,agent_color):
    box = Tk()
    box.title("Mazzle")
    box.geometry("500x300")
    box.configure(bg='#856ff8')
    def close():
        box.destroy()
    btn1 = Button(box,text = "Easy Mode",fg="white",bg="black",width=30,
                  command=lambda: [close(),fun_game(5,5,color_theme,agent_color)])
    btn1.place(relx=0.5, rely=0.2, anchor=CENTER)
    btn2 = Button(box,text = "Normal Mode",fg="white",bg="black",width=30,
                  command=lambda: [close(),fun_game(10,10,color_theme,agent_color)])
    btn2.place(relx=0.5, rely=0.4, anchor=CENTER)
    btn3 = Button(box,text = "Hard Mode",fg="white",bg="black",width=30,
                  command=lambda: [close(),fun_game(15,15,color_theme,agent_color)])
    btn3.place(relx=0.5, rely=0.6, anchor=CENTER)
    btn4 = Button(box,text = "Very Hard Mode",fg="white",bg="black",width=30,
                  command=lambda: [close(),fun_game(20,20,color_theme,agent_color)])
    btn4.place(relx=0.5, rely=0.8, anchor=CENTER)
    box.mainloop()

def theme_setting():
    box = Tk()
    box.title("Mazzle")
    box.geometry("500x300")
    box.configure(bg='#856ff8')
    def close():
        box.destroy()
    heading = Label(box,text = "select Theme from below",width=60)
    heading.place(relx=0.5, rely=0.2, anchor=CENTER)
    btn1 = Button(box,text = "Light Theme",fg="white",bg="black",width=30,
                  command=lambda: [close(),agent_color_setting(COLOR.light)])
    btn1.place(relx=0.5, rely=0.4, anchor=CENTER)
    btn2 = Button(box,text = "Dark Theme",fg="white",bg="black",width=30,
                  command=lambda: [close(),agent_color_setting(COLOR.dark)])
    btn2.place(relx=0.5, rely=0.6, anchor=CENTER)
    box.mainloop()

def agent_color_setting(color_theme):
    box = Tk()
    box.title("Mazzle")
    box.geometry("500x500")
    box.configure(bg='#856ff8')
    def close():
        box.destroy()
    heading = Label(box,text = "Select Color of the Block",width=60)
    heading.place(relx=0.5, rely=0.1, anchor=CENTER)
    btn1 = Button(box,text = "Black",fg="white",bg="black",width=30,
                  command=lambda: [close(),size_setting(color_theme,'black')])
    btn1.place(relx=0.5, rely=0.3, anchor=CENTER)
    btn2 = Button(box,text = "Red",fg="white",bg="black",width=30,
                  command=lambda: [close(),size_setting(color_theme,'red')])
    btn2.place(relx=0.5, rely=0.4, anchor=CENTER)
    btn3 = Button(box,text = "Cyan",fg="white",bg="black",width=30,
                  command=lambda: [close(),size_setting(color_theme,'cyan')])
    btn3.place(relx=0.5, rely=0.5, anchor=CENTER)
    btn4 = Button(box,text = "Green",fg="white",bg="black",width=30,
                  command=lambda: [close(),size_setting(color_theme,'green')])
    btn4.place(relx=0.5, rely=0.6, anchor=CENTER)
    btn5 = Button(box,text = "Blue",fg="white",bg="black",width=30,
                  command=lambda: [close(),size_setting(color_theme,'blue')])
    btn5.place(relx=0.5, rely=0.7, anchor=CENTER)
    btn6 = Button(box,text = "Yellow",fg="white",bg="black",width=30,
                  command=lambda: [close(),size_setting(color_theme,'yellow')])
    btn6.place(relx=0.5, rely=0.8, anchor=CENTER)
    box.mainloop()
def start_window():
    box = Tk()
    box.title("Mazzle")
    box.geometry("500x300")
    box.configure(bg='#856ff8')
    def close():
        box.destroy()
    btn1 = Button(box,text = "Start default Game",fg="white",bg="black",width=30,
                  command=lambda: [close(),fun_game(10,10,COLOR.dark,'blue')])
    btn1.place(relx=0.5, rely=0.3, anchor=CENTER)
    btn2 = Button(box,text = "Exit game",fg="white",bg="black",width=30,command=close)
    btn2.place(relx=0.5, rely=0.7, anchor=CENTER)
    btn3 = Button(box,text = "Customized Game setting",fg="white",bg="black",width=30,command=lambda: [close(),theme_setting()])
    btn3.place(relx=0.5, rely=0.5, anchor=CENTER)
    box.mainloop()
start_window()