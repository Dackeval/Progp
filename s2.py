# Labb S2: Sköldpaddegrafik
import sys
from sys import stdin
from typing import Text
import re
import math
sys.setrecursionlimit(100000000)

class Syntaxfel(Exception):
    pass

# Vi börjar med att skapa objektet Leona
class Leona:
    def __init__(self, color="#0000FF", x=0, y=0, riktning=0, upphojt=True):
        self.color = color
        self.x = x
        self.y = y
        self.riktning = riktning
        self.upphojt = upphojt


class Token:  # Token, ett simpelt objekt med typ och värde
    def __init__(self, typ, row, value=None):
        self.typ = typ
        self.row = row
        self.value = value


class Node:
    def __init__(self,token=None, value=None, next=None, rep=None):
        self.token = token
        self.value = value
        self.next = next
        self.rep = rep


def readinput():  # läser input
    f = open("leona-12.txt", "r")
    text = f.readlines()
    return text

def removeDot(elem):
    newelem = elem.replace(".", " . ")
    return newelem

def removeQuo(elem):
    newelem = elem.replace('"', '" ')
    return newelem

def Lexikalanalysator():  # För att kunna dela upp indatafilen i tokens
    row = 0  # - counter
    tokList = []  # - lista för tokens
    tokList.append(Token("Initierad lista", row))
    textlist = readinput() #bort för kattis
    #textlist = sys.stdin.readlines()   # För Kattis
    tokenlist = 0
    for item in textlist:
        row = row + 1
        item = item.rstrip()
        item = item.rstrip('\n')
        newitem = item
        if newitem != "":
            newitem1 = newitem.split("%", 1)
            rmwproc = newitem1[0]
            if "." in rmwproc:
                rmwproc = removeDot(rmwproc)
            if '"' in rmwproc:
                rmwproc = removeQuo(rmwproc)
            rmwproclist = rmwproc.split()
            tokenlist = instr(rmwproclist, row, tokList)

    return tokenlist



def instr(instrk, row, tokList):
    for i in range(len(instrk)):
        if instrk[i].lower() == "forw":
            tokList.append(Token("FORW", row))
        elif instrk[i].lower() == "back":
            tokList.append(Token("BACK", row))
        elif instrk[i].lower() == "left":
            tokList.append(Token("LEFT", row))
        elif instrk[i].lower() == "right":
            tokList.append(Token("RIGHT", row))
        elif instrk[i].lower() == "color":
            tokList.append(Token("COLOR", row))
        elif instrk[i].lower() == "rep":
            tokList.append(Token("REP", row))
        elif instrk[i].lower() == "down":
            tokList.append(Token("DOWN", row))
        elif instrk[i].lower() == "up":
            tokList.append(Token("UP", row))
        elif instrk[i] == ".":
            tokList.append(perQuo(instrk[i], row))
        elif instrk[i] == '"':
            tokList.append(perQuo(instrk[i], row))
        elif instrk[i].isdigit():
            tokList.append(decimal(instrk[i], row))
        elif hex(instrk[i]):
            tokList.append(Token("HEX", row, instrk[i]))
        else:
            tokList.append(Token("ERROR", row))

    return tokList


def perQuo(elem, row):
    if elem == '"':
        return Token('QUOTE', row)
    else:
        return Token("PERIOD", row)


def decimal(elem, row):
    return Token("DECIMAL", row, int(elem))


def hex(elem):
    reg = re.search("^#[0-9A-Fa-f]{6}$",elem)
    if reg != None:
        return True
    else:
        return False

tokenlista = Lexikalanalysator() # Full lista med allt inmatat separerat i tokens.

tokenlista2 = tokenlista

#------ Parser


movementTokenlista = ["FORW", "BACK", "LEFT", "RIGHT"]
penTokenlista = ["UP", "DOWN"]


def peek(tokenlist, i):
    return tokenlist[i+1].typ

def peekNum(tokenlist, i):
    return tokenlist[i+1].value

def leonafunc(tokenlist): 
    if len(tokenlist) == 0: # Om längden = 0, skapa en tom nod 
        N = Node()
    else:
        N = instruktion(tokenlist) # om ej lika med noll gå till instruktion 
        if len(tokenlist) != 1:
            N.next = leonaInner(tokenlist)
    return N


