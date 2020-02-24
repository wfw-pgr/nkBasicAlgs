import numpy as np

# ========================================================= #
# ===  slice Data to get certain Data on plane or line  === #
# ========================================================= #
def sliceData( Data, xyz, Axis="x", value=0.0, eps=1.d-10 ):
    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( Data is None ): sys.exit( "[sliceData] Data == ???" )
    if ( xyz  is None ): sys.exit( "[sliceData]  xyz == ???" )

    # ------------------------------------------------- #
    # --- [2] slice Data to find certain Data       --- #
    # ------------------------------------------------- #
    x_,y_,z_ = 0,1,2
    if ( Axis=="x" ): d_ = x_
    if ( Axis=="y" ): d_ = y_
    if ( Axis=="z" ): d_ = z_
    vMin,vMax = value-eps, value+eps
    refAxis   = np.ravel( xyz[:,d_] )
    index     = np.where( ( refAxis >= vMin ) & ( refAxis <= vMax ) ) 
    if ( len( index[0] ) == 0 ):
        print( "[sliceData] WARNING !! No data :: (vMin,vMax) = ( {0}, {1} )".format( vMin, vMax ) )
        print( "[sliceData] WARNING !!         :: Axis        =   {0}       ".format( Axis       ) )
        return()

    # ------------------------------------------------- #
    # --- [3] return sliced Data                    --- #
    # ------------------------------------------------- #
    retData = Data[index] 
    retXYZ  = 


# ======================================== #
# ===  実行部                          === #
# ======================================== #
if ( __name__=="__main__" ):
    sliceData()
