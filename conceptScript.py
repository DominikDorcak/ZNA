import pickle
import Concept
with open("concepts.pickle", "rb") as infile:
    concepts = pickle.load(infile)

descfile=open('concepts.txt','w+')
print(len(concepts))

for c in concepts:
    print(c.fullDesc(),file=descfile);