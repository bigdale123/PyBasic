import os
#   - PyBasic editor program - 
# This program acts as a "console" where you enter 
# PyBasic code line by line for testing purposes.
# It's also supposed to replicate something like the
# BASIC screen on the C64.

print("     **** PYTHON BASIC 1.0 ****     ")
print

# The memory file is supposed to act like memory,
# Every time a command is entered into the editor, it gets stored in this 
# file for the interpreter.py program to run it
memory_file = open("memory.txt","a")

# function for writing commands to the "memory file"
def memory_write(str):
	memory_file.write(choice + "\n")
	return		

# - Run functionality not implemented
# - The following code is the editor,
#   Valid commands are regular PyBasic
#   Syntax, or exit and save (and soon run)
# - if you type in "save", the current program gets saved to a
#   file the user specifies.
choice=""
while choice.lower() != "exit":
	choice = raw_input("> ")
	choice = choice.lower()
	if choice == "save":
		memory_file.close()
		file_name = raw_input("Enter a filename: ")
		os.system("cp memory.txt " + file_name + ".bas")
		memory_file = open("memory.txt","a")
	elif choice != "exit":
		memory_write(choice)

#clear out the memory file upon exit
os.system("rm memory.txt")

		 