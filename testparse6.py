import os
from xml.etree import cElementTree as ET
import csv
import math

file_name = 'mongo1.xml'
full_file = os.path.abspath(os.path.join('data', file_name))
# csvfile="C://Users/JG31348/Documents/htmltesting2/data/test20.csv"
csvfile2="C://Users/JG31348/Documents/htmltesting2/data/test141.csv"
branch_name = 'mongo-master'

dom = ET.parse(full_file)

partition = dom.find('Partition/Partition')
start1 = 'Users.Grant.Downloads.darktable-master.'
start2 = 'C:\\Users\\JG31348\\Downloads\\darktable-master\\darktable-master\\'
langnum = input('What language?: ')

n =0 #for the checking of the folders
m=0 #for the rows
l=0 #for th ecolumns
folders = []
for p in partition:
    try:
        folders.append(p.attrib['name'])
    except KeyError:
        name = False
finalpart1=[]
for f in folders:
    f=f.replace(start1,start2)
    temp=f.split('.')
    temp1=''
    for t in temp:
        temp1+='\\'+t
    temp1=temp1[1:]
    finalpart1.append(temp1)
folders=finalpart1
#print (folders)
# folders.append('ignore')

partition2 = dom.findall('Partition/Partition/Partition/Partition/Partition')
subfold = []
for p2 in partition2:
    if p2.attrib['name'].endswith('.h')==False and p2.attrib['name'].endswith('.c')==False and p2.attrib['name'].endswith('.cpp')==False:
        subfold.append(p2.attrib['name'])
finalpart1=[]
for f in subfold:
    f=f.replace(start1,start2)
    temp=f.split('.')
    temp1=''
    for t in temp:
        temp1+='\\'+t
    temp1=temp1[1:]
    finalpart1.append(temp1)
subfold=finalpart1
print (subfold)
# subfold.append('ignore')

lst = dom.iter()
final = []
for p1 in lst:
    try:
        if((p1.attrib['name'].endswith('.h')==True or p1.attrib['name'].endswith('.c')==True or p1.attrib['name'].endswith('.cpp')==True or p1.attrib['name'].endswith('.hpp')==True) ):
            final.append(p1.attrib['name'])
    except KeyError:
        name =False
finalpart1=[]
for f in final:
    f=f.replace(start1,start2)
    temp=f.split('.')
    temp1=''
    if f.endswith('.h')==False and f.endswith('.c')==False and f.endswith('.cpp')==False:
        for t in temp:
            if t=='*':
                do=False
            else:
                temp1+='\\'+t
    else:
        for t in temp:
            if t=='*':
                do=False
            elif t == temp[len(temp)-1]:
                temp1+='.'+t
            else:
                temp1+='\\'+t
    temp1=temp1[1:]
    finalpart1.append(temp1)
final=finalpart1

# save the values of the partitions (inc highest overall folders)
# save as [ [ part1 start, part1 end]...]
partitionloc =[]
tree =ET.ElementTree(file= file_name)
root = tree.getroot()
n=0
temp=0
finalpart=[]
for elem in tree.iter(tag='Partition'):
    finalpart.append(elem.attrib['name'])

finalpart1=[]
for f in finalpart:
    f=f.replace(start1,start2)
    temp=f.split('.')
    temp1=''
    if f.endswith('.h')==False and f.endswith('.c')==False and f.endswith('.cpp')==False:
        for t in temp:
            if t=='*':
                do=False
            else:
                temp1+='\\'+t
    else:
        for t in temp:
            if t=='*':
                do=False
            elif t == temp[len(temp)-1]:
                temp1+='.'+t
            else:
                temp1+='\\'+t
    temp1=temp1[1:]
    finalpart1.append(temp1)
finalpart=finalpart1

for f in finalpart:
    if f.endswith('.h')==False and f.endswith('.c')==False and f.endswith('.cpp')==False:
        try:
            if finalpart[n+1].endswith('.h')==True or finalpart[n+1].endswith('.c')==True or finalpart[n+1].endswith('.cpp')==True or finalpart[n+1].endswith('.hpp')==True:
                    temp=finalpart[n+1]
        except IndexError:
            print(temp, f)
    else:
        try:
            if finalpart[n+1].endswith('.h')==False and finalpart[n+1].endswith('.c')==False and finalpart[n+1].endswith('.cpp')==False and finalpart[n+1].endswith('.hpp')==False:
                partitionloc.append([temp,f])
        except IndexError:
            partitionloc.append([temp,f])
    n+=1

