import random
import sqlite3
from datetime import date
import os
# van 5 rondes na 3 winnen optie
#anders dan getal opniewu vraag bij rondes
#wie welke ronde

datum = date.today()
con = sqlite3.connect("scoredatabase.db")
cur = con.cursor()

steen, papier, schaar = "steen", "papier", "schaar"
sps = [steen, papier, schaar]
spsCheck = {steen: schaar, papier: steen, schaar: papier}
rondes = 0
rondesCheck = False

cur.execute("CREATE TABLE IF NOT EXISTS game(username, wvg, score, datum, nummer)")
cur.execute("CREATE TABLE IF NOT EXISTS opties(naam, value, id)")


def kiesZetComputer():
  num = random.randint(1, 3)
  
  computerzet = {
    1: steen,
    2: papier,
    3: schaar
  }
  for i in computerzet:
    if i == num:
      return computerzet[i]


def optieCheck():
  #dictionary met opties true of false maken bij opstart en na optie update
  #dus optieCheck() in bijopstart
  a = "werkt niet"
  for row in cur.execute("SELECT value FROM opties WHERE id = 0"):
    for i in row:
      if i == 1: 
        # afronden true
        pass
      elif i == 0:
        #afronden false
        pass
  return a
        

def opties():
  # deze check bij opstart functie doen en die functie maken
  for row in cur.execute("SELECT count(*) FROM opties"):
    for i in row:
        if i == 0:
            naam = "afrond"
            value = True
            optieId = 0
            cur.execute("""INSERT INTO opties VALUES(?,?,?)""",(naam, value, optieId))
            con.commit()
  id = 0
  print("Optie commands:")
  print("    -afrondWin (afronndWin_aan/afrondWin_uit)")
  print("huidige geselecteerde opties: ")
  for row in cur.execute("SELECT * FROM opties"):
    print(row)
  optiesInvoer = input("optie: ").lower()
  if optiesInvoer == "afrondwin_aan":
    afrondKeuze = True
  elif optiesInvoer == "afrondwin_uit":
    afrondKeuze = False
  cur.execute('''UPDATE opties SET value = ? WHERE id = ?''', (afrondKeuze, id)) #hier de id values updaten
  con.commit()


def winCheck(w, v, g, speler, compKeuze, rondes, username, rondesTot, score):
  if speler == compKeuze:
    g += 1
    rondes += 1
    score.append(f"Ronde {rondesTot} Gelijk gespeeld!")
    print("Gelijkspel, speel de ronde opnieuw!")
  elif speler != compKeuze:
    for i in spsCheck:
      spsChecki = i + spsCheck[i]
      spelerWint = str(speler) + str(compKeuze)
      computerWint = str(compKeuze) + str(speler)
      if spsChecki == spelerWint:
        w += 1
        score.append(f"Ronde {rondesTot} gewonnen")
        print(f"{username} wint met {speler}")
      elif spsChecki == computerWint:
        v += 1
        score.append(f"Ronde {rondesTot} Verloren")
        print(f"Computer wint met {compKeuze}")
  return w, v, g, rondes, score

def printScore():
  for row in cur.execute(
      "SELECT username, wvg, score, datum, nummer FROM game"):
    username, wvg, score, datum, nummer = row
    splitScore = score.split(", ")
    print(f"{username}     |     {wvg}")
    print("--------------------")
    for i in splitScore:
      print(i)
    print("--------------------")
    print(f"{datum}     | game ID: {nummer}")
    print("")
  terugInvoer = input("Wil je terug naar het keuze menu?  j/n: ").lower()
  if terugInvoer == "j":
    keuzeMenu()
  else:
    pass

