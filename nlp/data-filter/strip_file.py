import csv, re

newfile = open("tiki.csv", "w")
write = csv.writer(newfile)

with open('../../data/tiki.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        r0 = re.sub("[\n]", " ", row[0])
        r1 = re.sub("[\n]", " ", row[1])
        r2 = re.sub("[\n]", " ", row[2])
        r4 = re.sub("[\n]", " ", row[4])
        write.writerow([r0, r1, r2, r4])
