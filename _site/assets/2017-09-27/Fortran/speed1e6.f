      program main

c gfortran speed1e7.f
c ./a.out
      implicit none
      real*8, dimension(1000000) :: X
      real*8, dimension(1000000) :: Y
      real*8, dimension(10) :: runtimes
      double precision t1, t2, meanruntimes
      integer i

      do 10, i = 1, 10
         X(:) = 1
         Y(:) = 1
         call cpu_time ( t1 )
         X = X + 2*Y
         call cpu_time ( t2 )
         runtimes(i) = t2 - t1
10    continue
      meanruntimes = sum(runtimes) / 10.0
      write ( *, '(a)' ) 'mean run time in seconds'
      write ( *, * ) meanruntimes

      stop
      end
