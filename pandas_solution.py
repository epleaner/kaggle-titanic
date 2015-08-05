import pandas as pd
import numpy as np
import csv as csv
csv_file_object = csv.reader(open('csv/train.csv', 'rb'))
header = csv_file_object.next()
data = []

for row in csv_file_object:
    data.append(row)
data = np.array(data)

df = pd.read_csv('csv/train.csv', header = 0)

df['Gender'] = df.Sex.map( {'female': 0, 'male': 1} )
df['EmbarkedInt'] = df.Embarked.map( { 'Q': 0, 'C': 1, 'S': 2})

median_ages = np.zeros((2,3))
median_ages

for i in range(0,2):
    for j in range(0,3):
        median_ages[i,j] = df[(df['Gender'] == i) & \
                             (df['Pclass'] == j + 1)]['Age'].dropna().median()

df['AgeFill'] = df['Age']
for i in range(0,2):
    for j in range(0,3):
        df.loc[ (df.Age.isnull()) & (df.Gender == i) & (df.Pclass == j+1),\
                'AgeFill'] = median_ages[i,j]

print df[ df['Age'].isnull() ][['Gender','Pclass','Age','AgeFill']].head(10)

