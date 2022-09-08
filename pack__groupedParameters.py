import re,sys

# ========================================================= #
# ===  pack__groupedParameters.py                       === #
# ========================================================= #

def pack__groupedParameters( const=None, group=None, strip_groupName=False ):

    # ------------------------------------------------- #
    # --- [1] argument check                        --- #
    # ------------------------------------------------- #
    if ( const is None ): sys.exit( "[pack__groupedParameters.py] const == ???" )
    if ( group is None ): sys.exit( "[pack__groupedParameters.py] const == ???" )

    # ------------------------------------------------- #
    # --- [2] packing                               --- #
    # ------------------------------------------------- #
    expression   = group + r"\.(.+)"
    group_keys   = [ re.match( expression, key ) for key in list(const.keys()) ]
    group_keys   = [ key.group(1) for key in group_keys if ( key is not None ) ]
    if ( strip_groupName ):
        groupName = ""
    else:
        groupName = group + "."
    group_params = { (groupName+key):const[ group+"."+key ] for key in group_keys }
    return( group_params )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):

    const = { "ch1.name":"name1", "ch1.value":0.1, "ch1.flag":True, \
              "ch2.name":"name2", "ch2.value":0.2, "ch2.flag":False  }

    ret1  = pack__groupedParameters( const=const, group="ch1", strip_groupName=True  )
    ret2  = pack__groupedParameters( const=const, group="ch2", strip_groupName=False )
    print( ret1 )
    print( ret2 )
