subroutine calc__grad2d( func, dfdx1, dfdx2, dx1, dx2, LI, LJ, difftype )
  implicit none
  integer         , intent(in)  :: LI, LJ
  double precision, intent(in)  :: dx1, dx2
  double precision, intent(in)  :: func(LI,LJ)
  double precision, intent(out) :: dfdx1(LI,LJ), dfdx2(LI,LJ)
  character(1)    , intent(in)  :: difftype
  integer                       :: i, j
  logical                       :: check = .false.
  double precision              :: dx1Inv, dx2Inv

  ! ------------------------------------------------------ !
  ! --- [1] preparation                                --- !
  ! ------------------------------------------------------ !
  !  -- [1-1] zero clear of return array               --  !
  do j=1, LJ
     do i=1, LI
        dfdx1(i,j) = 0.d0
        dfdx2(i,j) = 0.d0
     enddo
  enddo

  ! ------------------------------------------------------ !
  ! --- [2] calculation of grad field                  --- !
  ! ------------------------------------------------------ !

  ! -- difftype.(1) Central Difference  -- !
  write(6,*) trim( difftype )
  if ( trim(difftype).eq."c" ) then
     dx1Inv = 1.d0 / ( 2.d0 * dx1 )
     dx2Inv = 1.d0 / ( 2.d0 * dx2 )
     do j=2, LJ-1
        do i=2, LI-1
           dfdx1(i,j) = ( func(i+1,j  ) - func(i-1,j  ) )*dx1Inv
           dfdx2(i,j) = ( func(i  ,j+1) - func(i  ,j-1) )*dx2Inv
        enddo
     enddo
     check = .true.
  endif
  ! -- difftype.(2) Forward Difference  -- !
  if ( trim(difftype).eq."f" ) then
     dx1Inv = 1.d0 / dx1
     dx2Inv = 1.d0 / dx2
     do j=1, LJ-1
        do i=1, LI-1
           dfdx1(i,j) = ( func(i+1,j  ) - func(i  ,j  ) )*dx1Inv
           dfdx2(i,j) = ( func(i  ,j+1) - func(i  ,j  ) )*dx2Inv
        enddo
     enddo
     check = .true.
  endif
  ! -- difftype.(3) Backward Difference -- !
  if ( trim(difftype).eq."b" ) then
     dx1Inv = 1.d0 / dx1
     dx2Inv = 1.d0 / dx2
     do j=2, LJ
        do i=2, LI
           dfdx1(i,j) = ( func(i  ,j  ) - func(i-1,j  ) )*dx1Inv
           dfdx2(i,j) = ( func(i  ,j  ) - func(i  ,j-1) )*dx2Inv
        enddo
     enddo
     check = .true.
  endif

  if ( check.eqv..false. ) then
     write(6,*)
     write(6,*) "[calc__grad2d.f90] CAUTION difftype is not unknown...."
     write(6,*) "[calc__grad2d.f90] NO grad2d calculation....  [ERROR] "
     write(6,*)
     return
  endif
  
  return
end subroutine calc__grad2d