def leonaInner(tokenlist): #tar listan gör en nod av nästa instruktion, om det finns grejer kvar och inte är en quote då gör man om och noden pekar på nästa 
    N = instruktion(tokenlist)
    if len(tokenlist) > 1 and not N == None:
        N.next = leonaInner(tokenlist)

    return N



def checkrecur(N, leona):
    if N == None:
        pass
    elif N.token != None:
        if N.token == "UP":
            leona.upphojt = True
        elif N.token == "DOWN":
            leona.upphojt = False
        elif N.token == "LEFT":
            leona.riktning = leona.riktning + N.value
        elif N.token == "RIGHT":
            leona.riktning = leona.riktning - N.value
        elif N.token == "FORW":
            v = leona.riktning
            xprev = (float(leona.x))
            yprev = (float(leona.y))
            temp = float(leona.x) + float(N.value) * math.cos(math.pi * float(v) / float(180))
            format_temp = (temp)
            if format_temp == "-0.0000":
                format_temp = "0.0000"
            leona.x = format_temp
            temp = float(leona.y) + float(N.value) * math.sin(math.pi * float(v) / float(180))
            format_temp = (temp)
            if format_temp == "-0.0000":
                format_temp = "0.0000"
            leona.y = format_temp
            if (leona.upphojt == False):
                print(str(leona.color).upper() + " " + str(xprev) + " " + str(yprev) + " " + str(leona.x) + " " + str(leona.y))
        elif N.token == "BACK":
            v = leona.riktning
            xprev = (float(leona.x))
            yprev = (float(leona.y))
            temp = float(leona.x) - float(N.value) * math.cos(math.pi * float(v) / float(180))
            format_temp = (temp)
            if format_temp == "-0.0000":
                format_temp = "0.0000"
            leona.x = format_temp
            temp = float(leona.y) - float(N.value) * math.sin(math.pi * float(v) / float(180))
            format_temp = (temp)
            if format_temp == "-0.0000":
                format_temp = "0.0000"
            leona.y = format_temp
            if (leona.upphojt == False):
                print(str(leona.color).upper() + " " + str(xprev) + " " + str(yprev) + " " + str(leona.x) + " " + str(leona.y))
        elif N.token == "REP":
            x = N.value
            for i in range(x):
                checkrecur(N.rep, leona) # Utskrift för REP, rekursivt och i for loop. Går djupar in i trädet genom det rekursiva anropet, men hamnar tillbaka där den börja när den kommit till botten och repeterar x antal gånger. Där d är DEC från REP.
        elif N.token == "COLOR":
            leona.color = N.value

        checkrecur(N.next, leona)


# det som måste göras är att skilja på ifall det finns en quote eller inte efter REP-satsen 


def instruktion(tokenlist):
    N = Node() # Skapar objekt av typen nod, som sedan i slutet av instruktion returneras

    if peek(tokenlist, 0) == "ERROR": # om nästa token är error då har vi error 
        raise Syntaxfel("Syntaxfel på rad " + str(tokenlist[1].row))
    elif peek(tokenlist, 0) == "QUOTE": #  handlar det om att det kan komma släpande quote.
        return 
    elif peek(tokenlist, 0) in movementTokenlista: # Checkar om elemnt i tokenlista är Forw etc
        try:
            if int(peekNum(tokenlist, 1)) > 0:
                if peek(tokenlist, 2) == "PERIOD": 
                    N.value = peekNum(tokenlist, 1)
                    N = movementToken(tokenlist, N)
                else:
                    raise Syntaxfel("Syntaxfel på rad " + str(tokenlist[3].row)) #error om nästa inte har en period 
            else:
                raise Syntaxfel("Syntaxfel på rad " + str(tokenlist[1].row)) #om numret är inte större än noll, FORW 0. ska ej godkännas
        except (ValueError, TypeError):
            raise Syntaxfel("Syntaxfel på rad " + str(tokenlist[2].row))

    elif peek(tokenlist, 0) in penTokenlista:
        try:
            if peek(tokenlist, 1) == "PERIOD":
                N = penToken(tokenlist, N)
            else:
                raise Syntaxfel("Syntaxfel på rad " + str(tokenlist[2].row))
        except IndexError:
            raise Syntaxfel("Syntaxfel på rad " + str(tokenlist[1].row))
    elif peek(tokenlist, 0) == "COLOR":
        try:
            if hex(tokenlist[2].value):
                if peek(tokenlist, 2) == "PERIOD":
                    N.token = "COLOR"
                    N.value = tokenlist[2].value
                    tokenlist.pop(1)
                    tokenlist.pop(1)
                    tokenlist.pop(1)
                else:
                    raise Syntaxfel("Syntaxfel på rad " + str(tokenlist[3].row))
        except (IndexError, TypeError):
            raise Syntaxfel("Syntaxfel på rad " + str(tokenlist[1].row))
    elif peek(tokenlist, 0) == "REP":
        N = repToken(tokenlist, N)
    else:
        raise Syntaxfel("Syntaxfel på rad " + str(tokenlist[1].row))

    return N

