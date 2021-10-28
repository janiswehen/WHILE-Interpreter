from os import _exit
from interpreter import Interpreter

fileName = "x'.WHILE"
fileObj = open(fileName, "r")
prog = fileObj.read()
fileObj.close()
args = [11,23]

inter = Interpreter()

if __name__ == "__main__":
    inter.setProg(prog)
    inter.setInput([2])
    res = inter.run()
    print(res)
    #test = True
    #fail1,fail2 = 0,0
    #for i in range(1,21):
    #    for j in range(1,21):
    #        inter.setInput([i,j])
    #        res = inter.run()
    #        print(str(i) + "%" + str(j) + "= " + str(i%j) + " | " + str(res))
    #        if not i%j == res:
    #            test = False
    #            fail1,fail2 = i,j
    #            break

    #if test:
    #    print("Sucsess!")
    #else:
    #    print("Failed at" + str(fail1) + ", " + str(fail2) + "!")