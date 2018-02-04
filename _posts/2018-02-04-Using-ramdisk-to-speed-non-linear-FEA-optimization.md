---
title:  "Using tmpfs to speed up non-linear finite element models"
date:   2018-02-04 11:52:00
description: Benchmark of a HDD, SSD, and tmpfs (RAM disk) for read/write, and an optimization on a non-linear FE model.
keywords: [SSD FE model performance, SSD FE model improvement, make FE model faster, speed up non-linear FEA, FE model compare HDD SSD, tmpfs for non-linear fea, ramdisk to speed up fea]
---

tl;dr Use a solid state drive (SSD) or tmpfs to speed up non-linear FE models in optimizations.

I frequently run optimizations on non-linear finite element (FE) models. In my case these optimizations require the FE model to be solved for thousands of different configurations. A lot of commercial non-linear FE codes write a substantial amount of information to the hard drive. Much of this written information can not be turned off! For large models (with a large number of degrees of freedom) the computational time required to solve the problem dominates the overall run time of the analysis. However, for small FE models the information written to the hard drive can be primary contribution of model run time.

The optimizations I've performed on non-linear FE models use somewhere between one and five hundred elements. So I'm generally in a case where the hard drive is a performance bottleneck. The benchmark for this problem is a single element non-linear FE analysis. I'm running a [genetic algorithm](https://en.wikipedia.org/wiki/Genetic_algorithm) on the FE model to find the best possible set of material parameters that match some experimental result. The genetic algorithm is using a population of 30, such that a single iteration requires the FE model to be evaluated 30 times. Before I get into the optimization results, let's cover the difference between the hard drives that I use.

[Hard disk drives](https://en.wikipedia.org/wiki/Hard_disk_drive) (HDD) have been the primary data storage mechanism for years. They are reliable, but slow by Today's standards. [Solid-state drive](https://en.wikipedia.org/wiki/Solid-state_drive) (SSD) offer significant speed improvements over traditional HDD, however the speed comes at a price. An SSD will cost more, and is potentially less reliable than a HDD.

 One of my SSDs is a 500 GB Samsung 850 evo, whose five year warranty only covers the first [125 TB's written](http://www.samsung.com/semiconductor/minisite/ssd/product/consumer/850evo/). Thus far, I've written about 30 TB of data to it. For comparison's sake let's consider a HDD. A Seagate Baracuda's warranty is just two years at [55 TB a year](https://www.seagate.com/www-content/datasheets/pdfs/desktop-hdd-8tbDS1770-9-1603US-en_US.pdf). So you get a shorter warranty in terms of time with the HDD, but you get more write cycles a year with it.

I've been interested in comparing my SSD performance to a [RAM drive](https://en.wikipedia.org/wiki/RAM_drive) for a while. A temporary file system, [tmpfs](https://en.wikipedia.org/wiki/Tmpfs), is a popular unix file system for creating a RAM drive. These RAM drives are really fast, however data stored to the RAM drive is volatile. This means that all information stored in the RAM drive will be permanently lost during a power cycle.

I run 32 GB of RAM on my workstation, and on my laptop (Thinkpad 13). So I often have a lot of RAM to use tmpfs. Creating a tmpfs partition is easy, all I need to run is
```bash
sudo mkdir /mnt/ramdisk
sudo mount -t tmpfs none /mnt/ramdisk -o size=16g
```
to create a 16 GB tmpfs drive.

### HDD SSD tmpfs benchmarks

I'm going to use fio to perform a worst case read/write benchmark comparison. (I don't want to use dd since I have critical data on my drives, and since I want to get an idea about the file system performance on each drive.) For information about fio see [this](https://askubuntu.com/posts/991311/revisions) post by Mikko Rantalainen.

I'm going to run
```bash
fio --name TEST --eta-newline=5s --filename=fio-tempfile.dat --rw=randrw --size=500m --io_size=10g --blocksize=4k --ioengine=libaio --fsync=1 --iodepth=1 --numjobs=1 --runtime=60 --group_reporting
```  
on my HDD, SSD, and tmpfs to demonstrate a worst case read/write speed comparison.

| **Drive**       | **Read speed (KB/s)** | **Write speed (KB/)**  |
| --------------- |:---------------------:|:----------------------:|
| **HDD**         | 101                   | 101 |
| **SSD**         | 1,890                 |   1,890 |
| **tmpfs**       | 359,782               |   363,972 |

Okay so the tmpfs RAM disk is almost 200 times faster in a worst case read/write scenario than my SSD. The SSD was about 18 times faster than my HDD.

### Optimization benchmark
I'm going to run two iterations of the genetic algorithm on the non-linear FE model for various number of CPU resources. I run the HDD only once, because it takes longer to run. This will be 60 non-linear FE analysis run for each case (two iterations of the genetic algorithm). The results are provided in the table below.

| **Drive**       | **CPU cores** | **Wall time (s)**  |
| --------------- |:---------------------:|:----------------------:|
| **HDD**         | 30                   | 1676 |
| **SSD**         | 30                 |   209 |
| **tmpfs**       | 30               |   191 |
| **SSD**         | 16                 |   268 |
| **tmpfs**       | 16              |   256 |
| **SSD**         | 8                 |   410 |
| **tmpfs**       | 8               |   398 |

The speeds between the SSD and tmpfs are very similar, with tmpfs being slightly faster in every case. Both the SSD and tmpfs are about 8 times faster than the HDD when using 30 cores. This is a significant time savings.

Since tmpfs is significantly faster than the SSD, I was hoping that the optimization would run even faster on tmpfs than the SSD. However, it appears that the hard drive bottleneck diminishes for this processes when moving to a SSD.

### Lessons learned

- consider using tmpfs or RAM disk when running optimizations on FE models
- HDD might be a performance bottleneck when evaluating several small FE models
- worst case read/write performance doesn't translate to actual performance gain

These results have convinced me that I'll never run optimizations of FE models on a HDD. SSDs are much faster than HDDs. If I can afford the RAM, I'll always consider running temporary jobs in tmpfs or similar RAM disk. In my cases, I delete the majority of data generated by a non-linear FE analysis after it is completed. It makes sense to run these jobs in tmpfs, because the data isn't crucial, and I get a performance increase.
