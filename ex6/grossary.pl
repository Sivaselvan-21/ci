% ----------- FACTS (Item, Price) -----------

item(rice, 50).
item(wheat, 40).
item(milk, 30).
item(sugar, 45).
item(oil, 120).

% ----------- ADD NEW ITEM -----------

add_item(Name, Price) :-
    assertz(item(Name, Price)),
    write('Item added successfully!'), nl.

% ----------- GET PRICE -----------

get_price(Item, Price) :-
    item(Item, Price).

% ----------- CALCULATE SUBTOTAL -----------

% Subtotal = Price * Quantity
subtotal(Item, Quantity, Subtotal) :-
    item(Item, Price),
    Subtotal is Price * Quantity.

% ----------- ORDER MULTIPLE ITEMS -----------

% Base case
total([], 0).

% Recursive case
total([[Item, Qty] | Rest], Total) :-
    subtotal(Item, Qty, Sub),
    total(Rest, RestTotal),
    Total is Sub + RestTotal.

% ----------- DISPLAY BILL -----------

print_bill([]).
print_bill([[Item, Qty] | Rest]) :-
    subtotal(Item, Qty, Sub),
    write(Item), write(' x '), write(Qty),
    write(' = '), write(Sub), nl,
    print_bill(Rest).

% ----------- FINAL ORDER SYSTEM -----------

order(Items) :-
    write('----- BILL -----'), nl,
    print_bill(Items),
    total(Items, Total),
    write('----------------'), nl,
    write('Total Amount: '), write(Total), nl.
