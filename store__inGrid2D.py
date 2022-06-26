import numpy            as np
import numpy.ctypeslib  as Flib
import ctypes, sys
import os.path

# ================================================================ #
# ===  store__inGrid2D                                         === #
# ================================================================ #
def store__inGrid2D( Data=None, x1MinMaxNum=None, x2MinMaxNum=None, x3MinMaxNum=None, \
                     size=None, xyzRange=None ):
    # ------------------------------------------------- #
    # --- [1]   引数チェック                        --- #
    # ------------------------------------------------- #
    if ( Data        is None ): sys.exit( "[store__inGrid2D] Data ???" )
    if ( ( size is not None ) and ( xyzRange is not None ) ):
        x1MinMaxNum = np.array( [ xyzRange[0,0], xyzRange[1,0], size[2] ] )
        x2MinMaxNum = np.array( [ xyzRange[0,1], xyzRange[1,1], size[1] ] )
    if ( x1MinMaxNum is None ): sys.exit( "[store__inGrid2D] x1MinMaxNum == ???" )
    if ( x2MinMaxNum is None ): sys.exit( "[store__inGrid2D] x2MinMaxNum == ???" )
    
    # ------------------------------------------------- #
    # --- [2]   引数準備                            --- #
    # ------------------------------------------------- #
    
    #  -- [2-1] 使用する引数を準備                  --  #
    LI,LJ     = int( x1MinMaxNum[2] ), int( x2MinMaxNum[2] )
    nData     = Data.shape[0]
    nCmp      = Data.shape[1]
    dx        = ( x1MinMaxNum[1] - x1MinMaxNum[0] ) / float( x1MinMaxNum[2] - 1 )
    dy        = ( x2MinMaxNum[1] - x2MinMaxNum[0] ) / float( x2MinMaxNum[2] - 1 )
    delta     = np.array( [ dx, dy ] )
    xyzRange  = [ [ x1MinMaxNum[0], x2MinMaxNum[0], ], \
                  [ x1MinMaxNum[1], x2MinMaxNum[1], ]  ]
    ret       = np.zeros( ( LJ,LI,nCmp ) )
    
    #  -- [2-2] Fortranサイズへ変換                 --  #
    Data_     =     np.array( Data    , dtype=np.float64  )
    ret_      =     np.array( ret     , dtype=np.float64  )
    nData_    = ctypes.byref( ctypes.c_int64( nData  )    )
    nCmp_     = ctypes.byref( ctypes.c_int64( nCmp   )    )
    LI_       = ctypes.byref( ctypes.c_int64( LI     )    )
    LJ_       = ctypes.byref( ctypes.c_int64( LJ     )    )
    delta_    =     np.array( delta   , dtype=np.float64  )
    xyzRange_ =     np.array( xyzRange, dtype=np.float64  )

    # ------------------------------------------------- #
    # --- [3]   ライブラリをロード                  --- #
    # ------------------------------------------------- #
    
    #  -- [3-1] ライブラリを定義                    --  #

    pyLIB  = Flib.load_library( 'pylib.so', os.path.abspath( os.path.dirname(__file__) ) )
    
    #  -- [3-2] 入出力管理                          --  #
    pyLIB.store__ingrid2d_.argtypes = [
        Flib.ndpointer( dtype=np.float64 ),
        Flib.ndpointer( dtype=np.float64 ),
        ctypes.POINTER( ctypes.c_int64   ),
        ctypes.POINTER( ctypes.c_int64   ),
        ctypes.POINTER( ctypes.c_int64   ),
        ctypes.POINTER( ctypes.c_int64   ),
        Flib.ndpointer( dtype=np.float64 ),
        Flib.ndpointer( dtype=np.float64 ),
    ]
    pyLIB.store__ingrid2d_.restype = ctypes.c_void_p

    # ------------------------------------------------- #
    # --- [4]   関数呼出 / 返却                     --- #
    # ------------------------------------------------- #
    pyLIB.store__ingrid2d_( Data_, ret_, nData_, nCmp_, LI_, LJ_, delta_, xyzRange_ )
    return( ret_ )


# ================================================================ #
# ===  テスト用 呼び出し                                       === #
# ================================================================ #
if ( __name__=='__main__' ):

    import nkUtilities.equiSpaceGrid as esg
    x1MinMaxNum = [ 0.0, 1.0, 101 ]
    x2MinMaxNum = [ 0.0, 1.0,  81 ]
    x3MinMaxNum = [ 0.0, 0.0,   1 ]
    radius      = 0.8
    ret         = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                     x3MinMaxNum=x3MinMaxNum, returnType = "point" )
    radii       = np.sqrt( ret[:,0]**2 + ret[:,1]**2 )
    Data        = np.zeros( (ret.shape[0],5) )
    Data[:,0:3] = ret
    Data[:,  3] = np.exp( - 0.5 * radii**2 )
    Data[:,  4] = Data[:,0]
    Data        = Data[ np.where( radii < radius ) ]
    ret         = store__inGrid2D( Data=Data, x1MinMaxNum=x1MinMaxNum, \
                                   x2MinMaxNum=x2MinMaxNum )
    print( ret.shape )
    ret      = np.reshape( ret, ( 1, 81, 101, 5 )  )
    
    import nkVTKRoutines.convert__vtkStructuredGrid as vts
    outFile  = "out.vts"
    names    = [ "data1", "data2" ]
    vts.convert__vtkStructuredGrid( Data=ret, outFile=outFile, names=names )
