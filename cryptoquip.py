import sys
import colorama

def undo(source, transformations):
    if transformations == []:
        return source
    a, b = transformations[-1]
    source = source.replace(b, a)
    transformations.pop(-1)
    return source

def stats(source, transformations):
    counts = {}
    for char in source:
        counts[char] = counts.get(char,0)+1
    print sorted(counts.iteritems(), key=lambda x:x[1])
    return source

def transforms(source, transformations):
    print transformations
    return source

def colorformat(astr):
    result = ""
    for char in astr:
        if char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            result += colorama.Fore.RED + char + colorama.Fore.RESET
        else:
            result += char
    return result
        

def main():
    transformations = []
    cmds = {'u' : undo,
            'stat' : stats,
            't' : transforms}
    source = open(sys.argv[1]).read()
    while True:
        print colorformat(source)
        cmd = raw_input()
        cmd = cmd.split()
        if len(cmd) == 0:
            continue
        if len(cmd) == 1:
            if cmd[0] not in cmds:
                print "Invalid command", cmds.keys()
                continue
            source = cmds[cmd[0]](source, transformations)
        else:
            if cmd[1] in source:
                print "Already in use"
                continue
            source = source.replace(cmd[0],cmd[1])
            transformations.append((cmd[0],cmd[1]))
colorama.init()
print colorama.Style.BRIGHT,
main()
