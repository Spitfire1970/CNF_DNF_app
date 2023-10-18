def read_leaderboard():
    try:
        f = open("userData.txt", "r")
    except:
        open("userData.txt", "x")
        f = open("userData.txt", "r")
    d = {}
    for i in f.read().split("\n")[:-1]:
        key, value = i.split()
        d[key] = int(value)
    return d

def update_leaderboard(d):
    f = open("userData.txt", "w")
    for i in d.keys():
        f.write(i + " " + str(d[i]) + "\n")
    return

def update_user_record(username, score):
    d = read_leaderboard()
    if username not in d.keys():
        d[username] = score
    elif d[username] > score:
        return d[username]
    else:
        d[username] = score
    update_leaderboard(d)
    return score