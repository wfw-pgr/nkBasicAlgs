import numpy            as np
import numpy.ctypeslib  as Flib
import ctypes, sys
import os.path


# ================================================================ #
# === reordering of the numpy ( physical memory base )         === #
# ================================================================ #
def reorder__ijk_kji( Data=None, shape=None, DataType="structured", \
                      with__coordinate=True, convert ="ijk_kji" ):
    # ---------------------------------------- #
    # --- [1]   引数チェック               --- #
    # ---------------------------------------- #
    if ( Data is None ): sys.exit( "[reorder__ijk_kji] Data ???" )

    if ( shape is None ):
        if ( DataType == "structured" ):
            if ( with__coordinate ):
                if ( convert == "ijk_kji" ):
                    LILJLK = ( Data.shape[:-1] )[::-1]
                    nCmp   = Data.shape[  -1]
                if ( convert == "kji_ijk" ):
                    LILJLK = Data.shape[1:]
                    nCmp   = Data.shape[0 ]
            else:
                if ( convert == "ijk_kji" ):
                    LILJLK = Data.shape[::-1]
                    nCmp   = 1
                if ( convert == "kji_ijk" ):
                    LILJLK = Data.shape
                    nCmp   = 1
        else:
            print   ( "[reorder__ijk_kji] no shape information....[ERROR]" )
            sys.exit( "[reorder__ijk_kji] " )
    else:
        #  -- shepe :: [LI,LJ,LK]  -- #
        nCmp   = Data.shape[-1]
        LILJLK = shape

    ndim = len(LILJLK)
    if   ( ndim == 2 ):
        LI, LJ, LK = LILJLK[0], LILJLK[1], 1
    elif ( ndim == 3 ):
        LI, LJ, LK = LILJLK[0], LILJLK[1], LILJLK[2]
    else:
        print   ( "[reorder__ijk_kji] only ndim = 2 or 3 is supported... [ERROR]" )
        sys.exit( "[reorder__ijk_kji] " )

        
    # ---------------------------------------- #
    # --- [2]   引数準備                   --- #
    # ---------------------------------------- #
    #  -- [2-1] 使用する引数を準備         --  #
    
    #  -- [2-2] Fortranサイズへ変換        --  #
    Data_    =     np.array( Data, dtype=np.float64  )
    LI_      = ctypes.byref( ctypes.c_int64( LI   )  )
    LJ_      = ctypes.byref( ctypes.c_int64( LJ   )  )
    LK_      = ctypes.byref( ctypes.c_int64( LK   )  )
    nCmp_    = ctypes.byref( ctypes.c_int64( nCmp )  )
    #  -- [2-3] return array               --  #
    #  -- point case :: shape is same      --  #
    if   ( DataType == "point"      ):
        retShape = ( LI*LJ*LK, nCmp )
        
    #  -- structured case ::               --  #
    elif ( DataType == "structured" ):
        if ( with__coordinate ):
            if ( convert == "ijk_kji" ):
                retShape = ( nCmp,LI,LJ,LK )
            if ( convert == "kji_ijk" ):
                retShape = ( LK,LJ,LI,nCmp )
        else:
            if ( convert == "ijk_kji" ):
                retShape = ( LI,LJ,LK )
            if ( convert == "kji_ijk" ):
                retShape = ( LK,LJ,LI )
    ret_     =     np.zeros( retShape, dtype=np.float64 )

    # ---------------------------------------- #
    # --- [3]   ライブラリをロード         --- #
    # ---------------------------------------- #
    #  -- [3-1] ライブラリを定義           --  #
    path   = __file__
    pyLIB  = Flib.load_library( 'pylib.so', path )
    if ( DataType == "structured" ):
        if ( convert == "ijk_kji" ):
            func_to_be_used = pyLIB.reorder__ijk2kji_structured_
        if ( convert == "kji_ijk" ):
            func_to_be_used = pyLIB.reorder__kji2ijk_structured_
    if ( DataType == "point" ):
        if ( convert == "ijk_kji" ):
            func_to_be_used = pyLIB.reorder__ijk2kji_point_
        if ( convert == "kji_ijk" ):
            func_to_be_used = pyLIB.reorder__kji2ijk_point_
        
    #  -- [3-2] 入出力管理                 --  #
    func_to_be_used.argtypes = [
        Flib.ndpointer( dtype=np.float64 ),
        Flib.ndpointer( dtype=np.float64 ),
        ctypes.POINTER( ctypes.c_int64   ),
        ctypes.POINTER( ctypes.c_int64   ),
        ctypes.POINTER( ctypes.c_int64   ),
        ctypes.POINTER( ctypes.c_int64   ),
    ]
    func_to_be_used.restype = ctypes.c_void_p

    # ---------------------------------------- #
    # --- [4]   関数呼出 / 返却            --- #
    # ---------------------------------------- #
    func_to_be_used( Data_, ret_, LI_, LJ_, LK_, nCmp_ )
    return( ret_ )


# ================================================================ #
# ===  テスト用 呼び出し                                       === #
# ================================================================ #
if ( __name__=='__main__' ):

    import nkUtilities.generate__testprofile as gtp
    import nkUtilities.equiSpaceGrid         as esg
    import nkUtilities.save__pointFile       as spf
    x1MinMaxNum = [ 0.0, 1.0, 31 ]
    x2MinMaxNum = [ 0.0, 1.0, 21 ]
    x3MinMaxNum = [ 0.0, 1.0, 11 ]

    # ------------------------------------------------- #
    # --- [1] ijk -> kji                            --- #
    # ------------------------------------------------- #
    # ret         = gtp.generate__testprofile( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
    # 	                                     x3MinMaxNum=x3MinMaxNum, returnType = "point" )
    # print( ret.shape )
    # spf.save__pointFile( outFile="testprofile.dat", Data=ret, DataOrder="ijk" )
    
    # trn = reorder__ijk_kji( Data=ret, DataType="point", shape=(31,21,11), convert="ijk_kji" )
    # print( trn.shape )
    # spf.save__pointFile( outFile="transposed.dat", Data=trn, DataOrder="kji" )


    # ------------------------------------------------- #
    # --- [2] kji -> ijk                            --- #
    # ------------------------------------------------- #
    ret         = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                     x3MinMaxNum=x3MinMaxNum, returnType = "structured", \
                                     DataOrder  ="kji" )
    print( ret.shape )
    spf.save__pointFile( outFile="testprofile.dat", Data=ret, DataOrder="kji" )
    
    trn = reorder__ijk_kji( Data=ret, DataType="structured", convert="kji_ijk" )
    print( trn.shape )
    spf.save__pointFile( outFile="transposed.dat", Data=trn, DataOrder="ijk" )
