import numpy as np

# ========================================================= #
# ===  pileup Array ( join multiple arrays into 1 )     === #
# ========================================================= #
def pileupArray( arrs=None, NewAxis=True, axis=-1 ):
    if ( arrs is None ):
        sys.exit( "pileupArray( arr=( x,y,z,...), NoNewAxis=Bool, axis=integer )" )
    if ( NewAxis ):
        return( np.concatenate( [ arr[...,np.newaxis] for arr in arrs ], axis=-1 ) )
    else:
        return( np.concatenate( [ arr for arr in arrs], axis=axis ) )


# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):

    arr = + np.reshape( ( np.arange( 100 ) ), (10,10) )
    brr = - np.reshape( ( np.arange( 100 ) ), (10,10) )
    
    ret = pileupArray( ( arr, brr ) )
    print( ret.shape )

    ret = pileupArray( ( arr, brr ), NewAxis=False )
    print( ret.shape )
