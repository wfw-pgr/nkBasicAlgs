

! ====================================================== !
! === reorder__ijk_2_kji ( point ver. )              === !
! ====================================================== !
subroutine reorder__ijk2kji_point( data, ret, LI, LJ, LK, nComponents )
  implicit none
  integer         , intent(in)  :: LI, LJ, LK, nComponents
  double precision, intent(in)  :: data(nComponents,LI*LJ*LK)
  double precision, intent(out) ::  ret(nComponents,LI*LJ*LK)
  integer                       :: i, j, k, h, ptr1, ptr2


  if ( ( LI.gt.1 ).and.( LJ.gt.1 ).and.( LK.gt.1 ) ) then
     !  -- 3D case -- !
     do k=1, LK
        do j=1, LJ
           do i=1, LI
              ptr1 = (LJ*LI)*(k-1) + (LI)*(j-1) + (i-1) + 1
              ptr2 = (LJ*LK)*(i-1) + (LK)*(j-1) + (k-1) + 1
              do h=1, nComponents
                 ret(h,ptr2) = data(h,ptr1)
              enddo
           enddo
        enddo
     enddo
     
  else if ( ( LI.gt.1 ).and.( LJ.gt.1) ) then
     !  -- 2D case -- !
     do j=1, LJ
        do i=1, LI
           ptr1 = (LI)*(j-1) + (i-1) + 1
           ptr2 = (LJ)*(i-1) + (j-1) + 1
           do h=1, nComponents
              ret(h,ptr2) = data(h,ptr1)
           enddo
        enddo
     enddo
     
  else if ( ( LI.gt.1 ) ) then
     !  -- 1D case -- !
     write(6,*) "[reorder__ijk2kji_point] (LI,LJ,LK) == ", LI, LJ, LK
     write(6,*) "[reorder__ijk2kji_point]  1D-array :: no reordering..."
     
  endif
     
  return
end subroutine reorder__ijk2kji_point



! ====================================================== !
! === reorder__kji_2_ijk ( point ver. )              === !
! ====================================================== !
subroutine reorder__kji2ijk_point( data, ret, LI, LJ, LK, nComponents )
  implicit none
  integer         , intent(in)  :: LI, LJ, LK, nComponents
  double precision, intent(in)  :: data(nComponents,LI*LJ*LK)
  double precision, intent(out) ::  ret(nComponents,LI*LJ*LK)
  integer                       :: i, j, k, h, ptr1, ptr2

  if ( ( LI.gt.1 ).and.( LJ.gt.1 ).and.( LK.gt.1 ) ) then
     !  -- 3D case -- !
     do k=1, LK
        do j=1, LJ
           do i=1, LI
              ptr1 = (LJ*LI)*(k-1) + (LI)*(j-1) + (i-1) + 1
              ptr2 = (LJ*LK)*(i-1) + (LK)*(j-1) + (k-1) + 1
              do h=1, nComponents
                 ret(h,ptr1) = data(h,ptr2)
              enddo
           enddo
        enddo
     enddo

  else if ( ( LI.gt.1 ).and.( LJ.gt.1) ) then
     !  -- 2D case -- !
     do j=1, LJ
        do i=1, LI
           ptr1 = (LI)*(j-1) + (i-1) + 1
           ptr2 = (LJ)*(i-1) + (j-1) + 1
           do h=1, nComponents
              ret(h,ptr1) = data(h,ptr2)
           enddo
        enddo
     enddo
     
  else if ( ( LI.gt.1 ) ) then
     !  -- 1D case -- !
     write(6,*) "[reorder__ijk2kji_point] (LI,LJ,LK) == ", LI, LJ, LK
     write(6,*) "[reorder__ijk2kji_point]  1D-array :: no reordering..."
     
  endif
     
  return
end subroutine reorder__kji2ijk_point



! ====================================================== !
! === reorder__ijk_2_kji  ( structured ver. )        === !
! ====================================================== !
subroutine reorder__ijk2kji_structured( data, ret, LI, LJ, LK, nComponents )
  implicit none
  integer         , intent(in)  :: LI, LJ, LK, nComponents
  double precision, intent(in)  :: data(nComponents,LI,LJ,LK)
  double precision, intent(out) ::  ret(LK,LJ,LI,nComponents)
  integer                       :: i, j, k, h
  
  do k=1, LK
     do j=1, LJ
        do i=1, LI
           do h=1, nComponents
              ret(k,j,i,h) = data(h,i,j,k)
           enddo
        enddo
     enddo
  enddo
  
  return
end subroutine reorder__ijk2kji_structured



! ====================================================== !
! === reorder__kji_2_ijk  ( structured ver. )        === !
! ====================================================== !
subroutine reorder__kji2ijk_structured( data, ret, LI, LJ, LK, nComponents )
  implicit none
  integer         , intent(in)  :: LI, LJ, LK, nComponents
  double precision, intent(in)  :: data(LK,LJ,LI,nComponents)
  double precision, intent(out) ::  ret(nComponents,LI,LJ,LK)
  integer                       :: i, j, k, h
  
  do k=1, LK
     do j=1, LJ
        do i=1, LI
           do h=1, nComponents
              ret(h,i,j,k) = data(k,j,i,h)
           enddo
        enddo
     enddo
  enddo
  
  return
end subroutine reorder__kji2ijk_structured
