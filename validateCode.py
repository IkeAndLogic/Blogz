import hashlib,random, string

def verifyUserName(userName):
    if len(userName)<3:
        return False
    elif len(userName)>20:
        return False
    else:
        return True
    
def verifyPassword(password, password2):
    count = 0
#Rule 1
    for item in password:
        if item == " ":
            return False
            break
        else:
            for item in password2:
                if item == " ":
                    return False
                    break
    # Rule 2
    for p in password:
        pas = [password, password2]
    for p in pas:
        if len(p)<3:
            return False
            break
        elif len(p)>20:
            return False
            break
        else: pass
    if password==password2:
        return True
    else:
        return False

def verifyEmail(email):
    if len(email) == 0:
        return True
    countAt = 0
    countDot = 0
    # rule 1
    if len(email)<3:
        return False
    elif len(email) > 20 :
        return False
    else:
        for item in email:
            if item == "@" :
                countAt += 1
            elif item == ".":
                countDot += 1
            elif item ==" ":
                return False
            else:
                continue
        if countAt != 1:
            return False
        elif countDot != 1:
            return False
        else:
            return True 


def makeSalt():
    return "".join([random.choice(string.ascii_letters) for i in range(5)]).encode()

def hashPassword(password, salt = None):
    if not salt:
        salt = makeSalt()
    return hashlib.sha256(password.encode() + salt).hexdigest(),salt.decode()


