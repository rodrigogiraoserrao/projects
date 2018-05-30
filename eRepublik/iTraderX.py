#!/usr/bin/python3

import atexit
atexit.register(input, "...")
atexit.register(input,"@@@@@ The program is about to close.\nIf you didn't use the <exit> command,\n   please take a screenshot and send it to Rojer97 @@@@@")

## Coded by Rojer97
### Want to join the game?? Register now! http://www.erepublik.com/en/referrer/Rojer97
# (please do register with the above link xD)
## Check me on eRepublik: http://www.erepublik.com/en/citizen/profile/6328829

import hashlib
import json
import argparse
import datetime
import html.parser
import urllib.request
from re import search
from time import sleep, time

VERSION = "1.1.0 Beta"

print("Welcome!!")
sleep(0.5)
print("""  _ _____              _           
 (_)_   _| __ __ _  __| | ___ _ __ 
 | | | || '__/ _` |/ _` |/ _ \ '__|
 | | | || | | (_| | (_| |  __/ |   
 |_| |_||_|  \__,_|\__,_|\___|_|   
                                   """)
#ASCII artwork @ http://patorjk.com/software/taag/#p=display&f=Standard&t=iTrader
print("Version {}".format(VERSION))
print("This nice program was brought to you by Rojer97!")
print("A donation of 1 gold would be enough to motivate me,")
print("to keep improving this program!")
start = time()
l = ["....", " ...", ". ..", ".. .", "... "]
while True:
    for l1 in l:
        print("Loading "+l1, end="\r")
        sleep(0.2)
    if time()-start > 3.5:
        print("Loaded!!    ")
        break
print()
input("(press any key)")
print("\n"*40)

PROMPT = "iTrader(beta)$ "

class Search_Parser(html.parser.HTMLParser):

    def __init__(self):
        html.parser.HTMLParser.__init__(self)
        self.try_name = False
        self.try_exp = False
        self.matches = []
        self.temp_link = None
        self.temp_name = None
    
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "a":
            d = dict(attrs)
            if "class" in d.keys():
                if d["class"] == "dotted":
                    self.temp_link = d["href"]
                    self.try_name = True
        if tag == "span":
            d = dict(attrs)
            if "class" in d.keys():
                if d["class"] == "special fakeheight":
                    self.try_exp = True
        
    def handle_data(self, data):
        if self.try_name:
            self.temp_name = data
            self.try_name = False
        if self.try_exp:
            self.try_exp = False
            self.matches.append((self.temp_name, self.temp_link, data))
            self.temp_name = None
            self.temp_link = None
            
    def error(self, error):
        pass
        
def handle_matches(data):
    base_url = "http://erepublik.com"
    if data == []:  
        return {}
    d = {}
    # index 0 is name
    # index 1 is link
    # index 2 is exp
    for tup in data:
        match = search(r"[0123456789]+", tup[1])
        link_id = match.group()
        d[tup[0]] = {"name": tup[0], "id": link_id, "link": base_url+tup[1],
                        "exp": tup[2]}
    return d

def DEBUG(g, l, e):
    '''Debugging function to be called when errors were expected.
    Receives as arguments the locals() and globals() of the scope in which the
error was to be raised, just as the error. The error gets printed and a loop
runs until the debugger exits with \'exit(X)\''''
    # <g> and <l> are both the globals and locals from which the debugging
    #function was called! This lets me play around with the problems
    print("You just entered the debugger")
    print("The error that took you here was:")
    print(e)
    print("#"*40)
    while True:
        try:
            exec(input("[debugger] > "), g, l)
        except Exception as error:
            print("[Error...]")
            print(error)

def SAVE(file_name, data):
    try:
        with open(file_name, "w") as f:
            json.dump(data, f, sort_keys=True, indent=8)
    except Exception as e:
        print("Error while saving:")
        print(e)
        return False
    return True

def LOAD(file_name):
    try:
        with open(file_name, "r") as f:
            unparsed_data = f.read()
    except IOError:
        print("Could not load data.")
        return False
    try:
        data = json.loads(unparsed_data)
    except Exception as e:
        print("Error loading data...")
        print(file_name)
        DEBUG(globals(), locals(), e)
    return data
        
def LOG(file_name, data):
    try:
        with open(file_name, "a") as f:
            f.write(str(data))
    except IOError:
        print("Could not open logging file.")
        return False
    return True
    
main_parser = argparse.ArgumentParser()

main_parser.add_argument("action", help="Define the action to execute. Type <help> for a complete help.",
            choices=["trade", "register", "calc", "exit", "print", "check",
                "search", "help", "log", "convert", "list", "find"], metavar="action")
