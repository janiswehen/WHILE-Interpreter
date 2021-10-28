from interpreter import Interpreter
import os

arr = os.listdir()
mods = []
for str1 in arr:
    if str1[-6:] == ".WHILE":
        mods.append(str1[:-6])

fileName = "STACK.WHILE"
fileObj = open(fileName, "r")
prog = fileObj.read()
fileObj.close()

mods.remove(fileName[:-6])

inter = Interpreter()

which = 3

if __name__ == "__main__":
    inter.setProg(prog)
    inter.setMods(mods)
    if which == 0:
        test = True
        fail1,fail2 = 0,0
        for i in range(1,21):
            for j in range(1,21):
                inter.setInput([i,j])
                res = inter.run()
                #print(str(i) + "//" + str(j) + "= " + str(i//j) + " | " + str(res))
                if not i//j == res:
                    test = False
                    fail1,fail2 = i,j
                    break
        if test:
            print("Div:Sucsess!")
        else:
            print("Failed at" + str(fail1) + ", " + str(fail2) + "!")
    elif which == 1:
        test = True
        fail1,fail2 = 0,0
        for i in range(1,21):
            for j in range(1,21):
                inter.setInput([i,j])
                res = inter.run()
                #print(str(i) + "%" + str(j) + "= " + str(i%j) + " | Res:" + str(res))
                if not i%j == res:
                    test = False
                    fail1,fail2 = i,j
                    break
        if test:
            print("Mod: Sucsess!")
        else:
            print("Failed at: " + str(fail1) + ", " + str(fail2))
    elif which == 2:
        test = True
        fail1,fail2 = 0,0
        for i in range(0,10):
            for j in range(0,10):
                inter.setInput([])
                res = inter.run()
                print("i:" + str(i) + " | j:"  + str(j)+ " | Exp:" + str(((i+j)*(i+j+1))//2 + j) + " | Res:" + str(res))
                if not ((i+j)*(i+j+1))//2 + j == res:
                    test = False
                    fail1,fail2 = i,j
                    break
        if test:
            print("Pair: Sucsess!")
        else:
            print("Failed at: " + str(fail1) + ", " + str(fail2))
    else:
        inter.setInput([1,2,3,4,5])
        res = inter.run()
        print("Res:" + str(inter.variabels))