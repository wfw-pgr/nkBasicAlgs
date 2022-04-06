import os,sys,inspect
import numpy as np

# ========================================================= #
# ===  gauss-legendre integration (1-3D)                === #
# ========================================================= #

def integrate__GaussLegendre( nGauss =15  , function=None, dim=0, kwargs=None, \
                              x1Range=None, x2Range =None, x3Range=None ):
    
    # ------------------------------------------------- #
    # --- [0] arguments                             --- #
    # ------------------------------------------------- #
    if ( not( inspect.isfunction( function ) ) ):
        sys.exit( "[integrate__GaussLegendre] function == ???" )
    if ( dim == 0 ):
        nArguments      = function.__code__.co_argcount
        nParameters     = function.__defaults__
        if ( nParameters is None ):
            nParameters = 0
        elif ( type( nParameters ) is tuple ):
            nParameters = len( nParameters )
        else:
            print( "[integrate__GaussLegendre.py] unknown argument.... function.__defaults__ == ???" )
            print( nParameters )
            sys.exit( "\n" )
        nPositionals    = nArguments - nParameters
        dim             = nPositionals
    if ( kwargs is None ):
        kwargs = {}
    if ( len(kwargs) > nParameters ):
        print()
        print( "[integrate__GaussLegendre.py] unmatched kwargs & function....[ERROR] " )
        print( "[integrate__GaussLegendre.py] kwargs      :: ", kwargs )
        print( "[integrate__GaussLegendre.py] nParameters :: ", nParameters )
        print()
        
    # ------------------------------------------------- #
    # --- [2] integral range check                  --- #
    # ------------------------------------------------- #
    if   ( dim == 1 ):
        if ( x1Range is None ): sys.exit( "[integrate__GaussLegendre.py] dim==1, x1Range == ??? " )
    if   ( dim == 2 ):
        if ( x1Range is None ): sys.exit( "[integrate__GaussLegendre.py] dim==2, x1Range == ??? " )
        if ( x2Range is None ): sys.exit( "[integrate__GaussLegendre.py] dim==2, x2Range == ??? " )
    if   ( dim == 3 ):
        if ( x1Range is None ): sys.exit( "[integrate__GaussLegendre.py] dim==3, x1Range == ??? " )
        if ( x2Range is None ): sys.exit( "[integrate__GaussLegendre.py] dim==3, x2Range == ??? " )
        if ( x3Range is None ): sys.exit( "[integrate__GaussLegendre.py] dim==3, x3Range == ??? " )
    
    # ------------------------------------------------- #
    # --- [1] call Gauss-Legendre routines          --- #
    # ------------------------------------------------- #
    if   ( dim == 1 ):
        integ = integrate__GaussLegendre_1D( nGauss=nGauss, function=function, kwargs=kwargs, \
                                             x1Range=x1Range )
    elif ( dim == 2 ):
        integ = integrate__GaussLegendre_2D( nGauss=nGauss, function=function, kwargs=kwargs, \
                                             x1Range=x1Range, x2Range=x2Range )
    elif ( dim == 3 ):
        integ = integrate__GaussLegendre_3D( nGauss=nGauss, function=function, kwargs=kwargs, \
                                             x1Range=x1Range, x2Range=x2Range, x3Range=x3Range )
    return( integ )

# ========================================================= #
# ===  gauss-legendre integration (1D)                  === #
# ========================================================= #

def integrate__GaussLegendre_1D( nGauss=9, function=None, kwargs={}, x1Range=None ):

    from_, upto_ = 0, 1

    # ------------------------------------------------- #
    # --- [0] arguments                             --- #
    # ------------------------------------------------- #
    if ( not( inspect.isfunction( function ) ) ):
        sys.exit( "[integrate__GaussLegendre_1D] function == ???" )
    if ( x1Range is None ): sys.exit( "[integrate__GaussLegendre.py] dim==1, x1Range == ??? " )
        
    # ------------------------------------------------- #
    # --- [1] obtain legendre-root and weights      --- #
    # ------------------------------------------------- #
    tk, wk = np.polynomial.legendre.leggauss( nGauss )

    # ------------------------------------------------- #
    # --- [2] convert gauss-point                   --- #
    # ------------------------------------------------- #
    coef1   =      0.5*( x1Range[upto_] - x1Range[from_] )
    xk1     = tk * 0.5*( x1Range[upto_] - x1Range[from_] ) + 0.5*( x1Range[upto_] + x1Range[from_] )
    integ   = coef1 * np.sum( wk * function( xk1, **kwargs ) )
    return( integ )


# ========================================================= #
# ===  gauss-legendre integration (2D)                  === #
# ========================================================= #

