from bpp.variables import *
import bpp.variables as var
from bpp.general.core import DomainPair
from bpp.general.findcoordinates import findcoordinates
from bpp.logger import log

def modifyandpush(i, j, rel, dom):
    """Push the relation "rel" between box i and box j to info stack. If "dom"
    is True, the relation is removed from the domain. If "dom" is False,
    the relation "rel" is imposed between boxes "i" and "j"."""
    
    log.debug('modifyandpush [%d][%d]', i, j)
    
    if dom:
        r = rel
        var.domain[i][j][rel] = False
    else:
        r = var.relation[i][j]
        var.relation[i][j] = rel

    indexes = (i, j)

    if var.indexes2dpair.has_key(indexes):
        pair = var.indexes2dpair[indexes]
        pair.update(r, dom)
    else:
        pair = DomainPair(i, j, r, dom)
        var.domstack.append(pair)
        var.indexes2dpair[indexes] = pair

#     print 'modifyandpush:', pair

    if len(var.domstack) == STACKDEPTH:
        raise Exception("Stack filled")

def popdomains(pair):
    """Pop all relations between boxes from the stack. The stack is emptied
    downto the depth given by "pos"."""

    log.debug('popdomains [%d][%d]', pair.i, pair.j)

    if pair in var.domstack:
        i = var.domstack.index(pair)
    else:
        i = -1


    for p in var.domstack[i:]:
        var.domstack.remove(p)
        
        log.debug('popdomains action [%d][%d]', pair.i, pair.j)
    
        if pair.domain:
            var.domain[pair.i][pair.j][pair.relation] = True
        else:
            var.relation[pair.i][pair.j] = pair.relation

def checkdomain(info, i, j, n, boxes, value):
    """Temporarily impose the relation "value" between boxes "i" and "j",
    and check whether a feasible assignment of coordinates exists which
    respects all currently imposed relations. 
      If the relation cannot be satisfied, it is removed from the domain
    and pushed to a stack, so that it can be restored upon backtracking."""

    log.debug("\ncheckdomain [%d][%d] Type: %d Value: %d" , i, j, value, int(var.domain[i][j][value]))

    if var.domain[i][j][value] == False:
        return # not allowed in any case
    
    var.relation[i][j] = value

    if findcoordinates(info, boxes) == False:
        log.debug("call modifyandpush")
        modifyandpush(i, j, value, True)

def reducedomain(info, n, boxes):
    """Constraint propagation algorithm. For each relation in the domain of
    boxes "i" and "j", check if the relation has the posibility of being
    satisfied. If some of the relations cannot be satisfied any more, they
    are removed from the domain (and pushed to a stack, so that they can
    be restored when the master search algorithm backtracks). If only one
    relation remains in the domain, the relation is imposed at this node
    and all descendant nodes."""
    m = 0
    for i in xrange(0, n - 1):
        for j in xrange(i + 1, n - 1):
            if var.relation[i][j] == UNDEF:
                log.debug('reducedomain [%d][%d]', i, j)
                checkdomain(info, i, j, n, boxes, LEFT);
                checkdomain(info, i, j, n, boxes, RIGHT);
                checkdomain(info, i, j, n, boxes, UNDER);
                checkdomain(info, i, j, n, boxes, ABOVE);
                checkdomain(info, i, j, n, boxes, FRONT);
                checkdomain(info, i, j, n, boxes, BEHIND);
                var.relation[i][j] = UNDEF;
                l = 0
                for k in xrange(LEFT, UNDEF):
                    if var.domain[i][j][k]:
                        l += 1; m = k;
                
                log.debug('reducedomain [%d][%d] l=%d', i, j, l)
                if l == 0:
                    return False
                if l == 1:
                    modifyandpush(i, j, m, False)

    return True