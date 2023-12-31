import argparse
import os
import sys
import colorama

from ciphertext import CipherText

try:
    import gnureadline as readline
except Exception:
    print("Failed to import readline")
    import dummyreadline as readline

def onexit(*args, **kwargs):
    readline.write_history_file(".cryptoquip_history")
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
    parser.add_argument('inputfiles', nargs="+", help='input files.')
    parser.add_argument('--translation-file', help='translation file to use')
    parser.add_argument('-b', action='store_true', help='batch mode')
    options = parser.parse_args(args)

    colorama.init()
    print(colorama.Style.BRIGHT,)

    sources = []
    for s in options.inputfiles:
        with open(s) as afile:
            sources.append(afile.read())

    source = "\n\n".join(sources)

    ciphertext = CipherText(source)
    if options.translation_file:
        ciphertext.load_transformations(['', options.translation_file])

    if options.b:
        print(source)
        print(ciphertext)
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
