# CogFile_manage stores functions to clear, write and read the cog file
# clearCogFile: Used to clear the cogFile
async def clearCogFile():
    # Clear the entire file
    print("[Utils.Cogfile_manage.ClearCogFile] Cleaning cogFile")
    open("./cogFile.txt", "w").close()
    print("[Utils.Cogfile_manage.ClearCogFile] Cleaned\n")

# writeCommentCogFile: Writes the comment section on top of the cog file
async def writeCommentCogFile():
    print("[Utils.Cogfile_manage.WriteCommentCogFile] Writing comments on cogFile")

    # Writes a entire new file
    with open("./cogFile.txt", "w+") as cogFile:
        cogFile.write('''################################################################################################ 
# Cog List                                                                                     #
#                                                                                              #
# This file is used to read all cogs presents in the code, to be loaded on the bot             #
# To load your cog here, put your cog code on /cogs/your_cog.py                                #
# And add the filename here (without the .py)                                                  #
# Done, the bot will load it in startup                                                        #
# Any cog that starts with '!' are deactivated, so they will not be loaded                     #
#                                                                                              #
# Commented cog_example here because we dont use it, its just a template for new cogs (:       #
#                                                                                              #
# On this file, any line that starts with '#' will be ignored                                  #
# If you want to add comments here, please, respect this template so you dont break our        #
# readers!                                                                                     #
# Dont leave empty lines here too! It will break our readers sadly. Use # instead to space:    #
#                                                                                              #
# Failing to do so will mess up the cog loading/reloading/unloading functions ):               #
################################################################################################
#
# cog_example
''')
    print("[Utils.Cogfile_manage.WriteCommentCogFile] Done writing default cogFile\n")

# writeCogFile: Default function used by other cogs to join the voice channel
async def writeCogFile(text):
    print("[Utils.Cogfile_manage.WriteCogFile] Writing new cogFile")

    #First writes the comment section
    await writeCommentCogFile()

    # Appends the new content
    with open("./cogFile.txt", "a") as cogFile:
        for line in text:
            cogFile.write(line + "\n")
    print("[Utils.Cogfile_manage.WriteCogFile] Done writing new cogFile\n")

# readCogFile: Opens the cogFile and returns the contets ignoring comments
def readCogFile():
    # Opens the Cog file
    print("[Utils.Cogfile_manage.ReadCogFile] Reading cogFile")

    lineList = []
    with open("./cogFile.txt") as cogFile:
        cogFileContent = cogFile.read().splitlines()
        for line in cogFileContent:
            # Ignore comments
            if line[0] == "#":
                continue
            lineList.append(line)
        print("[Utils.Cogfile_manage.ReadCogFile] Done reading cogFile\n")
        # Returns the final list of lines
        return lineList
