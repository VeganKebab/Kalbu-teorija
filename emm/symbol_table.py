from emm.exceptions import *

#Simboliu lentele, sauganti kintamuosius ir funkcijas
class SymbolTable:
    __func = 'functions'
    __sym = 'symbols'
    __local = 'local'

    __table = {
        __func: {},
        __sym: {},
        __local: []
    }
    #Tikriname ar kintamasis yra vietinis
    def __is_local(self):
        return len(self.__table[self.__local]) > 0

    def table(self):
        return self.__table

    #Grazinam lokaliu simboliu lentele
    def get_local_table(self):
        t = self.__table[self.__local]
        return t[len(t) - 1]
    #Jeigu flag - true tai sukuriame nauja lokaliu simboliu lentele. Kitu atveju ja pasaliname
    def set_local(self, flag):
        if flag:
            self.__table[self.__local].append({})
        else:
            self.__table[self.__local].pop()

    #Grazina simboli is lenteles
    def get_sym(self, sym):
        if self.__is_local():
            # TIkriname ar egzistuoja lokalioje lenteleje
            for tab in reversed(self.__table[self.__local]):
                if sym in tab:
                    return tab[sym]

        # Kitu atveju tikrinam globalius kintamuosius
        if sym in self.__table[self.__sym]:
            return self.__table[self.__sym][sym]

        raise SymbolNotFound("Undefined variable '%s'" % sym)

    def set_sym(self, sym, val):
        if self.__is_local():
            self.get_local_table()[sym] = val
        else:
            self.__table[self.__sym][sym] = val

    def get_func(self, name):
        if name in self.__table[self.__func]:
            return self.__table[self.__func][name]

        raise SymbolNotFound("Undefined function '%s'" % name)

    def set_func(self, name, val):
        if name in self.__table[self.__func]:
            raise DuplicateSymbol("Cannot redeclare function '%s'" % name)

        self.__table[self.__func][name] = val
