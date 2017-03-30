# A Set of Logic Bombs
This repository contains a set of artificial logic bombs following our DSN paper, <a href = "https://dsn2017.github.io">Concolic Execution on Small-Size Binaries: Challanges and Empirical Study</a>.
A major purpose of the bomb is to test the capability of symbolic/concolic execution tools.

## Lists of enclosed bomb techniques 
In our paper, we propose several accuracy challenges and scalability challenges for concolic execution tools. The logic bombs are designed leveraging the chllenges. 
### Accuracy Challanges
Context Symbolic Variable </br>
Covert Symbolic Propagation </br>
Parallel Program </br>
Symbolic Array </br>
Symbolic Jump </br>
Symbolic Context Variable </br>
Floating-point Number

### Scalability Challanges
External Function Call </br>
Crypto Function

## Installation
#:git clone https://github.com/hxuhack/logic_bombs.git </br>
#:mkdir build </br>
#:cd build </br>
#:cmake ..

## More Tips
Enable ping: sudo sysctl -w net.ipv4.ping_group_range='0 10' </br>  
