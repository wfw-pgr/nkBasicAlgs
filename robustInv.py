import sys
import numpy as np

# ========================================================= #
# ===  Robust Reciprocal Number                         === #
# ========================================================= #

def robustInv( Data, Flag__positive=False ):
    
    # ---------------------------------------- #
    # ---  [1] integer case                --- #
    # ---------------------------------------- #
    if ( type( Data ) is int ):
        if ( Data == 0 ):
            ret = 0
        else:
            ret = 1 / Data
        return( ret )
    
    # ---------------------------------------- #
    # ---  [2] float case                  --- #
    # ---------------------------------------- #
    if ( type( Data ) is float ):
        if ( Data == 0.0 ):
            ret = 0.0
        else:
            ret = 1.0 / Data
        return( ret )
    
    # ---------------------------------------- #
    # ---  [3] list case                   --- #
    # ---------------------------------------- #
    if ( type( Data ) is list ):
        Data = np.array( Data )
    
    # ---------------------------------------- #
    # ---  [4] numpy array case            --- #
    # ---------------------------------------- #
    if ( type( Data ) is np.ndarray ):
        
        if ( Flag__positive ):
            Data[ np.where( Data <= 0.0 ) ] = 0.0

        ret        = np.zeros_like( Data )
        index      = np.where( Data != 0.0 )
        ret[index] = 1.0 / Data[index]
        return( ret )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):
    print()
    print( " robustInv(2.0)   :: {0}".format( robustInv( 2.0 ) ) )
    print( " robustInv(1.0)   :: {0}".format( robustInv( 1.0 ) ) )
    print( " robustInv(0.0)   :: {0}".format( robustInv( 0.0 ) ) )
    print( " robustInv(-1.0)  :: {0}".format( robustInv(-1.0 ) ) )
    print()
    print( " robustInv(1)     :: {0}".format( robustInv(  1 ) ) )
    print( " robustInv(2)     :: {0}".format( robustInv(  2 ) ) )
    print( " robustInv(0)     :: {0}".format( robustInv(  0 ) ) )
    print( " robustInv(-1)    :: {0}".format( robustInv( -1 ) ) )
    print()
    list1 = [1.0,0.0,2.0]
    list2 = [1.0,3.0,2.0]
    list3 = [0.0,0.0,0.0]
    print( " list1            :: {0}".format( list1 ) )
    print( " list2            :: {0}".format( list2 ) )
    print( " list3            :: {0}".format( list3 ) )
    print( " robustInv(list1) :: {0}".format( robustInv( list1 ) ) )
    print( " robustInv(list2) :: {0}".format( robustInv( list2 ) ) )
    print( " robustInv(list3) :: {0}".format( robustInv( list3 ) ) )
    print()
    print( " robustInv(arr1)  :: {0}".format( robustInv( np.array( list1 ) ) ) )
    print( " robustInv(arr2)  :: {0}".format( robustInv( np.array( list2 ) ) ) )
    print( " robustInv(arr3)  :: {0}".format( robustInv( np.array( list3 ) ) ) )
    print()

    
    #     if   ( Data.ndim == 1 ):
    #         import fLIB.fLIB__robustInv1D as inv1
    #         ret = inv1.robustInv1D( Data=Data )
    #     elif ( Data.ndim == 2 ):
    #         import fLIB.fLIB__robustInv2D as inv2
    #         ret = inv2.robustInv2D( Data=Data )
    #     else:
    #         sys.exit( "[robustInv] Dimension = 1, 2 ??" )
    # # ---------------------------------------- #
    # # ---  その他 のケース                 --- #
    # # ---------------------------------------- #
    # else:
    #     if ( Flag__positive ):
    #         if ( Data > 0.0 ):
    #             ret  = 1.0 / float( Data )
    #         else:
    #             ret  = 0.0
    #     else:
    #         if ( Data != 0.0 ):
    #             ret  = 1.0 / float( Data )
    #         else:
    #             ret  = 0.0
    # return( ret )
