import mysql.connector as mc

dbHost = "127.0.0.1"
dbUser = "root"
dbPass = "#6eo#6eo"
dbSchema = "Tema_18"
teamsTable = "Tema_18.Echipe"
playersTable = "Tema_18.Fotbalisti"

dbConn = mc.connect(host=dbHost, user=dbUser, password=dbPass, database=dbSchema)
cursor = dbConn.cursor()



def checkIfExists(name, table) -> bool:
    cursor.execute(f"SELECT EXISTS(SELECT * FROM {table} WHERE `Nume` = '{name}')")
    res = cursor.fetchone()
    if res[0] == 0:
        return False
    else:
        print(f"{name} exista deja, pretene.")
        return True
    
def getId(name, table) -> int:
    cursor.execute(f"SELECT ID FROM {table} WHERE `Nume` LIKE '{name}'")
    return cursor.fetchone()[0]

def getNameFromId(id, table) -> str:
    cursor.execute(f"SELECT `Nume` FROM {table} WHERE `Id` = {id}")
    return cursor.fetchone()[0]



# creati functii de insert in tabela echipe 
def addClub(name, colors, founded, fans):
    if checkIfExists(name, teamsTable) == False:
        cursor.execute(f"INSERT INTO {teamsTable} (`Nume`, `Culori`, `Infiintat`, `Suporteri`) VALUES ('{name}', '{colors}', {founded}, {fans})")
        dbConn.commit()
        print(f"{name} a fost adaugat in lista noastra de cluburi. Inca o optiune de spalat bani. ")
        


def addClubFromTerminal():
    name = input("Numele Clubului: ")
    colors = ""
    founded = None
    fans = 0

    if checkIfExists(name, teamsTable) == False:
        colors = input("Ce culori are acum? ")
        founded = int(input("De cand exista? "))
        fans = int(input("Cati fani are?"))
    else:
        return
    
    addClub(name, colors, founded, fans)



# creati functii de insert in tabela jucatori 
def addPlayer(name, surname, birthday, value, team):
    #get ID of the team. or something.

    if not checkIfExists(name, playersTable):
        cursor.execute(f"INSERT INTO {playersTable} (`Nume`, `Prenume`, `Data_Nasterii`, `Valoare`, `Echipa`) VALUES ('{name}', '{surname}', '{birthday}', {value}, {getId(team, teamsTable)})")
        dbConn.commit()
        print(f"Am adaugat-o pe {name} la lista de jucatori.")



def addPlayerFromTerminal():
    name = input("Numele: ")
    year = None
    month = None
    day = None
    value = 0
    team = None

    if not checkIfExists(name, playersTable):
        surname = input("Prenumele: ")
        year = input("Anul Nasterii: ")
        month = input("Luna: ")
        day = input("Ziua: ")
        value = input("Valoarea jucatorului: ")
        team = input("Echipa: ")
    else:
        return
    
    birthday = f"{year}={month}-{day}"
    addPlayer(name, surname, birthday, value, team)



# creati o functie care afiseaza toate echipele disponibile (executa select in baza de date si le afiseaza pe cate o linie in forma: id nume) 
def listTeams() :
    cursor.execute(f"SELECT Id, Nume FROM {teamsTable}")
    result = cursor.fetchall()
    print(f"ID {24*'_'} NUME")
    for e in result:
        print(f"{e[0]} {25*'_'} {e[1]}")



# creati o functie pentru calcularea valorii celui mai scump jucator de la echipa a carui id este transmis ca parametru 
def getMostExpensivePlayer(club):
    cursor.execute(f"SELECT * FROM {playersTable} WHERE `Id` = {getId(club, teamsTable)} AND (SELECT MAX(`Valoare`) FROM {playersTable});")
    return cursor.fetchone()
    


def printMostExpensivePlayer(club):
    result = getMostExpensivePlayer(club)
    print(f"Cea mai scumpa jucatoare din {club} e {result[1]} {result[2]}, in valoare de {result[4]} de lei sau euro. Nici nu stiu")



# -creati o functie care le imbina pe cele 2 de mai sus astfel: se afiseaza toate echipele disponibile, 
# se citeste id-ul echipei de la tastatura si apoi se apeleaza functia care afiseaza cel mai scump jucator de la echipa respectiva
def getMostExpensiveFromTeamsList():
    listTeams()
    clubSelection = getNameFromId(int(input("Scumpa de la care grup vrei sa vezi? tasteaza ID-ul: ")), teamsTable)
    printMostExpensivePlayer(clubSelection)



# calculati numaru de jucatori din fiecare echipa (vedeti problema cu group by din cursul anterior)
def getNumberOfPlayers():
    cursor.execute(f"SELECT {teamsTable}.Nume, COUNT(*) FROM {teamsTable} INNER JOIN {playersTable} ON {teamsTable}.Id = {playersTable}.Echipa GROUP BY {teamsTable}.Nume")
    return cursor.fetchall()



def printNumberOfPlayers():
    players = getNumberOfPlayers()
    verb = None

    for p in players:
        if p[1] == 1:
            verb = "Este"
        else:
            verb = "Sunt"
        print(f"{verb} {p[1]} jucatoare in clubu din {p[0]}")



# calculati cel mai scump jucator din fiecare echipa (tot cu group by trebuie )
def getAllMostExpensivePlayers():
    sqlCmd = f"SELECT {playersTable}.Nume, {playersTable}.Prenume, {playersTable}.Valoare, {teamsTable}.Nume FROM {playersTable} INNER JOIN {teamsTable} ON {teamsTable}.Id = {playersTable}.Echipa INNER JOIN (SELECT Echipa, MAX(Valoare) AS 'MaxValoare' FROM {playersTable} GROUP BY Echipa) AS MaxValues ON {playersTable}.Echipa = MaxValues.Echipa AND {playersTable}.Valoare = MaxValues.MaxValoare;"
    cursor.execute(sqlCmd)
    return cursor.fetchall()



def printAllMostExpensivePlayers():
    playerInfos = getAllMostExpensivePlayers()
    for i in playerInfos:
        print(f"Cea mai scumpa din {i[3]} ii {i[0]} {i[1]}, are {i[2]}")



# calculati valoarea lotului fiecarei echipe
def getClubValues():
    cursor.execute(f"SELECT SUM(Valoare), {teamsTable}.Nume FROM {playersTable} INNER JOIN {teamsTable} ON {teamsTable}.Id = {playersTable}.Echipa GROUP BY {teamsTable}.Nume")
    return cursor.fetchall()



def printClubValues():
    clubsAndValues = getClubValues()
    print(f"Valoarea cluburilor este urmatoarele, nu stim daca e in euro sau lei:")
    for c in clubsAndValues:
        print(f"{c[1]} : {c[0]}")



#Call these functions
# addClub("Csikszereda", "kek, okker", 1990, 200000)
# addClubFromTerminal()
# addPlayer("Matyas",  "Hajnalka", "1989-05-21", 300000, "Csikszereda")
# addPlayerFromTerminal()
# listTeams()
# getMostExpensivePlayer("Castelsardo")
# getMostExpensiveFromTeamsList()
# printNumberOfPlayers()
# printAllMostExpensivePlayers()
# printClubValues()

#cleanup the bullcrap
cursor.close()
dbConn.close()
