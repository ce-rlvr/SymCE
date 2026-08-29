import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def check_bool_attr(obj, attr):
    if not hasattr(obj, attr):
        return None
    val = getattr(obj, attr)
    if callable(val):
        return val()
    return val

def is_dp_nonabelian_simple(G):
    if hasattr(G, 'is_dp_nonabelian_simple'):
        val = getattr(G, 'is_dp_nonabelian_simple')
        return val() if callable(val) else bool(val)
    
    try:
        is_simp = check_bool_attr(G, 'is_simple')
        is_ab = check_bool_attr(G, 'is_abelian')
        if is_simp is True and is_ab is False:
            return True
    except Exception:
        pass

    try:
        order_attr = getattr(G, 'order')
        order = order_attr() if callable(order_attr) else order_attr
        if order <= 1:
            return False
        
        comp_attr = getattr(G, 'composition_series')
        series = comp_attr() if callable(comp_attr) else comp_attr
        
        for i in range(len(series) - 1):
            o1_attr = getattr(series[i], 'order')
            o1 = o1_attr() if callable(o1_attr) else o1_attr
            
            o2_attr = getattr(series[i+1], 'order')
            o2 = o2_attr() if callable(o2_attr) else o2_attr
            
            factor_order = o1 // o2
            if sympy.isprime(factor_order):
                return False
        return True
    except Exception:
        pass

    return False

def frattini_is_nontrivial(G):
    if hasattr(G, 'frattini_is_nontrivial'):
        val = getattr(G, 'frattini_is_nontrivial')
        return val() if callable(val) else bool(val)
    
    try:
        if hasattr(G, 'frattini_subgroup'):
            frat_attr = getattr(G, 'frattini_subgroup')
            frat = frat_attr() if callable(frat_attr) else frat_attr
            forder = frat.order() if callable(frat.order) else frat.order
            return forder > 1
    except Exception:
        pass

    try:
        if hasattr(G, 'maximal_subgroups'):
            max_attr = getattr(G, 'maximal_subgroups')
            max_subs = max_attr() if callable(max_attr) else max_attr
            
            if not max_subs:
                order_attr = getattr(G, 'order')
                order = order_attr() if callable(order_attr) else order_attr
                return order > 1
            
            frat = max_subs[0]
            for H in max_subs[1:]:
                if hasattr(frat, 'intersection'):
                    frat = frat.intersection(H)
                else:
                    frat = frat.intersect(H)
                
                forder = frat.order() if callable(frat.order) else frat.order
                if forder == 1:
                    return False
            
            forder = frat.order() if callable(frat.order) else frat.order
            return forder > 1
    except Exception:
        pass

    return False

def conditions(witness) -> list[bool]:
    try:
        h1 = is_dp_nonabelian_simple(witness)
    except Exception:
        h1 = False
        
    try:
        neg_q = frattini_is_nontrivial(witness)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is isomorphic to a direct product of non-abelian simple groups",
    "¬Q: The Frattini subgroup of G is not the trivial subgroup"
]

N_HYP = 1
NEG_Q_INDEX = 1