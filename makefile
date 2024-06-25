# Compiler settings - Can change these according to your system setup
CC=gcc
MPICC=mpicc

# Compiler flags
CFLAGS=-lm
MPIFLAGS=-lm

# Targets
all: nt-serial nt-parallel

# Compile nt-serial
nt-serial: nt-serial.c
	$(CC) $(CFLAGS) nt-serial.c -o nt-serial

# Compile nt-parallel
nt-parallel: nt-parallel.c
	$(MPICC) $(MPIFLAGS) nt-parallel.c -o nt-parallel

# Clean targets
clean:
	rm -f nt-serial nt-parallel
