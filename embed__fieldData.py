import numpy as np
import os, sys
import nkUtilities.load__pointFile   as lpf
import nkBasicAlgs.structurize__grid as stg


# ========================================================= #
# ===  embed__fieldData.py                              === #
# ========================================================= #

def embed__fieldData( embed=None, target=None, coordinate="3d", digit=2, out_of_boundary="ignore" ):

    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    if ( embed  is None ): sys.exit( "[embed__fieldData.py] embed  == ???" )
    if ( target is None ): sys.exit( "[embed__fieldData.py] target == ???" )
    target_ = np.copy( np.reshape( target, (-1,target.shape[-1]) ) )
    embed_  = np.copy( np.reshape( embed , (-1,embed .shape[-1]) ) )
    
    # ------------------------------------------------- #
    # --- [2] inquire grid information              --- #
    # ------------------------------------------------- #
    gi_target = stg.structurize__grid( Data=target_, returnType="dict", \
                                       coordinate=coordinate, digit=digit )
    gi_embed  = stg.structurize__grid( Data=embed_ , returnType="dict", \
                                       coordinate=coordinate, digit=digit )
    embed_          = gi_embed ["Data"]
    target_         = gi_target["Data"]
    if ( ( gi_embed["dx"] != gi_target["dx"] ) or \
         ( gi_embed["dy"] != gi_target["dy"] ) or \
         ( gi_embed["dz"] != gi_target["dz"] )      ):
        print( "[embed__fieldData.py] dx,dy,dz differ... error " )
        print( "[embed__fieldData.py] embed  :: (dx,dy,dz) :: ( {}, {}, {} )"\
               .format( gi_embed ["dx"], gi_embed ["dy"], gi_embed ["dz"] ) )
        print( "[embed__fieldData.py] target :: (dx,dy,dz) :: ( {}, {}, {} )"\
               .format( gi_target["dx"], gi_target["dy"], gi_target["dz"] ) )
        sys.exit()

    if ( gi_embed["dx"] == 0.0 ):
        dxInv = 0.0
    else:
        dxInv = 1.0 / gi_embed["dx"]

    if ( gi_embed["dy"] == 0.0 ):
        dyInv = 0.0
    else:
        dyInv = 1.0 / gi_embed["dy"]

    if ( gi_embed["dz"] == 0.0 ):
        dzInv = 0.0
    else:
        dzInv = 1.0 / gi_embed["dz"]
        
    # ------------------------------------------------- #
    # --- [3] search index                          --- #
    # ------------------------------------------------- #
    iMin_t  = round( ( ( gi_embed ["xMin"] - gi_target["xMin"] ) ) * dxInv )
    iMax_t  = round( ( ( gi_embed ["xMax"] - gi_target["xMin"] ) ) * dxInv )
    jMin_t  = round( ( ( gi_embed ["yMin"] - gi_target["yMin"] ) ) * dyInv )
    jMax_t  = round( ( ( gi_embed ["yMax"] - gi_target["yMin"] ) ) * dyInv )
    kMin_t  = round( ( ( gi_embed ["zMin"] - gi_target["zMin"] ) ) * dzInv )
    kMax_t  = round( ( ( gi_embed ["zMax"] - gi_target["zMin"] ) ) * dzInv )
    iMin_e  = max( 0, (0-iMin_t) )
    jMin_e  = max( 0, (0-iMin_t) )
    kMin_e  = max( 0, (0-iMin_t) )
    iMax_e  = min( gi_embed["LI"]-1, (gi_embed["LI"]-1)-( iMax_t-(gi_target["LI"]-1) ) )
    jMax_e  = min( gi_embed["LJ"]-1, (gi_embed["LJ"]-1)-( jMax_t-(gi_target["LJ"]-1) ) )
    kMax_e  = min( gi_embed["LK"]-1, (gi_embed["LK"]-1)-( kMax_t-(gi_target["LK"]-1) ) )

    # ------------------------------------------------- #
    # --- [4] out bounrady                          --- #
    # ------------------------------------------------- #
    if ( out_of_boundary.lower() == "stop" ):
        if ( iMin_t <  0 ):
            print( "[embed__fieldData.py] iMin_t exceeds limit... {} [ERROR] ".format( iMin_t ) )
            sys.exit()
        if ( jMin_t <  0 ):
            print( "[embed__fieldData.py] jMin_t exceeds limit... {} [ERROR] ".format( jMin_t ) )
            sys.exit()
        if ( kMin_t <  0 ):
            print( "[embed__fieldData.py] kMin_t exceeds limit... {} [ERROR] ".format( kMin_t ) )
            sys.exit()
        if ( iMax_t >= gi_target["LI"] ):
            print( "[embed__fieldData.py] iMax_t exceeds limit... {} [ERROR] ".format( iMax_t ) )
            sys.exit()
        if ( jMax_t >= gi_target["LJ"] ):
            print( "[embed__fieldData.py] jMax_t exceeds limit... {} [ERROR] ".format( jMax_t ) )
            sys.exit()
        if ( kMax_t >= gi_target["LK"] ):
            print( "[embed__fieldData.py] kMax_t exceeds limit... {} [ERROR] ".format( kMax_t ) )
            sys.exit()
        
    # ------------------------------------------------- #
    # --- [3] substitution                          --- #
    # ------------------------------------------------- #
    target_[kMin_t:kMax_t+1,jMin_t:jMax_t+1,iMin_t:iMax_t+1,:] = \
        np.copy( embed_[ kMin_e:kMax_e+1, jMin_e:jMax_e+1, iMin_e:iMax_e+1, : ] )
    return( target_ )



# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):

    x_, y_, z_ = 0, 1, 2

    # # ------------------------------------------------- #
    # # --- [1] example  (3D)                         --- #
    # # ------------------------------------------------- #
    # import nkBasicAlgs.robustInv     as inv
    # import nkUtilities.equiSpaceGrid as esg
    # x1MinMaxNum = [ -1.0, 1.0, 21 ]
    # x2MinMaxNum = [ -1.0, 1.0, 21 ]
    # x3MinMaxNum = [ -1.0, 1.0, 21 ]
    # coord       = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
    #                                  x3MinMaxNum=x3MinMaxNum, returnType = "point" )
    # radii       = np.sqrt( coord[:,x_]**2 + coord[:,y_]**2 + coord[:,z_]**2 )
    # rInv        = inv.robustInv( radii )
    # vector      = coord * np.repeat( rInv[:,None], 3, axis=1 ) * 0.0
    # target      = np.concatenate( [coord,vector], axis=1 )

    # x1MinMaxNum = [  0.0, 1.1, 12 ]
    # x2MinMaxNum = [  0.0, 1.1, 12 ]
    # x3MinMaxNum = [  0.0, 1.1, 12 ]
    # coord       = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
    #                                  x3MinMaxNum=x3MinMaxNum, returnType = "point" )
    # radii       = np.sqrt( coord[:,x_]**2 + coord[:,y_]**2 + coord[:,z_]**2 )
    # rInv        = inv.robustInv( radii )
    # vector      = coord * np.repeat( rInv[:,None], 3, axis=1 )
    # embed       = np.concatenate( [coord,vector], axis=1 )
    
    # # ------------------------------------------------- #
    # # --- [2] embed                                 --- #
    # # ------------------------------------------------- #
    # ret         = embed__fieldData( embed=embed, target=target, coordinate="3d" )
    # print( ret.shape )

    # import nkVTKRoutines.convert__vtkStructuredGrid as cvs
    # cvs.convert__vtkStructuredGrid( Data=ret, outFile="out.vts" )


    # ------------------------------------------------- #
    # --- [1] example  (2D)                         --- #
    # ------------------------------------------------- #
    import nkBasicAlgs.robustInv     as inv
    import nkUtilities.equiSpaceGrid as esg
    x1MinMaxNum = [ -1.0, 1.0, 21 ]
    x2MinMaxNum = [ -1.0, 1.0, 21 ]
    x3MinMaxNum = [  0.0, 0.0,  1 ]
    coord       = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                     x3MinMaxNum=x3MinMaxNum, returnType = "point" )
    radii       = np.sqrt( coord[:,x_]**2 + coord[:,y_]**2 + coord[:,z_]**2 )
    rInv        = inv.robustInv( radii )
    vector      = coord * np.repeat( rInv[:,None], 3, axis=1 ) * 0.0
    target      = np.concatenate( [coord,vector], axis=1 )

    x1MinMaxNum = [  0.0, 1.1, 12 ]
    x2MinMaxNum = [  0.0, 1.1, 12 ]
    x3MinMaxNum = [  0.0, 0.0,  1 ]
    coord       = esg.equiSpaceGrid( x1MinMaxNum=x1MinMaxNum, x2MinMaxNum=x2MinMaxNum, \
                                     x3MinMaxNum=x3MinMaxNum, returnType = "point" )
    radii       = np.sqrt( coord[:,x_]**2 + coord[:,y_]**2 + coord[:,z_]**2 )
    rInv        = inv.robustInv( radii )
    vector      = coord * np.repeat( rInv[:,None], 3, axis=1 )
    embed       = np.concatenate( [coord,vector], axis=1 )
    
    # ------------------------------------------------- #
    # --- [2] embed                                 --- #
    # ------------------------------------------------- #
    ret         = embed__fieldData( embed=embed, target=target, coordinate="3d" )
    import nkUtilities.save__pointFile as spf
    outFile     = "dat/out.dat"
    spf.save__pointFile( outFile=outFile, Data=ret )

    import nkVTKRoutines.convert__vtkStructuredGrid as cvs
    cvs.convert__vtkStructuredGrid( Data=ret, outFile="out.vts" )
