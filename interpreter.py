import os
tokens = []
num_stack = []
symbols = {}

#Function to read program file
def open_file(filename):
	data = open(filename, "r").read()
	return data

# Function to lexically determine valid syntax
# Takes the whole file, busts it up into individual characters in the same order
# takes the individual characters and adds them together until it identifies a valid syntax word
# It then creates a token that represents that syntax for the parsing function
# This function acts like a translator for the parse function
def lex(filecontents):
	tok = ""
	state = 0
	com_state = 0
	varStarted = 0
	var = ""
	string = ""
	expr = ""
	n = ""
	isexpr = 0
	filecontents = list(filecontents)
	for char in filecontents:
		tok += char
		#print(tok)
		if tok == " ":
			if state == 0:
				if varStarted == 1:
					varStarted = 0
					if var != "":
						tokens.append("VAR:" + var)
						var = ""
						tok = ""
				else:
					tok = ""
					
			elif state == 1:
				tok = " "
			else:
				print("RUNTIME ERROR")
		elif tok == "\t":
			tok = ""
		elif tok == "\n" or tok == "<EOF>":
			if expr != "" and isexpr == 1:
				tokens.append("EXPR:" + expr)
				expr = ""
			elif expr != "" and isexpr == 0:
				tokens.append("NUM:" + expr)
				expr = ""
			elif var != "":
				tokens.append("VAR:" + var)
				var = ""
				varStarted = 0
			elif com_state == 1:
				com_state = 0
			tok = ""
			isexpr = 0
		elif tok == "=" and state == 0:
			if expr != "" and isexpr == 0:
				tokens.append("NUM:" + expr)
				expr = ""
			if var != "":
				tokens.append("VAR:" + var)
				var = ""
				varStarted = 0
			if tokens[-1] == "EQUALS":
				tokens[-1] = "COND:EQUALTO"
			elif tokens[-1] == "COND:GREATERTHAN":
				tokens[-1] = "COND:GREATEROREQUAL"
			elif tokens[-1] == "COND:LESSTHAN":
				tokens[-1] = "COND:LESSOREQUAL"
			else:
				tokens.append("EQUALS")
			tok = ""
		elif tok == "!=" and state == 0:
			if expr != "" and isexpr == 1:
				tokens.append("EXPR:" + expr)
				expr = ""
			elif expr != "" and isexpr == 0:
				tokens.append("NUM:" + expr)
				expr = ""
			elif var != "":
				tokens.append("VAR:" + var)
				var = ""
				varStarted = 0
			tokens.append("COND:NOTEQUAL")
			tok = ""
		elif tok == "<" and state == 0:
			if expr != "" and isexpr == 1:
				tokens.append("EXPR:" + expr)
				expr = ""
			elif expr != "" and isexpr == 0:
				tokens.append("NUM:" + expr)
				expr = ""
			elif var != "":
				tokens.append("VAR:" + var)
				var = ""
				varStarted = 0
			tokens.append("COND:LESSTHAN")
			tok = ""
		elif tok == ">" and state == 0:
			if expr != "" and isexpr == 1:
				tokens.append("EXPR:" + expr)
				expr = ""
			elif expr != "" and isexpr == 0:
				tokens.append("NUM:" + expr)
				expr = ""
			elif var != "":
				tokens.append("VAR:" + var)
				var = ""
				varStarted = 0
			tokens.append("COND:GREATERTHAN")
			tok = ""
		elif tok == "$" and state == 0:
			varStarted = 1
			var += tok
			tok = ""
		elif tok == "#" and com_state == 0:
			com_state = 1
			tok = ""
		elif varStarted == 1:
			var += tok
			tok = ""
		elif tok.lower() == "end":
			tokens.append("END")
			tok = ""
		elif tok.lower() == "print":
			tokens.append("PRINT")
			tok = ""
		elif tok.lower() == "clear_screen":
			tokens.append("CLS")
			tok = ""
		elif tok.lower() == "input":
			tokens.append("INPUT")
			tok = ""
		elif tok.lower() == "fi":
			tokens.append("FI")
			tok = ""
		elif tok.lower() == "if":
			tokens.append("IF")
			tok = ""
		elif tok.lower() == "then":
			if expr != "" and isexpr == 0:
				tokens.append("NUM:" + expr)
				expr = ""
			tokens.append("THEN")
			tok = ""

		elif tok in "0123456789" and state == 0:
			expr += tok
			tok = ""
		elif tok in "+-*/^()" and state == 0:
			isexpr = 1
			if tok == "^":
				expr += "**"
			else:
				expr += tok
			tok = ""
		elif tok == "\"" or tok == " \"":
			if state == 0:
				state = 1
			elif state == 1:
				tokens.append("STRING:" + string + "\"")
				string = ""
				state = 0
				tok = ""
		elif state == 1:
			string += tok
			tok = ""
	print(tokens)
	#print(expr)
	return tokens


