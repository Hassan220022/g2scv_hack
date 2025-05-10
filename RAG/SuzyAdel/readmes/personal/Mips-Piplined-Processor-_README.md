# Mips-Piplined-Processor

## Project Description & Functionality:
The MIPS pipeline processor revolutionizes computer architecture by introducing a streamlined approach to instruction execution. Built on the principles of RISC architecture, MIPS processors employ a pipelined design to boost performance and efficiency. 

This implementation of a simple MIPS processor in VHDL can perform six basic arithmetic and logical operations, as detailed in the accompanying table:
Additionally, it includes a BONUS mathematical operation/Bit wise operations , "Sine" , “Jump”, “And”, “Or”, "less than" .. 

## Structral Hazard 
OUR Processors employs a Structural hazard technique to handle these hazards, such as:

In a pipelined processor, structural hazards occur when two or more instructions require the same hardware resource simultaneously, leading to conflicts and potential delays. 

One effective partial solution to mitigate structural hazards is duplicating critical resources such as memory. 

Specifically, in the context of a MIPS pipelined processor, duplicating the memory into separate instruction memory and data memory can significantly reduce conflicts.
By having dedicated **instruction memory** for fetching instructions and separate **data memory** for reading and writing data, the processor can handle instruction fetch 
and data access in parallel without resource contention. 

This minimizes the chances of pipeline stalls caused by simultaneous access requests to the same memory hardware, thereby improving the overall efficiency and throughput of the processor. This architectural strategy allows the pipeline to operate more smoothly, as each stage can proceed independently without waiting for shared resources, effectively addressing a common cause of structural hazards.



