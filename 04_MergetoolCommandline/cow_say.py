import cmd
import shlex
from cowsay import cowsay, list_cows, cowthink, make_bubble


class Cow(cmd.Cmd):
    prompt = '>'

    def do_list_cows(self, args):
        """Lists all cow file names in the given directory"""

        args = shlex.split(args)
        if len(args) == 1:
            print(list_cows(args[0]))
        else:
            print(list_cows())

    def do_make_bubble(self, args):
        """Wraps text is wrap_text is true, then pads text and sets inside a bubble. This is the text that appears above the cows"""
        args = shlex.split(args)
        #brackets = args[args.index("-b") + 1] if "-b" in args else "cowsay"
        #width = args[args.index("-d") + 1] if "-d" in args and args[args.index("-d") + 1].isdigit() else '40'

        print(make_bubble(args[0]))
        '''brackets=brackets, width=int(width)))'''

    def do_cowsay(self, args):
        """Similar to the cowsay command. Parameters are listed with their corresponding options in the cowsay command. Returns the resulting cowsay string"""
        args = shlex.split(args)

        cow = args[args.index("-c") + 1] if "-c" in args else "default"
        eyes = args[args.index("-e") + 1] if "-e" in args else 'oo'
        tongue = args[args.index("-T") + 1] if "-T" in args else ''

        print(cowsay(args[0], cow=cow, eyes=eyes, tongue=tongue))

    def do_cowthink(self, args):
        """Similar to the cowthink command. Parameters are listed with their corresponding options in the cowthink command. Returns the resulting cowthink string"""

        args = shlex.split(args)

        cow = args[args.index("-c") + 1] if "-c" in args else "default"
        eyes = args[args.index("-e") + 1] if "-e" in args else 'oo'
        tongue = args[args.index("-T") + 1] if "-T" in args else ''

        print(cowthink(args[0], cow=cow, eyes=eyes, tongue=tongue))

    def complete_cowsay(self, prefix, line, start, end):
        vars = ["-e 00 -T U", "-e XX -T V", "-e :: -T G", "-e JJ -t C", "-e 88 -T J"]
        print(prefix, line, start, end)
        return [s for s in vars if s.startswith(prefix)]
    
    def complete_cowthink(self, prefix, line, start, end):
        vars = ["-e 00 -T U", "-e XX -T V", "-e :: -T G", "-e JJ -t C", "-e 88 -T J"]
        print(prefix, line, start, end)
        return [s for s in vars if s.startswith(prefix)]
        
    def complete_make_bubble(self, prefix, line, start, end):
        vars = ["cowsay", "cowthink"]
        return [i for i in vars if i.startswith(text)]

Cow().cmdloop()
