import os, sys
import numpy as np

# ========================================================= #
# ===  structurize__intoGrid.py                         === #
# ========================================================= #

def structurize__intoGrid( Data=None, inpFile=None, digit=5, \
                           x1MinMaxNum=None, x2MinMaxNum=None, x3MinMaxNum=None, \
                           xMin=None, yMin=None, zMin=None, xMax=None, yMax=None, zMax=None, \
                           LI=None, LJ=None, LK=None ):

    x_  ,y_  ,z_   = 0, 1, 2
    min_,max_,num_ = 0, 1, 2
    
    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( Data is None ):
        if ( inpFile is None ):
            print( "[structurize__intoGrid_python.py] Data & inpFile is None... ??? " )
            sys.exit()
        else:
            import nkUtilities.load__pointFile as lpf
            Data    = lpf.load__pointFile( inpFile=inpFile, returnType="point" )

    # ------------------------------------------------- #
    # --- [2] pre-process                           --- #
    # ------------------------------------------------- #
    Data_       = np.copy( Data )

    # ------------------------------------------------- #
    # --- [3] Range                                 --- #
    # ------------------------------------------------- #
    x1MinMaxNum, dx, LI = prepare__range( x1MinMaxNum=x1MinMaxNum, Data=Data_, xMin=xMin, xMax=xMax, LI=LI, digit=digit )
    x2MinMaxNum, dy, LJ = prepare__range( x1MinMaxNum=x2MinMaxNum, Data=Data_, xMin=yMin, xMax=yMax, LI=LJ, digit=digit )
    x3MinMaxNum, dz, LK = prepare__range( x1MinMaxNum=x3MinMaxNum, Data=Data_, xMin=zMin, xMax=zMax, LI=LK, digit=digit )

    # ------------------------------------------------- #
    # --- [4] make coordinate                       --- #
    # ------------------------------------------------- #
    import nkUtilities.equiSpaceGrid as esg
    coord       = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                     x3MinMaxNum=x3MinMaxNum, returnType = "structured" )
        
    # ------------------------------------------------- #
    # --- [5] store in grid                         --- #
    # ------------------------------------------------- #
    i_index = np.array( np.round( ( Data_[:,x_] - x1MinMaxNum[min_] ) / dx ), dtype=np.int64 )
    j_index = np.array( np.round( ( Data_[:,y_] - x2MinMaxNum[min_] ) / dy ), dtype=np.int64 )
    k_index = np.array( np.round( ( Data_[:,z_] - x3MinMaxNum[min_] ) / dz ), dtype=np.int64 )
    t_index = np.concatenate( [i_index[:,np.newaxis],j_index[:,np.newaxis],k_index[:,np.newaxis],], axis=1 )
    i_overf = np.where( ( i_index > LI-1 ) | ( i_index < 0 ), True, False )
    j_overf = np.where( ( j_index > LJ-1 ) | ( j_index < 0 ), True, False )
    k_overf = np.where( ( k_index > LK-1 ) | ( k_index < 0 ), True, False )
    t_overf = np.concatenate( [i_overf[:,np.newaxis],j_overf[:,np.newaxis],k_overf[:,np.newaxis],], axis=1 )
    i_index[ i_overf ] = 0
    j_index[ j_overf ] = 0
    k_index[ k_overf ] = 0
    
    nField                                = Data_.shape[1]-3
    field                                 = np.zeros( (LK,LJ,LI,nField) )
    field[ i_index, j_index, k_index, : ] = Data_[:,3:]
    ret                                   = np.concatenate( [coord,field], axis=3 )
    return( ret )


# ========================================================= #
# ===  prepare__range                                   === #
# ========================================================= #

