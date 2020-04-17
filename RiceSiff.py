import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler as Scaler
import pickle

# citanie dat z csv suboru
from Concept import Concept


def getData():
    student_mat = pd.read_csv("student-alcohol-consumption/student-mat.csv")
    return student_mat


# ------------------------------------------------------------------------------------------------------------------------
# pomocne transformacne funkcie
def school_to_numeric(X):
    if X == "GP":
        return 1
    else:
        return 0


def sex_to_numeric(X):
    if X == "M":
        return 1
    else:
        return 0


def address_to_numeric(X):
    if X == "U":
        return 1
    else:
        return 0


def famsize_to_numeric(X):
    if X == "GT3":
        return 1
    else:
        return 0


def Pstatus_to_numeric(X):
    if X == "T":
        return 1
    else:
        return 0


def job_to_numeric(X):
    if X == "teacher":
        return 0
    if X == "health":
        return 1
    if X == "services":
        return 2
    if X == "at_home":
        return 3
    if X == "other":
        return 4


def reason_to_numeric(X):
    if X == "home":
        return 0
    if X == "reputation":
        return 1
    if X == "course":
        return 2
    if X == "other":
        return 3


def guardian_to_numeric(X):
    if X == "mother":
        return 0
    if X == "father":
        return 1
    if X == "other":
        return 2


def yesno_to_numeric(X):
    if X == "yes":
        return 1
    else:
        return 0


# ------------------------------------------------------------------------------------------------------------------------


def getPreparedData():
    data = getData()
    attributes = data.columns
    # transformacia kategorickych parametrov na celociselne
    data['school'] = data['school'].apply(school_to_numeric)
    data['sex'] = data['sex'].apply(sex_to_numeric)
    data['address'] = data['address'].apply(address_to_numeric)
    data['famsize'] = data['famsize'].apply(famsize_to_numeric)
    data['Pstatus'] = data['Pstatus'].apply(Pstatus_to_numeric)
    data['Mjob'] = data['Mjob'].apply(job_to_numeric)
    data['Fjob'] = data['Fjob'].apply(job_to_numeric)
    data['reason'] = data['reason'].apply(reason_to_numeric)
    data['guardian'] = data['guardian'].apply(guardian_to_numeric)
    data['schoolsup'] = data['schoolsup'].apply(yesno_to_numeric)
    data['famsup'] = data['famsup'].apply(yesno_to_numeric)
    data['paid'] = data['paid'].apply(yesno_to_numeric)
    data['activities'] = data['activities'].apply(yesno_to_numeric)
    data['nursery'] = data['nursery'].apply(yesno_to_numeric)
    data['higher'] = data['higher'].apply(yesno_to_numeric)
    data['internet'] = data['internet'].apply(yesno_to_numeric)
    data['romantic'] = data['romantic'].apply(yesno_to_numeric)

    # transformacia vsetkych dat do intervalu [0,1]
    scaler = Scaler(feature_range=(0, 1)).fit(data)
    data = pd.DataFrame(scaler.transform(data), columns=attributes)
    return np.array(data)


class Ricesiff:

    def __init__(self, data):
        self.I = np.array(data)
        self.X = list(range(self.I.shape[0]))
        self.Y = list(range(self.I.shape[1]))

    def arrowUp(self,A):
        result = [None]*len(self.Y)
        for y in self.Y:
            minimum = 2
            for x in A:
                if self.I[x][y]<minimum:
                    minimum = self.I[x][y]
            result[y] = minimum
        return result

    def arrowDown(self,B):
        result = []
        for x in self.X:
            islower = False
            for y in self.Y:
                if self.I[x][y] < B[y]:
                    islower = True
            if not islower:
                result.append(x)
        return result

    def dist(self,X1,X2):
        sumin = sum([min(X1.intent[y],X2.intent[y]) for y in self.Y])
        sumax = sum([max(X1.intent[y],X2.intent[y]) for y in self.Y])
        return (1.0 - (sumin/sumax))


    def getMin(self,D):
        minimum = 2
        for x1 in D:
            for x2 in D:
                d = self.dist(x1,x2)
                if (not(d==0)) and (d < minimum):
                     minimum = d
        return minimum

    def getE(self,D,m):
        result = set()
        for x1 in D:
            for x2 in D:
                if self.dist(x1,x2) == m:
                    result.add((x1,x2))
        return result

    def getV(self,D,E):
        result = set()
        for x in D:
            for y in D:
                if (x,y) in E:
                    result.add(x)
        return result

    def getN(self,E):
        result = set()
        for (x1,x2) in E:
            un = x1.extent.union(x2.extent)
            toadd = Concept(self.arrowUp(un),self.arrowDown(self.arrowUp(un)))
            result.add(toadd)
        return result



    def RSALG(self):
        C = set()
        D = set()
        for x in self.X:
            elem = Concept(self.arrowUp([x]),self.arrowDown(self.arrowUp([x])))
            C.add(elem)
            D.add(elem)

        print("uvodna dlzka C:", len(C))
        print("uvodna dlzka D:", len(D))
        print([str(c) for c in C])

        i =0;
        while(len(D)>1):
            i+=1;
            print("iteracia: ",i)
            m = self.getMin(D)
            print("min: ",m)
            E = self.getE(D,m)
            print("E: ", [(str(c),str(c2)) for (c,c2) in E])
            V = self.getV(D,E)
            print("V: ", [str(c) for c in V])
            N = self.getN(E)
            print("N: ", [str(c) for c in N])
            D = D.difference(V).union(N)
            print("dlzka D:",len(D))
            C = C.union(N)
            print("dlzka C:",len(C))
        return C





rs = Ricesiff(getPreparedData());
concepts = rs.RSALG()
with open("concepts.pickle","wb") as out:
    pickle.dump(concepts,out)

print([str(c) for c in concepts])
