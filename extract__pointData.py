import numpy as np


# ========================================================= #
# ===  extract the dimension of the data                === #
# ========================================================= #
def extract__pointData( Data=None, ref_=None, vMin=None, vMax=None, epsilon=1.e-8, value=0.0 ):
    # -- Data :: [nData,nComponents] -- #
    if ( Data is None ): sys.exit( "[extract__pointData] Data == ???" )
    if ( vMin is None ): vMin = value - epsilon
    if ( vMax is None ): vMax = value + epsilon
    if ( ref_ is None ):
        print( "[extract__pointData] ref_ :: not specified :: default ref_=0..." )
        ref_ = 0
    
    index    = np.where( ( ( Data[:,ref_] > vMin ) & ( Data[:,ref_] < vMax ) ) )
    lenFound = np.size( index[0] )
    if (  lenFound == 0 ):
        print( "[extract__pointData] No element was found :: (vMin,vMax) = ({0},{1})"\
               .format( vMin, vMax ) )
        return( None )
    else:
        ret = Data[ index ][:]
        return( ret )



# ======================================== #
# ===  実行部                          === #
# ======================================== #
if ( __name__=="__main__" ):

    import nkUtilities.generate__testprofile as gtp
    x1MinMaxNum = [ 0.0, 1.0, 11 ]
    x2MinMaxNum = [ 0.0, 1.0, 11 ]
    x3MinMaxNum = [ 0.0, 1.0, 11 ]
    vMin, vMax  = 0.0, 1.0
    ret         = gtp.generate__testprofile( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                             x3MinMaxNum=x3MinMaxNum, returnType ="point", \
                                             vMin       =vMin       , vMax       =vMax )
    ret = extract__pointData( Data=ret, ref_=1, value=0.2 )
    print( ret )
