import itertools
import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def extract_ring_and_M(witness):
    """
    Parses the witness into (R_elements, add, mul, zero, one, M_set).
    Supports multiple convenient formats for Boolean rings.
    """
    # Case 1: witness is a tuple (n, M) where R is Z_2^n
    if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], int):
        n, M_list = witness
        if not isinstance(n, int) or n < 1 or n > 6:
            return None
        R_elements = list(itertools.product([0, 1], repeat=n))
        def add(x, y): return tuple(a^b for a,b in zip(x,y))
        def mul(x, y): return tuple(a&b for a,b in zip(x,y))
        zero = tuple([0]*n)
        one = tuple([1]*n)
        try:
            if n == 1 and all(isinstance(x, int) for x in M_list):
                M_set = set((x,) for x in M_list)
            else:
                M_set = set(M_list)
        except Exception:
            return None
        return R_elements, add, mul, zero, one, M_set

    # Case 2: witness is just M (list/set of tuples or ints)
    if isinstance(witness, (list, set, tuple)):
        try:
            M_set = set(witness)
            if not M_set:
                n = 1
            else:
                first = next(iter(M_set))
                if not isinstance(first, tuple):
                    if all(isinstance(x, int) for x in M_set):
                        n = 1
                        M_set = set((x,) for x in M_set)
                    else:
                        return None
                else:
                    n = len(first)
            
            if n < 1 or n > 6: return None
            R_elements = list(itertools.product([0, 1], repeat=n))
            def add(x, y): return tuple(a^b for a,b in zip(x,y))
            def mul(x, y): return tuple(a&b for a,b in zip(x,y))
            zero = tuple([0]*n)
            one = tuple([1]*n)
            return R_elements, add, mul, zero, one, M_set
        except Exception:
            pass

    # Case 3: witness is explicitly (R, add, mul, zero, one, M)
    if isinstance(witness, tuple) and len(witness) == 6:
        R, add_f, mul_f, z, o, M = witness
        try:
            R_elements = list(R)
            M_set = set(M)
            return R_elements, add_f, mul_f, z, o, M_set
        except Exception:
            pass

    return None

def check_H1(R_elements, add, mul, zero, one):
    try:
        if zero is None or one is None: return False
        if zero == one: return False
        if zero not in R_elements or one not in R_elements: return False
        
        # Check closure and Boolean property (x^2 = x)
        for x in R_elements:
            if mul(x, x) != x: return False
            for y in R_elements:
                if add(x, y) not in R_elements: return False
                if mul(x, y) not in R_elements: return False
                
        # Check abelian group under add
        for x in R_elements:
            if add(x, zero) != x: return False
            if add(zero, x) != x: return False
            if add(x, x) != zero: return False
            for y in R_elements:
                if add(x, y) != add(y, x): return False
                for z in R_elements:
                    if add(add(x, y), z) != add(x, add(y, z)): return False
                    
        # Check mul properties (identity, commutativity, associativity, distributivity)
        for x in R_elements:
            if mul(x, one) != x: return False
            if mul(one, x) != x: return False
            for y in R_elements:
                if mul(x, y) != mul(y, x): return False
                for z in R_elements:
                    if mul(mul(x, y), z) != mul(x, mul(y, z)): return False
                    if mul(x, add(y, z)) != add(mul(x, y), mul(x, z)): return False
                    
        return True
    except Exception:
        return False

def check_M_subset(R_elements, M_set):
    return all(x in R_elements for x in M_set)

def is_ideal(R_elements, add, mul, zero, M_set):
    if not M_set: return False
    if zero not in M_set: return False
    for x in M_set:
        for y in M_set:
            if add(x, y) not in M_set: return False
        for r in R_elements:
            if mul(x, r) not in M_set: return False
    return True

def is_maximal_ideal(R_elements, add, mul, zero, one, M_set):
    if not is_ideal(R_elements, add, mul, zero, M_set): return False
    if one in M_set: return False # Must be a proper ideal
    
    # Check if any strictly larger ideal is the whole ring
    for x in R_elements:
        if x not in M_set:
            gen_ideal = set()
            for m in M_set:
                for r in R_elements:
                    gen_ideal.add(add(m, mul(r, x)))
            if one not in gen_ideal:
                return False
    return True

def condition_C(R_elements, add, mul, zero, one, M_set):
    for x in R_elements:
        neg_x = None
        for y in R_elements:
            if add(x, y) == zero:
                neg_x = y
                break
        if neg_x is None: neg_x = x
        one_minus_x = add(one, neg_x)
        
        in_M_x = x in M_set
        in_M_1_minus_x = one_minus_x in M_set
        if in_M_x == in_M_1_minus_x:
            return False
    return True

def conditions(witness) -> list[bool]:
    extracted = extract_ring_and_M(witness)
    if extracted is None:
        return [False, False]
    
    R_elements, add, mul, zero, one, M_set = extracted
    
    try:
        h1 = check_H1(R_elements, add, mul, zero, one) and check_M_subset(R_elements, M_set)
    except Exception:
        h1 = False
        
    try:
        is_max = is_maximal_ideal(R_elements, add, mul, zero, one, M_set)
        cond_c = condition_C(R_elements, add, mul, zero, one, M_set)
        neg_q = (is_max != cond_c)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring with multiplicative identity 1 and M is a subset of R",
    "¬Q: M is a maximal ideal iff exactly one of x and 1-x is in M is FALSE"
]

N_HYP = 1
NEG_Q_INDEX = 1