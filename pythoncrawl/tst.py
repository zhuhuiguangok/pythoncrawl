import re
s="dsadasdasd1sdasdasdas12325343sdasfas"
p=re.compile('[0-9][\d]+', re.IGNORECASE)
phone=re.findall(p,s)
biaoji=1
for cha in phone:
    if cha=="":
        biaoji=1
    else:
        biaoji=0
    if biaoji:
        biaoji=1
        cha="无"
        print(cha)
    else:
        biaoji=0
        print(cha)
