import argparse
import sys
import colorama
import tempfile
try:
    import readline
except Exception:
    print("Failed to import readline")
    import dummyreadline as readline
import ast

def onexit(*args, **kwargs):
    readline.write_history_file(".cryptoquip_history")

class CipherText():
    def __init__(self, source):
        if type(source) in set([bytes, str]):
            self.source = [("Encoded", s) for s in source]
        self.transformations = []

    def replace(self, a, b):
        for i, (t,s) in enumerate(self.source[:]):
            if t == a[0] and s == a[1]:
                self.source.pop(i)
                self.source.insert(i, b)

    def undo(self, **kwargs):
        if not self.transformations:
            return
        a, b = self.transformations[-1]
        self.replace(b, a)
        self.transformations.pop(-1)

    def transforms(self, **kwargs):
        print(self.transformations)

    def remove_transform(self, cmd, **kwargs):
        if len(cmd) != 2:
            print("remove takes one argument")
            return source
        target = cmd[1]
        for transform in self.transformations:
            if transform[1] == ("Decoded", target) or transform[0] == ("Encoded", target):
               break
        self.replace(transform[1], transform[0])
        self.transformations.remove(transform)

    def save_transformations(self, cmd, **kwargs):
        if len(cmd) != 2:
            print("Need to specify output file")
            return source
        afile = open(cmd[1], "w")
        afile.write(str(self.transformations))
        return source

    def load_transformations(self, cmd, **kwargs):
        if len(cmd) != 2:
            print("Need to specify input file")
            return source
        afile = open(cmd[1])
        new_transformations = ast.literal_eval(afile.read()) # TODO: Make this more secure
        for i in range(len(transformations)):
            source = undo(source, transformations, [])
        for transform in new_transformations:
            source = new_transformation(source, transformations, transform)
        return source

    def __str__(self):
        acc = ""
        for e in self.source:
            t, s = e
            if t == "Encoded":
                acc += s
            else:
                acc += colorama.Fore.RED + s + colorama.Fore.WHITE
        return acc

    def stats(self, **kwargs):
        counts = {}
        for code in self.source:
            counts[code] = counts.get(code,0)+1
        print(sorted(counts.items(), key=lambda x:x[1]))

    def new_transformation(self, cmd, **kwargs):
        if ("Decoded", cmd[1]) in self.source:
            print("Already in use")
            return
        transform = (("Encoded", cmd[0]), ("Decoded", cmd[1]))
        self.replace(transform[0], transform[1])
        self.transformations.append(transform)

def main(args):

    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile', help='input file.')
    parser.add_argument('--translation-file', help='translation file to use')
    parser.add_argument('-b', action='store_true', help='batch mode')
    options = parser.parse_args(args)

    colorama.init()
    print(colorama.Style.BRIGHT,)

    with open(options.inputfile) as afile:
        source = afile.read()

    ciphertext = CipherText(source)
    if options.translation_file:
        ciphertext.load_transformations(['', options.translation_file])

    if options.b:
        print(source)
        return

    cmds = {'u' : ciphertext.undo,
            'stat' : ciphertext.stats,
            't' : ciphertext.transforms,
            'remove' : ciphertext.remove_transform,
            'load' : ciphertext.load_transformations,
            'save' : ciphertext.save_transformations}
    readline.read_history_file(".cryptoquip_history")
    while True:
        print(ciphertext)
        try:
            cmd = input()
        except EOFError:
            return
        cmd = cmd.split()
        if len(cmd) == 0:
            continue
        # Handle standard transform first
        elif len(cmd) == 2 and len(cmd[0]) == 1 and len(cmd[1]) == 1:
            ciphertext.new_transformation(cmd)
        # Handle commands
        elif len(cmd) >= 1 and cmd[0] in cmds:
            cmds[cmd[0]](cmd=cmd)
        else:
            print("Invalid command", cmds.keys())
            continue

if __name__ == "__main__":
    import atexit
    atexit.register(onexit)
    main(sys.argv[1:])
