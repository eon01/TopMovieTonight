TopMovieTonight (TMT)
========

A python script that answer an existential question:  Which movie to watch tonight on TV? 

It works with French(CanalSat), Swiss and Belgian TV channels for the moment and uses Kazer.org for XMLTV service.

Don't forget to :
-Set the USERHASH
-Set the TMPDIR (in function of your os)
-Install dependancies

HowTo ?
========

Add your USERHASH to TMT.py 
You can get one here: http://kazer.org/  
You should create an account and you select the channels here http://kazer.org/my-channels.html
Downloading the zip file, parsing IMDB and sorting the list of dits, takes a long time, so choose only necessary channels.
Save your choice and run the script with your USERHASH. 
TMPDIR by default is /tmp/, just change it to whatever you want according to your OS, or just keep it if you're using *nix system.

WantToClone?
========

git clone https://github.com/eon01/TopMovieTonight.git


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/eon01/topmovietonight/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

