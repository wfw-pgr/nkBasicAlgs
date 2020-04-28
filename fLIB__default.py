import numpy            as np
import numpy.ctypeslib  as Flib
import ctypes, sys
import os.path

# ================================================================ #
# ===                                               === #
# ================================================================ #
def funcxxx( v1=None, v2=None ):
    # ---------------------------------------- #
    # --- [1]   引数チェック               --- #
    # ---------------------------------------- #
    if ( v1 is None ): sys.exit( "[funcxxx] v1 ???" )
    if ( v2 is None ): sys.exit( "[funcxxx] v2 ???" )

    # ---------------------------------------- #
    # --- [2]   引数準備                   --- #
    # ---------------------------------------- #
    #  -- [2-1] 使用する引数を準備         --  #
    LI, LJ   = v1.shape[1], v1.shape[0]
    Amat     = np.zeros( ( LJ,LI ) )
    Flag     = True
    coord    = "RTZ"
    #  -- [2-2] Fortranサイズへ変換        --  #
    v1_      =     np.array( v1  , dtype=np.float64  )
    v2_      =     np.array( v2  , dtype=np.float64  )
    LI_      = ctypes.byref( ctypes.c_int64( LI   )  )
    LJ_      = ctypes.byref( ctypes.c_int64( LJ   )  )
    Amat_    =     np.array( Amat, dtype=np.float64  )
    Flag_    =     np.array( Flag , dtype=np.bool    )
    coord_   = coord.encode()

    # ---------------------------------------- #
    # --- [3]   ライブラリをロード         --- #
    # ---------------------------------------- #
    #  -- [3-1] ライブラリを定義           --  #
    path   = os.path.expanduser('~') + "/.python/lib/fLIB/"
    pyLIB  = Flib.load_library( 'pylib.so', path )
    #  -- [3-2] 入出力管理                 --  #
    pyLIB.funcxxx_.argtypes = [
        Flib.ndpointer( dtype=np.float64 ),
        Flib.ndpointer( dtype=np.float64 ),
        ctypes.POINTER( ctypes.c_int64   ),
        ctypes.POINTER( ctypes.c_int64   ),
        Flib.ndpointer( dtype=np.float64 ),
        ctypes.c_char_p                   ,
        Flib.ndpointer( dtype=np.bool    )
    ]
    pyLIB.funcxxx_.restype = ctypes.c_void_p

    # ---------------------------------------- #
    # --- [4]   関数呼出 / 返却            --- #
    # ---------------------------------------- #
    pyLIB.funcxxx_( v1_, v2_, LI_, LJ_, Amat_, Flag_, coord_ )
    return( Amat_ )


# ================================================================ #
# ===                                               === #
# ================================================================ #
if ( __name__=='__main__' ):
    # ---- テスト用 プロファイル ---- #
    # -- 座標系 xg, yg -- #
    xa     = np.linspace( -1.0, 1.0, 11 )
    ya     = np.linspace( -1.0, 1.0, 11 )
    
