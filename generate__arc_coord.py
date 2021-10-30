
import numpy as np

# ========================================================= #
# ===  generate__arc_coord                              === #
# ========================================================= #

def generate__arc_coord( xc=[0,0,0], radius=1.0, th1=0.0, th2=30.0, nDiv=101, plane="xy", help=False, outFile=None, degree=True ):

    x_, y_, z_ = 0, 1, 2

    # ------------------------------------------------- #
    # --- [1] argument                              --- #
    # ------------------------------------------------- #
    if ( help ):
        print( "[generate__arc_coord.py] xc, radius, th1, th2, nDiv, plane, help, degree " )
        return()
    if ( degree ):
        th1, th2 = th1*np.pi/180.0, th2*np.pi/180.0
        
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
    generate__arc_coord( xc=[0,0,0], radius=1.0, th1=20.0, th2=300.0, \
                         nDiv=101, outFile="test/out.dat" )

    import nkUtilities.load__pointFile as lpf
    Data    = lpf.load__pointFile( inpFile="test/out.dat", returnType="point" )

    import nkUtilities.plot1D       as pl1
    import nkUtilities.load__config as lcf
    
    x_,y_                    = 0, 1
    pngFile                  = "png/out.png"
    config                   = lcf.load__config()
    config["plt_xAutoRange"] = False
    config["plt_yAutoRange"] = False
    config["plt_xRange"]     = [ -1.2, +1.2 ]
    config["plt_yRange"]     = [ -1.2, +1.2 ]

    fig  = pl1.plot1D( pngFile=pngFile, config=config )
    fig.add__plot( xAxis=Data[:,x_], yAxis=Data[:,y_], color="royalblue", linestyle="--" )
    fig.set__axis()
    fig.save__figure()


