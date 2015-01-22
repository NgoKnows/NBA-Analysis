import urllib2 as u
import codecs
import os

def parse_players(letter):
    url = "http://www.basketball-reference.com/players/" + letter + "/"
    page = u.urlopen(url).read()
    count = page.count('<a href="/players/' + letter)
    
    start = 0
    a = '<a href="/players/' + letter
    b = '">'
    c = '<h1>'
    d = "Height:</span>"
    e = 'id = "per_game">'
    h = '<td align'
    j = '>'

    newpath = os.path.join(os.getcwd(), "Player Stats")
    if not os.path.exists(newpath): os.makedirs(newpath)
    os.chdir(newpath)
    
    for i in range(count):
        pc1 = page.find(a, start)
        pc2 = page.find(b, pc1)

        
        player_code = page[pc1 + len(a) + 1: pc2]
        player_code = player_code.split(".")[0]
        start = pc2
        
        pp = u.urlopen(url + player_code + ".html").read()

        #name
        name1 = pp.find(c, 0)
        name2 = pp.find("</h1>", name1)
        player_name = pp[name1 + len(c) : name2]

        #height
        height1 = pp.find(d) + len(d)
        height = pp[height1 : height1 + 5]
        height = height.split()[0].split("&")[0]


        season_count = pp.count('id="per_game.')
        fname = player_name + '.csv'
        fle = codecs.open(fname, "w", "utf-8")
        write_categories(fle)

        f  = 'id="all_totals"'
        g = 'id="totals.'
        start2 = pp.find(f, 0)
        print player_name
        removed = 0

        try:
            for season in xrange(season_count):

                season2 = pp.find(g, start2)
                start2 = season2 + 4
                season = pp[season2 + len(g): season2 + len(g) + 4]
                
            
                season = str(int(season) - 1) + "-"  + str(season)

                #season
                skip = pp.find(h, start2)
                start2 = skip + len(h)

                #skip league
                skip = pp.find(h, start2)
                start2 = skip + len(h)


                #age
                age2 = pp.find(j, start2)
                age3 = pp.find("</", age2)
                start2 = age2 + len(h)
                age = pp[age2 + len(j): age3]

                #team
                age2 = pp.find(j, start2)
                age3 = pp.find("</", age2)
                start2 = age2 + len(h) + 55
                team = pp[age2 + len(j): age3]
                if len(age) != 3:
                    start2 += len(team) * 2
                    team = team[-3:]

                if(age == "TOT"):
                    skip = pp.find(h, start2)
                    start2 = skip + len(h)

                #Positon
                age2 = pp.find(j, start2)
                age3 = pp.find("</", age2)
                start2 = age2 + len(h)
                position = pp[age2 + len(j): age3]
                if position == "":
                    position = pp[age2 + 10: age3 + 31].split(">")[1].split("<")[0]
                    start2 += 40
                    if position.isdigit():
                        position = ""
                        start2 -= 40
                
            #try:
                age4 = age
                age2 = pp.find(j, start2)
                age3 = pp.find("</", age2)
                start2 = age3
                age = pp[age2 + len(j): age3]
                if(len(age) > 5):
                    age = age.split(">")[1].strip()
                if(age == ""):
                        age = ".000"
                games = int(age.strip())
                '''except:
                    
                    continue'''
        
                
                fle.write(player_name + ",")
                fle.write(team + ",")
                fle.write(season + ",")
                fle.write(" " + height + ",")
                fle.write(position + ",")
                fle.write(age4 + ",")

    #games
                fle.write(str(games) + ",")
                
    #gs
                age2 = pp.find(j, start2)
                age3 = pp.find("</", age2)
                start2 = age3
                age = pp[age2 + len(j): age3]
                if(len(age) > 5):
                    age = age.split(">")[1].strip()
                if(age == ""):
                        age = ".000"
                age = age.strip()
            

    #mp

                age2 = pp.find(j, start2)
                age3 = pp.find("</", age2)
                start2 = age3
                age = pp[age2 + len(j): age3]
                if(len(age) > 5):
                    age = age.split(">")[1].strip()
                if(age == ""):
                        age = ".000"
                age = age.strip()
                fle.write(age + ",")
    #mpg
                mpg = str(float(age) / games)
                fle.write(mpg + ",")

    #fg

                age2 = pp.find(j, start2)
                age3 = pp.find("</", age2)
                start2 = age3
                age = pp[age2 + len(j): age3]
                if(len(age) > 5):
                    age = age.split(">")[1].strip()
                if(age == ""):
                        age = ".000"
                age = age.strip()
                fle.write(age + ",")

    #fga

                age2 = pp.find(j, start2)
                age3 = pp.find("</", age2)
                start2 = age3
                age = pp[age2 + len(j): age3]
                if(len(age) > 5):
                    age = age.split(">")[1].strip()
                if(age == ""):
                        age = ".000"
                age = age.strip()
                fle.write(age + ",")

    #fg%
                age2 = pp.find(j, start2)
                age3 = pp.find("</", age2)
                start2 = age3
                age = pp[age2 + len(j): age3]
                if(len(age) > 5):
                    age = age.split(">")[1].strip()
                if(age == ""):
                        age = ".000"
                age = age.strip()
                fle.write(age + ",")

    #3ptm

                age2 = pp.find(j, start2)
                age3 = pp.find("</", age2)
                start2 = age3
                age = pp[age2 + len(j): age3]
                if(len(age) > 5):
                    age = age.split(">")[1].strip()
                if(age == ""):
                        age = ".000"
                age = age.strip()

                fle.write(age + ",")
    #3pta

                age2 = pp.find(j, start2)
                age3 = pp.find("</", age2)
                start2 = age3
                age = pp[age2 + len(j): age3]
                if(len(age) > 5):
                    age = age.split(">")[1].strip()
                if(age == ""):
                        age = ".000"
                age = age.strip()

                fle.write(age + ",")
    #3pt%

                age2 = pp.find(j, start2)
                age3 = pp.find("</", age2)
                start2 = age3
                age = pp[age2 + len(j): age3]
                if(len(age) > 5):
                    age = age.split(">")[1].strip()
                if(age == ""):
                        age = ".000"
                age = age.strip()

                fle.write(age + ",")

    #ftm

                age2 = pp.find(j, start2)
                age3 = pp.find("</", age2)
                start2 = age3
                age = pp[age2 + len(j): age3]
                if(len(age) > 5):
                    age = age.split(">")[1].strip()
                if(age == ""):
                        age = ".000"
                age = age.strip()

                fle.write(age + ",")

    #ftm

                age2 = pp.find(j, start2)
                age3 = pp.find("</", age2)
                start2 = age3
                age = pp[age2 + len(j): age3]
                if(len(age) > 5):
                    age = age.split(">")[1].strip()
                if(age == ""):
                        age = ".000"
                age = age.strip()

                fle.write(age + ",")

    #ft%

                age2 = pp.find(j, start2)
                age3 = pp.find("</", age2)
                start2 = age3
                age = pp[age2 + len(j): age3]
                if(len(age) > 5):
                    age = age.split(">")[1].strip()
                if(age == ""):
                        age = ".000"
                age = age.strip()

                fle.write(age + ",")
    #orb

                age2 = pp.find(j, start2)
                age3 = pp.find("</", age2)
                start2 = age3
                age = pp[age2 + len(j): age3]
                if(len(age) > 5):
                    age = age.split(">")[1].strip()
                if(age == ""):
                        age = ".000"
                age = age.strip()
                fle.write(age + ",")
    #orbg
                orbg = str(float(age)/games)
                fle.write(orbg + ",")

            
    #drb
                age2 = pp.find(j, start2)
                age3 = pp.find("</", age2)
                start2 = age3
                age = pp[age2 + len(j): age3]
                if(len(age) > 5):
                    age = age.split(">")[1].strip()
                if(age == ""):
                        age = ".000"
                age = age.strip()
                fle.write(age + ",")

    #drbg
                drbg = str(float(age)/games)
                fle.write(drbg + ",")
                
    #trb
                
                age2 = pp.find(j, start2)
                age3 = pp.find("</", age2)
                start2 = age3
                age = pp[age2 + len(j): age3]
                if(len(age) > 5):
                    age = age.split(">")[1].strip()
                if(age == ""):
                        age = ".000"
                age = age.strip()
                fle.write(age + ",")

    #trbg
                trbg = str(float(age)/games)
                fle.write(trbg + ",")

    #ast
                

                age2 = pp.find(j, start2)
                age3 = pp.find("</", age2)
                start2 = age3
                age = pp[age2 + len(j): age3]
                if(len(age) > 5):
                    age = age.split(">")[1].strip()
                if(age == ""):
                        age = ".000"
                age = age.strip()
                fle.write(age + ",")

    #apg
                apg = str(float(age)/games)
                fle.write(apg + ",")

    #stl

                age2 = pp.find(j, start2)
                age3 = pp.find("</", age2)
                start2 = age3
                age = pp[age2 + len(j): age3]
                if(len(age) > 5):
                    age = age.split(">")[1].strip()
                if(age == ""):
                        age = ".000"
                age = age.strip()
                fle.write(age + ",")

    #spg
                spg = str(float(age)/games)
                fle.write(spg + ",")

    #blk

                
                age2 = pp.find(j, start2)
                age3 = pp.find("</", age2)
                start2 = age3
                age = pp[age2 + len(j): age3]
                if(len(age) > 5):
                    age = age.split(">")[1].strip()
                if(age == ""):
                        age = ".000"
                age = age.strip()
                fle.write(age + ",")
    #bpg

                bpg = str(float(age)/games)
                fle.write(bpg + ",")

    #to

                age2 = pp.find(j, start2)
                age3 = pp.find("</", age2)
                start2 = age3
                age = pp[age2 + len(j): age3]
                if(len(age) > 5):
                    age = age.split(">")[1].strip()
                if(age == ""):
                        age = ".000"
                age = age.strip()
                fle.write(age + ",")

    #topg
                topg = str(float(age)/games)
                fle.write(topg + ",")

    #pf

                age2 = pp.find(j, start2)
                age3 = pp.find("</", age2)
                start2 = age3
                age = pp[age2 + len(j): age3]
                if(len(age) > 5):
                    age = age.split(">")[1].strip()
                if(age == ""):
                        age = ".000"
                age = age.strip()
                fle.write(age + ",")

    #pts

                age2 = pp.find(j, start2)
                age3 = pp.find("</", age2)
                start2 = age3
                age = pp[age2 + len(j): age3]
                if(len(age) > 5):
                    age = age.split(">")[1].strip()
                if(age == ""):
                        age = ".000"
                age = age.strip()
                fle.write(age + ",")

                

    #ppg
                ppg = str(float(age)/games)
                fle.write(ppg + ",")
                fle.write("\n")

        except:
            removed +=1
            print removed
            fle.close()
            os.remove(fname)
            
        
        

def write_categories(fle):
    fle.write('Player,')
    fle.write('Team,')
    fle.write('Season,')
    fle.write('Height,')
    fle.write('Position,')
    fle.write('Age,')
    fle.write('G,')
    fle.write('MIN,')
    fle.write('MINPG,')
    fle.write('FGM,')
    fle.write('FGA,')
    fle.write('FGP,')
    fle.write('TPM,')
    fle.write('TPA,')
    fle.write('TPP,')
    fle.write('FTM,')
    fle.write('FTA,')
    fle.write('FTP,')
    fle.write('ORB,')
    fle.write('ORBPG,')
    fle.write('DRB,')
    fle.write('DRBPG,')
    fle.write('TRB,')
    fle.write('TRBPG,')
    fle.write('AST,')
    fle.write('ASTPG,')
    fle.write('STL,')
    fle.write('STLPG,')
    fle.write('BLK,')
    fle.write('BLKPG,')
    fle.write('TO,')
    fle.write('TOPG,')
    fle.write('PF,')
    fle.write('PTS,')
    fle.write('PTSPG,')
    fle.write("\n")
    

def main():
    letters = "abcdefghijklmnopqrstuvwxyz"
    for letter in letters:
        parse_players(letter)
        

main()


