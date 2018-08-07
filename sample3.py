import csv
import math
import time
import openpyxl


dest = "C:/Users/JG31348/Documents/DLmetric.xlsx"
# wb = openpyxl.load_workbook(filename = dest)
# ws=wb.active
gnum = 1

#This method is used to find the maxlength of the longest file directory
#This variable is used in a for loop in order to find where the first discrepency is, savedvl is passed as a benchmark directory address
def findLen(csvfile):
    with open(csvfile,newline='') as csvfile1: #python code to open csv file
        spamreader=csv.reader(csvfile1,delimiter=",",quotechar='|') #parse into spamreader, repeated because spamreader doesnt like to be called twice
        maxlen=0;
        for row in spamreader:
            savedval=row[0] #this is just a reference value
            part=row[0].split("\\") #splits into an array with every string between the \
            if(maxlen<len(part)):
                maxlen = len(part) #finds the longest length for the for loop in the next method
        findLow(savedval,maxlen,csvfile)

#This method finds the first discrepency
#This discrepency will determine where the layers are, to find the lowest layer, passing the location of the discrepency
#The average entry looks like C:\Users\JG31348\Downloads\nginx-master\nginx-master\src\event\ngx_event.h
#the first place nginx deviates is after src, so these would be the different possible layers
def findLow(savedval,maxlen,csvfile):
    minval=10000
    with open(csvfile,newline='') as csvfile1:
        spamreader=csv.reader(csvfile1,delimiter=",",quotechar='|')
        for row in spamreader:
            for i in range(0,maxlen): #this for loop iterates through each part of the split
                try:
                    part = savedval.split("\\")[i] #iterates through reference value
                    newpart=row[0].split("\\")[i] #iterates through each row in the set
                    if (part!=newpart and minval>i):  #if the part is different in the same spot
                        minval=i
                except(IndexError): #since not all strings are the same length, the error is not important because the deviation will be before the end
                    nothing=True
        if (minval==0):
            for i in range(0,100): #this is just a spam message in the command line in case the header wasnt deleted
                print("STOP AND CHECK YOUR HEADER IN THE CSV FILE. SOMETHING IS WRONG")
        findNext(minval,csvfile)

#This method finds the names of the folders where the layers differ
def findNext(minval,csvfile):
    nextval=[]
    with open(csvfile,newline='') as csvfile1:
        spamreader=csv.reader(csvfile1,delimiter=",",quotechar='|')
        for row in spamreader: #this for loop stores all the possible folders
            try:
                nextval.index(row[0].split("\\")[minval])
            except(ValueError):
                nextval.append(row[0].split("\\")[minval])
        countDepOn(minval,nextval,csvfile)

