#This Program was created to make retreiving data files from the AWS server more efficient. By inputting the necessary variables,
# a script will be generated that can be copy pasted into the command line to retrieve all data into the RedditData folder.


#Gain User Input on the needed variables.


#Name of Subreddit
subreddit = input('Subreddits (Enter as a comma separated list without spaces):')
#Year from which you want to start copying data from the server.
startYear = int(input('Start year:'))
#Month from which you want to start copying data from the server.
startMonth = int(input('Start month:'))
#Year to go up to.
endYear = int(input('End year:'))
#Month to go up to.
endMonth = int(input('End month:'))
#Server Key. It's a .pem file. You make it when you begin the server.
key = input('key (do not write .pem at the end, just the name):')
#IP address of the server. This is found on the bottom right side of the description of the server in the AWS website.
ip = input('ip address:')
#Is the data posts or comments?
postscomments = input('Posts or Comments (p/c)?')

if (postscomments != 'p' and postscomments != 'c'):
	print('Error. Invalid Post or Comments Input')
	exit(1)

#Is the data all reddit users?
alluser = input('All Users Posts (y/n)?')

if (alluser == 'y'):
	alluser = '-U'
elif (alluser =='n'):
	alluser = ''
else:
	print('Error. Invalid All User Posts Input')
	exit(1)

#Create the function to make command line code for a specific subreddit.
def generateCommandLineCode(subR, startY, startM, endY, endM, key1, ip1, pc, alluser1):
	#Create first command and write it to returnString.
	returnString = 'scp -i ' + key1 + '.pem ubuntu@' + ip1 + ':' + subR + '_' + str(startY) + '-'
	if (startM < 10):
		returnString = returnString + '0'
	returnString = returnString + str(startM) + '-' + pc + alluser1 + '.csv' + ' RedditData2019'
	startM = startM + 1

	#Structure and write the commands to the returnString. The commands are separated by a semicolon.
	#This allows all commands to be run one after another regardless of whether the last command failed or not.
	while startY != endY:
		while startM <= 12:
			returnString = returnString + ';' + 'scp -i ' + key1 + '.pem ubuntu@' + ip1 + ':' + subR + '_' + str(startY) + '-'
			if (startM < 10):
				returnString = returnString + '0'
			returnString = returnString + str(startM) + '-' + pc + alluser1 + '.csv' + ' RedditData2019'
			startM = startM + 1
		startY = startY + 1
		startM = 1


	#Repeat Code for Final Year Indexing only up to the last month.
	while startM <= endM:
		returnString = returnString + ';' + 'scp -i ' + key1 + '.pem ubuntu@' + ip1 + ':' + subR + '_' + str(startY) + '-'
		if (startM < 10):
			returnString = returnString + '0'
		returnString = returnString + str(startM) + '-' + pc + alluser1 + '.csv' + ' RedditData2019'
		startM = startM + 1

	return returnString

#Split Subreddits into list.
subredditList = subreddit.split(',')

#Make a folder in your current directory titled RedditData. This folder is where all of the retrieved data will be stored.
finalString = ''

#Run Code for every Subreddit.
for s in subredditList:
	finalString = finalString + generateCommandLineCode(s,startYear,startMonth,endYear,endMonth,key,ip,postscomments,alluser)

#Prints final output. This can be copy pasted directly into the command line to retrieve all data from the server that you indicate. Tested working on 6/25/2019
print(finalString)
