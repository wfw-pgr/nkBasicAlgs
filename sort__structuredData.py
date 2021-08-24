import numpy as np

# ========================================================= #
# ===  sort__structuredData.py                          === #
# ========================================================= #

def sort__structuredData( Data=None, order="ijk", dim=3, component_index=None ):

    x_,y_,z_ = 0,1,2
    
    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( Data is None ): sys.exit( "[sort__structuredData.py] Data == ???" )
    if ( component_index is None ):
        component_index = Data.ndim - 1
        nCmp            = Data.shape[-1]
    else:
        nCmp            = Data.shape[component_index]
        sys.exit( "[sort__structuredData.py] not yet deployed. " )
        
    # ------------------------------------------------- #
    # --- [2] preparation                           --- #
    # ------------------------------------------------- #
    Data_     = Data.reshape( (-1,nCmp) )
    xa        = set( np.ravel( Data_[:,x_] ) )
    ya        = set( np.ravel( Data_[:,y_] ) )
    za        = set( np.ravel( Data_[:,z_] ) )
    LI        = len( xa )
    LJ        = len( ya )
    LK        = len( za )
    xMin,xMax = np.min( Data_[:,x_] ), np.max( Data_[:,x_] )
    yMin,yMax = np.min( Data_[:,y_] ), np.max( Data_[:,y_] )
    zMin,zMax = np.min( Data_[:,z_] ), np.max( Data_[:,z_] )

    # ------------------------------------------------- #
    # --- [3] index making                          --- #
    # ------------------------------------------------- #
    index_x   = ( ( np.ravel( Data_[:,x_] ) - xMin ) / ( xMax - xMin ) * LI )
    index_y   = ( ( np.ravel( Data_[:,y_] ) - yMin ) / ( yMax - yMin ) * LJ )
    index_z   = ( ( np.ravel( Data_[:,z_] ) - zMin ) / ( zMax - zMin ) * LK )
    idigit   = int( "1" + len( str( LI ) ) * "0" )
    jdigit   = int( "1" + len( str( LJ ) ) * "0" )
    kdigit   = int( "1" + len( str( LK ) ) * "0" )

    # ------------------------------------------------- #
    # --- [4] sorting                               --- #
    # ------------------------------------------------- #
    if   ( order.lower() == "ijk" ):
        index = index_x + index_y*idigit + index_z*idigit*jdigit
        shape = (LK,LJ,LI,nCmp)
    elif ( order.lower() == "kji" ):
        index = index_z + index_y*kdigit + index_x*jdigit*kdigit
        shape = (LI,LJ,LK,nCmp)
    sort      = np.argsort( index )
    Data_     = Data_[sort,:]
    Data_     = np.reshape( Data_, shape )
    return( Data_ )


# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):

    import nkUtilities.equiSpaceGrid as esg
    x1MinMaxNum = [ 0.0, 1.0, 11 ]
    x2MinMaxNum = [ 0.0, 1.0, 11 ]
    x3MinMaxNum = [ 0.0, 1.0, 11 ]
    coord       = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                     x3MinMaxNum=x3MinMaxNum, returnType = "point" )
    field       = np.copy( coord )
    radius      = np.sqrt( np.sum( coord**2, axis=1 ) )
    field[:,0]  = radius
    field[:,1]  = radius**2
    field[:,2]  = 1.0 + radius**3
    Data        = np.concatenate( [coord,field], axis=1 )
    LILJLK      = coord.shape[0]
    index       = np.array( list( range( LILJLK ) ), dtype=np.int64 )
    np.random.shuffle( index )
    Data        = Data[index]

    import nkUtilities.save__pointFile as spf
    outFile   = "dat/before.dat"
    spf.save__pointFile( outFile=outFile, Data=Data )
    
    ret       = sort__structuredData( Data=Data )

    outFile   = "dat/after.dat"
    spf.save__pointFile( outFile=outFile, Data=ret  )
