import sys
import numpy as np

# ========================================================= #
# ===  ロバスト割り算ルーチン                           === #
# ========================================================= #
def robustInv( Data, Flag__positive=False ):
    # ---------------------------------------- #
    # ---  numpy のケース                  --- #
    # ---------------------------------------- #
    if ( type( Data ) is np.ndarray ):
        if   ( Flag__positive ):
            Data[np.where( Data < 0.0 )] = 0.0
        if   ( Data.ndim == 1 ):
            import fLIB.fLIB__robustInv1D as inv1
            ret = inv1.robustInv1D( Data=Data )
        elif ( Data.ndim == 2 ):
            import fLIB.fLIB__robustInv2D as inv2
            ret = inv2.robustInv2D( Data=Data )
        else:
            sys.exit( "[robustInv] Dimension = 1, 2 ??" )
    # ---------------------------------------- #
    # ---  その他 のケース                 --- #
    # ---------------------------------------- #
    else:
        if ( Flag__positive ):
            if ( Data > 0.0 ):
                ret  = 1.0 / float( Data )
            else:
                ret  = 0.0
        else:
            if ( Data != 0.0 ):
                ret  = 1.0 / float( Data )
            else:
                ret  = 0.0
    return( ret )
