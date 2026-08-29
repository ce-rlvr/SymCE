import sympy
from sympy import eye, zeros, Rational, Integer, Symbol
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a Boolean ring with a multiplicative identity 1",
    "¬Q: 1-x fails to satisfy x(1-x) = 0 and x + (1-x) = 1"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    if isinstance(witness, tuple):
        val = witness[-1]
    else:
        val = witness

    try:
        if hasattr(val, 'shape') and len(val.shape) == 2 and val.shape[0] == val.shape[1]:
            one = sympy.eye(val.shape[0])
        else:
            one = 1
            
        diff = one - val
        prod = val * diff
        add = val + diff
        h1 = True
    except Exception:
        h1 = False

    try:
        if hasattr(val, 'shape') and len(val.shape) == 2 and val.shape[0] == val.shape[1]:
            one = sympy.eye(val.shape[0])
            zero = sympy.zeros(val.shape[0], val.shape[1])
        else:
            one = 1
            zero = 0
            
        diff = one - val
        prod = val * diff
        add = val + diff
        
        prod_zero = False
        if hasattr(prod, 'simplify'):
            try:
                prod = prod.simplify()
            except Exception:
                pass
        
        if prod == zero:
            prod_zero = True
        elif hasattr(prod, 'is_zero') and prod.is_zero is True:
            prod_zero = True
            
        add_one = False
        if hasattr(add, 'simplify'):
            try:
                add = add.simplify()
            except Exception:
                pass
                
        if add == one:
            add_one = True
        elif hasattr(add, 'is_one') and add.is_one is True:
            add_one = True
            
        neg_q = not (prod_zero and add_one)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]