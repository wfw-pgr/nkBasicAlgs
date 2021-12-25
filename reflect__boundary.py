import sys
import numpy as np

# ========================================================= #
# ===  reflect__boundary                                === #
# ========================================================= #

def reflect__boundary( Data=None, boundary="z", parity="even" ):

    x_ , y_ , z_  = 0, 1, 2
    vx_, vy_, vz_ = 3, 4, 5

    # -------------------------------------------- #
    # parity :: ( e.g. x - boundary )
    # -------------------------------------------- #
    # if ( parity == odd ):
    #      vx = - vx
    #      vy =   vy
    #      vz =   vz
    # vx is odd function against x=0 boundary.
    #
    # -------------------------------------------- #
    # if ( parity == even ):
    #      vx =   vx
    #      vy = - vy
    #      vz = - vz
    # vx is even function against x=0 boundary.
    #
    # -------------------------------------------- #
    
    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    if ( Data   is None ): sys.exit( "[reflect__boundary] Data == ???" )
    if ( type( Data ) is np.ndarray ):
        if ( Data.ndim != 4 ):
            sys.exit( "[reflect__boundary.py] dim of Data == {0} ??? ".format( Data.ndim ) )
        else:
            LI, LJ, LK = Data.shape[2], Data.shape[1], Data.shape[0]
    else:
        sys.exit( "[reflect__boundary.py] type( Data )  is not np.ndarray... :: {0}".format( type( Data ) ) )
    if ( not( parity  .lower() in [ "odd", "even" ] ) ):
        sys.exit( "[reflect__boundary.py] parity ( odd, even ) == {0} ???".format( parity   ) )
    if ( not( boundary.lower() in [ "x", "y", "z" ] ) ):
        sys.exit( "[reflect__boundary.py] boundary ( x, y, z ) == {0} ???".format( boundary ) )
    
    # ------------------------------------------------- #
    # --- [2] reflect Data                          --- #
    # ------------------------------------------------- #
    if ( boundary.lower() == "x" ):
        reverse            = np.copy( Data[:,:,:0:-1,:] )
        reverse[:,:,:, x_] = - reverse[:,:,:, x_]
        if   ( parity == "odd"  ):
            reverse[:,:,:,vx_] = - reverse[:,:,:,vx_]
        elif ( parity == "even" ):
            reverse[:,:,:,vy_] = - reverse[:,:,:,vy_]
            reverse[:,:,:,vz_] = - reverse[:,:,:,vz_]
        ret                = np.concatenate( [ reverse, Data ], axis=2 )
        
    if ( boundary.lower() == "y" ):
        reverse            = np.copy( Data[:,:0:-1,:,:] )
        reverse[:,:,:, y_] = - reverse[:,:,:, y_]
        if   ( parity == "odd"  ):
            reverse[:,:,:,vy_] = - reverse[:,:,:,vy_]
        elif ( parity == "even" ):
            reverse[:,:,:,vx_] = - reverse[:,:,:,vx_]
            reverse[:,:,:,vz_] = - reverse[:,:,:,vz_]
        ret                = np.concatenate( [ reverse, Data ], axis=1 )
        
    if ( boundary.lower() == "z" ):
        reverse            = np.copy( Data[:0:-1,:,:,:] )
        reverse[:,:,:, z_] = - reverse[:,:,:, z_]
        if   ( parity == "odd"  ):
            reverse[:,:,:,vz_] = - reverse[:,:,:,vz_]
        elif ( parity == "even" ):
            reverse[:,:,:,vx_] = - reverse[:,:,:,vx_]
            reverse[:,:,:,vy_] = - reverse[:,:,:,vy_]
        ret                = np.concatenate( [ reverse, Data ], axis=0 )
        
    # ------------------------------------------------- #
    # --- [3] return value                          --- #
    # ------------------------------------------------- #
    return( ret )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):

    vx_,vy_,vz_  = 0, 1, 2
    
    import nkUtilities.equiSpaceGrid as esg
    x1MinMaxNum  = [ 0.0, 1.0, 11 ]
    x2MinMaxNum  = [ 0.0, 1.0, 11 ]
    x3MinMaxNum  = [ 0.0, 1.0, 11 ]
    coord        = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                      x3MinMaxNum=x3MinMaxNum, returnType = "structured" )
    field        = np.copy( coord )
    norm         = np.repeat( ( np.sqrt( field[...,vx_]**2 + field[...,vy_]**2 + field[...,vz_]**2 ) )[:,:,:,None], 3, axis=3 )
    field        = field / norm
    field        = np.nan_to_num( field, nan=0.0 )
    Data         = np.concatenate( [coord,field], axis=3 )
    Data         = reflect__boundary( Data=Data, boundary="x", parity="even" )

    import nkUtilities.save__pointFile as spf
    outFile   = "test/out.dat"
    spf.save__pointFile( outFile=outFile, Data=Data )

    import nkVTKRoutines.convert__vtkStructuredGrid as vsg
    outFile = "test/out.vts"
    vsg.convert__vtkStructuredGrid( Data=Data, outFile=outFile )
    
