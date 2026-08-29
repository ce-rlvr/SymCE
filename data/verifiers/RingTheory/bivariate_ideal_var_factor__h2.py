import sympy as sp
from sympy.abc import x, y, z, a, b, c, t, u, v, w
import sympy.combinatorics.named_groups
import sympy.matrices

S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: The factor ring R(x)/(I, x) is not isomorphic to R/I"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R_obj, I_gens = witness
            if isinstance(I_gens, (list, tuple)):
                gens = list(I_gens)
            else:
                gens = [I_gens]
        else:
            if not isinstance(witness, (list, tuple)):
                gens = [witness]
            else:
                gens = list(witness)
                
        gens = [sp.sympify(g) for g in gens]
        
        if not all(isinstance(g, sp.Expr) for g in gens):
            return [False, False]
            
        symbols = set()
        for g in gens:
            symbols.update(g.free_symbols)
            
        x_sym = sp.Symbol('x')
        if x_sym in symbols:
            R_vars = sorted(list(symbols - {x_sym}), key=lambda s: s.name)
        else:
            R_vars = sorted(list(symbols), key=lambda s: s.name)
            
        H1 = True
        if isinstance(witness, tuple) and len(witness) == 2:
            R_obj = witness[0]
            if hasattr(R_obj, 'is_commutative') and R_obj.is_commutative is False:
                H1 = False
            if hasattr(R_obj, 'is_abelian') and R_obj.is_abelian is False:
                H1 = False
                
        I_0_gens = [g.subs(x_sym, 0) for g in gens]
        
        if x_sym in symbols:
            order = [x_sym] + R_vars
            gb = sp.groebner(gens, *order, order='lex')
            I_cap_R_gens = [p for p in gb if x_sym not in p.free_symbols]
        else:
            I_cap_R_gens = gens
            
        def get_gb(ideal_gens, vars):
            if not ideal_gens:
                return [sp.S.Zero]
            if not vars:
                vals = [sp.simplify(g) for g in ideal_gens]
                if any(v != 0 for v in vals):
                    return [sp.S.One]
                else:
                    return [sp.S.Zero]
            gb = sp.groebner(ideal_gens, *vars)
            return list(gb)

        gb_0 = get_gb(I_0_gens, R_vars)
        gb_cap = get_gb(I_cap_R_gens, R_vars)
        
        if gb_0 == [sp.S.One] and gb_cap != [sp.S.One]:
            neg_Q = True
        elif gb_0 != [sp.S.One] and gb_cap == [sp.S.One]:
            neg_Q = True
        elif gb_0 == [sp.S.Zero] and gb_cap != [sp.S.Zero]:
            neg_Q = True
        elif gb_0 != [sp.S.Zero] and gb_cap == [sp.S.Zero]:
            neg_Q = True
        else:
            neg_Q = (gb_0 != gb_cap)
            
    except Exception:
        return [False, False]
        
    return [H1, neg_Q]