#This method counts the number of dependencies on and on by each class
#Also, this method calculates the amount of dependencies on each class
def countDepOn(minval,nextval,csvfile):
    counto=[] #counts dependencies on other files
    countob=[] #counts the # of occurrencesof dep on by other files
    countarro=[] #counts the number of unique files each folder depends on
    countarrob=[]
    bestlen=[]
    for n in nextval: #creates the lists, list of lists
        counto.append(0)
        countob.append(0)
        countarro.append([])
        countarrob.append([])
    with open(csvfile,newline='') as csvfile1:
        spamreader=csv.reader(csvfile1,delimiter=",",quotechar='|')
        for row in spamreader: #n^2, i know. iterates through each row and checks each potential value
            for n in nextval:
                if(n==row[0].split("\\")[minval]): #if the value in the same place is the same, row[0] is source
                    try:
                        countob[nextval.index(row[1].split("\\")[minval])]+=1 #if the value is already entered, add 1
                    except (ValueError):
                        countob.append(1) #if not, add to the arrays. the place in countob
                        nextval.append(row[1].split("\\")[minval])
                        countarrob.append([])
                    try:
                        countarrob[nextval.index(row[1].split("\\")[minval])].index(row[0].split("\\")[minval])
                    except (ValueError):
                        countarrob[nextval.index(row[1].split("\\")[minval])].append(row[0].split("\\")[minval])
                elif(n==row[1].split("\\")[minval]): #row[1] is target
                    counto[nextval.index(row[0].split("\\")[minval])]+=1
                    try:
                        countarro[nextval.index(row[0].split("\\")[minval])].index(row[1].split("\\")[minval])
                    except (ValueError):
                        countarro[nextval.index(row[0].split("\\")[minval])].append(row[1].split("\\")[minval])
        while(len(countarro)!=len(countarrob)): #to balance (error fix for one of the files)
            countarro.append([])
            counto.append(0)

    # The code below is to find the highest level layer, not confirmed
        t1=0
        temp1=[]
        temp=[]
        max=0
        for c in countarrob:
            if len(c)<2:
                temp1.append(t1)
                if len(countarro[t1])>max:
                    max=len(countarro[t1])
            t1+=1
        for t in temp1:
            if len(countarro[t])==max:
                temp.append(t)
        if len(temp)==0:
            max=0
            for c in countarro:
                if len(c)>max:
                    max=len(c)
            t=0
            for c in countarro:
                if len(c)==max:
                    temp.append(t)
                t+=1


    # #this section of code is to get the lowest layer of the system
    #     #comparing each project I have done to Lattix and their layer division, it has proved to be right 90-95% of the time
    #     #look at the dependencies graph in understand, generally to the right.
    #     temp=[]
    #     temp1=[]
    #     t=0
    #     for d in countarro:
    #         if(len(d)<2): #if the folder depends on less than 2 other folders, it's possible that it could be the undisputed lowest layer. 2 because it could be itself or not (0 or 1)
    #             temp.append(t)
    #         t+=1
    #     # print (temp)
    #     for k in temp:
    #         if(len(countarro[k])<len(countarrob[k])): #for these folders, make sure that the dependencies on by other folders is greater, so this eliminates the case where
    #             temp1.append(k)
    #     # print(temp1)
    #     for k in temp1: #this part is to eliminate single dir line folders, optimally, the lowest layer wouldn't have any dpenedencies coming out of it, but these programs aren't written well. 2 way deps are allowed
    #         z1=0
    #         for n in countarrob[k]: #for each folder that the folder depends on by
    #             next = nextval.index(n)
    #             for l in countarro[k]: #for each folder that this folder depends on
    #                 if l not in countarrob[next]: #if this folder is not in dep on by (aka it is a single direction line where the selected file dep on a file (not the lowest layer))
    #                     temp1=[]
    #         z = nextval[k]
    #         for n in countarro:
    #             if z in n:
    #                 z1+=1
    #         if(z1<3): #this if statement resets the var if the folder selected has less than 3 dep on it, so cases where theres one stray folder that only has dep on it from 1-2 classes
    #             temp1=[] #(and no dependencies from it bc it only provides little info to one class) but isnt the lowest layer are removed (see 147)
    #     # print(temp1)
    #     t=0
    #     high=0
    #     prev=1000000
    #     highest =0
    #     z=0
    #     temp2=[]
    #     if(len(temp1)==0): #if the above code has not selected the lowest layer
    #         while (True):
    #             if(len(temp1)==0):
    #                 for c in countarrob:
    #                     if(len(c)>high and len(c)<prev): #calculate the highestnumber of dep on by to try first. make sure it's lower than the last one so it doesn't continually test the same var
    #                         high=len(c)
    #                 for i in countarrob:
    #                     # try:
    #                     if(len(i)==high and len(countarrob[t])>len(countarro[t])): #find the folder with the highest num of dep on by other folders (calc above) and make sure there are more dep on by than dep on
    #                         # print(countarrob[t],countarro[t]) #the second half is to automatically filter options that have more dep on because these will not be the lowest layer
    #                         temp1.append(t)
    #                         # print(temp1,nextval[temp1[0]])
    #                         if(high>highest):
    #                             highest=high #store this variable in case every folder fails in order to throw out all these rules and use max num of dep to calc DL
    #                     t+=1
    #                     # except(IndexError): #just in case
    #                     #     do=False
    #             # if(len(temp1)==0):
    #             #     prev=high #if the if statement above failed, check the next highest num of dep
    #             # print(temp1)
    #             # time.sleep(1)
    #             for k in temp1:
    #                 for n in countarro[k]:
    #                     if n not in countarrob[k]: #single dir line test again
    #                         # temp2.append(k)
    #                         temp1=[]
    #                         prev=high
    #             # for t in temp1:
    #             #     if t not in temp2:
    #             #         temp.append(t)
    #             # if len(temp)>0:
    #             #     temp1=temp
    #             if(len(temp1)): #since the val in temp1 would be not null if it passed the other requirements ### was prev != high if this fails
    #                 break
    #             if(z>100): #break the while if there is no solution in the folders to prevent from a continuous loop
    #                 t=0
    #                 for c in countarrob:
    #                     if(len(c)==highest): #uses the folders with the most number of files dep on by other folders
    #                         temp1.append(t)
    #                     t+=1
    #                 break
    #             high=0
    #             t=0
    #             z+=1
    #             # print(temp1)
    #     # print(temp1)
    #     if(len(temp1)==len(countarrob)): #this code is just for if the code has 2-3 folders and they're connecte both ways, without a clear lower layer. Makes it so the lowest layer has the most dep on by the other
    #         temp1=[]
    #         high=0
    #         for n in countob:
    #             if(n>high):
    #                 high=n
    #         t=0
    #         for n in countob:
    #             if(high==n):
    #                 temp1.append(t)
    #             t+=1
    #     temp=[]
    #     temp=temp1

        calcDL1(nextval,temp,countob,minval,csvfile)

