import random

class Game:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.evaluate = 0
        self.change = 0
        self.win = 0
        self.check = 1
        self.board = [ \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
            ]

        self.score = [0]*15*15
    
    def rand_choice(self, step):
        if step==0:
            for i in range(15):
                for j in range(15):
                    blank = 8
                    while self.board[i][j]!=0 and blank > 0:
                        for c in range(3):
                            for d in range(3):
                                if (i-1+c<0 or i-1+c>14) or (j-1+d<0 or j-1+d>14):
                                    continue
                                                            
                                if self.board[i-1+c][j-1+d]==0:
                                    choice = random.randint(0, 1)
                                                                    
                                    if choice%2==0:
                                        self.x = j+d
                                        self.y = i+c
                                        print("check")
                                        print("x = {}, y = {}".format(self.x, self.y))
                                        return 0
                                else: 
                                    blank-=1
                                                                    

    def check_line(self, num):
        count = num - 1
        full_1 = 0
        full_2 = 0
            
        if num==4:
            full_1 = 1000000
            full_2 = 500000
        elif num==3:
            full_1 = 40000
            full_2 = 20000
        else:
            full_1 = 4000
            full_2 = 3000
            
        #检查行
        for i in range(15):
            for j in range(16-num):
                q = i * 15 + j
                self.check = self.check_pre(q, num, 1, i, j)
                q = i * 15 + j + num
                            
                #满检测 
                if self.check!=0:
                    a = 0
                    b = 0
                    if 0<=q<=224:
                        a = self.score[q]
                    if 0<=q-num-1<=224:
                        b = self.score[q-num-1]
                    block = 0
                    if num!=5:
                        if  j!=15-num and self.board[i][j+num]==0:
                            if self.change==self.evaluate:
                                self.score[q]+=full_1
                            else:
                                self.score[q]+=full_2
                                            
                            if j==15-num-1 and num!=4:
                                self.score[q] = a

                            block+=1
                                            
                        if j!=0 and self.board[i][j-1]==0:
                            if self.change==self.evaluate:
                                self.score[q-num-1]+=full_1
                            else:
                                self.score[q-num-1]+=full_2
                                                            
                            if j==1 and num!=4:
                                self.score[q-num-1] = b

                            block+=1
                                                            
                        if block==1 and num!=4 and self.change!=self.evaluate and \
                           0<=q<=224 and 0<=q-num-1<=224:
                            self.score[q] = a
                            self.score[q-num-1] = b
                    else:
                        return self.check

        #检查列
        for i in range(16-num):
            for j in range(15):
                q = i * 15 + j
                self.check = self.check_pre(q, num, 15, i, j)
                q = i * 15 + j + num * 15
                            
                #满检测 
                if self.check!=0:
                    a = 0
                    b = 0
                    block = 0
                    if 0<=q<=224:
                        a = self.score[q]
                    if 0<=q-num*15-15<=224:
                        b = self.score[q-num*15-15]
                    if num!=5:
                        if  i!=15-num and self.board[i+num][j]==0:
                            if self.change==self.evaluate:
                                self.score[q]+=full_1
                            else:
                                self.score[q]+=full_2
                                            
                            if i==15-num-1 and num!=4:
                                self.score[q] = a

                            block+=1
                                            
                        if i!=0 and self.board[i-1][j]==0:
                            if self.change==self.evaluate:
                                self.score[q-num*15-15]+=full_1
                            else:
                                self.score[q-num*15-15]+=full_2
                                                            
                            if i==1 and num!=4:
                                self.score[q-num*15-15] = b

                            block+=1
                                                            
                        if block==1 and num!=4 and self.change!=self.evaluate and \
                           0<=q<=224 and 0<=q-num*15-15<=224:
                            self.score[q] = a
                            self.score[q-num*15-15] = b
                    else:
                        return self.check
            
        #检查副对角
        for i in range(num-1, 15):
            for j in range(16-num):
                q = i * 15 + j
                self.check = self.check_pre(q, num, -14, i, j)
                q = i * 15 + j - num * 14
                            
                #满检测 
                if self.check!=0:
                    a = 0
                    b = 0
                    block = 0
                    if 0<=q<=224:
                        a = self.score[q]
                    if 0<=q+num*14+14<=224:
                        b = self.score[q+num*14+14]
                    if num!=5:
                        if i!=num-1 and j!=15-num and self.board[i - num][j + num]==0:
                            if self.change==self.evaluate:
                                self.score[q]+=full_1
                            else:
                                self.score[q]+=full_2
                                            
                            if (j==15-num-1 or i==num) and num!=4:
                                self.score[q] = a

                            block+=1
                                            
                        if j!=0 and i!=14 and self.board[i + 1][j - 1]==0:
                            if self.change==self.evaluate:
                                self.score[q+num*14+14]+=full_1
                            else:
                                self.score[q+num*14+14]+=full_2
                                                            
                            if (j==1 or i==13) and num!=4:
                                self.score[q+num*14+14] = b

                            block+=1
                                                            
                        if block==1 and num!=4 and self.change!=self.evaluate and \
                           0<=q<=224 and 0<=q+num*14+14<=224:
                            self.score[q] = a
                            self.score[q-num*15-15] = b
                    else: 
                        return self.check

        #检查主对角
        for i in range(16-num):
            for j in range(16-num):
                q = i * 15 + j
                self.check = self.check_pre(q, num, 16, i, j)
                q = i * 15 + j + num * 16
                            
                #满检测 
                if self.check!=0:
                    a = 0
                    b = 0
                    block = 0
                    if 0<=q<=224:
                        a = self.score[q]
                    if 0<=q-num*16-16<=224:
                        b = self.score[q-num*16-16]
                    if num!=5:
                        if i!=15-num and j!=15-num and self.board[i + num][j + num]==0:
                            if self.change==self.evaluate:
                                self.score[q]+=full_1
                            else:
                                self.score[q]+=full_2
                                            
                            if (j==15-num-1 or i==num) and num!=4:
                                self.score[q] = a

                            block+=1
                                            
                        if j!=0 and i!=0 and self.board[i - 1][j - 1]==0:
                            if self.change==self.evaluate:
                                self.score[q-num*16-16]+=full_1
                            else:
                                self.score[q-num*16-16]+=full_2
                                                            
                            if (j==1 or i==13) and num!=4:
                                self.score[q-num*16-16] = b

                            block+=1
                                                            
                        if block==1 and num!=4 and self.change!=self.evaluate and \
                           0<=q<=224 and 0<=q-num*16-16<=224:
                            self.score[q] = a
                            self.score[q-num*16-16] = b
                    else:
                        return self.check
                
        return 0

    def check_emp_1(self, direct, i, j, num):
        emp_1 = 0
        emp_2 = 0
            
        if num==5:
            emp_1 = 1000000
            emp_2 = 500000
        elif num==4:
            emp_1 = 2000
            emp_2 = 1000
        elif num==3:
            emp_1 = 4
            emp_2 = 3
        else:
            emp_1 = 2
            emp_2 = 1
            
        #有空检测 
        q = i*15 + j
        side = 0
        while self.board[q//15][q%15]!=0:
            side+=1
            q += direct
            
        if side!=0 and side!=num-1:
            if self.change==self.evaluate:
                self.score[q] += emp_1
            else:
                self.score[q] += emp_2
                                    
        q1 = i * 15 + j - direct
        q2 = i * 15 + j + num * direct
        
        if num!=5 and 225>q1>=0 and 0<=q2<225:
            if self.board[q1//15][q1%15]!=0 and self.board[q2//15][q2%15]!=0:
                self.score[q] -= 2500
            
        return 0
        
    def check_emp_2(self, direct, i, j):      
        emp_1 = 4000
        emp_2 = 2000
            
        #有空检测 
        q = i*15 + j
        q1 = q+3*direct
        q2 = q
        if self.board[q1//15][q1%15]==0 and self.board[q2//15][q2%15]!=0:
            q = q1
        elif self.board[q1//15][q1%15]!=0 and self.board[q2//15][q2%15]==0:
            q = q2
        else:
            return 0
            
        if self.change==self.evaluate:
            self.score[q] += emp_1
        else:
            self.score[q] += emp_2

        q1 = q+3*direct
        q2 = q-direct

        if q1<15 and q2>=0:
            if self.board[q1//15][q1%15]!=0 and self.board[q2//15][q2%15]!=0:
                self.score[q] -= 2500
            
        return 0
        
    def check_pre(self, q, num, direct, i, j):
        X = 0
        O = 0
        blank = 0
        count = num - 1
        while count >= 0:
            if self.board[q//15][q%15]==1:
                X+=1
            elif self.board[q//15][q%15]==2:
                O+=1
            else:
                blank+=1
                
            q += direct
            count-=1
                            
        if X>O:
            self.evaluate = 0
        elif O>X:
            self.evaluate = 1
                            
        if X==num:
            return -1
        elif O==num:
            return -2
        elif (X==num-1 or O==num-1) and num!=2 and blank==1:
            self.check_emp_1(direct, i, j, num)
        elif (X==num-2 or O==num-2) and num==4 and blank==2:
            self.check_emp_2(direct, i, j)
            
        return 0
        
    def caculate(self):    
        step = 0
        index = self.check_all()
                    
        #检查行列
        if index>=0:
            self.x = index%15+1
            self.y = index//15+1
        elif index!=-100:
            return index

        if self.board[self.y-1][self.x-1]==0:
            step = 1
            print("CHECK")
            print("x = {}, y = {}".format(self.x, self.y))
            
        self.rand_choice(step)
            
        if self.change==0:
            self.board[self.y-1][self.x-1] = 1
            self.change = 1
        else:
            self.board[self.y-1][self.x-1] = 2
            self.change = 0
        
    def check_blank(self):
        for i in range(15):
            for j in range(15):
                if self.board[i][j]==0:
                    return 1
            
        return 0

    def check_score(self):
        index = -100
        tmax = 1
            
        for i in range(225):
            if self.score[i]>=tmax:
                index = i
                tmax = self.score[i]

        return index

    def check_all(self):
        index = 0
        
        for i in range(225):
            self.score[i] = 0

        self.win = self.check_line(5)
        self.check_line(4)
        self.check_line(3)
        self.check_line(2)

        if self.win==-1 or self.win==-2:
            return self.win
        else:
            index = self.check_score()
            
        return index

    def game(self):
        count = 0
        cancel = 0
            
        if self.x==0 and self.y==0:
            cancel = 1
            self.board[7][7] = 1
        elif self.change==0:
            self.board[self.y-1][self.x-1] = 1
            self.change = 1
        else:
            self.board[self.y-1][self.x-1] = 2
            self.change = 0
            
        if self.check>0:
            self.caculate()
            self.check = self.check_blank()
                    
            if cancel:
                cancel = 0
                self.board[7][7] = 0

    def check_five(self):
        #检查行
        for i in range(15):
            for j in range(11):
                q = i * 15 + j

                O = 0
                count = 4
                while count >= 0:
                    if self.board[q//15][q%15]==2:
                        O+=1
                        
                    q += 1
                    count-=1

                if O==5:
                    self.win = -2

        #检查列
        for i in range(11):
            for j in range(15):
                q = i * 15 + j

                O = 0
                count = 4
                while count >= 0:
                    if self.board[q//15][q%15]==2:
                        O+=1
                        
                    q += 15
                    count-=1

                if O==5:
                    self.win = -2
            
        #检查副对角
        for i in range(4, 15):
            for j in range(11):
                q = i * 15 + j

                O = 0
                count = 4
                while count >= 0:
                    if self.board[q//15][q%15]==2:
                        O+=1
                        
                    q -= 14
                    count-=1

                if O==5:
                    self.win = -2

        #检查主对角
        for i in range(11):
            for j in range(11):
                q = i * 15 + j

                O = 0
                count = 4
                while count >= 0:
                    if self.board[q//15][q%15]==2:
                        O+=1
                        
                    q += 16
                    count-=1

                if O==5:
                    self.win = -2
                
