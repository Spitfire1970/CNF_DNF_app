import random

#returns negation of string with 1/3 chance
def not_funct(formula):
    coin = [True, False]
    weighted_coin = random.choices(coin, weights=(33, 67), k=1)
    if weighted_coin[0] is True:
        return ("¬"  + formula)
    else:
        return formula

#generates arbitrary propositional formula with specific number of variables
def generate_question(num_letters):
    #list of propositional letters
    variables = random.choice([['A', 'B', 'C', 'D', 'E'], ['P', 'Q', 'R', 'S', 'T']])
    variable_seq_1 = random.choices(variables, k = 10)
    variable_seq = [[i, 1] for i in variable_seq_1]
    #list of operators
    operators = ["↔", "→", "∨", "∧"]
    operator_seq = random.choices(operators, weights=(10, 24, 33, 33), k = 8)
    
    #initialize
    temp = random.choice(variable_seq)
    picked = [not_funct(temp[0]), 1]

    #using recursive definition of propositional formulas
    while picked[1] != num_letters:
        temp1 = random.choice(variable_seq)
        if picked[1] + temp1[1] > 1:
            variable_seq.append(["("+not_funct(picked[0] + " " + random.choice(operator_seq) + " " + not_funct(temp1[0]) + ")"), picked[1]+temp1[1]])
        else:
            variable_seq.append([not_funct(picked[0] + " " + random.choice(operator_seq) + " " + not_funct(temp1[0])), picked[1]+temp1[1]])
        temp2 = random.choice(variable_seq)
        picked[0] = temp2[0]
        picked[1] = temp2[1]
    return picked[0]

