import os
import findCity.models City, State

estados = ['ac', 'al', 'am', 'ap', 'ba', 'ce', 'df', 'es', 'go', 'ma', 'mg', 'ms', 'mt', 'pa', 'pb', 'pe', 'pi', 'pr', 'rj', 'rn', 'ro', 'rr', 'rs', 'sc', 'se', 'sp', 'to']

for i, estado in enumerate(estados):
    with open(estado, "r") as f:
        estado_nome = f.readline().rstrip("\n")
        s = State(name=estado_nome, slug=estados[i].upper())
        s.save()

        print(f'\n=========== {estado_nome.upper()} ({estados[i].upper()}) ================')
        for row in f:
            cidade = row.split("\t")[0]
            print(cidade)
            c = City(name=cidade, state=s)
            c.save()
