import time
import emm.parser as p
import emm.ast
import emm.externai
import emm.exceptions
import pprint
import sys

def execute(source):
    p.disable_warnings = True
    try:
        res = p.get_parser().parse(source)
        externai.declare_env(emm.ast.symbols)

        for node in res.children:
            node.eval()
    except Exception as e:
        print(e.__class__.__name__ + ': ' + str(e), file=sys.stderr)