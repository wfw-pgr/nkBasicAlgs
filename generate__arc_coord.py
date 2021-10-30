import numpy as np

# ========================================================= #
# ===  generate__arc_coord                              === #
# ========================================================= #

def generate__arc_coord( xc=[0,0,0], radius=1.0, th1=0.0, th2=30.0, nDiv=101, plane="xy", help=False, outFile=None ):

    x_, y_, z_ = 0, 1, 2

    # ------------------------------------------------- #
    # --- [1] argument                              --- #
    # ------------------------------------------------- #
    if ( help ):
        print( "[generate__arc_coord.py] xc, radius, th1, th2, nDiv, plane, help " )
        return()
    
    # ------------------------------------------------- #
    # --- [2] arc coordinate                        --- #
    # ------------------------------------------------- #
    theta       = np.linspace( th1, th2, nDiv )
    coord       = np.zeros( (nDiv,3) )
    if   ( plane.lower() in ["xy","yx"] ):
        coord[:,x_] = xc[x_] + radius * np.cos( theta )
        coord[:,y_] = xc[y_] + radius * np.sin( theta )
        coord[:,z_] = xc[z_] 
    elif ( plane.lower() in ["yz","zy"] ):
        coord[:,x_] = xc[x_] 
        coord[:,y_] = xc[y_] + radius * np.cos( theta )
        coord[:,z_] = xc[z_] + radius * np.sin( theta )
    elif ( plane.lower() in ["xz","zx"] ):
        coord[:,x_] = xc[x_] + radius * np.cos( theta ) 
        coord[:,y_] = xc[y_]
        coord[:,z_] = xc[z_] + radius * np.sin( theta )
    
    # ------------------------------------------------- #
    # --- [3] save in a file / return               --- #
    # ------------------------------------------------- #
    if ( outFile is not None ):
        import nkUtilities.save__pointFile as spf
        spf.save__pointFile( outFile=outFile, Data=coord )

    return( coord )


# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):
    generate__arc_coord( xc=[0,0,0], radius=1.0, th1=0.0, th2=30.0, \
                         nDiv=101, outFile="test/out.dat" )
    
