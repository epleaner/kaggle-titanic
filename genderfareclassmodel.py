import csv as csv
import numpy as numpy

csv_file_object = csv.reader(open('csv/train.csv', 'rb'))

header = csv_file_object.next()

data = []
for row in csv_file_object:
    data.append(row)
data = numpy.array(data)

fare_ceiling = 40
data[data[0::, 9].astype(numpy.float) >= fare_ceiling, 9] = fare_ceiling - 1.0

fare_bracket_size = 10
number_of_price_brackets = fare_ceiling / fare_bracket_size

number_of_classes = len(numpy.unique(data[0::, 2]))

survival_table = numpy.zeros((2, number_of_classes, number_of_price_brackets))

for class_ndx in xrange(number_of_classes):
    for price_bracket_ndx in xrange(number_of_price_brackets):

        women_only_stats = data[
            (data[0::, 4] == "female")
            & (data[0::, 2].astype(numpy.float) == class_ndx + 1)
            & (data[0::, 9].astype(numpy.float) >= price_bracket_ndx * fare_bracket_size)
            & (data[0::, 9].astype(numpy.float) < (price_bracket_ndx + 1) * fare_bracket_size)
            , 1]

        men_only_stats = data[
            (data[0::, 4] == "male")
            & (data[0::, 2].astype(numpy.float) == class_ndx + 1)
            & (data[0::, 9].astype(numpy.float) >= price_bracket_ndx * fare_bracket_size)
            & (data[0::, 9].astype(numpy.float) < (price_bracket_ndx + 1) * fare_bracket_size)
            , 1]

        survival_table[0, class_ndx, price_bracket_ndx] = numpy.mean(women_only_stats.astype(numpy.float))
        survival_table[1, class_ndx, price_bracket_ndx] = numpy.mean(men_only_stats.astype(numpy.float))

survival_table[survival_table != survival_table] = 0
survival_table[survival_table < .5] = 0
survival_table[survival_table >= .5] = 1
print survival_table

test_file = open('csv/test.csv', 'rb')
test_file_object = csv.reader(test_file)
header = test_file_object.next()
predictions_file = open('csv/genderclassmodel.csv', 'wb')
p = csv.writer(predictions_file)
p.writerow(['PassengerId', 'Survived'])

for row in test_file_object:

    for price_bracket_ndx in xrange(number_of_price_brackets):

        try:
            row[8] = float(row[8])
        except:
            bin_fare = 3 - float(row[1])
            break

        if row[8] > fare_ceiling:
            bin_fare = number_of_price_brackets - 1
            break

        if row[8] >= price_bracket_ndx * fare_bracket_size\
                & (row[8] < (price_bracket_ndx + 1) * fare_bracket_size):

            bin_fare = price_bracket_ndx
            break

        if row[3] == 'female':
            p.writerow([row[0], int(survival_table[0], float(row[1]) - 1, bin_fare)])
        else:
            p.writerow([row[0], int(survival_table[1], float(row[1]) - 1, bin_fare)])

test_file.close()
predictions_file.close()




