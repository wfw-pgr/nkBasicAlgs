import numpy as np
import os, sys
import cv2

# ========================================================= #
# ===  search__nearestPoint.py                          === #
# ========================================================= #

def search__nearestPoint( vec1=None, vec2=None, returnType="index-distance", foreach=1 ):
    
    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    if ( vec1 is None ): sys.exit( "[search__nearestPoint.py] vec1 == ???" )
    if ( vec2 is None ): sys.exit( "[search__nearestPoint.py] vec2 == ???" )
    if ( vec1.ndim == 1 ): vec1 = vec1[:,None]
    if ( vec2.ndim == 1 ): vec2 = vec2[:,None]
    if ( vec1.shape[1] != vec2.shape[1] ):
        print( "[search__nearestPoint.py] vec1 & vec2 have different number of dimension." )
        print( "[search__nearestPoint.py] vec1'shape :: {} ".format( vec1.shape ) )
        print( "[search__nearestPoint.py] vec2'shape :: {} ".format( vec2.shape ) )
        sys.exit()
    else:
        nLen1 = vec1.shape[0]
        nLen2 = vec2.shape[0]
        nDims = vec1.shape[1]
    if   ( foreach == 2 ):
        axis = 0       # -- compress vec1 -- #
    elif ( foreach == 1 ):
        axis = 1       # -- compress vec2 -- #
    else:
        print( "[search__nearestPoint.py] foreach must be [ 1, 2 ].... but foreach == {} [ERROR] "\
               .format( foreach ) )
    
    # ------------------------------------------------- #
    # --- [2] calculate distance                    --- #
    # ------------------------------------------------- #
    diff = np.zeros( (nLen1,nLen2,nDims) )
    for ik in range( nDims ):
        g1,g2        = np.meshgrid( vec1[:,ik], vec2[:,ik], indexing="ij" )
        diff[:,:,ik] = g1 - g2
    dist = np.sqrt( np.sum( diff**2, axis=2 ) )
        
    # ------------------------------------------------- #
    # --- [3] find minimum distance                 --- #
    # ------------------------------------------------- #
    index    = np.argmin( dist, axis=axis, keepdims=True  )
    distance = np.take_along_axis( dist, index, axis=axis )
    index    = np.reshape( index   , (-1,) )
    distance = np.reshape( distance, (-1,) )
    
    # ------------------------------------------------- #
    # --- [4] return                                --- #
    # ------------------------------------------------- #
    if   ( returnType.lower() in [ "distance" ] ):
        ret = distance
    elif ( returnType.lower() in [ "index" ] ):
        ret = index
    elif ( returnType.lower() in [ "index-distance" ] ):
        ret = ( index, distance )
    return( ret )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):


    vMin, vMax = -1.0, +1.0
    vec1       = np.random.random( (300, 2) ) * ( vMax -vMin ) + vMin
    vec2       = np.random.random( (400, 2) ) * ( vMax -vMin ) + vMin
    print( vec1.shape, vec2.shape )
    
    returnType = "index-distance"
    index, distance = search__nearestPoint( vec1=vec1, vec2=vec2, returnType=returnType, foreach=2 )
    print( index.shape, distance.shape )


    # ------------------------------------------------- #
    # --- [2] draw test map                         --- #
    # ------------------------------------------------- #
    x_, y_, z_ = 0, 1, 2
    import nkUtilities.plot1D         as pl1
    import nkUtilities.load__config   as lcf
    import nkUtilities.configSettings as cfs
    pngFile                  = "png/test.png"
    config                   = lcf.load__config()
    config                   = cfs.configSettings( configType="plot.def", config=config )
    config["plt_xAutoRange"] = False
    config["plt_yAutoRange"] = False
    config["plt_xRange"]     = [ vMin-0.2, vMax+0.2 ]
    config["plt_yRange"]     = [ vMin-0.2, vMax+0.2 ]
    fig     = pl1.plot1D( config=config, pngFile=pngFile )
    fig.add__plot( xAxis=vec1[:,x_], yAxis=vec1[:,y_], color="Red" , linestyle="none", marker="o" )
    fig.add__plot( xAxis=vec2[:,x_], yAxis=vec2[:,y_], color="Blue", linestyle="none", marker="o"  )
    for ik,conn in enumerate( index ):
        xAxis = np.array( [ vec1[conn,x_], vec2[ik,x_] ] )
        yAxis = np.array( [ vec1[conn,y_], vec2[ik,y_] ] )
        fig.add__plot( xAxis=xAxis, yAxis=yAxis, color="Grey", linestyle="-" )
    fig.set__axis()
    fig.save__figure()


    
