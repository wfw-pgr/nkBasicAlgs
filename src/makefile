target = ../pylib.so
object = \
  calc__grad2d.f90 \
  calc__curl2d.f90 \
  reorder__ijk_kji.f90 \
  calc__laplacian.f90

#FC = ifort
FC = gfortran

FFLAGS  = -O3
LDFLAGS =
PYFLAGS = -shared -fPIC

.SUFFIXES: .so .f90
$(target): $(object)
	$(FC) $(PYFLAGS) $(FFLAGS) $(LDFLAGS) -o $(target) $(object)

.PHONY:all clean
clean:
	$(RM) $(target) 
all: clean $(target)
