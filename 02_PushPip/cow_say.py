import cowsay
import argparse
import sys

parsing = argparse.ArgumentParser()

parsing.add_argument('message', type=str, nargs='?', default='',  help='Cows message')
parsing.add_argument('-e', '--eye', default='oo', help='Option initiates Borg mode')
parsing.add_argument('-f', '--cowfile', help='option specifies a particular cow picture file to use')
parsing.add_argument('-l', default='default', help='List all cowfiles on the current COWPATH')
parsing.add_argument('-p', '--paranoia',  dest='p', action='store_true', help='Causes a state of paranoia to come over the cow')
parsing.add_argument('-d', '--dead', dest='d', action='store_true', help='Causes the cow to appear dead')
parsing.add_argument('-s', '--stoned', dest='s', action='store_true')
parsing.add_argument('-t', '--tired', dest='t', action='store_true', help='Tired cow')
parsing.add_argument('-T', '--tongue', default='', help='Manually specifies the cow′s tongue shape')
parsing.add_argument('-W', '--width', default=40, type=int, help='Specifies width of the speech balloon in columns')
parsing.add_argument('-y', '--youth',  dest='y', action='store_true', help='Brings on the cows youthful apperance')
parsing.add_argument('-b', '--borg', dest='b', action='store_true', help='Option initiates Borg mode')
parsing.add_argument('-g', '--greedy', dest='g', action='store_true', help='Invokes greedy mode')
parsing.add_argument('-n', '--wrap', dest='wrap', action='store_true')

args = parsing.parse_args()

if args.l != 'default':
    print(cowsay.list_cows())
else:
    basic = 'dpstybg'
    preset = ''
    for i in basic:
        if i in args.__dict__:
            preset += i

    #print(preset)
    print(cowsay.cowsay(message=args.message, eyes=args.eye, tongue=args.tongue, width=args.width, cowfile=args.cowfile, preset=preset, wrap_text=args.wrap))