import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.DihedralGroup(2)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def extract_bool(witness, names):
    for name in names:
        if hasattr(witness, name):
            val = getattr(witness, name)
            if callable(val):
                try: 
                    res = val()
                    if res is not None:
                        return bool(res)
                except: 
                    pass
            else:
                try: 
                    if val is not None:
                        return bool(val)
                except: 
                    pass
    if isinstance(witness, dict):
        for name in names:
            if name in witness and witness[name] is not None:
                return bool(witness[name])
    return None

def check_subset(IJ, Ann):
    if isinstance(IJ, int) and isinstance(Ann, int):
        if Ann == 0:
            return IJ == 0
        return IJ % Ann == 0
    try:
        if hasattr(IJ, 'gens') and hasattr(Ann, 'contains'):
            return all(Ann.contains(g) for g in IJ.gens)
    except:
        pass
    try:
        return IJ.issubset(Ann)
    except:
        pass
    try:
        return IJ <= Ann
    except:
        pass
    return False

def conditions(witness):
    h1 = extract_bool(witness, ['check_H1', 'check_h1', 'h1', 'H1', 'is_commutative'])
    h2 = extract_bool(witness, ['check_H2', 'check_h2', 'h2', 'H2', 'is_module_M'])
    h3 = extract_bool(witness, ['check_H3', 'check_h3', 'h3', 'H3', 'is_annihilator_I'])
    h4 = extract_bool(witness, ['check_H4', 'check_h4', 'h4', 'H4', 'is_annihilator_J'])
    neg_q = extract_bool(witness, ['check_neg_Q', 'check_neg_q', 'neg_Q', 'neg_q', 'fails_conclusion'])

    if any(x is not None for x in [h1, h2, h3, h4, neg_q]):
        return [
            bool(h1) if h1 is not None else False,
            bool(h2) if h2 is not None else False,
            bool(h3) if h3 is not None else False,
            bool(h4) if h4 is not None else False,
            bool(neg_q) if neg_q is not None else False
        ]

    h1, h2, h3, h4, neg_q = False, False, False, False, False

    if isinstance(witness, tuple):
        if len(witness) == 2:
            I, J = witness
            R = getattr(I, 'ring', None)
            M, N = None, None
        elif len(witness) == 3:
            R, I, J = witness
            M, N = None, None
        elif len(witness) == 5:
            R, M, N, I, J = witness
        else:
            I, J = None, None
            
        if I is not None and J is not None:
            try:
                if isinstance(I, int) and isinstance(J, int):
                    h1 = True
                    h2 = True
                    h3 = True
                    h4 = True
                    IJ = I * J
                    Ann = math.gcd(I, J)
                    subset = check_subset(IJ, Ann)
                    neg_q = not subset
                    return [h1, h2, h3, h4, neg_q]
                else:
                    h1 = getattr(R, 'is_commutative', True) if R else True
                    h2 = True
                    h3 = True
                    h4 = True
                    IJ = I * J
                    Ann = None
                    if M is not None and N is not None:
                        try:
                            Ann = M.tensor_product(N).annihilator()
                        except:
                            pass
                    if Ann is None:
                        Ann = I + J
                    subset = check_subset(IJ, Ann)
                    neg_q = not subset
                    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]
            except:
                pass

    try:
        if hasattr(witness, 'R'):
            h1 = getattr(witness.R, 'is_commutative', True)
        else:
            h1 = True
            
        h2 = True
        h3 = True
        h4 = True
        
        IJ = None
        Ann = None
        
        if hasattr(witness, 'IJ'):
            IJ = witness.IJ
        elif hasattr(witness, 'I') and hasattr(witness, 'J'):
            IJ = witness.I * witness.J
            
        if hasattr(witness, 'Ann'):
            Ann = witness.Ann
        elif hasattr(witness, 'Ann_tensor'):
            Ann = witness.Ann_tensor
        elif hasattr(witness, 'M') and hasattr(witness, 'N'):
            try:
                Ann = witness.M.tensor_product(witness.N).annihilator()
            except:
                if hasattr(witness, 'I') and hasattr(witness, 'J'):
                    Ann = witness.I + witness.J
        elif hasattr(witness, 'I') and hasattr(witness, 'J'):
            Ann = witness.I + witness.J
            
        if IJ is not None and Ann is not None:
            subset = check_subset(IJ, Ann)
            neg_q = not subset
            return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]
            
    except Exception:
        pass

    return [False, False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: M is an R-module",
    "H_3: I is the annihilator ideal of M in R",
    "H_4: J is the annihilator ideal of N in R",
    "¬Q: The product ideal IJ is not a subset of the annihilator ideal of the tensor product M \\otimes_R N"
]

N_HYP = 4
NEG_Q_INDEX = 4