def delID():
  try:
    welkeRow = int(input("welke game wil je verwijderen? :"))
    if welkeRow >= 0:
      cur.execute(f"DELETE FROM game WHERE nummer = {welkeRow}")
      con.commit()
      idCheck = 0
      nieuwID = 0
      for row in cur.execute("SELECT nummer FROM game"):
        for i in row:
          idCheck += 1
          if int(i) >= idCheck:
            nieuwID = i - 1
            cur.execute('''UPDATE game SET nummer = ? WHERE nummer = ?''', (nieuwID, i)) #hier de id values updaten
            con.commit()
    else:
      print("Vul een geldige invoer in!")
      printID()
  except:
    print("Vul een geldige invoer in!")
    delID()
  terugInvoer = input("Wil je terug naar het keuze menu?  j/n: ").lower()
  if terugInvoer == "j":
    keuzeMenu()
  else:
    pass


def printID():
  try:
    welkeRow = int(input("welke game? :"))
    if welkeRow > 0:
      for row in cur.execute(f"SELECT username, wvg, score, datum, nummer FROM game WHERE nummer = {welkeRow}"):
        username, wvg, score, datum, nummer = row
        splitScore = score.split(", ")
        print(f"{username}     |     {wvg}")
        print("--------------------")
        for i in splitScore:
          print(i)
        print("--------------------")
        print(f"{datum}     | game ID: {nummer}")
        print("")
    else:
      print("Vul een geldige invoer in!")
      printID()
  except:
    print("Vul een geldige invoer in!")
    printID()
  terugInvoer = input("Wil je terug naar het keuze menu?  j/n: ").lower()
  if terugInvoer == "j":
    keuzeMenu()
  else:
    pass
  

def startGame(rondesCheck):
  username = input("username:")
  while rondesCheck == False:
    try:
      rondes = int(input("Rondes:"))
      if rondes > 0:
        rondesCheck = True
        return username, rondes
      else:
        print("Vul een geldige invoer in!")
    except:
      print("Vul een geldige invoer in!")
  

def spel(username, rondes, score):
  afrond = optieCheck()
  print(afrond) #dit test ^ook
  rondesTot = 0
  w=v=g= 0
  nummer = 0
  for row in cur.execute("SELECT nummer FROM game"):
    for i in row:
      nummer = i + 1
  while rondesTot < rondes:
    compKeuze = kiesZetComputer()
    spelerKeuze = input("Steen, papier of schaar of :").lower()
    rondesTot += 1
    if spelerKeuze not in sps:
      rondesTot -= 1
      print("Voer steen, papier of schaarin")
    elif spelerKeuze in sps:
      w, v, g, rondes, score = winCheck(w, v, g, spelerKeuze, compKeuze, rondes, username, rondesTot, score)
    if rondes == rondesTot:
      print("afgelopen")
      wvg = f"W/V/G = {w}/{v}/{g}"
      scorelist = ", ".join(score)
      cur.execute("""INSERT INTO game VALUES(?,?,?,?,?)""",(username, wvg, scorelist, datum, nummer))
      con.commit()
      for i in score:
        print(i)
    else:
      pass
  terugInvoer = input("Wil je terug naar het keuze menu?  j/n: ").lower()
  if terugInvoer == "j":
    keuzeMenu()
  else:
    pass


def keuzeMenu():
  score=[]
  print("Je kan kiezen tussen:")
  print("   -Start (begin het steen papier schaar spel!)")
  print("   -Score (Laat je de score zien van vorige games gespeeld.)")
  print("   -ID (laat je een specifieke game score zien van een game met id die je invult)")
  print("   -DEL (verwijder specefieke game met het spel id)")
  print("   -Opties (voor opties in de game die opgeslagen blijven)")
  menuKeuzeInvoer = input("voer in start/opties/score/ID/DEL :").lower()
  if menuKeuzeInvoer == "score":
    printScore()
  elif menuKeuzeInvoer == "start":
    username, rondes = startGame(rondesCheck)
    spel(username, rondes, score)
  elif menuKeuzeInvoer == "id":
    printID()
  elif menuKeuzeInvoer == "del":
    delID()
  elif menuKeuzeInvoer == "opties":
    opties()
  else:
    print("spelfout")
    keuzeMenu()
  
keuzeMenu()




#Jesse   |   W/V/G
#--------------------
#Ronde 1 gewonnen
#ronde 2 gelijk
#ronde 3 verloren
#--------------------
#13-10-2023
