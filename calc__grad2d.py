import sys
import numpy            as np
import numpy.ctypeslib  as Flib
import ctypes
import os.path

# ================================================================ #
# ===  calc__grad2d :: gradiant for 2D Field                   === #
# ================================================================ #
def calc__grad2d( dx1=None, dx2=None, Data=None, x1Axis=None, x2Axis=None, difftype="central", \
                  boundary="copy" ):
    
    # ------------------------------------------------- #
    # --- [1]  引数チェック                         --- #
    # ------------------------------------------------- #
    # -- Data           :: array [LJ,LI]             -- #
    # -- dx1, dx2       :: float value               -- #
    # -- xAxis1, xAxis2 :: array [LI], [LJ]          -- #
    # -- difftype       :: central, forward, backward-- #
    
    if ( Data is None   ):
        sys.exit("[calc__grad2d.py] Data == ???  [ERROR]" )
    if ( Data.ndim != 2 ):
        sys.exit("[calc__grad2d.py] Data dimension is incompatible ( 2D ) [ERROR]" )
    if ( dx1  is None   ):
        if ( xAxis1 is None ):
            sys.exit( "[calc__grad2d.py] No dx1 & No xAxis1 [ERROR] " )
        else:
            dx1 = x1Axis[1] - x1Axis[0]
    if ( dx2  is None   ):
        if ( xAxis1 is None ):
            sys.exit( "[calc__grad2d.py] No dx1 & No xAxis1 [ERROR] " )
        else:
            dx2 = x2Axis[1] - x2Axis[0]
    LI, LJ    = Data.shape[1], Data.shape[0]
    dfdx1_    = np.zeros( (LJ,LI) )
    dfdx2_    = np.zeros( (LJ,LI) )

    # -- translation of difftype into one charactor          -- #
    if ( difftype.lower() in [ "central", "forward", "backward" ] ):
        if ( difftype.lower() == "central"  ):
            difftype_ = "c"
        if ( difftype.lower() == "forward"  ):
            difftype_ = "f"
        if ( difftype.lower() == "backward" ):
            difftype_ = "b"
    else:
        sys.exit( "[calc__grad2d.py] difftype should be chosen from [ central, forward, backward ]" )
    
    
    # ------------------------------------------------- #
    # --- [2] ライブラリをロード                    --- #
    # ------------------------------------------------- #
    #  -- [2-1] ライブラリを定義 --  #
    pyLIB     = Flib.load_library( 'pylib.so', os.path.abspath( os.path.dirname( __file__ ) ) )
    #  -- [2-2] 入出力管理       --  #
    pyLIB.calc__grad2d_.argtypes = [
        Flib.ndpointer( dtype=np.float64 ),
        Flib.ndpointer( dtype=np.float64 ),
        Flib.ndpointer( dtype=np.float64 ),
        Flib.ndpointer( dtype=np.float64 ),
        Flib.ndpointer( dtype=np.float64 ),
        ctypes.POINTER( ctypes.c_int64   ),
        ctypes.POINTER( ctypes.c_int64   ),
        ctypes.c_char_p
    ]
    pyLIB.calc__grad2d_.restype = ctypes.c_void_p
    #  -- [2-3] Fortranサイズへ  --  #
    func_     = np.array( Data  , dtype=np.float64  )
    dfdx1_    = np.array( dfdx1_, dtype=np.float64  )
    dfdx2_    = np.array( dfdx2_, dtype=np.float64  )
    dx1_      = np.array( dx1   , dtype=np.float64  )
    dx2_      = np.array( dx2   , dtype=np.float64  )
    LI_       = ctypes.byref( ctypes.c_int64( LI )  )
    LJ_       = ctypes.byref( ctypes.c_int64( LJ )  )
    difftype_ = difftype_.encode()

    # ------------------------------ #
    # --- [3]  関数呼出 / 返却   --- #
    # ------------------------------ #
    pyLIB.calc__grad2d_( func_, dfdx1_, dfdx2_, dx1_, dx2_, LI_, LJ_, difftype_  )
    ret        = np.zeros( (LJ,LI,2) )
    ret[:,:,0] = np.copy( dfdx1_ )
    ret[:,:,1] = np.copy( dfdx2_ )

    # ------------------------------------------------- #
    # --- [4] 境界領域処理                          --- #
    # ------------------------------------------------- #
    if   ( boundary.lower() in ["copy"] ):
        ret[ 0, :,:] = np.copy( ret[ 1, :,:] )
        ret[-1, :,:] = np.copy( ret[-2, :,:] )
        ret[ :, 0,:] = np.copy( ret[ :, 1,:] )
        ret[ :,-1,:] = np.copy( ret[ :,-2,:] )
    elif ( boundary.lower() in ["none"] ):
        pass
    elif ( boundary.lower() in ["trim"] ):
        ret = np.copy( ret[1:-1,1:-1,:] )
    else:
        sys.exit( "[calc__grad2d.py] boundary == {0} ??? ".format( boundary ) )
    
    return( ret )


# ================================================================ #
# ===  実行部                                                  === #
# ================================================================ #
if ( __name__=="__main__" ):
    # ---- テスト用 プロファイル ---- #
    # -- 座標系 xg, yg -- #

    x_,y_,z_      = 0, 1, 2
    import nkUtilities.equiSpaceGrid as esg
    x1MinMaxNum   = [ -1.0, 1.0, 21 ]
    x2MinMaxNum   = [ -1.0, 1.0, 21 ]
    x3MinMaxNum   = [  0.0, 1.0,  1 ]
    ret           = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                       x3MinMaxNum=x3MinMaxNum, returnType = "structured" )
    ret[:,:,:,z_] = np.sqrt( ret[:,:,:,x_]**2 + ret[:,:,:,y_]**2 )
    dx1           = ret[0,0,1,x_] - ret[0,0,0,x_]
    dx2           = ret[0,1,0,y_] - ret[0,0,0,y_]
    Data          = np.reshape( ret[:,:,:,z_], ( ret.shape[1], ret.shape[2] ) )
    grad          = calc__grad2d( Data=Data, dx1=dx1, dx2=dx2  )
    xAxis         = np.ravel( ret[0,:,:,x_] )
    yAxis         = np.ravel( ret[0,:,:,y_] ) 
    grad_x,grad_y = np.copy( np.ravel( grad[:,:,0] ) ), np.copy( np.ravel( grad[:,:,1] ) )
    Data          = np.ravel( Data )

    print( xAxis.shape, yAxis.shape, grad_x.shape, grad_y.shape, Data.shape )
    import nkUtilities.cMapTri as cmt
    cmt.cMapTri( xAxis=xAxis, yAxis=yAxis, cMap=Data  , pngFile='source.png' )
    cmt.cMapTri( xAxis=xAxis, yAxis=yAxis, cMap=grad_x, pngFile='grad_x.png' )
    cmt.cMapTri( xAxis=xAxis, yAxis=yAxis, cMap=grad_y, pngFile='grad_y.png' )
