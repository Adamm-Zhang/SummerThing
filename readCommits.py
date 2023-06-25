import os
import itertools as it

os.chdir('files')

changedFileList = []    # contains list of changed files
fileCodeList = []   # contains the code of the respective patch files
numberLinesAdded = 0
numberLinesRemoved = 0

numberComments = 0

originalCode = []
patchedCode = []

fileCount = 0

#with open('0016b5ef37a763b1573039c63f018a3cf86f2b43.patch', 'r') as file:
with open('patch.patch', 'r') as file:

    # we wanna keep track of these headers, so we can keep only .cpp files.
    currentPatchHeader = file.readline()

    # cover the first commit file to start the list; only if its a .cpp file.
    if "cpp" in str(currentPatchHeader).split()[2].split(".")[1]:
        changedFileList.append(currentPatchHeader.split()[2][1:])
        fileCount += 1

    # splits patch into individual files
    for key, group in it.groupby(file, lambda line: line.startswith('diff')):

        if not key:
            if "cpp" not in str(currentPatchHeader).split()[2].split(".")[1]:    # this makes sure we only take in .cpp files, not like .js
                # print(str(currentPatchHeader).split(" ")[2].split(".")[1])    # prints file type
                continue
            else:
                # get the actual code per each file in a list organized by line
                group = list(group)
                fileCodeList.append(group)
        else:

            # get the .cpp file name, this is in order with the previous part; only if its a .cpp file.
            currentPatchHeader = list(group)[0].split(" ")
            if "cpp" in currentPatchHeader[2].split(".")[1]:
                changedFileList.append(currentPatchHeader[2][1:])
                fileCount += 1

print(changedFileList)

for item in fileCodeList:
    print(item)

# extract original and fixed code
for item in fileCodeList:
    originalCodePerFile = []
    patchedCodePerFile = []

    # go thru each file collected in the list
    for i in range(3, len(item)):
        # print(item[i])

        # look for original code; i.e. stuff that was removed (-) or untouched
        if item[i][0] != "+":

            if item[i][0] == "-":   # Count number of deleted lines
                originalCodePerFile.append(" " + item[i][1:])
                numberLinesRemoved += 1

                if "//" in item[i] or "/*" in item[i]:     # Count deleted comments
                    numberComments -= 1

            # This else check just makes sure we don't lose characters upon tracking unchanged lines
            else:
                originalCodePerFile.append(item[i])

        # look for new code; stuff that was added (+) or untouched
        if item[i][0] != "-":

            if "//" in item[i] or "/*" in item[i]:     # Count current comments (original + added)
                numberComments += 1

            if item[i][0] == "+":   # Count number of added lines
                patchedCodePerFile.append(" " + item[i][1:])
                numberLinesAdded += 1

            # This else check just makes sure we don't lose characters upon tracking unchanged lines
            else:
                patchedCodePerFile.append(item[i])

    originalCode.append(originalCodePerFile)
    patchedCode.append(patchedCodePerFile)

# purely for testing: printing out some code
if fileCount > 0:
    print("OLD CODE:")
    for items in originalCode[1]:
        print(items, end='')
    print("NEW CODE:")
    for items in patchedCode[1]:
        print(items, end='')
else:
    print("blank")

print("file Count: " + str(fileCount))
print("Added Lines: " + str(numberLinesAdded))
print("Removed Lines: " + str(numberLinesRemoved))
print("Comments: " + str(numberComments))
