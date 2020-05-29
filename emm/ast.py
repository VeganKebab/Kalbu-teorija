import operator
from types import LambdaType
from emm.exceptions import *
import emm.symbol_table

symbols = emm.symbol_table.SymbolTable()

#AST sintakses medis
#Kiekvienam opearcijos elementui aprasoma klase, kuri evaluatina isvedima, papildo simboliu lentele ir t.t

#Operaciju saraso tipas. Grazinamas listas su evaluatinatias operaciju rezultatais
class InstructionList:
    def __init__(self, children=None):
        if children is None:
            children = []
        self.children = children

    def __len__(self):
        return len(self.children)

    def __iter__(self):
        return iter(self.children)

    def eval(self):
        ret = []
        for n in self:
            if isinstance(n, ExitStatement):
                return n

            res = n.eval()

            if isinstance(res, ExitStatement):
                return res
            elif res is not None:
                ret.append(res)

        return ret

#Bazine ekspresija
class BaseExpression:
    def eval(self):
        raise NotImplementedError()

#Uzbagimas
class ExitStatement(BaseExpression):
    def __iter__(self):
        return []

    def eval(self):
        pass

#Grazinimas
class ReturnStatement(ExitStatement):
    def __init__(self, expr: BaseExpression):
        self.expr = expr

    def eval(self):
        return full_eval(self.expr)

#Pilna evaluatiniti visa ekspresiona
def full_eval(expr: BaseExpression):
    while isinstance(expr, BaseExpression):
        expr = expr.eval()

    return expr


class Primitive(BaseExpression):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value

#Gavimas per identifikatoriu
class Identifier(BaseExpression):
    is_function = False #Numatytu atveju tai ne funkcija

    def __init__(self, name):
        self.name = name

    def assign(self, val):
        if self.is_function:
            symbols.set_func(self.name, val)
        else:
            symbols.set_sym(self.name, val)

    def eval(self):
        if self.is_function: #Pasiemame funkcija
            return symbols.get_func(self.name)

        return symbols.get_sym(self.name) #Kitu atveju pasiemame kintamji

#Masyvas
class Array(BaseExpression):
    def __init__(self, values: InstructionList):
        self.values = values

    def eval(self):
        return self.values.eval()


class ArrayAccess(BaseExpression):
    def __init__(self, array: Identifier, index: BaseExpression):
        self.array = array
        self.index = index


    def eval(self):
        return self.array.eval()[self.index.eval()]


class ArrayAssign(BaseExpression):
    def __init__(self, array: Identifier, index: BaseExpression, value: BaseExpression):
        self.array = array
        self.index = index
        self.value = value

    def eval(self):
        self.array.eval()[self.index.eval()] = self.value.eval()


#Priskyrimas
class Assignment(BaseExpression):
    def __init__(self, identifier: Identifier, val):
        self.identifier = identifier
        self.val = val

    def eval(self):
        if self.identifier.is_function:
            self.identifier.assign(self.val)
        else:
            self.identifier.assign(self.val.eval())



class BinaryOperation(BaseExpression):
    __operations = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '**': operator.pow,
        '/': operator.truediv,
        '%': operator.mod,

        '>': operator.gt,
        '>=': operator.ge,
        '<': operator.lt,
        '<=': operator.le,
        '==': operator.eq,
        '!=': operator.ne,

        'and': lambda a, b: a.eval() and b.eval(),
        'or': lambda a, b: a.eval() or b.eval(),
    }

    def __init__(self, left, right, op):
        self.left = left
        self.right = right
        self.op = op

    def eval(self):
        left = None
        right = None

        
        # parenkame kokia operacija bus ivikdyta
        op = self.__operations[self.op]

        # and or atveju 
        if isinstance(op, LambdaType):
            return op(self.left, self.right)

        #Paprastu atveju kvieciame matematine operacija
        left = self.left.eval()
        right = self.right.eval()
        return op(left, right)

#Sutrumpintos matematines operacijos
class CompoundOperation(BaseExpression):
    __operations = {
        '+=': operator.iadd,
        '-=': operator.isub,
    }

    def __init__(self, identifier: Identifier, modifier: BaseExpression, operation: str):
        self.identifier = identifier
        self.modifier = modifier
        self.operation = operation

    def eval(self):
        #Sutrumpintus operatorius paverciame paprastomis matematinemis operacijomis

        l = self.identifier.eval()
        r = self.modifier.eval()
        self.identifier.assign(self.__operations[self.operation](l, r))

