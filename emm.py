import emm
import sys

if len(sys.argv) == 1:
    print("Naudojimas: %s filename" % __file__)
else:
    with open(sys.argv[1]) as f:
        emm.execute(f.read())