# Used to calculate math expressions in the Parse function
def evalExpression(expr):
	return eval(expr)

# Print function for the Parse function
def doPRINT(toPRINT):
	if(toPRINT[0:6] == "STRING"):
		toPRINT = toPRINT[8:]
		toPRINT = toPRINT[:-1]
	elif(toPRINT[0:3] == "NUM"):
		toPRINT = toPRINT[4:]
	elif(toPRINT[0:4] == "EXPR"):
		toPRINT = evalExpression(toPRINT[5:])
	print(toPRINT)
	return

# "fakes" the creation and use of variables by storing them in dictionaries
def doASSIGN(varname, varvalue):
	symbols[varname[4:]] = varvalue
	return

# Gets the value of a variable from the dictionary for variables
def getVARIABLE(varname):
	varname = varname[4:]
	if varname in symbols:
		return symbols[varname]
	else:
		return "VAR ERROR: Undefined Variable"

# Function used to create if statements in the interpreter
def doIF(testvar1,condition,testvar2):
	#print("YES")
	condition = condition[5:]
	#print(condition)
	if condition == "EQUALTO":
		if testvar1 == testvar2:
			return True
		else:
			return False
	elif condition == "NOTEQUAL":
		if testvar1 != testvar2:
			return True
		else:
			return False
	elif condition == "LESSTHAN":
		if testvar1 < testvar2:
			return True
		else:
			return False
	elif condition == "GREATERTHAN":
		if testvar1 > testvar2:
			return True
		else:
			return False
	elif condition == "LESSOREQUAL":
		if testvar1 <= testvar2:
			return True
		else:
			return False
	elif condition == "GREATEROREQUAL":
		if testvar1 >= testvar2:
			return True
		else:
			return False
	else:
		return "ERROR, NOT A VALID CONDITIONAL OPERATOR" 
	

