% Addition
add(X, Y, Result) :- Result is X + Y.

% Subtraction
sub(X, Y, Result) :- Result is X - Y.

% Multiplication
mul(X, Y, Result) :- Result is X * Y.

% Division (Floating point)
div(X, Y, Result) :- 
    Y =\= 0, 
    Result is X / Y.

% Integer Division
idiv(X, Y, Result) :- 
    Y =\= 0, 
    Result is X // Y.

% Modulo (Remainder)
mod_op(X, Y, Result) :- 
    Y =\= 0, 
    Result is X mod Y.

% Power (Exponentiation)
pow(X, Y, Result) :- Result is X ** Y.

