import os, sys
import numpy as np

# ========================================================= #
# ===  rotate vector                                    === #
# ========================================================= #

def rotate__vector( points=None, theta=0.0, nvec=[0,0,1], degree=True ):

    # -- points :: np.array [ nPoints, 3 ] or np.array [ nPoints, 2 ]
    
    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if ( points is None ): sys.exit( "[rotate__vector.py] points == ???" )
    if ( type( points ) is list ):
        points = np.array( points )
    if ( type( points ) is not np.ndarray ):
        sys.exit( "[rotate__vector.py] points must be list or numpy array. " )
    if ( points.ndim == 1 ):
        points = np.reshape( points, (1,-1) )
    if ( degree is True ):
        theta = theta / 180.0 * np.pi
    nvec = np.array( nvec )
        
    # ------------------------------------------------- #
    # --- [2] 2D case                               --- #
    # ------------------------------------------------- #
    if ( points.shape[1] == 2 ):
        cos  = np.cos( theta )
        sin  = np.sin( theta )
        Rmat = np.array( [ [ cos, -sin ], [ sin, cos ] ] )
        ret  = np.transpose( np.dot( Rmat, np.transpose( points ) ) )
        ret  = np.dot( points, np.transpose( Rmat) )

    # ------------------------------------------------- #
    # --- [3] 3D case along nvec                    --- #
    # ------------------------------------------------- #
    # -- from rotatation formula
    #  - R(th) r = r costh + n (n.r) ( 1 - costh )  + ( n x r ) sinth - #
    if ( points.shape[1] == 3 ):
        nrep = np.repeat( nvec[None,:], points.shape[0], axis=0 )
        cos  = np.cos( theta )
        sin  = np.sin( theta )
        rcos = points * cos
        ndr  = np.sum( nrep*points, axis=1 )
        ndrn = ( 1.0-cos ) * ( np.repeat( ndr[:,None], 3, axis=1 ) * nrep )
        snxr =       sin   * np.cross( nrep, points )
        ret  = rcos + ndrn + snxr
        
    return(ret)



# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #
if ( __name__=="__main__" ):

    # ------------------------------------------------- #
    # --- [1] 2D test                               --- #
    # ------------------------------------------------- #
    points = np.array( [ [0.0, 1.0], [1.0,0.0], [1.0,1.0] ] )
    theta  = 90.0
    ret    = rotate__vector( points=points, theta=theta )
    print( ret )

    # ------------------------------------------------- #
    # --- [2] 3D test                               --- #
    # ------------------------------------------------- #
    nvec   = [ 1., 0., 0. ]
    points = np.array( [ [0.0,1.0,0.0 ], [1.0,0.0,0.0], [1.0,1.0,0.0], [0.0,-1.0,0.0] ] )
    points = [ 0.0, 1.0, 0.0 ]
    theta  = 90.0
    ret    = rotate__vector( points=points, theta=theta, nvec=nvec )
    print( ret )