def calcDL1(nextval,finalval,countob,minval,csvfile):
    with open(csvfile,newline='') as csvfile1:
        spamreader=csv.reader(csvfile1,delimiter=",",quotechar='|')
        total=countuniq(csvfile)
        count=[]
        countm=[]
        currentclass=0
        currentfold=0
        tempcount=0
        tempdep=0
        currentnext=0
        finalval1=[]
        sum=0
        countllf=0
        cycle=True
        currentstringstart=0
        listoffolders=[]
        countmcount=0
        countcount=0
        name1=[]
        for f in range(0,len(finalval)): #makes the numerical index of the upper layer into a string to compare
             finalval1.append(nextval[finalval[f]])
        for row in spamreader: #below makes sure that every possible node is in the name list
            try:
                name1.index(row[0])
            except(ValueError):
                name1.append(row[0])
            try:
                name1.index(row[1])
            except(ValueError):
                name1.append(row[1]) #this makes it so each file is included and not in multiple times
        for row in name1:
            temprow= row.split("\\") #this for loop takes the file name apart, and takes out the class so the filecount per folder can be grouped
            ee=0
            for t in temprow:
                if(ee==0):
                    tempstringstart=t
                    ee+=1
                elif(ee!=len(temprow)-1):
                    tempstringstart=tempstringstart+"\\"+t
                    ee+=1
            tempsource=row.split("\\")
            try: #listoffolders is organized [name of folder, filecount,name,count...]
                tempnum = listoffolders.index(tempstringstart) #try finding the value and adding 1 to folder count
                listoffolders[tempnum+1]+=1
            except(ValueError):
                listoffolders.append(tempstringstart)
                listoffolders.append(1)
        #we now have the filecount for all the files and the "modules" or dolders the6yre if __name__ == '__main__':
            #now we need to know the number of dependencies in the upper layer
        sum=0
        #print("NEXT")
        countm2=[]
        countllf =countllf1(finalval,nextval,minval,csvfile)
        g=0
        for l in listoffolders:
            #print(g) #can delete, shows progress
            if(g %2==0 or g==0): #since the name is every even number, only do this in that case
                tempcount=listoffolders[g+1] #the count is stored immediately after
                with open(csvfile,newline='') as csvfile1:
                    spamreader=csv.reader(csvfile1,delimiter=",",quotechar='|')
                    tempdep=0
                    m= l.split("\\")
                    compfold=m[len(m)-1] #in the list, the folder is the last in the list
                    compb4=m[len(m)-2] #just to make sure in case there are 2 "util" folders that we only include the right one
                    try:
                        if(m[minval] in finalval1):#if we need to know the dependencies(we do)
                            tempclass1=[]
                            for k in spamreader:
                                temp = k[1].split("\\")
                                temp1= k[0].split("\\")
                                if (compfold==temp[len(temp)-2] and compb4==temp[len(temp)-3] and ((k[0].split("\\")[minval] not in finalval1)==True)):#if the file is a source file and part of the same folder
                                    tempclass=temp1[len(temp1)-1]
                                    try:
                                        tempclass1.index(k[0])
                                    except ValueError:
                                        tempclass1.append(k[0])
                                        tempdep+=1
                                if(compfold==temp1[len(temp1)-2] and compb4==temp1[len(temp1)-3] and ((k[1].split("\\")[minval] not in finalval1)==True)): #if the file is a target file
                                    tempclass=temp1[len(temp1)-1]
                                    try:
                                        tempclass1.index(k[1])
                                    except ValueError:
                                        tempclass1.append(k[1])
                                        tempdep+=1
                            countm2.append(l) #re add to new list in format [name,count,#dependencies...]
                            countm2.append(tempdep)
                            countm2.append(tempcount)
                        else:
                            countm2.append(l)#add with 0 dependencies (wont affect calc as *1-(0) is still 1)
                            countm2.append(tempdep)
                            countm2.append(tempcount)
                    except(IndexError):
                        do=False #for the shorter names, these files are not necessary
                g+=1
            else:
                g+=1
        #print(countm2,countllf)
        #print("half of the count")
        g=0
        sum1=0
        sum=0
        g=0
        #calculation done below
        # print(round(total/150))
        # roundednum =round(total/50)
        roundednum=5
        if roundednum<5:
            roundednum=5
        for c in countm2:
            if(g%3==0 or g==0 ): #since the name is every 3 spots
                tempdep=countm2[g+1] #the count is next
                tempcount=countm2[g+2] #the dependency
                if(tempcount>roundednum): #for the "cognitive penalty"
                    sum+=((tempcount/total)*((math.log(tempcount)/math.log(roundednum))**-1))*(1-(tempdep/countllf)) #checked against excel and handwritted math
                else:
                    sum+=(tempcount/total)*(1-(tempdep/countllf))
                g+=1
            else:
                g+=1
        print(total, finalval1, sum) #prints the DL metric...
        # ws.cell(row=gnum,column=29).value=sum

