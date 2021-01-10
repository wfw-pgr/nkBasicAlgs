import numpy            as np
import numpy.ctypeslib  as Flib
import ctypes, sys
import os.path


# ================================================================ #
# === calc__laplacian                                          === #
# ================================================================ #
def calc__laplacian( phi=None, dx=None, dy=None ):
    # ---------------------------------------- #
    # --- [1]   引数チェック               --- #
    # ---------------------------------------- #
    if ( phi is None ): sys.exit( "[calc__laplacian] phi ???" )
    if ( dx  is None ): dx = 1.0
    if ( dy  is None ): dy = 1.0

    # ---------------------------------------- #
    # --- [2]   引数準備                   --- #
    # ---------------------------------------- #
    #  -- [2-1] 使用する引数を準備         --  #
    LI, LJ   = phi.shape[1], phi.shape[0]
    lap      = np.zeros( ( LJ,LI ) )
    #  -- [2-2] Fortranサイズへ変換        --  #
    phi_     =     np.array( phi , dtype=np.float64  )
    lap_     =     np.array( lap , dtype=np.float64  )
    dx_      =     np.array( [dx], dtype=np.float64  )
    dy_      =     np.array( [dy], dtype=np.float64  )
    LI_      = ctypes.byref( ctypes.c_int64( LI   )  )
    LJ_      = ctypes.byref( ctypes.c_int64( LJ   )  )

    # ---------------------------------------- #
    # --- [3]   ライブラリをロード         --- #
    # ---------------------------------------- #
    #  -- [3-1] ライブラリを定義           --  #
    path   = os.path.expanduser('~') + "/.python/lib/nkBasicAlgs"
    pyLIB  = Flib.load_library( 'pylib.so', path )
    #  -- [3-2] 入出力管理                 --  #
    pyLIB.calc__laplacian_.argtypes = [
        Flib.ndpointer( dtype=np.float64 ),
        Flib.ndpointer( dtype=np.float64 ),
        Flib.ndpointer( dtype=np.float64 ),
        Flib.ndpointer( dtype=np.float64 ),
        ctypes.POINTER( ctypes.c_int64   ),
        ctypes.POINTER( ctypes.c_int64   ),
    ]
    pyLIB.calc__laplacian_.restype = ctypes.c_void_p
    
    # ---------------------------------------- #
    # --- [4]   関数呼出 / 返却            --- #
    # ---------------------------------------- #
    pyLIB.calc__laplacian_( phi_, lap_, dx_, dy_, LI_, LJ_, )
    return( lap_ )


# ================================================================ #
# ===  テスト用 呼び出し                                       === #
# ================================================================ #
if ( __name__=='__main__' ):
    import nkUtilities.equiSpaceGrid as esg
    x1MinMaxNum = [ 0.0, 1.0, 11 ]
    x2MinMaxNum = [ 0.0, 1.0, 11 ]
    x3MinMaxNum = [ 0.0, 0.0,  1 ]
    ret         = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                     x3MinMaxNum=x3MinMaxNum, returnType = "structured" )
    xAxis       = ret[0,:,:,0]
    yAxis       = ret[0,:,:,1]
    phi         = xAxis**2 + yAxis**2
    ret         = calc__laplacian( phi=phi )
    
    with open( "out.dat", "w" ) as f:
        np.savetxt( f, ret )
    
    import nkUtilities.cMapTri as cmt
    pngFile     = "out.png"
    xa,ya,za    = np.ravel( xAxis ), np.ravel( yAxis ), np.ravel( ret )
    cmt.cMapTri( xAxis=xa, yAxis=ya, cMap=za, pngFile=pngFile )
