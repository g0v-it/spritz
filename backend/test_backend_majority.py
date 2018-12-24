import shutil
import os,sys
import subprocess as sp

PROVADIR = 'provamajority'
CANDIDATESNUM = 5
VOTERSNUM = 1000
OPTIONSNUM = 6
GUARANTORSNUM = 2
HEXSTRINGLENGTHG = 55
HEXSTRINGLENGTHC = 48
KEYFILE = "KeyFile.txt"

def run_CreateMajority():
    cp2 = sp.run(["./CreateMajority", PROVADIR, str(CANDIDATESNUM), str(VOTERSNUM),  KEYFILE])
    
def run_Vote(i):
    word = "{:<48}".format("C"+str(i))
    hexword = sm.string2hex(word.ljust(HEXSTRINGLENGTHC))
    #cp1 = sp.run(["./Hash", hexword], stdout=sp.PIPE)
    #print("Hash:", word, hexword, cp1.stdout[15:-2])
    #hash value is: xxx
    cp2 = sp.run(["./Vote", PROVADIR, str(i), hexword])
    
def run_Close(i):
    word = "G" + str(i)
    hexword = sm.string2hex(word.ljust(HEXSTRINGLENGTHG))
    #cp1 = sp.run(["./Hash", hexword], stdout=sp.PIPE)
    #print("Words:", word, hexword, cp1.stdout[15:-2])
    #hash value is: xxx
    cp2 = sp.run(["./Close", PROVADIR, str(i), hexword])


if __name__ == '__main__':
    os.system("clear")
    # cancellare la directory di prova
    shutil.rmtree(PROVADIR, ignore_errors=True)

    # Lanciare la creazione della votazione
    run_CreateMajority()

