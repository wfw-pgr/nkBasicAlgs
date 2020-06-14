import numpy as np


# ========================================================= #
# ===  expand__axisymmetric                             === #
# ========================================================= #

def expand__axisymmetric( ra=None, fa=None, x1MinMaxNum=None, x2MinMaxNum=None, radius=None ):

    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( ra          is None ): sys.exit( "[expand__axisymmertic] ra          == ???" )
    if ( fa          is None ): sys.exit( "[expand__axisymmertic] fa          == ???" )
    if ( x1MinMaxNum is None ): sys.exit( "[expand__axisymmertic] x1MinMaxNum == ???" )
    if ( x2MinMaxNum is None ): sys.exit( "[expand__axisymmertic] x2MinMaxNum == ???" )
    if ( radius      is None ):
        radius = min( x1MinMaxNum[1], x2MinMaxNum[1] )
    
    # ------------------------------------------------- #
    # --- [2] grid making                           --- #
    # ------------------------------------------------- #
    import nkUtilities.equiSpaceGrid as esg
    x3MinMaxNum   = [ 0.0, 0.0, 1]
    grid          = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                       x3MinMaxNum=x3MinMaxNum, returnType = "point" )
    radii         = np.sqrt( grid[:,0]**2 + grid[:,1]**2 )
    index         = np.where( radii < radius )
    rp            = radii[index]

    # ------------------------------------------------- #
    # --- [3] interpolation                         --- #
    # ------------------------------------------------- #
    import nkInterpolator.LinearInterp1D as li1
    ret           = li1.LinearInterp1D( xa=ra, fa=fa, xp=rp )
    grid[index,2] = ret

    # ------------------------------------------------- #
    # --- [4] return                                --- #
    # ------------------------------------------------- #
    return( grid )


# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):


    inpFile     = "profile.dat"
    x1MinMaxNum = [ 0.0,0.8,101]
    x2MinMaxNum = [-0.8,0.8,101]

    ra          = np.linspace( 0.0, 1.0, 101 )
    fa          = np.cos( ra * np.pi * 0.5 ) ** 2
    
    ret         = expand__axisymmetric( ra=ra, fa=fa, radius=0.8, \
                                        x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum )
    import nkUtilities.cMapTri as cmt
    cmt.cMapTri( xAxis=ret[:,0], yAxis=ret[:,1], cMap=ret[:,2], pngFile="out.png" )
