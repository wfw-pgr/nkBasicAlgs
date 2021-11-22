import os, sys, subprocess


# ========================================================= #
# ===  execute__commands.py                             === #
# ========================================================= #

def execute__commands( commands=None, shell=False ):

    # ------------------------------------------------- #
    # --- [1] Arguments                             --- #
    # ------------------------------------------------- #
    if   ( commands is None ): sys.exit( "[execute__commands.py] commands == ???" )
    if   ( type(commands) is str  ):
        commands  = [ commands ]
        nCommands = len( commands )
    elif ( type(commands) is list ):
        pass
    else:
        sys.exit( "[execute__commands.py] type(commands) == {0} ??? ".format( type(commands) ) )
    
    # ------------------------------------------------- #
    # --- [2] execute commands                      --- #
    # ------------------------------------------------- #

    if ( shell is bool ):
    
    if ( shell == True ):

        for cmd in commands:
            print( cmd )
            subprocess.call( cmd, shell=True )
        
    else:
        for cmd in commands:
            print( cmd )
            subprocess.call( cmd.split() )
    

    return()


# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #
if ( __name__=="__main__" ):

    commands = [ "ls", "cd ../", "pwd" ]
    
    execute__commands( commands=commands )
