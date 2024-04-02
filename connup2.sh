HOME=/u/pswaix
. /u/pswaix/psw/1a/bin/parm.sh

var1=$1
export  var1
pswx.sh /u/pswaix/psw/1a/bin/_prog $db -led 200 200 dmy -p conn-up2.p
#mpro $db -led 200 200 dmy -db $HOME/psw/1a/dbsys/systool -ld toollimit -p romain.p

#_prog $db -le 100 100 -d dmy -db $HOME/cam/1a/db/dblog -p mmain.p -D 200 -yy 1900
