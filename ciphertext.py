import colorama
import ast

class CipherText():
    def __init__(self, source):
        if type(source) in set([bytes, str]):
            self.source = [("Encoded", s) for s in source]
        self.transformations = []

    def stats(self, **kwargs):
        counts = {}
        for code in self.source:
            counts[code] = counts.get(code,0)+1
        print(sorted(counts.items(), key=lambda x:x[1]))

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
        return self.source

    def load_transformations(self, cmd, **kwargs):
        if len(cmd) != 2:
            print("Need to specify input file")
            return source
        afile = open(cmd[1])
        new_transformations = ast.literal_eval(afile.read()) # TODO: Make this more secure
        for i in range(len(self.transformations)):
            self.undo()
        for transform in new_transformations:
            self.new_transformation((transform[0][1], transform[1][1]))
        return self.source

    def new_transformation(self, cmd, **kwargs):
        if ("Decoded", cmd[1]) in self.source:
            print("Already in use")
            return
        transform = (("Encoded", cmd[0]), ("Decoded", cmd[1]))
        print(transform)
        self.replace(transform[0], transform[1])
        self.transformations.append(transform)

    def __str__(self):
        acc = ""
        for e in self.source:
            t, s = e
            if t == "Encoded":
                acc += s
            else:
                acc += colorama.Fore.RED + s + colorama.Fore.WHITE
        return acc


