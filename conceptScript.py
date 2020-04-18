import pickle
import Concept
with open("concepts.pickle", "rb") as infile:
    concepts = pickle.load(infile)

print([c.fullDesc() for c in concepts]);