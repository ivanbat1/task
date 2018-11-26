with open('quotes', 'r+') as f:
    for i in f.readlines():
        g =  i.split()[0].split('/')
        if len(g) == 2:
            print g[0]+g[1]
        else:
            print g[0]