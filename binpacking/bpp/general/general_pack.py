import bpp.variables as var
from bpp.general.repack import recpack

def general_pack(info, boxes):
    """General packing procedure, which tests whether boxes f..l can be packed
    into a single bin. The algorithm is based on constraint programming, where
    each pair of boxes initially has an associated relation with domain LEFT,
    RIGHT, UNDER, ABOVE, FRONT, BEHIND. Then the recursive algorithm "recpack"
    is called, which repeatedly tries to assign the relation a value, using
    constraint propagation to decrease the domains of remaining boxes.
    """
    
    var.initVariables() # Dirty hack !!! Clear global variables !!! 
    
    feasible = False
    terminate = False
    
    var.bblevel = 1
    n = len(boxes)
#     n = l - f + 1
    
    # if n > info.exactn:
    #     info.exactn = n

    for i in xrange(n):
        for j in xrange(n):
            var.relation[i][j] = var.UNDEF
            for k in xrange(var.LEFT, var.UNDEF):
                var.domain[i][j][k] = True
#                 print "Domain[%d][%d][%d]=TRUE" % (i, j, k)
    
    var.domain[0][1][var.RIGHT ] = False
    var.domain[0][1][var.ABOVE ] = False
    var.domain[0][1][var.BEHIND] = False
    
    recpack(info, 0, 0, n, boxes, var.UNDEF)
    
    var.initVariables()
    
    return feasible