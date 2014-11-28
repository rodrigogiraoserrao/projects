projects
========

This GitHub repo is supposed to hold every single script/project that I develop and reaches a stage where it works.

Everyone is welcome to fork this repo and use it.
Any snippet of code, line of code or entire file, present in this repo, in its branches, in its forks,
or in any other place that aknowledges that it is from here is hereby referred to as "RojerGS projects' code"
You are allowed to distribute, use, modify and run RojerGS projects' code.
You are not allowed to sell or make any kind of profit with any piece of RojerGS projects' code.
You are not allowed to present any piece of RojerGS projects' code as your own's.
When using RojerGS projects' code, you are required to refer back to this repo and give credit to RojerGS.

Contributions/suggestions are much appreciated!

program rodrigo_rules;
const
	SIZE = 10;
	
type
	myArray = array [1..SIZE] of integer;
	
var
	a, b: myArray;
	i, j, count, temp: integer;
	inp: string;
	rand, found: boolean;
	
begin
	writeln('quer que o programa gira os 10 números (vezes 2) aleatoriamente');
	inp := 'l';
	while (upcase(inp[1]) <> 'S') and (upcase(inp[1]) <> 'N') do
	begin
	write('[S]im/[N]ão >> '); readln(inp);
	end;
	rand := upcase(inp[1]) = 'S';
	if rand then
	begin
		for i:=1 to SIZE do
		begin
			a[i] := random(100);
			b[i] := random(100);
		end;
	end
	else
	begin 
		for i:=1 to SIZE do
		begin
			writeln('input do a[',i,']');
		     readln(a[i]);
		end;
		for i:=1 to SIZE do
		begin
			writeln('input do b[',i,']');
		     readln(b[i]);
		end;
	end;
	count := 0;
	for i:=1 to SIZE do
	begin
		found := false;
		for j:=1 to SIZE do
		begin
			if (not found) and (a[i] = b[j]) then
			begin
				found := true;
				count := count + 1;
			end;
		end;
	end;	
	writeln('No array A há ', count, ' elementos que se encontram em B');
	for i:=2 to SIZE do
	begin
		j := i;
		while (j>1) and (a[j] < a[j-1]) do
		begin
			temp := a[j];
			a[j] := a[j-1];
			a[j-1] := temp;
			j := j-1;
		end;
	end;
	for i:=2 to SIZE do
	begin
		j := i;
		while (j>1) and (b[j] < b[j-1]) do
		begin
			temp := b[j];
			b[j] := b[j-1];
			b[j-1] := temp;
			j := j-1;
		end;
	end;
	writeln('o Array A ordenado:');
	for i:=1 to SIZE do
		write(a[i], '; ');
	writeln('');
	writeln('o Array B ordenado:');	
	for i:=1 to SIZE do
		write(b[i], '; ');	
end.
