import pickle as p
with open('savegame.bin','rb') as f:
    try:
        while True:
            rec=p.load(f)
            for i in rec:
                print(f'{i}:{rec[i]}')
    except:
        pass