class Interpreter:
    def __init__(self):
        self.program = ""
        self.args = []
        self.pc = 0
        self.vCount = 0
        self.variabels = []
        self.rep = 0
        self.wn = True
        self.mods = []
    
    def run(self):
        #print("Running Program:\n" + self.program + "\n")
        self.pc = 0
        self.cleanProg()
        self.initVars()
        self.wn = not len(self.program) == 0
        #print(self.program)

        self.runComand()

        #print(self.variabels)
        return self.variabels[0]
    
    def runComand(self):
        if self.wn:
            #print(self.variabels)
            start = self.pc
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
            #print(self.program[start:self.pc])
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
        
        if (self.program[self.pc] + self.program[self.pc + 1]) == "x_" or self.getCharAtPC().isdigit():
            e, num1 = self.getVar()
            if e == 1:
                return

            s = self.getCharAtPC()
            if self.getCharAtPC() == "-":
                self.pc += 1
                e, num2 = self.getVar()
                if e == 1:
                    return
                self.variabels[var1] = num1 - num2
            elif self.getCharAtPC() == "+":
                self.pc += 1
                e, num2 = self.getVar()
                if e == 1:
                    return
                self.variabels[var1]= num1 + num2
            else:
                self.variabels[var1] = num1
        else:
            err = True
            for s in self.mods:
                if self.testStringGoBack(s):
                    err = False
                    self.testString(s)
                    if not self.testString("("):
                        self.SError("Expected '('")
                        return
                    input = []
                    while self.getCharAtPC() != ")":
                        e, num = self.getVar()
                        if e == 1:
                            self.SError("Expected Var")
                            return
                        input.append(num)
                        if not self.getCharAtPC() == ",":
                            break
                        self.pc += 1
                    if not self.testString(")"):
                        self.SError("Expected ')'")
                        return
                    
                    fileName = s + ".WHILE"
                    fileObj = open(fileName, "r")
                    prog = fileObj.read()
                    fileObj.close()

                    inter = Interpreter()
                    inter.setProg(prog)
                    inter.setInput(input)
                    newmods = []
                    for mod in self.mods:
                        if not mod == s:
                            newmods.append(mod)
                    inter.setMods(newmods)
                    res = inter.run()
                    self.variabels[var1] = res
                    break
            if err:
                self.SError("No module found!")
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

        e, numtest = self.getVar()

        if e == 1:
            self.SError("Expected Number after Variabel!")
            return

        if not self.testString("DO"):
            self.SError("Expected 'DO'")
            return
        
        pc = self.pc
        wCount = 0
        wmax = 100000
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

    def getVar(self):
        if self.getCharAtPC().isdigit():
            num = self.getNumAndInc()
            return 0, num
        elif self.getCharAtPC() == "-":
            self.pc += 1
            num = self.getCharAtPCAndInc()
            if num == -1:
                self.SError("Missing Number")
                return 1, 0
            return 0, -num
        elif self.getCharAtPC() == "x":
            if not self.testString("x_"):
                self.SError("Expected 'x_'")
                return 1, 0
            var = self.getNumAndInc()
            if var == -1:
                self.SError("Expected Num after Var")
                return 1,0
            return 0, self.variabels[var]
        else:
            self.SError("Cound not find Number")
            return 1,0

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

    def testStringGoBack(self, str):
        b = self.getNextChars(len(str)) == str
        self.pc -= len(str)
        return b


    #prep functions
    def cleanProg(self):
        self.program = self.program.replace(" ", "")
        self.program = self.program.replace("\n", "")
        self.program = self.program.replace("\t", "")
        self.program += " "
    
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
    
    def setMods(self, mods):
        self.mods = mods