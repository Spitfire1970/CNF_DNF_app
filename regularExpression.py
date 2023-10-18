import re
def intoBrackets(s, index):
    reg = '\(([^\(]*?)\)'
    gotReg = re.search(reg, s)
    if gotReg == None:
        return None, None
    new_s = re.sub(reg, str(index), s, count=1)
    return new_s, gotReg.group(1)

def toExpression(formula):
    lst = []
    final = formula
    while True:
        formula, temp = intoBrackets(formula, len(lst))
        if formula == None:
            break
        final = formula
        lst.append(temp)

    lst.append(final)
    return lst

def toFormula(lst):
    s = lst[-1]
    while re.search("\d+", s):
        for num in re.findall("\d+", s):
            if re.search("^[a-zA-z]$", lst[int(num)]) or re.search("^¬ [a-zA-Z]$", lst[int(num)]):
                s = s.replace(num, lst[int(num)], 1)
            else:
                s = s.replace(num, "(" + lst[int(num)] + ")", 1)
    return s

def convertImplication(lst):
    new_lst = lst.copy()
    for i, string in enumerate(lst):
        reg = "^(.*?)↔(.*?)$"
        iff_reg = re.search(reg, lst[i])
        if iff_reg:
            a = iff_reg.group(1).strip()
            b = iff_reg.group(2).strip()
            if "¬" in a and "¬" in b:
                lst[i] = "(" + a.replace("¬", "") + " ∨ " + b + ") ∧ (" + b.replace("¬" ,"") + " ∨ " + a + ")"
            elif "¬" in a:
                lst[i] = "(" + a.replace("¬", "") + " ∨ " + b + ") ∧ (¬" + b + " ∨ " + a + ")"
            elif "¬" in b:
                lst[i] = "(¬" + a + " ∨ " + b + ") ∧ (" + b.replace("¬" ,"") + " ∨ " + a + ")"
            else:
                lst[i] = "(¬" + a + " ∨ " + b + ") ∧ (¬" + b + " ∨ " + a + ")"

        reg = "^(.*?)→(.*?)$"
        imp_reg = re.search(reg, lst[i])
        if imp_reg:
            a = imp_reg.group(1).strip()
            b = imp_reg.group(2).strip()
            if "¬" in a:
                lst[i] = a.replace("¬", "") + " ∨ " + b
            else:
                lst[i] = "¬" + a + " ∨ " + b
    
    return lst

def eliminateImplication(lst):
    one = 0
    double = 0
    for i in lst:
        for j in i:
            if j == "→":
                one += 1
            elif j == "↔":
                double += 1
    while one>0 or double>0:
        lst = convertImplication(lst)
        one -= 1
        double -= 1
    return lst
