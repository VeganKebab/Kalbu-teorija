### Dependencies ###

* Python3
* ply
* py2exe

### Features ###
* Variables
* Functions
* For loops
* If/else statements
* Loop exit statement
* String operations

### Data types ###
* Integer
* Float
* String
* Boolean
* Arrays

#### Variables ####

variables are dynamically typed immediately declared upon use `number = 42;`

#### Functions ####

functions are declared via the following grammar

    func func_name( [<arguments>,] ){
        < statements >
    }

    func random(){
        return 4;
    }

#### Conditionals ####

ntp supports `if` statements for flow control via the following syntax

    if < expression > {
        < statements >
    }

nb: Brackets are mandatory, while parenthesis on the expression are optional


### Loops ###

ntp supports `for` loops

** for syntax **

    for variable in sequence {
        < statements >
    }

nb: sequence accepts arrays and strings

    for variable in low -> high {
        < statements >
    }
    
down to loops are constructed as

    for variable in high <- low {
        < statements >
    }

nb: loop indexes are inclusive


All loops can be prematurely exited via the `exit` statement when necessary


### Arrays ###

Arrays have dynamic length and can be declared via the  `[ ... ]` expression


### Printing ###

Printing is supported via the `print` keyword which accepts a list of values to print. Note that `print` doesn't
add spaces nor newlines after printing.


### Standard library ###

Functions that were included from standard Python library:

* `read(prompt)` *shows the prompt and returns the result as a string*
* `int(x [, base])` 
* `float(x)`
* `round(value, precision)`
* `abs(x)`
* `log(x)`
* `rand`
* `randrange(lo, hi)`
* `sin(x)`
* `cos(x)`
* `tan(x)`
* `atan(x)`
* `len(str)`
* `array_insert(array, index, value)`
* `array_pop(array)` *returns removed value and modifies array*
* `array_push(array, value)`
* `array_remove(array, index)` *returns removed value and modifies array*
* `array_reverse(array)` *reverses array without returning it*
* `array_sort(array)` *sorts the array without returning it*
