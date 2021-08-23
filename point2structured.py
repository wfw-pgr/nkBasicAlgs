import os,sys
import numpy as np


# ========================================================= #
# ===  point2structured.py                              === #
# ========================================================= #

def point2structured( Data=None, dim=3 ):

    # ------------------------------------------------- #
    # --- [1] Argument Check                        --- #
    # ------------------------------------------------- #
    if ( Data is None ): sys.exit( "[point2structured] Data == ???" )

    # ------------------------------------------------- #
    # --- [2] size check                            --- #
    # ------------------------------------------------- #
    nPoint = Data.shape[0]
    nData  = Data.shape[1]

    if   ( dim == 2 ):
        x1,x2    = Data[:,0], Data[:,1]
        LI,LJ    = len( set( x1 ) ), len( set( x2 ) )
        if ( nPoint != LI*LJ ):
            print( "[point2structured] size incompatible... (LI,LJ) == ({0},{1}) "\
                   .format( LI,LJ ) )
            sys.exit()
        else:
            shape = (LJ,LI,nData)
        
    elif ( dim == 3 ):
        x1,x2,x3 = Data[:,0], Data[:,1], Data[:,2]
        LI,LJ,LK = len( set( x1 ) ), len( set( x2 ) ), len( set( x3 ) )
        if ( nPoint != LI*LJ*LK ):
            print( "[point2structured] size incompatible... (LI,LJ,LK) == ({0},{1},{2}) "\
                   .format( LI,LJ,LK ) )
            sys.exit()
        else:
            shape = (LK,LJ,LI,nData)
            
    # ------------------------------------------------- #
    # --- [3] reshape & return                      --- #
    # ------------------------------------------------- #
    ret = np.reshape( Data, shape )
    return( ret )
    

# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):

    import nkUtilities.equiSpaceGrid as esg
    x1MinMaxNum = [ -1.0, 1.0, 11 ]
    x2MinMaxNum = [ -2.0, 2.0, 21 ]
    x3MinMaxNum = [  3.0, 4.0,  5 ]
    Data        = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                     x3MinMaxNum=x3MinMaxNum, returnType = "point" )
    
    ret         = point2structured( Data=Data )

    print( ret[:,:,0,0] )
    
    print( Data.shape )
    print( ret.shape  )