main_parser.add_argument("args", nargs=argparse.REMAINDER, metavar="arguments",
                        help="The arguments for the action")

FILE_INFO = "itrade.data"
FILE_LOG = "itrade_trades.log"
FILE_TRADERS = "itrade_traders.data"
items = {"wq6": "Weapons Q6", "wq7": "Weapons Q7", "wq5": "Weapons Q5", "wq4": "Weapons Q4",
    "wq3": "Weapons Q3", "wq2": "Weapons Q2", "wq1": "Weapons Q1", "fq1": "Food Q1",
    "fq2": "Food Q2", "fq3": "Food Q3", "fq4": "Food Q4", "fq5": "Food Q5", "fq6": "Food Q6",
    "fq7": "Food Q7", "wrm": "Weapon Raw Material", "frm": "Food Raw Material", "gold": "Gold"}

itrade_info = LOAD(FILE_INFO)
if itrade_info == False:
    del itrade_info
    itrade_info = dict()
    open(FILE_INFO, "w").close()
    print("Type in your name:")
    name = input(PROMPT)
    itrade_info["name"] = name
    itrade_info["stock"] = {}
    for key in items.keys():
        itrade_info["stock"][key] = 0
    itrade_info["profit"] = 0
    success = SAVE(FILE_INFO, itrade_info)
    if not(success):
        print("Problem saving...")
        DEBUG(globals(), locals(), "")
    
traders = LOAD(FILE_TRADERS)
if traders == False:
    traders = {}
    open(FILE_TRADERS, "w").close()
    success = SAVE(FILE_TRADERS, traders)
    if not(success):
        print("Problem saving the traders...")
        print(globals(), locals(), "")
                
d = {"buy": ["bought", "spending"], "sell": ["sold", "gaining"]}

### Define all the parsers outside the loop

convert_parser = argparse.ArgumentParser()
convert_parser.add_argument("gold", type=int, help="Amount of gold "\
                            "bought.", metavar="gold")
convert_parser.add_argument("cc", type=float, help="Amount of cc "\
                            "converted into gold.", metavar="CC")
                            
log_parser = argparse.ArgumentParser()
log_parser.add_argument("n", help="Number of logs to show.", metavar="N")

print_parser = argparse.ArgumentParser()
print_parser.add_argument("player", metavar="player", nargs="?",
                            help="Type the player ID to print")
                            
check_parser = argparse.ArgumentParser()
check_parser.add_argument("id_number", metavar="id", help="ID to check.")

trade_parser = argparse.ArgumentParser()
trade_parser.add_argument("transaction", metavar="transaction", 
help="The type of transaction. [buy | sell]", choices = ["buy", "sell"])
trade_parser.add_argument("id_number", metavar="id", help="The id of "\
            "the player with whom you traded.")
trade_parser.add_argument("item", metavar="item", help="The item that "\
            "was traded.")
trade_parser.add_argument("amount", metavar="amount", help="The amount"\
            " that was traded.", type=int)
trade_parser.add_argument("price", metavar="price", help="The total "\
            "price paid for those items.", type=float)
            
register_parser = argparse.ArgumentParser()
register_parser.add_argument("id_number", metavar="id_number", help="The "\
            "id of the trader.")
register_parser.add_argument("nick", metavar="nick", help="The trader's "\
            "eRepublik nick.", nargs="*")
register_parser.add_argument("-n", "--nick", metavar="irc", help="The nick "\
            "in IRC.", nargs=1, dest="irc", default="-")
register_group = register_parser.add_mutually_exclusive_group()
register_group.add_argument("-u", metavar="update", dest="u", const=True,
            default=False, action="store_const", help="Update switch.")
register_group.add_argument("-d", metavar="update", dest="d", const=True,
            default=False, action="store_const", help="Delete switch.")
register_parser.add_argument("-i", "--info", metavar="info", dest="info",
            help="Additional info about the trader.", nargs="+", default="")
register_parser.add_argument("-v", metavar="voice", dest="v", help="Flag "\
            "if trader has voice in #itrade.", const="True", default="False",
            action="store_const")
            
search_parser = argparse.ArgumentParser()
search_parser.add_argument("criteria", metavar="criteria", help="The string to"\
            " search for.", nargs="+")
search_group = search_parser.add_mutually_exclusive_group()
search_group.add_argument("-a", "--alphabetical", help=\
            "Sort the results alphabetically.", action="store_true", dest="a")
search_group.add_argument("-n", "--numerical", help=\
            "Sort the results numerically.", action="store_true", dest="n")
            
find_parser = argparse.ArgumentParser()
find_parser.add_argument("player", help="The player's name to search.", nargs="+")

