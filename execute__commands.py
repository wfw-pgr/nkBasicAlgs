import os, sys, subprocess, glob


# ========================================================= #
# ===  execute__commands.py                             === #
# ========================================================= #

def execute__commands( commands=None, shell=False, confirm_file=True, error_handling="environ" ):

    # ------------------------------------------------- #
    # --- [1] Arguments ( commands ) check          --- #
    # ------------------------------------------------- #
    #  -- [1-1] command type check                  --  #
    if ( commands is None ): sys.exit( "[execute__commands.py] commands == ???" )
    if ( type(commands) is str  ):
        commands  = [ commands ]
    if ( type(commands) is list ):
        nCommands = len( commands )
    else:
        sys.exit( "[execute__commands.py] type(commands) == {0} ??? ".format( type(commands) ) )

    #  -- [1-2] empty command check                 --  #
    for cmd in commands:
        if ( len( cmd.split() ) == 0 ):
            print( "[execute__commands.py] empty command :: {0} [ERROR]".format( commands ) )
            sys.exit()

    #  -- [1-3] error_handling check                --  #
    if ( error_handling.lower() == "environ" ):
        if ( "PYTHON_ERROR_HANDLING_MODE" in os.environ ):
            error_handling = ( os.environ["PYTHON_ERROR_HANDLING_MODE"] ).lower()
        else:
            print( "[execute__commands.py] error_handling == environ, however can't find PYTHON_ERROR_HANDLING_MODE" )
            sys.exit()

        if ( error_handling.lower() in ["ignore","alert","stop","wait","skip"] ):
            pass
        else:
            print( "[execute__commands.py] unknown error_handling :: {0}".format( error_handling ) )
            print( "[execute__commands.py] please choose from  [ ignore, alert, stop, wait ]." )
            sys.exit()
            
        
    # ------------------------------------------------- #
    # --- [2] Arguments ( shell ) check             --- #
    # ------------------------------------------------- #
    if ( type(shell) is bool ):
        shell = [ shell for ik in range( nCommands ) ]
    if ( type(shell) is list ):
        if ( type( shell[0] ) is bool ):
            pass
        else:
            print( "[execute__commands] type( shell ) is NOT [ bool / list of bool. ]" )
            print( "[execute__commands] shell :: ", shell )
    else:
        print( "[execute__commands] type( shell ) is NOT [ bool / list of bool. ]" )
        print( "[execute__commands] shell :: ", shell )

    # ------------------------------------------------- #
    # --- [3] file confirmation                     --- #
    # ------------------------------------------------- #
    ex_commands = [ cmd for cmd in commands ]
    if ( confirm_file ):
        for ik,cmd in enumerate(commands):

            command   = ( ( cmd.split() )[0] ).lower()
            options   = [ word for word in ( cmd.split() )[1:] if ( word[0] == "-" ) ]
            operands  = [ word for word in ( cmd.split() )[1:] if ( word[0] != "-" ) ]

            
            if ( command in [ "rm", "cd" ] ):

                if ( len( operands ) < 1 ):
                    print( "[execute__commands.py] illegal command :: {0} [ERROR] ".split( cmd ) )
                    print( "[execute__commands.py] operands are insufficient... " )
                    sys.exit()

                for hfile in operands:
                    if ( len( glob.glob( hfile ) ) > 0 ):
                        pass
                    else:
                        handle__error( error_handling=error_handling, cmd=cmd, \
                                       operands=operands, nofile=hfile, commands=ex_commands )
                
            if ( command in [ "mv", "cp" ] ):

                if ( len( operands ) < 2 ):
                    print( "[execute__commands.py] illegal command :: {0} [ERROR] ".split( cmd ) )
                    print( "[execute__commands.py] operands are insufficient... " )
                    sys.exit()

                src = operands[:-1]
                dst = operands[ -1]
                
                for hfile in src:
                    if ( len( glob.glob( hfile ) ) > 0 ):
                        pass
                    else:
                        handle__error( error_handling=error_handling, cmd=cmd, \
                                       operands=operands, nofile=hfile, commands=ex_commands )

                if ( os.path.exists( dst ) ):
                    if ( os.path.isdir( dst ) ):
                        pass
                    else:
                        path_split = dst.split( "/" )
                        if   ( len( path_split ) == 0 ):
                            handle__error( error_handling=error_handling, cmd=cmd, \
                                           operands=operands, nofile=file_dir, commands=ex_commands )
                        elif ( len( path_split ) == 1 ):
                            pass
                        elif ( len( path_split ) >= 2 ):
                            file_dir = "/".join( path_split[:-1] ) + "/"
                            if ( os.path.exists( dst ) ):
                                pass
                            else:
                                handle__error( error_handling=error_handling, cmd=cmd, \
                                               operands=operands, nofile=file_dir, commands=ex_commands )
                else:
                    print( dst )
                    if ( dst[-1] == "/" ):
                        handle__error( error_handling=error_handling, cmd=cmd, \
                                       operands=operands, nofile=dst, commands=ex_commands )
                        
    # ------------------------------------------------- #
    # --- [3] execution of commands                 --- #
    # ------------------------------------------------- #
    for cmd in ex_commands:
        print( cmd )
        if ( shell[ik] ):
            ret = subprocess.run( cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
        else:
            ret = subprocess.run( cmd.split(),     stdout=subprocess.PIPE, stderr=subprocess.PIPE )
            
        if   ( ret.returncode ==  0 ):
            if ( len( ret.stdout.decode() ) > 0 ):
                print( ( ret.stdout.decode() ).strip() )

        elif ( ret.returncode !=  0 ):
            colorprint( "[execute__commands.py] returncode == -1. [ERROR]", color="red" )
            colorprint( "[execute__commands.py] stdout == {0}".format( ret.stdout.decode() ), color="red" )
            colorprint( "[execute__commands.py] stderr == {0}".format( ret.stderr.decode() ), color="red" )
        else:
            print( "[execute__commands.py] unknown returncode of subprocess :: {0}".format( ret.returncode ) )
            
    return()


# ========================================================= #
# ===  handle__error                                    === #
# ========================================================= #

def handle__error( error_handling=None, cmd=None, operands=None, nofile=None, commands=None ):

    # ------------------------------------------------- #
    # --- [1] error handling according to mode      --- #
    # ------------------------------------------------- #
    nop = True
    if ( error_handling.lower() in [ "alert", "wait", "stop", "ignore", "skip" ] ):
        colorprint( "[execute__commands.py] cannot find path. [ALERT] ", color="red" )
        if ( cmd      is not None ):
            print( "[execute__commands.py] command     :: {0}".format( cmd   ) )
        if ( operands is not None ):
            print( "[execute__commands.py] operands    :: {0}".format( " ".join ( operands ) ) )
        if ( nofile   is not None ):
            print( "[execute__commands.py] cannot find :: {0}".format( nofile ) )
        nop = False

    if ( error_handling.lower() in [ "skip"] ):
        try:
            commands.remove( cmd )
        except:
            pass
        return()

    if ( error_handling.lower() in [ "ignore" ] ):
        print( "[execute__commands.py] ignore error catch" )
        return()
        
    if ( error_handling.lower() in [ "wait" ] ):
        print( "[execute__commands.py] proceed anyway ???  [y/n] >> ", end="" )
        console = ( input() ).strip()
        if   ( console.lower() == "y" ):
            pass
        elif ( console.lower() == "n" ):
            colorprint( "[execute__commands.py] exit...", color="red" )
            error_handling = "exit"
        else:
            colorprint( "[execute__commands.py] please input [y/n]. anyway, exit...", color="red" )
            error_handling = "exit"
            
    if ( error_handling.lower() in [ "stop", "exit" ] ):
        sys.exit()

    if ( nop ):
        print( "[execute__commands.py] unknown error_handling mode... :: {0} " )
        print( error_handling )
        print()
    return()


# ========================================================= #
# ===  color print function                             === #
# ========================================================= #

def colorprint( statement, color="red" ):

    if   ( color.lower() == "red"  ):
        print( "\033[31m",end="" )
        print( statement )
        print("\033[0m", end=""  )
    elif ( color.lower() == "green" ):
        print( "\033[32m",end="" )
        print( statement )
        print("\033[0m", end=""  )
    elif ( color.lower() == "blue"  ):
        print( "\033[34m",end="" )
        print( statement )
        print("\033[0m", end=""  )
    else:
        print( "\033[31m",end="" )
        print( statement )
        print("\033[0m", end=""  )

        
# ========================================================= #
# ===   実行部                                          === #
# ========================================================= #
if ( __name__=="__main__" ):

    commands = [ "ls", "cd ../", "pwd" ]
    execute__commands( commands=commands, shell=True )

    commands = [ "mkdir -p test/dir01", "mkdir -p test/dir02", "mkdir -p test/dir03" ]
    execute__commands( commands=commands )
    
    commands = [ "touch test/file01"  , "touch test/file02"  , "touch test/file03", "touch test/file05",    ]
    execute__commands( commands=commands )
    
    commands = [ "mv test/file04 test/dir01/", "cp test/file05 test/dir05/", "cp test/file06 test/dir04/" ]
    execute__commands( commands=commands, error_handling="skip" )

    commands = [ "cp test/file01 test/dir01/", "cp test/file02 test/dir02/", "cp test/file03 test/dir03/" ]
    execute__commands( commands=commands )

    
