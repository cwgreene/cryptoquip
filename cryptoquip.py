import sys
import colorama

def undo(source, transformations, cmd):
    if transformations == []:
        return source
    a, b = transformations[-1]
    source = source.replace(b, a)
    transformations.pop(-1)
    return source

def stats(source, transformations, cmd):
    counts = {}
    for char in source:
        counts[char] = counts.get(char,0)+1
    print sorted(counts.iteritems(), key=lambda x:x[1])
    return source

def transforms(source, transformations, cmd):
    print transformations
    return source

def remove_transform(source, transformations, cmd):
    if len(cmd) != 2:
        print "remove takes one argument"
        return source
    target = cmd[1]
    for transform in transformations:
        if transform[1] == target or transform[0] == target:
           break
    transformations.remove(transform)
    return source.replace(transform[1], transform[0])

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
            't' : transforms,
            'remove' : remove_transform}
    source = open(sys.argv[1]).read()
    while True:
        print colorformat(source)
        cmd = raw_input()
        cmd = cmd.split()
        if len(cmd) == 0:
            continue
        # Handle standard transform first
        elif len(cmd) == 2 and len(cmd[0]) == 1 and len(cmd[1]) == 1:
            if cmd[1] in source:
                print "Already in use"
                continue
            source = source.replace(cmd[0],cmd[1])
            transformations.append((cmd[0],cmd[1]))
        # Handle commandas
        elif len(cmd) >= 1 and cmd[0] in cmds:
            source = cmds[cmd[0]](source, transformations, cmd)
        else:
            print "Invalid command", cmds.keys()
            continue
colorama.init()
print colorama.Style.BRIGHT,
main()
