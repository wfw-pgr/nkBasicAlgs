import os, sys


# ========================================================= #
# ===  split__values.py                                 === #
# ========================================================= #

def split__values( string=None ):

    # ------------------------------------------------- #
    # --- [1] arguments                             --- #
    # ------------------------------------------------- #
    if ( string is None ): sys.exit( "[split__values] string == ???" )

    # ------------------------------------------------- #
    # --- [2] separation                            --- #
    # ------------------------------------------------- #
    #  -- [2-1] comma separation                    --  #
    cs_list = string.split( "," )

    #  -- [2-2] hyphone separation                  --  #
    hp_list = []
    for sval in cs_list:
        spl = sval.split("-")
        if   ( len( spl ) == 1 ):
            hp_list += spl
        elif ( len( spl ) == 2 ):
            hp_list += [ str(val) for val in range( int(spl[0]), int(spl[1])+1 ) ]
        else:
            sys.exit( "[split__values.py] illegal number of hyphone '-'. " )
    return( hp_list )
    

# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #

if ( __name__=="__main__" ):
    string = "8,11-13,15-17,20"
    ret = split__values( string=string )
    print( ret )