# The parsing function takes a list of tokens and then executes corresponding code in python
def parse(toks):
	i = 0
	while(i < len(toks)):
		
		# Just a dummy command to signify the end of a program
		if toks[i] == "END":
			break

		# Command used to signify the end of an if loop
		elif toks[i] == "FI":
			i += 1

		# Command used to clear the terminal (Only works in linux, but it's an easy change to windows)
		elif toks[i] == "CLS":
			os.system('clear')
			i += 1

		# Handles any kind of print statement that is valid
		elif (toks[i] + " " + toks[i+1][0:6] == "PRINT STRING") or (toks[i] + " " + toks[i+1][0:3] == "PRINT NUM") or (toks[i] + " " + toks[i+1][0:4] == "PRINT EXPR") or (toks[i] + " " + toks[i+1][0:3] == "PRINT VAR"):
			if toks[i+1][0:6] == "STRING":
				doPRINT(toks[i+1])		
			elif toks[i+1][0:3] == "NUM":
				doPRINT(toks[i+1])
			elif toks[i+1][0:4] == "EXPR":
				doPRINT(toks[i+1])
			elif toks[i+1][0:3] == "VAR":
				doPRINT(getVARIABLE(toks[i+1]))
			i += 2

		# Handles variable assignment
		elif toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:6] == "VAR EQUALS STRING" or toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "VAR EQUALS NUM" or toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:4] == "VAR EQUALS EXPR" or toks[i][0:3] + " " + toks[i+1] + " " + toks[i+2][0:3] == "VAR EQUALS VAR":
			if toks[i+2][0:6] == "STRING":
				doASSIGN(toks[i],toks[i+2])
				i += 3		
			elif toks[i+2][0:3] == "NUM":
				doASSIGN(toks[i],toks[i+2])
				i += 3
			elif toks[i+2][0:4] == "EXPR":
				doASSIGN(toks[i],"NUM:" + str(evalExpression(toks[i+2][5:])))
				i += 3
			elif toks[i+2][0:3] == "VAR" and toks[i+2][0:3] + " " + toks[i+3][0:4] != "VAR EXPR":
				doASSIGN(toks[i],getVARIABLE(toks[i+2]))
				i += 3
			elif toks[i+2][0:3] + " " + toks[i+3][0:4] == "VAR EXPR":
				variable_result = getVARIABLE(toks[i+2])
				doASSIGN(toks[i],("NUM:"+str(evalExpression(variable_result[4:] + toks[i+3][5:]))))
				i += 4

		# Handles user input and stores answer in variable
		elif toks[i][0:5] + " " + toks[i+1][0:6] + " " + toks[i+2][0:3] == "INPUT STRING VAR":
			doPRINT(toks[i+1])
			doASSIGN(toks[i+2],input("? "))
			i += 3

		# Checks for if statements & if they are valid (True)
		#   If an IF statement's condition is true, parser continues in regular step size and does not skip anything
		#   If an IF statement's condition is false, parser skips to FI token and continues
		elif toks[i] + " " + toks[i+1][0:3] + " " + toks[i+2][0:4] + " " + toks[i+3][0:3] + " " + toks[i+4] == "IF NUM COND NUM THEN":
			result = doIF(toks[i+1][4:],toks[i+2],toks[i+3][4:])
			fi_loc = toks.index("FI")
			if result == True:
				i += 5
			else:
				toks = toks[(fi_loc+1):]
				i = 0
		
		# Checks for if statements & if they are valid (True)
		#   If an IF statement's condition is true, parser continues in regular step size and does not skip anything
		#   If an IF statement's condition is false, parser skips to FI token and continues
		elif toks[i] + " " + toks[i+1][0:6] + " " + toks[i+2][0:4] + " " + toks[i+3][0:3] + " " + toks[i+4] == "IF STRING COND VAR THEN" or toks[i] + " " + toks[i+1][0:3] + " " + toks[i+2][0:4] + " " + toks[i+3][0:6] + " " + toks[i+4] == "IF VAR COND STRING THEN":
			if toks[i+1][0:6] == "STRING":
				#print(toks[i+1])
				#print(getVARIABLE(toks[i+3]))
				result = doIF(toks[i+1][8:-1],toks[i+2],getVARIABLE(toks[i+3]))
				fi_loc = toks.index("FI")
				if result == True:
					i += 5
				else:
					toks = toks[(fi_loc+1):]
					i = 0

		# Checks for if statements & if they are valid (True)
		#   If an IF statement's condition is true, parser continues in regular step size and does not skip anything
		#   If an IF statement's condition is false, parser skips to FI token and continues
		elif toks[i] + " " + toks[i+1][0:3] + " " + toks[i+2][0:4] + " " + toks[i+3][0:3] + " " + toks[i+4] == "IF VAR COND NUM THEN" or toks[i] + " " + toks[i+1][0:3] + " " + toks[i+2][0:4] + " " + toks[i+3][0:3] + " " + toks[i+4] == "IF NUM COND VAR THEN"or toks[i] + " " + toks[i+1][0:3] + " " + toks[i+2][0:4] + " " + toks[i+3][0:3] + " " + toks[i+4] == "IF VAR COND VAR THEN":
			if (toks[i+1][0:3] == "VAR") and (toks[i+3][0:3] == "NUM"):
				result = doIF(getVARIABLE(toks[i+1]),toks[i+2],toks[i+3][4:])
				fi_loc = toks.index("FI")
				if result == True:
					i += 5
				else:
					toks = toks[(fi_loc+1):]
					i = 0
			elif (toks[i+1][0:3] == "NUM") and (toks[i+3][0:3] == "VAR"):
				result = doIF(toks[i+1][4:],toks[i+2],getVARIABLE(toks[i+3]))
				fi_loc = toks.index("FI")
				if result == True:
					i += 5
				else:
					toks = toks[(fi_loc+1):]
					i = 0
			elif (toks[i+1][0:3] == "VAR") and (toks[i+3][0:3] == "VAR"):
				result = doIF(getVARIABLE(toks[i+1]),toks[i+2],getVARIABLE(toks[i+3]))
				fi_loc = toks.index("FI")
				if result == True:
					i += 5
				else:
					toks = toks[(fi_loc+1):]
					i = 0								
	#print(symbols)
	return

# Main function that runs other functions
def run():
	data = open_file("test.bas")
	toks = lex(data)
	parse(toks)

run()