def prepare__range( x1MinMaxNum=None, xMin=None, xMax=None, LI=None, Data=None, digit=5, xyz="x" ):
    
    x_  ,y_  ,z_   = 0, 1, 2
    min_,max_,num_ = 0, 1, 2
    idx_           = None
    if ( xyz.lower() == "x" ): idx_ = 0
    if ( xyz.lower() == "y" ): idx_ = 1
    if ( xyz.lower() == "z" ): idx_ = 2
    if ( xyz        is None ): sys.exit( "[ERROR], xyz == ??? {}".format( xyz ) )
    
    # ------------------------------------------------- #
    # --- [1] if x1MinMaxNum exists...              --- #
    # ------------------------------------------------- #
    if ( x1MinMaxNum is None ):
        if ( ( xMin is None ) or ( xMax is None ) ):
            xMin, xMax  = np.min( Data[:,idx_] ), np.max( Data[:,idx_] )
        if ( LI is None ):
            xAxis = np.sort( np.array( list( set( Data[:,idx_] ) ) ) )
            LI    = xAxis.shape[0]
            print( xAxis, LI )
        else:
            xAxis = np.linspace( xMin, xMax, LI )
        if   ( xMax-xMin  > 0.0 ):
            dx      = np.average( np.diff( xAxis ) )
            xdigit  = round( - np.log10( ( dx * 10** ( (-1.0) * digit ) ) ) )
            xAxis   = np.sort( np.array( list( set( np.round( Data[:,idx_], decimals=xdigit ) ) ) ) )
            dx      = np.round( ( np.diff( xAxis ) )[0], decimals=xdigit )
            LI      = round( ( xMax - xMin ) / dx ) + 1
        elif ( xMax-xMin == 0.0 ):
            dx      = 0.0
            LI      = 1
        x1MinMaxNum = [ xMin, xMax, LI ]

    else:
        dx_ = x1MinMaxNum[max_] - x1MinMaxNum[min_]
        x1MinMaxNum[num_] = int( x1MinMaxNum[num_] )
        if ( dx_ == 0.0 ):
            dx = 0.0
            LI = 1
        else:
            dx = dx_ / x1MinMaxNum[num_]
            LI = x1MinMaxNum[num_]
    
    
    # ------------------------------------------------- #
    # --- [2] return                                --- #
    # ------------------------------------------------- #
    return( ( x1MinMaxNum, dx, LI ) )



# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    
    import nkUtilities.equiSpaceGrid as esg
    x1MinMaxNum = [ 0.0, 1.0, 31 ]
    x2MinMaxNum = [ 0.0, 1.0, 31 ]
    x3MinMaxNum = [ 0.0, 1.0, 31 ]
    coord       = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                     x3MinMaxNum=x3MinMaxNum, returnType = "point" )
    radii       = np.reshape( np.sum( coord**2, axis=1 ), (-1,1) )
    Data        = np.concatenate( [coord,radii], axis=1 )
    index       = np.where( Data[:,3] <= 1.0 )
    Data_       = Data[index]
    Data        = np.reshape( Data, (x3MinMaxNum[2],x2MinMaxNum[2],x1MinMaxNum[2],4) )

    shuffle     = np.random.shuffle( Data_ )
    ret         = structurize__intoGrid( Data=Data_ )
    import nkUtilities.save__pointFile as spf
    outFile1   = "test/data_original.dat"
    outFile2   = "test/data_shuffled.dat"
    outFile3   = "test/data_rearange.dat"
    spf.save__pointFile( outFile=outFile1, Data=Data  )
    spf.save__pointFile( outFile=outFile2, Data=Data_ )
    spf.save__pointFile( outFile=outFile3, Data=ret   )

    print( "original :: ", Data.shape )
    print( "rearange :: ", ret .shape )
    
    import nkVTKRoutines.convert__vtkStructuredGrid as vts
    names      = ["data"]
    outFile1   = "test/data_original.vts" 
    outFile3   = "test/data_rearange.vts"
    vts.convert__vtkStructuredGrid( Data=Data , outFile=outFile1, names=names )
    vts.convert__vtkStructuredGrid( Data=ret  , outFile=outFile3, names=names )
    
    # if ( yMax - yMin > 0.0 ):
    #     dy      = np.average( np.diff( yAxis ) )
    #     ydigit  = round( - np.log10( ( dy * 10** ( (-1.0) * digit ) ) ) )
    #     yAxis   = np.sort( np.array( list( set( np.round( Data_[:,y_], decimals=ydigit ) ) ) ) )
    #     dy      = np.round( ( np.diff( yAxis ) )[0], decimals=ydigit )
    #     LJ      = round( ( yMax - yMin ) / dy ) + 1
    # else:
    #     dy      = 0.0
    #     LJ      = 1
        
    # if ( zMax - zMin > 0.0 ):
    #     dz      = np.average( np.diff( zAxis ) )
    #     zdigit  = round( - np.log10( ( dz * 10** ( (-1.0) * digit ) ) ) )
    #     zAxis   = np.sort( np.array( list( set( np.round( Data_[:,z_], decimals=zdigit ) ) ) ) )
    #     dz      = np.round( ( np.diff( zAxis ) )[0], decimals=zdigit )
    #     LK      = round( ( zMax - zMin ) / dz ) + 1
    # else:
    #     dz      = 0.0
    #     LK      = 1

