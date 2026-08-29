import itertools
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_witness_components(witness):
    if isinstance(witness, dict):
        elements = witness.get('elements')
        add = witness.get('add')
        mul = witness.get('mul')
        zero = witness.get('zero')
        one = witness.get('one')
        a = witness.get('a')
    else:
        elements = getattr(witness, 'elements', None)
        add = getattr(witness, 'add', None)
        mul = getattr(witness, 'mul', None)
        zero = getattr(witness, 'zero', None)
        one = getattr(witness, 'one', None)
        a = getattr(witness, 'a', None)
    return elements, add, mul, zero, one, a

def conditions(witness):
    try:
        elements, add, mul, zero, one, a = get_witness_components(witness)
        if elements is None:
            return [False, False]
        
        try:
            elements = list(elements)
        except TypeError:
            return [False, False]
            
        if len(elements) > 100 or len(elements) < 1:
            return [False, False]
            
        # H_1: R is a ring with identity
        # Note: We do NOT enforce associativity of multiplication, as the dropped hypothesis 
        # from the true theorem is "associative". The witness must be a non-associative ring.
        h1 = True
        if zero not in elements or one not in elements or a not in elements:
            h1 = False
            
        if h1:
            for x in elements:
                if add(x, zero) != x or add(zero, x) != x:
                    h1 = False; break
                if mul(x, one) != x or mul(one, x) != x:
                    h1 = False; break
                
                has_inv = False
                for y in elements:
                    if add(x, y) == zero and add(y, x) == zero:
                        has_inv = True
                        break
                if not has_inv:
                    h1 = False; break
                    
                for y in elements:
                    if add(x, y) not in elements: h1 = False; break
                    if mul(x, y) not in elements: h1 = False; break
                    if add(x, y) != add(y, x): h1 = False; break
                    
                    for z in elements:
                        if add(add(x, y), z) != add(x, add(y, z)): h1 = False; break
                        if mul(x, add(y, z)) != add(mul(x, y), mul(x, z)): h1 = False; break
                        if mul(add(x, y), z) != add(mul(x, z), mul(y, z)): h1 = False; break
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            # Check if a is a unit (has a two-sided inverse)
            is_unit = False
            for b in elements:
                if mul(a, b) == one and mul(b, a) == one:
                    is_unit = True
                    break
            
            # Check if L_a and R_a are bijective mappings from R to R
            def is_bijective(f):
                img = []
                for x in elements:
                    y = f(x)
                    if y not in elements:
                        return False
                    if y in img:
                        return False
                    img.append(y)
                return True
            
            L_a_bij = is_bijective(lambda x: mul(a, x))
            R_a_bij = is_bijective(lambda x: mul(x, a))
            
            # The conclusion states: a is a unit iff L_a and R_a are bijective
            conclusion = (is_unit == (L_a_bij and R_a_bij))
            
            # neg_Q is True if the conclusion FAILS
            neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring with identity",
    "¬Q: The element a is a unit iff L_a and R_a are bijective FAILS"
]

N_HYP = 1
NEG_Q_INDEX = 1