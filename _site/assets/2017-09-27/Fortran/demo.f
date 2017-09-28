      program main
c compile with GNU Fortran as
c gfortran -mcmodel=medium demo.f
c
c -mcmodel=medium is only needed for one billion elements
c
c to execture program run ./a.out
      implicit none
      real*8, dimension(1000000000) :: X
      real*8, dimension(1000000000) :: Y
      double precision t1, t2
      X(:) = 1
      Y(:) = 1
      call cpu_time ( t1 )
      X = X + 2*Y
      call cpu_time ( t2 )
      write ( *, '(a)' ) 'run time  in seconds: '
      write ( *, * ) t2-t1
      stop
      end
