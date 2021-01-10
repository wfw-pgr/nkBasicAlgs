import numpy            as np
import numpy.ctypeslib  as Flib
import ctypes, sys
import os.path

# ================================================================ #
# ===  calc__curl2d                                            === #
# ================================================================ #
def calc__curl2d( Data=None, dx1=None, dx2=None, x1Axis=None, x2Axis=None, coordinate="xyz", \
                  boundary="copy" ):
    
    # ------------------------------------------------- #
    # --- [1]   引数チェック                        --- #
    # ------------------------------------------------- #
    
    #  -- [1-1] Data & size check                   --  #
    if ( Data   is None ): sys.exit( "[calc__curl2d] Data == ???" )
    if ( Data.ndim != 3 ):
        sys.exit("[calc__grad2d.py] Data dimension must be 3 :: [x_,y_,cmp_] ) [ERROR]" )
    if ( Data.shape[2] != 3 ):
        sys.exit("[calc__grad2d.py] Data must have 3-component ( Data :: [x_,y_,cmp_] ) [ERROR]")
    #  -- [1-2] x1Axis check                        --  #
    if ( x1Axis is None ):
        if ( dx1 is None ):
            sys.exit( "[calc__curl2d] x1Axis & dx1 are None. [ERROR]" )
        else:
            x1Axis_ = dx1 * np.arange( Data.shape[1] )
    else:
        if ( x1Axis.ndim == 1 ):
            x1Axis_ = np.copy( x1Axis )
        elif ( x1Axis.ndim == 2 ):
            x1Axis_ = np.copy( x1Axis[0,:] )
        else:
            sys.exit( "[calc__curl2d] x1Axis size ==  {0} ?? ".format( x1Axis.shape ) )
    #  -- [1-3] x2Axis check                        --  #
    if ( x2Axis is None ):
        if ( dx2 is None ):
            sys.exit( "[calc__curl2d] x2Axis & dx2 are None. [ERROR]" )
        else:
            x2Axis_ = dx2 * np.arange( Data.shape[0] )
    else:
        if ( x2Axis.ndim == 1 ):
            x2Axis_ = np.copy( x2Axis )
        elif ( x2Axis.ndim == 2 ):
            x2Axis_ = np.copy( x2Axis[:,0] )
        else:
            sys.exit( "[calc__curl2d] x2Axis size ==  {0} ?? ".format( x2Axis.shape ) )
            
    # ------------------------------------------------- #
    # --- [2]   引数準備                            --- #
    # ------------------------------------------------- #
    
    #  -- [2-1] 使用する引数を準備                  --  #
    LI, LJ      = Data.shape[1], Data.shape[0]
    ret         = np.zeros( ( LJ,LI,3 ) )
    
    #  -- [2-2] Fortranサイズへ変換                 --  #
    Data_    =     np.array( Data   , dtype=np.float64  )
    ret_     =     np.array( ret    , dtype=np.float64  )
    x1Axis_  =     np.array( x1Axis_, dtype=np.float64  )
    x2Axis_  =     np.array( x2Axis_, dtype=np.float64  )
    LI_      = ctypes.byref( ctypes.c_int64( LI   )     )
    LJ_      = ctypes.byref( ctypes.c_int64( LJ   )     )
    coordinate_ = ( coordinate.lower() ).encode()

    # ------------------------------------------------- #
    # --- [3]   ライブラリをロード                  --- #
    # ------------------------------------------------- #
    
    #  -- [3-1] ライブラリを定義                    --  #
    pyLIB  = Flib.load_library( 'pylib.so', os.path.abspath( os.path.dirname(__file__) ) )
    
    #  -- [3-2] 入出力管理                          --  #
    pyLIB.calc__curl2d_.argtypes = [
        Flib.ndpointer( dtype=np.float64 ),
        Flib.ndpointer( dtype=np.float64 ),
        Flib.ndpointer( dtype=np.float64 ),
        Flib.ndpointer( dtype=np.float64 ),
        ctypes.POINTER( ctypes.c_int64   ),
        ctypes.POINTER( ctypes.c_int64   ),
        ctypes.c_char_p                   ,
    ]
    pyLIB.calc__curl2d_.restype = ctypes.c_void_p

    # ------------------------------------------------- #
    # --- [4]   関数呼出 / 返却                     --- #
    # ------------------------------------------------- #
    pyLIB.calc__curl2d_( Data_, ret_, x1Axis_, x2Axis_, LI_, LJ_, coordinate_ )

    # ------------------------------------------------- #
    # --- [5] 境界領域処理                          --- #
    # ------------------------------------------------- #
    if   ( boundary.lower() in ["copy"] ):
        ret_[ 0, :,:] = np.copy( ret_[ 1, :,:] )
        ret_[-1, :,:] = np.copy( ret_[-2, :,:] )
        ret_[ :, 0,:] = np.copy( ret_[ :, 1,:] )
        ret_[ :,-1,:] = np.copy( ret_[ :,-2,:] )
    elif ( boundary.lower() in ["none"] ):
        pass
    elif ( boundary.lower() in ["trim"] ):
        ret_ = np.copy( ret_[1:-1,1:-1,:] )
    else:
        sys.exit( "[calc__grad2d.py] boundary == {0} ??? ".format( boundary ) )
    

    
    return( ret_ )


# ================================================================ #
# ===  テスト用 呼び出し                                       === #
# ================================================================ #
if ( __name__=='__main__' ):

    x_,y_,z_      = 0, 1, 2
    import nkUtilities.equiSpaceGrid as esg
    x1MinMaxNum   = [ -1.0, 1.0, 101 ]
    x2MinMaxNum   = [ -1.0, 1.0, 101 ]
    x3MinMaxNum   = [  0.0, 1.0,   1 ]
    ret           = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                       x3MinMaxNum=x3MinMaxNum, returnType = "structured" )
    LI, LJ        = ret.shape[2], ret.shape[1]
    xAxis         = np.copy( np.reshape( ret[0,:,:,x_], (LJ,LI) ) )
    yAxis         = np.copy( np.reshape( ret[0,:,:,y_], (LJ,LI) ) )
    Data          = np.zeros( (LJ,LI,3) )
    vx_,vy_,vz_   = 0, 1, 2
    Data[:,:,vx_] = xAxis
    Data[:,:,vy_] = yAxis
    Data[:,:,vz_] = xAxis * yAxis

    curl          = calc__curl2d( Data=Data, x1Axis=xAxis, x2Axis=yAxis )

    xAxis         = np.ravel( xAxis )
    yAxis         = np.ravel( yAxis )
    curlx         = np.ravel( curl[:,:,vx_] )
    curly         = np.ravel( curl[:,:,vy_] )
    curlz         = np.ravel( curl[:,:,vz_] )

    import nkUtilities.cMapTri as cmt
    cmt.cMapTri( xAxis=xAxis, yAxis=yAxis, cMap=curlx, pngFile='curlx.png' )
    cmt.cMapTri( xAxis=xAxis, yAxis=yAxis, cMap=curly, pngFile='curly.png' )
    cmt.cMapTri( xAxis=xAxis, yAxis=yAxis, cMap=curlz, pngFile='curlz.png' )