# index values from the beginnign and end of partition so end-beg +1 =filecount
# save as [ [part 1 filecount]...]
filecounts = []
for f in partitionloc:
    filecounts.append(final.index(f[1])-final.index(f[0])+1)

cext=['c','h','cc','cpp','cxx','hh','hpp','hxx','inl','C','H']
javaext=['java']
phpext=['php']
pyext=['py']
jsext=['js']
obcext=['m','mm']
# find dep of highest level partitions (should be the first couple of partitions)
# save as [ [part 1 dep]]
lastlayer = subfold[1]
lastlayerind = finalpart.index(lastlayer)
print(lastlayerind)
foldnames=[]
foldnames1=[]
foldnames2 =[]
foldnames3=[]
folddepext=[]
if langnum=='c':
    ext = cext
elif langnum=='java':
    ext = javaext
for i in range (0, lastlayerind):
    temp=0
    for c in ext:
        if finalpart[i].endswith(c)==False:
            temp+=0
        elif finalpart[i].endswith(c)==True:
            temp+=1
    if temp==0:
        foldnames.append(finalpart[i])
    else:
        foldnames2.append(finalpart[i])

for f in foldnames:
    temp = f.split('.')
    temp1=''
    for k in temp:
        # if temp.index(k) < len(temp)-1:
        temp1 = temp1+ '\\'+k
        # else:
        #     temp1 =temp1+'.'+k
    temp1=temp1[1:]
    foldnames1.append(temp1)
foldnames1=foldnames

for f in foldnames2:
    temp = f.split('.')
    temp1=''
    for k in temp:
        if temp.index(k) < len(temp)-1:
            temp1 = temp1+ '\\'+k
        else:
            temp1 =temp1+'.'+k
    temp1=temp1[1:]
    foldnames3.append(temp1.replace('Users\\Grant\\Downloads','C:\\Users\\JG31348\\Downloads\\'+branch_name))

print(foldnames3)
filedep = []
foldnames4=[]
low = len(foldnames1[0].split('\\'))
# temploc= foldnames.index(subfold[1])
# lowest = len(foldnames[temploc].split('\\'))-1
# for i in range(0,temploc):
#     if(len(foldnames[i].split('\\'))==len(foldnames[temploc].split('\\'))):
#         foldnames4.append(foldnames1[i])
#     elif(len(foldnames[i].split('\\'))==len(foldnames[temploc].split('\\'))+1 and foldnames[i].split('\\')[-1]=='*'):
#         foldnames4.append(foldnames1[i])
# for f in foldnames4:
#     temp=f.split('\\')
#     folddepext.append(temp[lowest])
# end = foldnames2.index(subfold[1])
for f in partitionloc:
    tempdep=0
    temp = f[0].replace('Users\\Grant\\Downloads','C:\\Users\\JG31348\\Downloads\\'+branch_name)
    temp1 = f[1].replace('Users\\Grant\\Downloads','C:\\Users\\JG31348\\Downloads\\'+branch_name)
    if temp in foldnames3:
        tempclass1=[]
        for i in range(foldnames3.index(temp),foldnames3.index(temp1)+1):
            print(i)
            with open(csvfile2,newline='') as csvfile1:
                spamreader=csv.reader(csvfile1,delimiter=",",quotechar='|')
                for k in spamreader:
                    if (k[0]==foldnames3[i] and k[1] not in foldnames3):
                        try:
                            tempclass1.index(k[1])
                        except ValueError:
                            tempclass1.append(k[1])
                            tempdep+=1
                    if(k[1]==foldnames3[i] and k[0] not in foldnames3):
                        try:
                            tempclass1.index(k[0])
                        except ValueError:
                            tempclass1.append(k[0])
                            tempdep+=1
    filedep.append(tempdep)

print(filecounts, filedep)
sum = 0
total=0
totalllf=0
n=0
for f in filecounts:
    total+=f
for f in filedep:
    if(f==0):
        totalllf+=filecounts[n]
    else:
        do=False
    n+=1
n=0
print(total,totalllf)
for f in filecounts:
    if(f>5): #for the "cognitive penalty"
        sum+=((f/total)*((math.log(f)/math.log(5))**-1))*(1-(filedep[n]/totalllf)) #checked against excel and handwritted math
    else:
        sum+=(f/total)*(1-(filedep[n]/totalllf))
    n+=1
print(sum)


# with open(csvfile, "w") as output:
#     writer = csv.writer(output, lineterminator='\n')
#     for val in final:
#         writer.writerow([val])
