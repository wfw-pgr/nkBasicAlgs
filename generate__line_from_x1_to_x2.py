import numpy as np


# ========================================================= #
# ===  generate line from x1 to x2                      === #
# ========================================================= #
def generate__line_from_x1_to_x2( x1=[0.0,0.0], x2=[1.0,1.0], nDiv=101 ):

    dim       = len( x1 )

    if   ( dim == 2 ):
        ret       = np.zeros( (nDiv,2) )
        tval      = np.linspace( 0.0, 1.0, nDiv )
        ret[:,0]  = ( x2[0] - x1[0] ) * tval + x1[0]
        ret[:,1]  = ( x2[1] - x1[1] ) * tval + x1[1]

    elif ( dim == 3 ):
        ret       = np.zeros( (nDiv,3) )
        tval      = np.linspace( 0.0, 1.0, nDiv )
        ret[:,0]  = ( x2[0] - x1[0] ) * tval + x1[0]
        ret[:,1]  = ( x2[1] - x1[1] ) * tval + x1[1]
        ret[:,2]  = ( x2[2] - x1[2] ) * tval + x1[2]
        
    return( ret )


# ======================================== #
# ===  実行部                          === #
# ======================================== #
if ( __name__=="__main__" ):

    x1      = [ 0.0, 0.0, 0.0 ]
    x2      = [ 1.0, 1.0, 0.0 ]
    nDiv    = 101
    outFile = "out.dat"

    ret     = generate__line_from_x1_to_x2( x1=x1, x2=x2, nDiv=nDiv )

    with open( outFile, "w" ) as f:
        np.savetxt( f, ret )
