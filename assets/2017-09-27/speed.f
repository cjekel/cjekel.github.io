      program main

c gfortran -mcmodel=medium speed1e9.f
c ./a.out
      implicit none
      real*8, dimension(1000000000) :: X
      real*8, dimension(1000000000) :: Y
      real*8, dimension(10) :: runtimes
      double precision t1, t2, meanruntimes
      integer i

      do 10, i = 1, 10
         write (*, *) 'run',i
         X(:) = 1
         Y(:) = 1
         call cpu_time ( t1 )
         X = X + 2*Y
         call cpu_time ( t2 )
         runtimes(i) = t2 - t1
         write ( *, '(a)' ) 'run time  in seconds: '
         write ( *, * ) t2-t1
10    continue
      write ( *, * ) runtimes
      meanruntimes = sum(runtimes) / 10.0
      write ( *, * ) meanruntimes

      stop
      end
