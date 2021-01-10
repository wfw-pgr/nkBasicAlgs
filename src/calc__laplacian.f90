subroutine calc__laplacian( phi, lap, dx, dy, LI, LJ )
  implicit none
  integer         , intent(in)    :: LI, LJ
  double precision, intent(in)    :: dx, dy
  double precision, intent(in)    :: phi(LI,LJ)
  double precision, intent(out)   :: lap(LI,LJ)
  integer                         :: i, j
  double precision                :: dx2Inv, dy2Inv
  double precision, allocatable   :: phi_(:,:)

  ! ------------------------------------------------------ !
  ! --- [1] data copy & extend                         --- !
  ! ------------------------------------------------------ !
  allocate( phi_(0:LI+1,0:LJ+1) )
  do j=1, LJ
     do i=1, LI
        phi_(i,j) = phi(i,j)
     enddo
  enddo
  
  ! ------------------------------------------------------ !
  ! --- [2] natural boundary condition                 --- !
  ! ------------------------------------------------------ !
  do j=1, LJ
     phi_(0   ,j) = phi(1 ,j)
     phi_(LI+1,j) = phi(LI,j)
  enddo
  do i=1, LI
     phi_(i,   0) = phi(i, 1)
     phi_(i,LJ+1) = phi(i,LJ)
  enddo
  
  ! ------------------------------------------------------ !
  ! --- [3] calculate laplacian                        --- !
  ! ------------------------------------------------------ !
  dx2Inv = 1.d0 / dx**2
  dy2Inv = 1.d0 / dy**2
  do j=1, LJ
     do i=1, LI
        lap(i,j) = ( phi_(i+1,j) - 2.d0*phi_(i,j) + phi_(i-1,j) ) * dx2Inv &
             &   + ( phi_(i,j+1) - 2.d0*phi_(i,j) + phi_(i,j-1) ) * dy2Inv
     enddo
  enddo
  
  return
end subroutine calc__laplacian
