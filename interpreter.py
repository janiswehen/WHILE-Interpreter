class Interpreter:
    def __init__(self):
        self.program = ""
        self.args = []
        self.pc = 0
        self.vCount = 0
        self.variabels = []
        self.rep = 0
        self.wn = True
        self.errNo = 0
    
    def run(self):
        #print("Running Program:\n" + self.program + "\n")
        self.pc = 0
        self.cleanProg()
        self.initVars()
        self.wn = not len(self.program) == 0

        self.runComand()

        #print(self.variabels)
        return self.variabels[0]
    
    def runComand(self):
        if self.wn:
            self.checkRegs()
            self.wn = False
            if not self.haveNextComand():
                self.SError("Code ended badly!")
                return

            #run command
            if self.getCharAtPC() == "x":
                self.commandSet()
            elif self.getCharAtPC() == "W":
                self.commandWHILE()
            else:
                self.SError("Can't find command:'" + self.program[self.pc:self.pc+10] + "'")
                return
            self.checkRegs()
            self.runComand()


    #Commands            
    def commandSet(self):
        if not self.testString("x_"):
            self.SError("Expected 'x_'")
            return

        var1 = self.getNumAndInc()

        if var1 == -1:
            self.SError("Expected Number after Variabel!")
            return

        if not self.testString(":="):
            self.SError("Expected ':='")
            return

        if self.getCharAtPC().isdigit() or self.getCharAtPC() == "-":                       #set const
            sign = 1
            if self.getCharAtPC() == "-":
                sign = -1
                self.pc += 1
            num = self.getNumAndInc()

            if num == -1:
                self.SError("Expected Number")
                return
            
            self.variabels[var1] = sign * num
        elif self.getCharAtPC() == "x":                                                     #move
            if not self.testString("x_"):
                self.SError("Expected 'x_'")
                return
            var2 = self.getNumAndInc()
            if var1 == -1:
                self.SError("Expected Number after Variabel!")
                return
            if self.getCharAtPC() == "+":                                                       #and add
                self.pc += 1

                if self.getCharAtPC() == "x":
                    if not self.testString("x_"):
                        self.SError("Expected 'x_'")
                        return
                    var3 = self.getNumAndInc()
                    if var3 == -1:
                        self.SError("Expected Number after Variabel!")
                        return
                    self.variabels[var1] = self.variabels[var2] + self.variabels[var3]
                else:
                    num = self.getNumAndInc()
                    if num == -1:
                        self.SError("Can't read number!")
                        return
                    self.variabels[var1] = self.variabels[var2] + num
            elif self.getCharAtPC() == "-":                                                       #and add
                self.pc += 1
                if self.getCharAtPC() == "x":
                    if not self.testString("x_"):
                        self.SError("Expected 'x_'")
                        return
                    var3 = self.getNumAndInc()
                    if var3 == -1:
                        self.SError("Expected Number after Variabel!")
                        return
                    self.variabels[var1] = self.variabels[var2] - self.variabels[var3]
                else:
                    num = self.getNumAndInc()
                    if num == -1:
                        self.SError("Can't read number!")
                        return
                    self.variabels[var1] = self.variabels[var2] - num
            else:                                                                               #simply move
                self.variabels[var1] = self.variabels[var2]
        else:
            self.SError("Can't read Set")
            return
        
        if self.getCharAtPC() == ";":
            self.wn = True
            self.pc += 1

    def commandWHILE(self):
        if not self.testString("WHILE"):
            self.SError("Expected 'WHILE'")
            return

        if not self.testString("x_"):
            self.SError("Expected 'x_'")
            return

        vartest = self.getNumAndInc()

        if vartest == -1:
            self.SError("Expected Number after Variabel!")
            return

        if not self.testString("!="):
            self.SError("Expected '!='")
            return

        sign = 1
        if self.getCharAtPC() == "-":
            sign = -1
            self.pc += 1

        numtest = self.getNumAndInc()

        if numtest == -1:
            self.SError("Expected Number after Variabel!")
            return
        
        numtest *= sign

        if not self.testString("DO"):
            self.SError("Expected 'DO'")
            return
        
        pc = self.pc
        wCount = 0
        wmax = 100
        if self.variabels[vartest] == numtest:
            v = []
            for i in self.variabels:
                v.append(i)
            self.wn = True
            self.runComand()
            for i in range(len(v)):
                self.variabels[i] = v[i]
        while self.variabels[vartest] != numtest:
            self.pc = pc
            if wCount > wmax:
                self.SError("WHILE-loop exided more then " + str(wmax) + " repetitions!")
                return
            self.wn = True
            self.runComand()
            wCount += 1
        
        if not self.testString("END"):
            self.SError("Expected 'END'")
            return

        if self.getCharAtPC() == ";":
            self.wn = True
            self.pc += 1
            
    
    
    #info functions
    def haveNextComand(self):
        if self.pc >= len(self.program):
            return False
        return True

    def getNumAtP(self, place):
        snum = ""
        for i in range(place, len(self.program)):
            if not self.program[i].isdigit():
                break
            snum += self.program[i]
        if snum == "":
            return -1
        return int(snum)
    
    def getNum(self):
        return self.getNumAtP(self.pc)
    
    def getNumAndInc(self):
        snum = ""
        while True:
            if not self.getCharAtPC().isdigit():
                break
            snum += self.getCharAtPCAndInc()
        if snum == "":
            return -1
        return int(snum)

    def SError(self, str):
        print("Sytax Error: " + str)


    #getChar functions
    def getCharAtPC(self):
        if self.pc < 0 or self.pc >= len(self.program):
            return ""
        return self.program[self.pc]

    def getCharAtPCAndInc(self):
        c = self.getCharAtPC()
        self.pc += 1
        return c
    
    def getNextChars(self, count):
        str = ""
        for i in range(count):
            str += self.getCharAtPCAndInc()
        return str
           
    def testString(self, str):
        return self.getNextChars(len(str)) == str


#prep functions
    def cleanProg(self):
        self.program = self.program.replace(" ", "")
        self.program = self.program.replace("\n", "")
        self.program = self.program.replace("\t", "")
    
    def setVCount(self):
        m = 0
        for i in range(len(self.program)):
            if self.program[i] == "_":
                num = self.getNumAtP(i+1)
                if num > m:
                    m = num
        self.vCount = max(len(self.args), m) + 1
    
    def initVars(self):  
        self.setVCount()
        self.variabels = [0] * self.vCount
        for i in range(len(self.args)):
            self.variabels[i+1] = self.args[i]

    def checkRegs(self):
        for i in range(len(self.variabels)):
            if self.variabels[i] < 0:
                self.variabels[i] = 0


#set funktions
    def setInput(self, args):
        self.args = args

    def setProg(self, progCode):
        self.program = progCode