#this method counts the total number of files
def countuniq(csvfile):
    with open(csvfile,newline='') as csvfile1:
        spamreader=csv.reader(csvfile1,delimiter=",",quotechar='|')
        name=[]
        countun=0
        for row in spamreader: #below makes sure that every possible node is in the name list
            try:
                name.index(row[0])
            except(ValueError):
                name.append(row[0])
            try:
                name.index(row[1])
            except(ValueError):
                name.append(row[1])
        return len(name)

#this method is to count the number of lower level files
def countllf1(finalval,nextval,minval,csvfile):
    name=[]
    name1=[]
    with open(csvfile,newline='') as csvfile1:
        spamreader=csv.reader(csvfile1,delimiter=",",quotechar='|')
        for row in spamreader:
            try:
                name.index(row[0]) #makes sure that every possible node is in the name list
            except(ValueError):
                name.append(row[0])
            try:
                name.index(row[1])
            except(ValueError):
                name.append(row[1])
        for f in range(0,len(finalval)):
            finalval[f] = nextval[finalval[f]] #this puts the numerical top layer into a string
        for n in name:
            try:
                finalval.index(n.split('\\')[minval]) #if the top layer is in the list, do nothing
            except(ValueError):
                name1.append(n) #if its not (aka its a lower layer) and the index fails, put in new list then count
        #print(len(name1))
        return len(name1)

#this part automatically runs the code for each folder
for i in range(111,167):
    csvfile="C://Users/JG31348/Documents/htmltesting2/data/test"+str(i)+".csv"
    try:
        print(i)
        findLen(csvfile)
        gnum+=1
        print()
    except(FileNotFoundError):
        gnum+=1
    except(ZeroDivisionError):
        gnum+=1
# csvfile="C://Users/JG31348/Documents/htmltesting2/data/test3.csv"
# findLen(csvfile)
# wb.save(dest)
