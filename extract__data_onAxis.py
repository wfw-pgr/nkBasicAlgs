import numpy                          as np
import nkBasicAlgs.extract__pointData as ext


# ========================================================= #
# ===  extract Data on Axis                             === #
# ========================================================= #

def extract__data_onAxis( Data=None, inpFile=None, axis="x" ):

    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #

    if ( Data is None ):
        
        if ( inpFile is not None ):
            with open( inpFile, "r" ) as f:
                Data = np.loadtxt( f )
        else:
            sys.exit( "[extract__data_online] inpFile == ???" )

    # ------------------------------------------------- #
    # --- [2] settings axis                         --- #
    # ------------------------------------------------- #
    
    if   ( axis == "x" ):
        val = 0.0
        ref = 0
    elif ( axis == "y" ):
        val = 0.0
        ref = 1
    elif ( axis == "z" ):
        val = 0.0
        ref = 2

    # ------------------------------------------------- #
    # --- [3] data extraction                       --- #
    # ------------------------------------------------- #

    ret = ext.extract__pointData( Data=Data, ref_=ref, value=val )
    
    return( ret )


# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):
    import nkUtilities.genArgs as gar
    args    = gar.genArgs()

    import nkUtilities.generate__testprofile as gtp
    x1MinMaxNum = [ 0.0, 1.0, 11 ]
    x2MinMaxNum = [ 0.0, 1.0, 11 ]
    x3MinMaxNum = [ 0.0, 1.0, 11 ]
    ret         = gtp.generate__testprofile( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
    	                                     x3MinMaxNum=x3MinMaxNum, returnType = "point" )
    
    ret = extract__data_onAxis( Data=ret, axis="x" )
    print( ret )

    
