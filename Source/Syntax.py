from Test import Glob

def A():
    global Glob
    Glob = 4
    print(Glob)

def B():
    global Glob
    # Glob = 5
    print(Glob)
    
A()
B()