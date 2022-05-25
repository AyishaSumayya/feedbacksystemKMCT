import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import pandas as pd

class placement:
    data = pd.read_csv(r'D:\feedbacksm\feedbacksystem\feedbacksystem\static\newdataset.csv')
    qn=data.values[:,1]
    label=data.values[:,0]
    print(qn)
    print(label)
    xtrain, xtest, ytrain, ytest = train_test_split(qn, label, test_size=0.2, random_state=0)
    vector = TfidfVectorizer(stop_words='english')
    xtrain_vector = vector.fit_transform(xtrain)
    with open("vector.pkl", "wb") as handle:
        pickle.dump(vector, handle, protocol=pickle.HIGHEST_PROTOCOL)
    xtest_vector = vector.transform(xtest)
    rf=RandomForestClassifier()
    rf.fit(xtrain_vector,ytrain)

placement()