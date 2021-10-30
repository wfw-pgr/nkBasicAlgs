import numpy as np

# ========================================================= #
# ===  generate line from x1 to x2                      === #
# ========================================================= #
def generate__line_coord( x1=[0,0,0], x2=[1,1,1], nDiv=101, outFile=None ):

    x_, y_, z_ = 0, 1, 2
    dim        = len( x1 )

    # ------------------------------------------------- #
    # --- [1] line coordinate                       --- #
    # ------------------------------------------------- #
    
    if   ( dim == 2 ):
        coord        = np.zeros( (nDiv,2) )
        tval         = np.linspace( 0.0, 1.0, nDiv )
        coord[:,x_]  = ( x2[x_] - x1[x_] ) * tval + x1[x_]
        coord[:,y_]  = ( x2[y_] - x1[y_] ) * tval + x1[y_]

    elif ( dim == 3 ):
        coord        = np.zeros( (nDiv,3) )
        tval         = np.linspace( 0.0, 1.0, nDiv )
        coord[:,x_]  = ( x2[x_] - x1[x_] ) * tval + x1[x_]
        coord[:,y_]  = ( x2[y_] - x1[y_] ) * tval + x1[y_]
        coord[:,z_]  = ( x2[z_] - x1[z_] ) * tval + x1[z_]

    # ------------------------------------------------- #
    # --- [2] save in a file / return               --- #
    # ------------------------------------------------- #
    if ( outFile is not None ):
        import nkUtilities.save__pointFile as spf
        spf.save__pointFile( outFile=outFile, Data=coord )

    return( coord )


# ======================================== #
# ===  実行部                          === #
# ======================================== #
if ( __name__=="__main__" ):

    x1      = [ 0.0, 0.0, 0.0 ]
    x2      = [ 1.0, 1.0, 1.0 ]
    nDiv    = 101
    outFile = "test/out.dat"
    coord   = generate__line_coord( x1=x1, x2=x2, nDiv=nDiv, outFile=outFile )
