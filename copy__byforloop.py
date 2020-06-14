import numpy as np

# ========================================================= #
# ===  copy__byforloop                                  === #
# ========================================================= #

def copy__byforloop( Data=None ):

    ret_  = np.zeros( (Data.size,) )
    Data_ = np.copy( np.ravel( Data ) )

    for ik in range( Data_.size ):
        ret_[ik] = Data_[ik]
        
    ret   = np.reshape( ret_, Data.shape )

    return( ret )


# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):

    import nkUtilities.equiSpaceGrid as esg
    x1MinMaxNum = [ 0.0, 1.0, 11 ]
    x2MinMaxNum = [ 0.0, 1.0, 11 ]
    x3MinMaxNum = [ 0.0, 1.0, 11 ]
    ret         = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                     x3MinMaxNum=x3MinMaxNum, returnType = "point" )

    ret = copy__byforloop( Data=ret )
    print( ret )
