import mysql.connector as mc
import datetime

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
    cursor.execute(f"SELECT ID FROM {teamsTable} WHERE `NUME` LIKE '{team}'")
    teamID = cursor.fetchone()[0]

    if not checkIfExists(name, playersTable):
        cursor.execute(f"INSERT INTO {playersTable} (`Nume`, `Prenume`, `Data_Nasterii`, `Valoare`, `Echipa`) VALUES ('{name}', '{surname}', '{birthday}', {value}, {teamID})")
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
    pass



# -creati o functie care le imbina pe cele 2 de mai sus astfel: se afiseaza toate echipele disponibile, 
# se citeste id-ul echipei de la tastatura si apoi se apeleaza functia care afiseaza cel mai scump jucator de la echipa respectiva
def getMostExpensiveFromTeamsList():
    pass



# calculati numaru de jucatori din fiecare echipa (vedeti problema cu group by din cursul anterior)
def getNumberOfPlayers():
    pass



# calculati cel mai scump jucator din fiecare echipa (tot cu group by trebuie )
def getAllMostExpensivePlayers():
    pass



# calculati valoarea lotului fiecarei echipe
def getClubValue():
    pass



#Call these functions
# addClub("Csikszereda", "kek, okker", 1990, 200000)
# addClubFromTerminal()
# addPlayer("Matyas",  "Hajnalka", "1989-05-21", 300000, "Csikszereda")
# addPlayerFromTerminal()
# listTeams()


#cleanup the bullcrap
cursor.close()
dbConn.close()