#Vieno argumento opearotriai
class UnaryOperation(BaseExpression):
    __operations = {
        '+': operator.pos,
        '-': operator.neg,
        '~': operator.inv,
        'not': operator.not_,
    }

    def __init__(self, operation, expr: BaseExpression):
        self.operation = operation
        self.expr = expr

    def eval(self):
        return self.__operations[self.operation](self.expr.eval())

#Klase musu string funkcijoms atlikti
class ToUpper(BaseExpression):

    def __init__(self, op, expr: BaseExpression):
        self.op = op
        self.expr = expr

    def eval(self):
        if self.op == 'upp':
            return str(self.expr.eval()).upper()
        if self.op == 'low':
            return str(self.expr.eval()).lower()
        if self.op == '#':
            return len(str(self.expr.eval()))

class If(BaseExpression):
    def __init__(self, condition: BaseExpression, truepart: InstructionList, elsepart=None):
        self.condition = condition
        self.truepart = truepart
        self.elsepart = elsepart

    def eval(self):
        if self.condition.eval():
            return self.truepart.eval()
        elif self.elsepart is not None:
            return self.elsepart.eval()

#For loopas. Gali buti kylantis arba leidziantis
class For(BaseExpression):
    def __init__(self, variable: Identifier, start: Primitive, end: Primitive, asc: bool, body: InstructionList):
        self.variable = variable
        self.start = start
        self.end = end
        self.asc = asc  
        self.body = body

    def eval(self):
        if self.asc:
            lo = self.start.eval()
            hi = self.end.eval() + 1
            sign = 1
        else:
            lo = self.start.eval()
            hi = self.end.eval() - 1
            sign = -1

        #Vykdome python for loopa ir eval teiginius
        for i in range(lo, hi, sign):
            self.variable.assign(i)

            # exit aveju stapbdome loop'a
            if isinstance(self.body.eval(), ExitStatement):
                break


class ForIn(BaseExpression):
    def __init__(self, variable: Identifier, sequence: BaseExpression, body: InstructionList):
        self.variable = variable
        self.sequence = sequence
        self.body = body

    def eval(self):
        for i in self.sequence.eval():
            self.variable.assign(i)
            if isinstance(self.body.eval(), ExitStatement):
                break

#Spausdinimo apdorojimas
class PrintStatement(BaseExpression):
    def __init__(self, items: InstructionList):
        self.items = items

    def eval(self):
        print(*self.items.eval(), end='', sep='')

#Funkcijos kvietimas
class FunctionCall(BaseExpression):
    def __init__(self, name: Identifier, params: InstructionList):
        self.name = name
        self.params = params

    def __eval_builtin_func(self):
        func = self.name.eval()
        args = []

        for p in self.params:
            args.append(full_eval(p))

        return func.eval(args)

    def __eval_udf(self):
        func = self.name.eval()
        args = {}

        # Kiek tikimes argumentu ir kiek ju pateikta
        l1 = len(func.params)
        l2 = len(self.params)

        if l1 != l2:
            msg = "Invalid number of arguments for function {0}. Expected {1} got {2}"

        #Suporuojame argumentu pavadinimus su kvieciamom reiksmem (jas pirma ivertiname)
        for p, v in zip(func.params, self.params):
            args[p.name] = full_eval(v)

        return func.eval(args)

    def eval(self):
        #Tikriname ar naudojama externo funkcija ir ja kvieciame
        if isinstance(self.name.eval(), BuiltInFunction):
            return self.__eval_builtin_func()
        #Kitu atveju paleidziame musu numatyta funckcija
        return self.__eval_udf()

#Funkcijos objetkas
class Function(BaseExpression):
    def __init__(self, params: InstructionList, body: InstructionList):
        self.params = params #Parametrai
        self.body = body #kunas

    def eval(self, args):
        symbols.set_local(True) #Nustatome kad simboliai bus vietiniai

        for k, v in args.items():
            symbols.set_sym(k, v) #I simboliu lentele irasome argumentus (pavadinimas, reiksme)

        try:
            ret = self.body.eval() #Eval funkcijos kuna

            if isinstance(ret, ReturnStatement): #Jeigu sutinkame ReturnStatement - graziname jo reiksme
                return ret.eval()
        finally:
            symbols.set_local(False) #Baigiasi funkcija - nebelokalus kintamieji

        return None #Funkcija gali ir nieo negrazinti


class BuiltInFunction(BaseExpression):
    def __init__(self, func):
        self.func = func

    def eval(self, args):
        return self.func(*args)