def integrate__GaussLegendre_2D( nGauss=9, function=None, kwargs={}, \
                                 x1Range=None, x2Range=None ):

    from_, upto_ = 0, 1

    # ------------------------------------------------- #
    # --- [0] arguments                             --- #
    # ------------------------------------------------- #
    if ( not( inspect.isfunction( function ) ) ):
        sys.exit( "[integrate__GaussLegendre_2D] function == ???" )
    if ( x1Range is None ): sys.exit( "[integrate__GaussLegendre.py] dim==2, x1Range == ??? " )
    if ( x2Range is None ): sys.exit( "[integrate__GaussLegendre.py] dim==2, x2Range == ??? " )
        
    # ------------------------------------------------- #
    # --- [1] obtain legendre-root and weights      --- #
    # ------------------------------------------------- #
    tk, wk = np.polynomial.legendre.leggauss( nGauss )

    # ------------------------------------------------- #
    # --- [2] convert gauss-point                   --- #
    # ------------------------------------------------- #
    coef1   =      0.5*( x1Range[upto_] - x1Range[from_] )
    coef2   =      0.5*( x2Range[upto_] - x2Range[from_] )
    xk1     = tk * 0.5*( x1Range[upto_] - x1Range[from_] ) + 0.5*( x1Range[upto_] + x1Range[from_] )
    xk2     = tk * 0.5*( x2Range[upto_] - x2Range[from_] ) + 0.5*( x2Range[upto_] + x2Range[from_] )
    xg2,xg1 = np.meshgrid( xk2, xk1, indexing="ij" )
    wk2,wk1 = np.meshgrid( wk , wk , indexing="ij" )
    xg2,xg1 = np.reshape( xg2, (-1,) ), np.reshape( xg1, (-1,) )
    wk2,wk1 = np.reshape( wk2, (-1,) ), np.reshape( wk1, (-1,) )
    integ   = coef1*coef2 * np.sum( wk1*wk2 * function( xg1, xg2, **kwargs ) )
    return( integ )


# ========================================================= #
# ===  gauss-legendre integration (3D)                  === #
# ========================================================= #

def integrate__GaussLegendre_3D( nGauss=9, kwargs={}, function=None, \
                                 x1Range=None, x2Range=None, x3Range=None ):

    from_, upto_ = 0, 1

    # ------------------------------------------------- #
    # --- [0] arguments                             --- #
    # ------------------------------------------------- #
    if ( not( inspect.isfunction( function ) ) ):
        sys.exit( "[integrate__GaussLegendre_3D] function == ???" )
    if ( x1Range is None ): sys.exit( "[integrate__GaussLegendre.py] dim==3, x1Range == ??? " )
    if ( x2Range is None ): sys.exit( "[integrate__GaussLegendre.py] dim==3, x2Range == ??? " )
    if ( x3Range is None ): sys.exit( "[integrate__GaussLegendre.py] dim==3, x3Range == ??? " )

    # ------------------------------------------------- #
    # --- [1] obtain legendre-root and weights      --- #
    # ------------------------------------------------- #
    tk, wk = np.polynomial.legendre.leggauss( nGauss )

    # ------------------------------------------------- #
    # --- [2] convert gauss-point                   --- #
    # ------------------------------------------------- #
    coef1       =      0.5*( x1Range[upto_] - x1Range[from_] )
    coef2       =      0.5*( x2Range[upto_] - x2Range[from_] )
    coef3       =      0.5*( x3Range[upto_] - x3Range[from_] )
    xk1         = tk * 0.5*( x1Range[upto_] - x1Range[from_] ) + 0.5*( x1Range[upto_] + x1Range[from_] )
    xk2         = tk * 0.5*( x2Range[upto_] - x2Range[from_] ) + 0.5*( x2Range[upto_] + x2Range[from_] )
    xk3         = tk * 0.5*( x3Range[upto_] - x3Range[from_] ) + 0.5*( x3Range[upto_] + x3Range[from_] )
    xg3,xg2,xg1 = np.meshgrid( xk3,xk2,xk1, indexing="ij" )
    wk3,wk2,wk1 = np.meshgrid( wk ,wk ,wk , indexing="ij" )
    xg3,xg2,xg1 = np.reshape( xg3, (-1,) ), np.reshape( xg2, (-1,) ), np.reshape( xg1, (-1,) )
    wk3,wk2,wk1 = np.reshape( wk3, (-1,) ), np.reshape( wk2, (-1,) ), np.reshape( wk1, (-1,) )
    integ       = coef1*coef2*coef3 * np.sum( wk1*wk2*wk3 * function( xg1, xg2, xg3, **kwargs ) )
    return( integ )


# ========================================================= #
# ===   Execution of Pragram                            === #
# ========================================================= #

if ( __name__=="__main__" ):

    # ------------------------------------------------- #
    # --- [1] parameters                            --- #
    # ------------------------------------------------- #
    nGauss = 9
    x1Range = [ -0.0, 1.0 ]
    x2Range = [ -0.0, 1.0 ]
    x3Range = [ -0.0, 1.0 ]
    kwargs1 = { "coef1":3.0 }
    kwargs2 = {}
    kwargs3 = {}

    # ------------------------------------------------- #
    # --- [2] function to be integrated             --- #
    # ------------------------------------------------- #
    def function1D( x, coef1=3.0 ):
        return( coef1*x**2 )

    def function2D( x, y ):
        return( 4.0*x*y )

    def function3D( x, y, z, c0=1.0 ):
        return( 12.0*x*y*z**2+c0 )

    # ------------------------------------------------- #
    # --- [3] integration                           --- #
    # ------------------------------------------------- #
    ans1   = integrate__GaussLegendre( nGauss=nGauss, x1Range=x1Range,                                   function=function1D, kwargs=kwargs1 )
    ans2   = integrate__GaussLegendre( nGauss=nGauss, x1Range=x1Range, x2Range=x2Range,                  function=function2D, kwargs=kwargs2 )
    ans3   = integrate__GaussLegendre( nGauss=nGauss, x1Range=x1Range, x2Range=x2Range, x3Range=x3Range, function=function3D, kwargs=kwargs3 )
    print( "[sample.py] answer (1D) :: {0}".format( ans1 ) )
    print( "[sample.py] answer (2D) :: {0}".format( ans2 ) )
    print( "[sample.py] answer (3D) :: {0}".format( ans3 ) )
