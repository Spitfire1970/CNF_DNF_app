import re
from regularExpression import toExpression, eliminateImplication, convertImplication
from QuineMcCluskey import QMC
from tseitin import Tseitin
from question_generator import generate_question

LETTER = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
OPERATOR = "∧∨→↔"


def get_minterms(expression, variables):
    booleans = [i for i in range(2**len(variables))]
    res = []
    for bool in booleans:
        d = {}
        i = len(variables)-1
        temp = bool
        while temp != 0:
            d[variables[i]] = temp%2
            i -= 1
            temp //= 2
        while i >= 0:
            d[variables[i]] = 0
            i -= 1
        if test_expression(expression, d):
            res.append(bool)
    return res

def test_expression(expression, d):
    new_e = expression.copy()
    for i in range(len(new_e)):
        lst = new_e[i].replace("∨", " ∨ ").replace("∧", " ∧ ").split(" ")
        while "" in lst:
            lst.remove("")
        j = 0
        while j < len(lst):
            if lst[j] in d.keys():
                lst[j] = d[lst[j]]
                j += 1
                continue
            if lst[j][0] == "¬":
                if len(lst[j]) == 1:
                    lst[j+1] = not d[lst[j+1]]
                    del lst[j]
                elif lst[j][1] in d.keys():
                    lst[j] = not d[lst[j][1]]
                else:
                    lst[j] = not new_e[int(lst[j][1])]
                j += 1
                continue
            try:
                lst[j] = new_e[int(lst[j])]
                j += 1
                continue
            except:
                j += 1
                continue

        res = lst[0]
        j = 1
        while j < len(lst):
            if lst[j] == "∧":
                res = res and lst[j+1]
                j += 2
            elif lst[j] == "∨":
                res = res or lst[j+1]
                j += 2
        new_e[i] = res
    return new_e[-1]

def get_variables(formula):
    variables = []
    for i in formula.replace("(", "").replace(")", "").replace("¬", "").replace("∧", " ").replace("∨", " ").split(" "):
        if i == "":
            continue
        if i in LETTER and i not in variables:
            variables.append(i)
    return variables

def formula_to_cnf(formula):
    variables = get_variables(formula)
    expression = toExpression(formula)
    expression = eliminateImplication(expression)
    minterms = get_minterms(expression, variables)
    if minterms == []:
        return None
    if len(minterms) == 2**len(variables):
        return None
    res = QMC(minterms, variables)
    if res == [[]]:
        return None
    return res

def dnf_to_cnf(dnf):
    variables = []
    lst = [[0 for _ in range(len(dnf[i]))] for i in range(len(dnf))]
    for i in range(len(dnf)):
        for j in range(len(dnf[i])):
            x = dnf[i][j]
            if len(x) == 1:
                if x in variables:
                    lst[i][j] = variables.index(x)+1
                else:
                    variables.append(x)
                    lst[i][j] = len(variables)
            else:
                if x[1] in variables:
                    lst[i][j] = -1 * (variables.index(x[1])+1)
                else:
                    variables.append(x[1])
                    lst[i][j] = -1 * len(variables)
    cnf = Tseitin(lst)
    res = [[0 for _ in range(len(cnf[i]))] for i in range(len(cnf))]
    k = 0
    for i in range(len(cnf)):
        for j in range(len(cnf[i])):
            x = cnf[i][j]
            if abs(x) > len(variables):
                k += 1
                variables.append("n" + str(k))
            if x < 0:
                res[i][j] = "¬" + variables[abs(x)-1]
            else:
                res[i][j] = variables[x-1]

    return res

def solve(formula):
    formula = formula.replace("¬¬", "")
    dnf = formula_to_cnf(formula)
    if dnf == None:
        return None
    cnf = dnf_to_cnf(dnf)
    return " ∨ ".join("(" + " ∧ ".join(i) + ")" for i in dnf), " ∧ ".join("(" + " ∨ ".join(i) + ")" for i in cnf)

def check_dnf(formula):
    disjunctions = formula.split("∨")
    for i in disjunctions:
        reg = re.search("\s*\((.*?)\)\s*", i)
        if reg:
            a = reg.group(1)
            if "(" in a or ")" in a:
                return check_dnf(formula[1:-1]) if formula[0] == "(" else False
        elif "(" in i or ")" in i:
            return check_dnf(formula[1:-1]) if formula[0] == "(" else False
        if re.search("¬.*\(", i):
            return check_dnf(formula[1:-1]) if formula[0] == "(" else False
    return True

def check_cnf(formula):
    conjunctions = formula.split("∧")
    for i in conjunctions:
        reg = re.search("\s*\((.*?)\)\s*", i)
        if reg:
            a = reg.group(1)
            if "(" in a or ")" in a:
                return check_cnf(formula[1:-1]) if formula[0] == "(" else False
        elif "(" in i or ")" in i:
            return check_cnf(formula[1:-1]) if formula[0] == "(" else False
        if re.search("¬.*\(", i):
            return check_cnf(formula[1:-1]) if formula[0] == "(" else False
    return True

def check_validation(formula):
    flag = False
    for i in formula:
        if i in LETTER:
            flag = True
            break
    if not flag:
        return False
    stack = []
    last = False
    for i in formula.replace(" ", "").replace("¬", ""):
        if i == "(":
            stack.append("")
        elif i == ")":
            if stack == []:
                return False
            stack.pop()
        elif i in LETTER:
            if last:
                return False
            else:
                last = True
        elif i in OPERATOR:
            if last:
                last = False
            else:
                return False
        else:
            return False
    return True

def check_variables(formula, answers):
    d1 = get_variables(formula)
    d2 = get_variables(answers[0])
    for i in d1:
        if i not in d2:
            return False
    return True    

def check(formula, answers, dnf):
    if not check_validation(formula):
        return "Answer not valid"
    if not check_variables(formula, answers):
        return "Answer has undefined variable"
    if "↔" in formula or "→" in formula:
        return "Answer should not include implications"
    formula = formula.replace("¬¬", "").replace("¬ ¬", "")
    if dnf == 0:
        if not check_dnf(formula):
            return "Answer not in DNF"
    else:
        if not check_cnf(formula):
            return "Answer not in CNF"
        
    variables = get_variables(formula)
    if not get_minterms(toExpression(formula), variables) == get_minterms(toExpression(answers[0]), variables):
        return "Wrong Answer"
    return "Answer Correct"

def generate_formula(difficulty):
    while True:
        formula = generate_question(difficulty*2+1)
        answers = solve(formula)
        if answers != None:
            break
            
    return formula, answers