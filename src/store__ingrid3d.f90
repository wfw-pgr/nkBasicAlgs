subroutine store__ingrid3d( Data, ret, nData, nCmp, LI, LJ, LK, delta, xyzRange )
  implicit none
  integer         , intent(in)  :: LI, LJ, LK, nData, nCmp
  double precision, intent(in)  :: delta(3), xyzRange(3,2)
  double precision, intent(in)  :: Data(nCmp,nData)
  double precision, intent(out) :: ret (nCmp,LI,LJ,LK)
  integer                       :: i, j, k, m, ip, jp, kp
  double precision              :: dxInv, dyInv, dzInv
  integer         , parameter   :: x_=1, y_=2, z_=3, min_=1, max_=2

  ! ------------------------------------------------------ !
  ! --- [1] Initialization of return array             --- !
  ! ------------------------------------------------------ !
  do k=1, LK
     do j=1, LJ
        do i=1, LI
           ret(x_,i,j,k) = delta(x_) * dble(i-1) + xyzRange(x_,min_)
           ret(y_,i,j,k) = delta(y_) * dble(j-1) + xyzRange(y_,min_)
           ret(z_,i,j,k) = delta(z_) * dble(k-1) + xyzRange(z_,min_)
           ret(4:,i,j,k) = 0.d0
        enddo
     enddo
  enddo

  ! ------------------------------------------------------ !
  ! --- [2] storing the data into return array         --- !
  ! ------------------------------------------------------ !

  dxInv = 1.d0 / delta(x_)
  dyInv = 1.d0 / delta(y_)
  dzInv = 1.d0 / delta(z_)

  do m=1, nData
     ip = nint( ( Data(x_,m) - xyzRange(x_,min_) ) * dxInv ) + 1
     jp = nint( ( Data(y_,m) - xyzRange(y_,min_) ) * dyInv ) + 1
     kp = nint( ( Data(z_,m) - xyzRange(z_,min_) ) * dzInv ) + 1
     
     if      ( ( ip.lt.1 ).or.( ip.gt.LI ) ) then
        write(6,*) "[store__ingrid3d.f90] CAUTION out of range. ip ::  ", ip
     else if ( ( jp.lt.1 ).or.( jp.gt.LJ ) ) then
        write(6,*) "[store__ingrid3d.f90] CAUTION out of range. jp ::  ", jp
     else if ( ( kp.lt.1 ).or.( kp.gt.LK ) ) then
        write(6,*) "[store__ingrid3d.f90] CAUTION out of range. kp ::  ", kp
     else
        ret(:,ip,jp,kp) = Data(:,m)
     endif
  end do

end subroutine store__ingrid3d
