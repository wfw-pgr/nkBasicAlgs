subroutine calc__curl2d( Data, ret, x1, x2, LI, LJ, coordinate )
  implicit none
  character(3)    , intent(in)  :: coordinate ! 'xyz' or 'rzt' or 'rtz !'
  double precision, intent(in)  :: Data(3,LI,LJ)
  double precision, intent(out) :: ret (3,LI,LJ)
  double precision, intent(in)  :: x1(LI), x2(LJ)
  integer         , intent(in)  :: LI, LJ
  integer                       :: i, j
  integer                       :: ux_, uy_, uz_, ur_, ut_
  integer                       :: wx_, wy_, wz_, wr_, wt_
  double precision              :: dx1, dx2, ddx1Inv, ddx2Inv, rddrInv(LI)
  logical                       :: r0flag
  ! Data :: u-vector suffix !
  ! ret  :: w-vector suffix !

  ! ------------------------------------------------------ !
  ! --- [1] Coordinate Settings                        --- !
  ! ------------------------------------------------------ !
  if ( coordinate.eq.'xyz' ) then
     ux_=1; uy_=2; uz_=3; wx_=1; wy_=2; wz_=3
  endif
  if ( coordinate.eq.'rtz' ) then
     ur_=1; ut_=2; uz_=3; wr_=1; wt_=2; wz_=3
  endif
  if ( coordinate.eq.'rzt' ) then
     ur_=1; ut_=3; uz_=2; wr_=1; wt_=3; wz_=2
  endif
  dx1     = x1(2) - x1(1)
  dx2     = x2(2) - x2(1)
  ddx1Inv =  1.d0 / ( 2.d0 * dx1 )
  ddx2Inv =  1.d0 / ( 2.d0 * dx2 )
  do j=1, LJ
     do i=1, LI
        ret(wx_,i,j) = 0.d0
        ret(wy_,i,j) = 0.d0
        ret(wz_,i,j) = 0.d0
     enddo
  enddo
  

  ! ------------------------------------------------------ !
  ! --- [2]  curl calculation                          --- !
  ! ------------------------------------------------------ !
  !  -- [2-1] curl in Cartesian -- !
  if ( coordinate.eq.'xyz' ) then
     do j=2, LJ-1
        do i=2, LI-1
           ret(wx_,i,j) = + ( Data(uz_,i,j+1) - Data(uz_,i,j-1) ) * ddx2Inv
           ret(wy_,i,j) = - ( Data(uz_,i+1,j) - Data(uz_,i-1,j) ) * ddx1Inv
           ret(wz_,i,j) = + ( Data(uy_,i+1,j) - Data(uy_,i-1,j) ) * ddx1Inv &
                &         - ( Data(ux_,i,j+1) - Data(ux_,i,j-1) ) * ddx2Inv
        enddo
     enddo
  end if
  
  !  -- [2-2] curl in Cylindrical -- !
  if ( ( coordinate.eq.'rtz' ).or.( coordinate.eq.'rzt' ) ) then
     !  - [2-2-1] rddrInv   -   !
     r0flag = .false.
     do i=2, LI-1
        if ( x1(i).eq.0.d0  ) then
           r0flag     = .true.
           rddrInv(i) = 0.d0
        else
           rddrInv(i) = 1.d0 / ( x1(i)*dx1*2.d0 )
        endif
     enddo
     if ( r0flag.eqv..true. ) then
        write(6,*) '[calc__curl2d.f90] r=0 is included in x1 ( Not Error, just take care )'
     endif
     !  - [2-2-1] curl ( Main )  -   !
     do j=2, LJ-1
        do i=2, LI-1
           ret(wr_,i,j) = - (         Data(ut_,i,j+1) -         Data(ut_,i,j-1) ) * ddx2Inv
           ret(wt_,i,j) = + (         Data(ur_,i,j+1) -         Data(ur_,i,j-1) ) * ddx2Inv &
                  &       - (         Data(uz_,i+1,j) -         Data(uz_,i-1,j) ) * ddx1Inv
           ret(wz_,i,j) = + ( x1(i+1)*Data(ut_,i+1,j) - x1(i-1)*Data(ut_,i-1,j) ) * rddrInv(i)
        enddo
     enddo
  end if
  
  return
end subroutine calc__curl2d