def movementToken(tokenlist, N):
    if peek(tokenlist, 0) == "FORW":
        N.token = "FORW"
        tokenlist.pop(1)
        tokenlist.pop(1)
        tokenlist.pop(1)
    elif peek(tokenlist, 0) == "BACK":
        N.token = "BACK"
        tokenlist.pop(1)
        tokenlist.pop(1)
        tokenlist.pop(1)
    elif peek(tokenlist, 0) == "LEFT":
        N.token = "LEFT"
        tokenlist.pop(1)
        tokenlist.pop(1)
        tokenlist.pop(1)
    elif peek(tokenlist, 0) == "RIGHT":
        N.token = "RIGHT"
        tokenlist.pop(1)
        tokenlist.pop(1)
        tokenlist.pop(1)

    return N

def penToken(tokenlist, N):
    if peek(tokenlist, 0) == "UP":
        N.token = "UP"
        tokenlist.pop(1)
        tokenlist.pop(1)
    elif peek(tokenlist, 0) == "DOWN":
        N.token = "DOWN"
        tokenlist.pop(1)
        tokenlist.pop(1)

    return N

def repToken(tokenlist, N):
    try: # Om vi hamnar utanför tokenlist längd så gör vi en try sats för att inte ge felmeddelande.
        if int(peekNum(tokenlist, 1)) > 0:
            N.value = int(peekNum(tokenlist, 1))
            if peek(tokenlist, 2) == "QUOTE":
                if peek(tokenlist, 3) == "QUOTE": #FEL OM VI HAR EN TOM QUOTE 
                    raise Syntaxfel("Syntaxfel på rad " + str(tokenlist[3].row))
                N.token = "REP"
                tokenlist.pop(1)
                tokenlist.pop(1)
                tokenlist.pop(1)
                N.rep = leonaInner(tokenlist)
                try:
                    if peek(tokenlist, 0) == "QUOTE":
                        tokenlist.pop(1)
                        return N
                except:
                    raise Syntaxfel("Syntaxfel på rad " + str(lastrow))
            else:
                N.token = "REP"
                tokenlist.pop(1)
                tokenlist.pop(1)
                N.rep = instruktion(tokenlist)  #denna har lagts till 
        else:
            raise Syntaxfel("Syntaxfel på rad " + str(tokenlist[1].row))
    except (TypeError):
        raise Syntaxfel("Syntaxfel på rad " + str(tokenlist[1].row))
    return N

def syntaxTree(tokenlist):
    N = leonafunc(tokenlist)

    return N



leona = Leona()  # skapar leona objekt
if tokenlista !=0:

    if not "ERROR" in tokenlista:
        lastrow = tokenlista[-1].row

        try:
            tree = syntaxTree(tokenlista)
            if len(tokenlista) > 1: #denna plockar citattecken, kollar så att vi har gått igenom alla tokens
                raise Syntaxfel("Syntaxfel på rad " + str(tokenlista[1].row))
            checkrecur(tree, leona)  # skriver ut träd
        except Syntaxfel as fel:
            print(fel)