### All parsers defined
                        
while True:
    print("\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n")
    inp = input(PROMPT).split()
    if inp == []:
        continue
    try:
        data = main_parser.parse_args(inp)
    except SystemExit:
        if "-h" not in data.args:
            print("*** Bad input <{}>".format(inp))
        continue
        
    if data.action == "help":

        print("Please refer to the README.txt and TUTORIAL.txt,\n for a more"\
              " comprehensive explanation.")
        print()
        print("You can also type <command> <-h>\n for help on that command")
        print()
        print("<exit> Exits the system")
        print("<calc> Does basic maths (You lazy ass!)")
        print("<register> Registers a player in the database")
        print("<trade> Logs a trade between you and someone else")
        print("<check> Checks if an ID exists in your database")
        print("<search> Searches for something in your database")
        print("<find> Searches for a player in eRepublik itself")
        print("<convert> Converts some of your profit into CC")
        print("<log> Prints some trades for you")
        print("<print> Prints a player's info (or your own)")
        print("<list> Prints all the players in the database")
        print("<help> Displays this help")
        
    elif data.action == "calc":
        
        if "-h" in data.args:
            print("usage: itrade.py [-h] expression")
            print()
            print("positional arguments:")
            print("  expression    The mathematical expression to be evaluated")
            print()
            print("optional arguments:")
            print("  -h, --help  show this help message and exit")
            continue
        
        try:
            try:
                print(eval("".join(data.args)))
            except SyntaxError:
                print("*** Badly inputed calculation <{}>".format(" ".join(data.args)))
                print("Type <calc -h> for help")
                continue
        except NameError:
            print("*** Unknown character(s)")
            continue
            
    elif data.action == "list":
    
        if data.args != []:
            print("*** Wrong number of arguments for <list>: none allowed")
            continue
        print()
        t = []
        m = 0
        for key in traders.keys():
            t.append((traders[key]["nick"], key))
            if len(traders[key]["nick"]) > m:
                m = len(traders[key]["nick"])
        m += 1
        m2 = len(str(len(t)))+1
        s = "{:<@}. {:<$} : [{}]".replace("@", str(m2)).replace("$", str(m))
        i = 1
        for item in sorted(t):
            print(s.format(i, item[0], item[1]))
            i += 1
        print()
        print("{} traders registered in your database.".format(len(t)))
        
    elif data.action == "exit":

        if "-h" in data.args:
            print("usage: itrade.py [-h]")
            print()
            print("optional arguments:")
            print("  -h, --help            show this help message and exit")
            continue
        
        try:
            SAVE(FILE_TRADERS, traders)
        except Exception:
            print("*** Error when saving file 1 upon exit")
        try:
            SAVE(FILE_INFO, itrade_info)
        except Exception:
            print("*** Error when saving file 2 upon system exit")
        import sys
        sys.exit(0)
        
    elif data.action == "convert":

        if len(data.args) != 2 and "-h" not in data.args:
            print("*** Wrong number of arguments for <convert>: 2 needed")
            print("Type <convert -h> for help")
            continue
        
        try:
            data = convert_parser.parse_args(data.args)
        except SystemExit:
            if "-h" not in data.args:
                print("*** Badly inputed parameters <{}>".format(" ".join(data.args)))
                print("Type <convert -h> for help")
            continue

        try:
            itrade_info["profit"] -= data.cc
            itrade_info["stock"]["gold"] += data.gold
        except KeyError:
            print("*** Data corrupted")
            continue
        
        print("Converted {}cc into {} gold.".format(data.cc, data.gold))
        
    elif data.action == "log":
        
        if len(data.args) > 1 and "-h" not in data.args:
            print("*** Wrong number of arguments for <log>: 1 max")
            print("Type <log -h> for help")
            continue
        
        try:
            data = log_parser.parse_args(data.args)
        except SystemExit:
            if "-h" not in data.args:
                print("*** Badly inputed parameters <{}>".format(" ".join(data.args)))
                print("Type <log -h> for help")
            continue
            
        data.n = data.n.lower()
        if data.n == "all":
            with open(FILE_LOG, "r") as f:
                reads = f.read()
            print(reads)
        else:
            try:
                n = int(data.n)
            except ValueError:
                print("*** N has to be an integer or <all>")
                continue
            with open(FILE_LOG, "r") as f:
                reads = f.read()
            logs = reads.split("Registered ")
            n = -1*n
            if abs(n) >= len(logs):
                print(reads)
            elif n < 0:
                if abs(n) >= len(logs):
                    for log in logs[::-1]:
                        print(log)
                else:
                    for i in range(1, abs(n)+1):
                        print(logs[-i])
            else:
                for i in range(n):
                    print(logs[i])
        
    elif data.action == "search":
    
        if len(data.args) < 1 and "-h" not in data.args:
            print("*** Wrong number of arguments for <search>: 1 minimum")
            print("To check all your traders, use the command <traders>.")
            print("Type <search -h> for help")
            continue
        
        try:
            data = search_parser.parse_args(data.args)
        except SystemExit:
            if "-h" not in data.args:
                print("*** Badly inputed parameters <{}>".format(" ".join(data.args)))
                print("Type <search -h> for help")
            continue
            
        try:
            crit = " ".join(data.criteria).lower()
        except Exception:
            print("*** Badly inputed parameters <{}>".format(" ".join(data.args)))
            print("Type <search -h> for help")
            continue

        match = False
        # do specific search for +v users
        if data.a:
            m = 0
        if crit=="voice":
            if data.a:
                matches = [(traders[key]["nick"], key) for key in
                            traders.keys() if traders[key]["voice"] == "True"]
            else:
                matches = [(key, traders[key]["nick"]) for key in
                            traders.keys() if traders[key]["voice"] == "True"]
        else:
            matches = []
            for key in traders.keys():
                info = key+traders[key]["nick"]+traders[key]["irc"]+traders[key]["info"]
                if crit in info.lower():
                    if data.a:
                        matches.append((traders[key]["nick"], key))
                        if len(traders[key]["nick"]) > m:
                            m = len(traders[key]["nick"])
                    else:
                        matches.append((key, traders[key]["nick"]))
                    
        if matches == []:
            print("No results were found :(")
        else:
            if data.a:
                m += 1
                s = "* match found: {:<$} ({})".replace("$", str(m))
                for tup in sorted(matches):
                    print(s.format(tup[0], tup[1]))
            else:
                for tup in sorted(matches):
                    print("* match found: ({}) {}".format(tup[0], tup[1]))
        
    elif data.action == "print":

        if len(data.args) > 1 and "-h" not in data.args:
            print("*** Wrong number of arguments for <print>: either 0 or 1")
            print("Type <print -h> for help")
            continue
                         
        try:
            data = print_parser.parse_args(data.args)
        except SystemExit:
            if "-h" not in data.args:
                print("*** Badly inputed parameters <{}>".format(" ".join(data.args)))
                print("Type <print -h> for help")
            continue
            
        if data.player != None:
            try:
                int(data.player)
                is_n = True
            except ValueError:
                is_n = False
            if is_n:
                if data.player not in traders.keys():
                    print("*** Unregistered ID")
                    continue
                else:
                    if traders[data.player]["irc"] != "-":
                        irc = "His IRC nick is ".format(traders[data.player]["irc"])
                    else:
                        irc = "He doesn't have an IRC nick"
                    if traders[data.player]["info"] == "":
                        info = "No additional info"
                    else:
                        info = traders[data.player]["info"]
                    if traders[data.player]["voice"] == "True":
                        voice = "He is marked as having voice in #itrade"
                    else:
                        voice = "He isn't marked as having voice in #itrade"
                    s = """Player with id {id} is '{nick}'\n{irc}\n{voice}
{info}""".format(id=data.player, nick=traders[data.player]["nick"],
                 irc=irc, voice=voice, info=info)
                    print(s)
            else:
                print("*** ID must be a (usually 7-digit) number")
        else:
            print("Stocks:")
            for key in itrade_info["stock"]:
                if itrade_info["stock"][key] != 0:
                    print("\t"+items[key]+": "+str(itrade_info["stock"][key]))
            print("Overall profit = {}cc.".format(itrade_info["profit"]))
        
    elif data.action == "check":
        
        if len(data.args) != 1 and "-h" not in data.args:
            print("*** Wrong number of arguments for <check>: only 1 needed")
            print("Type <check -h> for help")
            continue
       
        try:
            data = check_parser.parse_args(data.args)
        except SystemExit:
            if "-h" not in data.args:
                print("*** Badly inputed parameters <{}>".format(" ".join(data.args)))
                print("Type <check -h> for help")
            continue
        
        if data.id_number in traders.keys():
            print("Registered ID: {}".format(traders[data.id_number]["nick"]))
        else:
            print("*** Unregistered ID")
            continue
        
    elif data.action == "trade":
        
        if len(data.args) != 5 and "-h" not in data.args:
            print("*** Wrong number of arguments for <trade>: 5 needed")
            print("Type <check -h> for help")
            continue
        
        try:
            data = trade_parser.parse_args(data.args)
        except SystemExit:
            if "-h" not in data.args:
                print("*** Badly inputed parameters <{}>".format(" ".join(data.args)))
                print("Type <trade -h> for help")
            continue

        try:
            int(data.id_number)
        except ValueError:
            print("*** Invalid ID {}".format(data.id_number))
            continue

        if data.item not in itrade_info["stock"].keys():
            print("*** Unknown item {}".format(data.item))
            continue
        
        if data.transaction == "buy":
            itrade_info["profit"] -= data.price
            itrade_info["stock"][data.item] += data.amount
        else:
            itrade_info["profit"] += data.price
            itrade_info["stock"][data.item] -= data.amount
            if itrade_info["stock"][data.item] <= 0:
                print("*** You are out of stock of "+items[data.item]+" !!")
                print("Your current stock is " + str(itrade_info["stock"][data.item]))

        if data.id_number in traders.keys():
            print("*** Known trader: " + traders[data.id_number]["nick"])
            know = "a registered"
            other = data.id_number + " ("+traders[data.id_number]["nick"]+")"
        else:
            print("*** Unknown trader with id " + data.id_number)
            know = "an unregistered"
            other = data.id_number
            
        s = """Registered transaction between ${my_name}$ and ${other}$ at {time}
    {act} {amount:,g} {item} for the total price of {money:,g}.
    This gives a rate of {r:.3f} / each piece.
    The transaction was made with {know} trader in our database.
    After this, your "{item}" stock is {stock:,g} and you have an overall profit of {profit:,g}cc\n\n""".format(
            act=d[data.transaction][0].capitalize(), amount=data.amount, item=items[data.item],
            r=data.price/data.amount, idn=data.id_number, act2=d[data.transaction][1],
            money=data.price, my_name=itrade_info["name"], stock=itrade_info["stock"][data.item],
            profit=itrade_info["profit"], know=know, time=str(datetime.datetime.now())[:-7], other=other)

        LOG(FILE_LOG, s)
        print(s[:-1])
        SAVE(FILE_INFO, itrade_info)
      
    elif data.action == "register":
        
        args = data.args            
        try:
            data = register_parser.parse_args(data.args)
        except SystemExit:
            if "-h" not in data.args:
                print("*** Badly inputed parameters <{}>".format(" ".join(args)))
                print("Type <register -h> for help")
            continue
            
        try:
            int(data.id_number)
        except Exception:
            print("*** argument <id_number> must be a number")
            print("Type <register -h> for help")
            continue
            
        if data.d:
            if data.id_number in traders.keys():
                del traders[data.id_number]
                SAVE(FILE_TRADERS, traders)
                continue
            else:
                print("*** Unregistered ID to delete")
                continue
        else:
            if data.nick == []:
                print("*** Badly inputed parameters <{}>".format(" ".join(args)))
                print("Type <register -h> for help")
                continue
            
        if data.id_number in traders.keys():
            if data.u:
                traders[data.id_number] = {"nick": " ".join(data.nick), "info": 
                    " ".join(data.info), "irc": " ".join(data.irc), "voice":data.v}
                print("*** ID registered""")
            else:
                print("*** You already registered that ID")
                print("To update use the update switch")
        else:
            traders[data.id_number] = {"nick": " ".join(data.nick), "info": 
                    " ".join(data.info), "irc": " ".join(data.irc), "voice":data.v}
            print("*** ID registered""")
            
        SAVE(FILE_TRADERS, traders)
        
    elif data.action == "find":
    
        if len(data.args) < 1 and "-h" not in data.args:
            print("*** Wrong number of arguments for <find>: minimum 1")
            print("Type <find -h> for help")
            continue
            
        try:
            data = find_parser.parse_args(data.args)
        except SystemExit:
            if "-h" not in data.args:
                print("*** Badly inputed parameters <{}>".format(" ".join(data.args)))
                print("Type <find -h> for help")
            continue
            
        crit = "+".join(data.player)
        print("Connecting to the Internet...")
        try:
            h = str(urllib.request.urlopen("http://www.erepublik.com/en/main/search/?q="+crit).read())
        except Exception:
            print("*** Could not request search")
            continue
        try:
            p = Search_Parser()
            p.feed(h)
            p.close()
        except Exception:
            print("*** Could not parse the retrieved results")
            continue
        data = handle_matches(p.matches)
        if data == {}:
            print("*** 0 results found.")
            print("(This may have happened because the criteria was too general)")
        for key in sorted(data.keys()):
            print("Player ID: {i}, {p} with {exp:,} total exp.".format(p=key, 
                i=data[key]["id"], exp=int(data[key]["exp"])))
            continue
