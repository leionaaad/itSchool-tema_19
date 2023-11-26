import mysql.connector as mc

dbHost = "127.0.0.1"
dbUser = "root"
dbPass = "#6eo#6eo"
dbSchema = "Tema_18"
teamsTable = "Tema_18.Echipe"
playersTable = "Tema_18.Fotbalisti"

dbConn = mc.connect(host=dbHost, user=dbUser, password=dbPass, database=dbSchema)
cursor = dbConn.cursor()



# creati functii de insert in tabela echipe 
def addClub(name, colors, founded, fans):
    #check if the club already exists
    
    cursor.execute(f"INSERT INTO {teamsTable} (`Nume`, `Culori`, `Infiintat`, `Suporteri`) VALUES ('{name}', '{colors}', {founded}, {fans})")
    dbConn.commit()



# creati functii de insert in tabela jucatori 
def addPlayer():
    pass



# creati o functie care afiseaza toate echipele disponibile (executa select in baza de date si le afiseaza pe cate o linie in forma: id nume) 
def getTeams() :
    pass



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
addClub("Csikszereda", "kek, okker", 1990, 200000)