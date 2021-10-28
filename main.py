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

if __name__ == "__main__":
    inter.setProg(prog)
    inter.setMods(mods)
    inter.setInput([1,2,3,4,5])
    res = inter.run()
    print("Res:" + str(inter.variabels))
