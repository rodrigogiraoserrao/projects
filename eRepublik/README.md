Small tool for a game I play;

Coded by Rojer97
Any problem, PM me in-eRepublik at:
http://www.erepublik.com/en/citizen/profile/6328829
or e-mail me at: ptarasmahalas@gmail.com
(not my personal email, so it may take a while to answer. An in-game PM is the fastest way to communicate)

You can check the most recent code on GitHub: https://github.com/RojerGS/eRepublik/tree/master

===ABOUT ME===

This project is free to edit, distribute, share, adapt, etc, etc. People are only asked to give proper
credit to the creators. Also, anyone who would like to support this project can:
	if it is an eRepublik player:
		donate any amount of gold or CC and address me a PM saying it is for the iTrader;
		(donate here http://www.erepublik.com/en/citizen/profile/6328829)
	if you're not an eRepublik player:
		registering under this link: http://www.erepublik.com/en/referrer/Rojer97
		and reaching at least level 10 ;) If you like, you can always play more!
	for both:
		go to github if you have an account, and star my repo: https://github.com/RojerGS/eRepublik/tree/master

		
WARNING: changing the name of the executable will make it stop working!

===HOW TO SETUP===

There is actually nothing to setup!
You just have to unzip the downloaded folder
And run the executable 'itrader.exe'.
It will say it couldn't load any data... Don't worry!
It will understand it is your first time, and it will ask for your name, just that.
Type in your name! It will say that no data was loaded... Don't worry :P It is ready to be used though.

The program will create 3 files. You can read them, but it is not advisable to edit them since you could be
messing up with the data. User-corrupted data is not from the responsibility of the coders and is not considered
as a bug. In those cases, deleting all the files is advised.

The built-in help system is not the best, but it works! There is also a file TUTORIAL.txt with commands for you
 to type, so you can understand better how all works.
For now, just stick with the tutorial below!


===COMMANDS===

NOTE: whenever talking about commands, the syntax will be:
<command_name> <argument> <argument> ...
	You don't actually have to type those '<>'.
	The '|' symbol denotes an option. So <buy|sell> means either type
<buy>, or type <sell>
	A <?> after a command means it is optional.
	Characters that you write starting with <->, like <-h> are ALWAYS
optional.

First, let's list all the commands available:

	1. exit
	2. help
	3. trade
	4. register
	5. calc
	6. print
	7. check
	8. search
	9. log
	10. convert
	
The first two commands are pretty straightforward.
	<exit> is the preferred way to close the program.
	<help> displays the help for the program (to be improved)
	
	If you type either <-h> or <command> <-h> you get a more specific
help on either the general program, or a specific command

3. trade
Used to log a trade between you and another player.
Use it like:
<trade> <buy|sell> <id> <item> <amount> <price>

<buy|sell> distinguishes if you were buying or selling.
Use <buy> when you bought, use <sell> when you sold.

<id> is the id of the player with whom you traded. The iTrader
keeps track of the IDs, not the nicknames!

<item> is the item you traded. Doesn't matter if you bought or sold.
One of you sent CC, the other an item. Type the item here.
	NOTE: For weapon raw material use <wrm> and for food raw material
use <frm>.
		For weapons use <wqX> and for food use <fqX> where <X> is the
quality of the food you bought.

<amount> The total amount traded.

<price> The CC traded.

After using <trade> the information about the trade will be automatically
logged into the file and printed for you to check.


4. register
Used to register a player in your database, to link it to an ingame nick,
an IRC nick and some information you choose.
Use it like:
<register> <id> <nick> <-u> <-i> <-n> <-v>

<id> is the in-game ID of the player to be registered
<nick> is the in-game nick
Use the flag <-u> if you are not registering a new one, but updating
information. When <-u> is used, you have to type everything you want to
be there. Otherwise the old data is just overriden.
<-i> Use this flag to add information about the player.
Do it like so: <-i some stuff you type bla bla bla>
<-n> Use it to store an IRC nick
Do it like so: <-n IRC nick>
<-v> Use it to flag if the user has voice or more in #itrade
Doesn't take anything after. Just <-v>


5. calc
Used to make mathematical calculations, like check total prices
Use it like so:
<calc> <expression>
<expression> doesn't care about whitespace. Writing:
<45*5435+5> is exactly the same as writing:
<    45   *             5435+     5>
The mathematical operators used are +*-/^()


6. print
Use it to print someone's information
Use it like so:
<print> <id>?
Omitting the ID will only print information about you, that is,
your stocks and your current profit.
If the id is not in your database, you will be warned.
NOTE: print doesn't work with nicks!


7. check
Used to check if a given ID is already in your database
Usage:
<check> <id>


8. search
Used to search for something in your database.
Use it like so:
<search> <search parameters>
The <search parameters> can be anything from some characters to an id
If anything in your database matches the parameters, it will be printed
NOTE: a search for "ab" will match against, for example, "aberration"


9. log
Used to print the most recent trades
Usage:
<log> <X>?
If X is omitted, the latest 5 transactions are omitted
NOTE: All trades are logged with a timestamp (from when the trade was
registered) so be aware of that when reading the logs.
If X is greater than 0, the latest X trades are printed
If X is smaller than 0, the first X trades are printed
You can also use <all> instead of a number, that will print ALL trades
in the database. If your database is big, not recommended.


10. convert
Used when you use your profit to buy gold
Use it like so: <convert> <gold> <cc>
<gold> is the amount of gold you bought
<cc> is the amount of CC you spent doing it

Using an unknown command doesn't hurt the program.
Backing up the data files from time to time is recommended.
