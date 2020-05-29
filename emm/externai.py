import os
import emm
import emm.ast as ast
import emm.symbol_table
import math
import random
import sys

#I simboliu lentele irasome ivariu Python native funkciju, kurias galime kviesti is savo kalbos
def array_push(arr: list, value):
    arr.append(value)


def array_pop(arr: list):
    return arr.pop()


def array_insert(arr: list, i: int, x):
    arr.insert(i, x)


def array_remove(arr: list, i: int):
    return arr.pop(i)


def array_reverse(arr: list):
    arr.reverse()


def array_sort(arr: list):
    arr.sort()


def declare_env(s: emm.symbol_table.SymbolTable):
    f = ast.BuiltInFunction

    # globalai
    s.set_sym('argv', sys.argv)

    # Matematines funkcijos
    s.set_func('int', f(int))
    s.set_func('float', f(float))
    s.set_func('round', f(round))
    s.set_func('abs', f(abs))
    s.set_func('log', f(math.log))
    s.set_func('log2', f(math.log))
    s.set_func('rand', f(random.random))
    s.set_func('randrange', f(random.randrange))
    s.set_func('sin', f(math.sin))
    s.set_func('cos', f(math.cos))
    s.set_func('tan', f(math.tan))
    s.set_func('atan', f(math.atan))

    # Array funkcijos
    s.set_func('array_insert', f(array_insert))
    s.set_func('array_pop', f(array_pop))
    s.set_func('array_push', f(array_push))
    s.set_func('array_remove', f(array_remove))
    s.set_func('array_reverse', f(array_reverse))
    s.set_func('array_sort', f(array_sort))
    s.set_func('len', f(len))

    # nuskaityti inputa
    s.set_func('read', f(input))