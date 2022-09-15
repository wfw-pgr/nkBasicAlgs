import os, sys
import numpy   as np
import nkUtilities.load__pointFile as lpf


# ========================================================= #
# ===  structurize__grid.py                             === #
# ========================================================= #

def structurize__grid( Data=None, inpFile=None, DataType="point", coordinate="xyz", \
                       digit=5  , reshape=True, returnType="Data" ):

    x_, y_, z_ = 0, 1, 2
    
    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( Data is None ):
        if ( inpFile is not None ):
            Data = lpf.load__pointFile( inpFile=inpFile, returnType=DataType )
        else:
            sys.exit( "[structurize__grid.py] Data == ???" )
    if ( DataType.lower() == "point" ):
        if ( Data.ndim != 2 ):
            print( "[structurize__grid.py] Data's ndim != 2 [ERROR] " )
            sys.exit()
    if ( DataType.lower() == "structured" ):
        print( "[structurize__grid.py] structure is not implemented yet. please confirm manually." )
        return()
    Data_ = np.copy( Data )

    if ( coordinate.lower() in [ "xy", "2d" ] ):
        if ( Data_.shape[1] <= 2 ):
            Data_ = np.concatenate( [ Data_, (Data_[:,x_])[:,None] ], axis=1 )

    # ------------------------------------------------- #
    # --- [2] identify shape, Min, Max value        --- #
    # ------------------------------------------------- #
    nData       = Data_.shape[0]
    nComponents = Data_.shape[1]
    xMin, xMax  = np.min( Data_[:,x_] ), np.max( Data_[:,x_] )
    yMin, yMax  = np.min( Data_[:,y_] ), np.max( Data_[:,y_] )
    zMin, zMax  = np.min( Data_[:,z_]) , np.max( Data_[:,z_] )
    
    # ------------------------------------------------- #
    # --- [3] identify Axis                         --- #
    # ------------------------------------------------- #
    xAxis       = np.sort( np.array( list( set( Data_[:,x_] ) ) ) )
    yAxis       = np.sort( np.array( list( set( Data_[:,y_] ) ) ) )
    zAxis       = np.sort( np.array( list( set( Data_[:,z_] ) ) ) )
    dx          = np.average( np.diff( xAxis ) )
    dy          = np.average( np.diff( yAxis ) )
    dz          = np.average( np.diff( zAxis ) )
    xdigit      = round( - np.log10( ( dx * 10** ( (-1.0) * digit ) ) ) )
    ydigit      = round( - np.log10( ( dy * 10** ( (-1.0) * digit ) ) ) )
    zdigit      = round( - np.log10( ( dz * 10** ( (-1.0) * digit ) ) ) )
    xAxis       = np.sort( np.array( list( set( np.round( Data_[:,x_], decimals=xdigit ) ) ) ) )
    yAxis       = np.sort( np.array( list( set( np.round( Data_[:,y_], decimals=ydigit ) ) ) ) )
    zAxis       = np.sort( np.array( list( set( np.round( Data_[:,z_], decimals=zdigit ) ) ) ) )
    dx          = np.round( ( np.diff( xAxis ) )[0], decimals=xdigit )
    dy          = np.round( ( np.diff( yAxis ) )[0], decimals=ydigit )
    dz          = np.round( ( np.diff( zAxis ) )[0], decimals=zdigit )
    
    # ------------------------------------------------- #
    # --- [4] identify nGrid                        --- #
    # ------------------------------------------------- #
    LI          = xAxis.shape[0]
    LJ          = yAxis.shape[0]
    LK          = zAxis.shape[0]

    # ------------------------------------------------- #
    # --- [5] exception for 2D case                 --- #
    # ------------------------------------------------- #
    if ( coordinate.lower() in [ "xy", "2d" ] ):
        zMin  = None
        zMax  = None
        zAxis = None
        dz    = None
        LK    = None

    # ------------------------------------------------- #
    # --- [6] reshape Data                          --- #
    # ------------------------------------------------- #
    if ( reshape ):
        if ( coordinate.lower() in [ "xy", "2d" ] ):
            Data_    = np.reshape( Data_, (   LJ,LI,nComponents) )
        else:
            Data_    = np.reshape( Data_, (LK,LJ,LI,nComponents) )
    else:
        pass
    
    # ------------------------------------------------- #
    # --- [7] return value                          --- #
    # ------------------------------------------------- #
    if ( returnType.lower() in ["dict","info"] ):
        ret = { "LI":LI, "LJ":LJ, "LK":LK, \
                "xAxis":xAxis, "yAxis":yAxis, "zAxis":zAxis, \
                "dx":dx, "dy":dy, "dz":dz, \
                "xMin":xMin, "yMin":yMin, "zMin":zMin, \
                "xMax":xMax, "yMax":yMax, "zMax":zMax, \
                "Data":Data_ }
    elif ( returnType.lower() == "data" ):
        ret = np.copy( Data_ )
    else:
        print( "[structurize__grid.py] unknown returnType. " )
        sys.exit()
    return( ret )

    

# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):

    # ------------------------------------------------- #
    # --- [1] make grid coordinate                  --- #
    # ------------------------------------------------- #
    import nkUtilities.equiSpaceGrid as esg
    x1MinMaxNum = [ 0.0, 1.0, 11 ]
    x2MinMaxNum = [ 0.0, 1.0, 11 ]
    x3MinMaxNum = [ 0.0, 1.0, 11 ]
    coord       = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                     x3MinMaxNum=x3MinMaxNum, returnType = "point" )
    field       = np.sqrt( np.sum( coord**2, axis=1 ) )
    Data        = np.concatenate( [coord, field[:,None]], axis=1 )
    
    # ------------------------------------------------- #
    # --- [2] call function                         --- #
    # ------------------------------------------------- #
    ret = structurize__grid( Data=Data )
    print( ret.shape )

    
