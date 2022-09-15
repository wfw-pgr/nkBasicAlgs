import os, sys, re, copy
import numpy as np


# ========================================================= #
# ===  group__keys                                      === #
# ========================================================= #

def group__keys( keys=None, NotGrouped="none", separator=".", joint="_", \
                 returnType="grouped" ):
    
    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    if ( keys        is None ): sys.exit( "[group__keys.py] keys == ???" )

    # ------------------------------------------------- #
    # --- [2] grouping keys                         --- #
    # ------------------------------------------------- #
    splited = [ ( key.split( separator ) ) for key in keys ]
    singles = [ [ NotGrouped,        spl[0]   , separator.join(spl) ] \
                for spl in splited  if ( len(spl) == 1 ) ]
    couples = [ [ spl[0],             spl[1]   , separator.join(spl) ] \
                for spl in splited  if ( len(spl) == 2 ) ]
    triples = [ [ spl[0], joint.join( spl[1:] ), separator.join(spl) ] \
                for spl in splited  if ( len(spl) >= 3 ) ]
    aranged = singles + couples + triples
    
    # ------------------------------------------------- #
    # --- [3] packing                               --- #
    # ------------------------------------------------- #
    groupNames    = [ arg[0] for arg in aranged ]
    groupNameSets = list( set( groupNames ) )
    grouped       = { grp:[] for grp in groupNameSets }
    for grp,param,_ in aranged:
        grouped[ grp ].append( param )
    backforwards  = { ( separator.join( [ arg[0], arg[1] ] ) ):arg[2] for arg in aranged }
    
    # ------------------------------------------------- #
    # --- [4] return                                --- #
    # ------------------------------------------------- #
    if   ( returnType.lower() == "grouped" ):
        return( grouped )
    elif ( returnType.lower() == "list" ):
        return( [ grouped, backforwards ] )
    elif ( returnType.lower() == "backforwards" ):
        return( backforwards )
    else:
        print( "[group__keys.py] unknown returnType :: {} ".format( returnType ) )
        
    


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):

    # ------------------------------------------------- #
    # --- [1] case 1                                --- #
    # ------------------------------------------------- #
    keys   = [ "float", "integer", "string" ]
    ret    = group__keys( keys=keys )
    print( ret )

    # ------------------------------------------------- #
    # --- [2] case 2                                --- #
    # ------------------------------------------------- #
    keys        = [ "float", "integer", "string" ]
    ret         = group__keys( keys=keys, NotGrouped="varType" )
    print( ret )

    # ------------------------------------------------- #
    # --- [3] case 3                                --- #
    # ------------------------------------------------- #
    keys   = [ "varType.float", "varType.integer", "varType.string" ]
    ret    = group__keys( keys=keys )
    print( ret )

    # ------------------------------------------------- #
    # --- [4] case 4                                --- #
    # ------------------------------------------------- #
    keys   = [ "varType.float", "varType.integer", "varType.string", "double" ]
    ret    = group__keys( keys=keys )
    print( ret )

    # ------------------------------------------------- #
    # --- [5] case 5                                --- #
    # ------------------------------------------------- #
    keys   = [ "varType.float", "varType.integer", "varType.string", "double" ]
    ret    = group__keys( keys=keys, NotGrouped="NotNamed" )
    print( ret )

    # ------------------------------------------------- #
    # --- [6] case 6                                --- #
    # ------------------------------------------------- #
    keys   = [ "varType.float", "varType.integer", "varType.string", \
               "param.type1.double", "param.type2.double" ]
    ret    = group__keys( keys=keys )
    print( ret )
