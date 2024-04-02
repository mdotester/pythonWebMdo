{ ibranch.i5 new }
{ ibranch.i1 new }

DEF VAR var1 AS CHAR.
var1 = OS-GETENV ("var1").

call HLCcfg "set" "/u/pswaix/psw/1a/CFG".

call HLCsocket 'connect' var1.

quit.