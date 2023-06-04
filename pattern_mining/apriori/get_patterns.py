import PAMI.frequentPattern.basic.Apriori as alg 

iFile = '../logs.csv'  #specify the input transactional database 
minSup = 2                      #specify the minSup value
seperator = ' '                  #specify the seperator. Default seperator is tab space. 
oFile = 'patterns.txt'   #specify the output file name

obj = alg.Apriori(iFile, minSup, seperator) #initialize the algorithm 
obj.startMine()                       #start the mining process
obj.save(oFile)               #store the patterns in file 
df = obj.getPatternsAsDataFrame()     #Get the patterns discovered into a dataframe 
obj.printResults()                      #Print the statistics of mining process
