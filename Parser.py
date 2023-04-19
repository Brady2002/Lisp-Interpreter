import operator
import math

vars = {}
functions = {}
ops = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv, "pow": operator.pow, ">": operator.gt, "<": operator.lt, ">=": operator.ge, "<=": operator.le, "=": operator.eq, "!=": operator.ne} 

def tokenize(line):
  return line.replace('(',' ( ').replace(')',' ) ').split()

def parse(line):
  tokens = line
  currentToken = tokens.pop(0)
  if '(' == currentToken:
    list = []
    while tokens[0] != ')':
      list.append(parse(tokens))
    tokens.pop(0)
    return list
  elif ')' == currentToken:
    print('closed parenthesis without initially opening parenthesis')
  else:
    try: return int(currentToken)
    except ValueError:
      try: return float(currentToken)
      except ValueError:
        return currentToken
          
def eval(line):
    if isinstance(line, list):
      if line[0] == "define":
        return define(line)
      elif line[0] == "defun":
        return defun(line)
      elif line[0] == "if":
        return ifStatement(line)
      elif line[0] == "lambda":
        return lambdaStatement(line)
      elif line[0] == "car":
        return car(line)
      elif line[0] == "cdr":
        return cdr(line)
      elif line[0] == "'":
        return line
      elif line[0] == "set!":
        return setStatement(line)
      elif line[0] == "sqrt":
        return sqrt(line)
      elif line[0] in ops:
        return arith(line)
      elif line[0] in vars:
        return vars[line[0]]
      elif line[0] in functions:
        return func(line)
      else:
        return line[0]

def define(line):
  variableName = line[1]
  variableValue = line[2]
  vars[variableName] = variableValue
  return variableName

def defun(line):
  functionName = line[1]
  functionParameters = line[2]
  functionBody = line[3]
  functions[functionName] = functionParameters, functionBody
  return functionName, functionParameters, functionBody

def func(line):
  functionName = line[0]
  functionParameters = line[1]
  functionBody = functions[functionName][1]
  for i in range(len(functionParameters)):
    functionBody[i+1] = str(functionParameters[i])
  return eval(functionBody)

def ifStatement(line):
  question = line[1]
  questionAnswer = eval(question)
  if questionAnswer:
    eval(line[2])
  else:
    eval(line[3])

def lambdaStatement(line):
  functionParameters = line[1]
  functionBody = line[2]
  return functionParameters, functionBody

def car(line):
  return line[2][0]

def cdr(line):
  return line[2][1:]

def setStatement(line):
  variableName = line[1]
  variableValue = line[2]
  vars[variableName] = eval(variableValue)
  return variableName

def sqrt(line):
  if isinstance(line[1], list):
    return math.sqrt(int(eval(line[1])))
  elif line[1] in vars:
    return math.sqrt(int(vars[line[1]]))
  elif line[1] in functions:
    return math.sqrt(int(eval(functions[line[1]])))
  else:
    return math.sqrt(line[1])

def arith(line):
  opChar = line[0]
  opFunc = ops[opChar]
  if isinstance(line[1], list):
    if isinstance(line[2], list):
      return opFunc(int(eval(line[1])), int(eval(line[2])))
    else:
      if line[2] in vars:
        return opFunc(int(eval(line[1])), int(vars[line[2]]))
      else:
        return opFunc(int(eval(line[1])), int(line[2]))
  elif isinstance(line[2], list):
    if line[1] in vars:
      return opFunc(int(vars[line[1]]), int(eval(line[2])))
    else:
      return opFunc(int(line[1]), int(eval(line[2])))
  else:
    if line[1] in vars:
      if line[2] in vars:
        return opFunc(int(vars[line[1]]), int(vars[line[2]]))
      else:
        return opFunc(int(vars[line[1]]), int(line[2]))
    else:
      if line[2] in vars:
        return opFunc(int(line[1]), int(vars[line[2]]))
      else:
        return opFunc(int(line[1]), int(line[2]))

def main():
  print("Enter your LISP command to be executed (type (quit) to exit):")
  takingInput = True
  while(takingInput):
    line = input()
    if(line == "(quit)"):
      takingInput = False
    else:
      print(eval(parse(tokenize(line))))

if __name__ == "__main__":
  main()