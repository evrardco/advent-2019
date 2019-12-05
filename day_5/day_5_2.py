from sys import argv, exit
POS_MODE = 0
IMMEDIATE_MODE = 1
MUL = 2
ADD = 1
STOP = 99
OPS = [None] #none to shift the indexing
def parse_opcode(s):
    '''
    @input: s => string rep of the opcode
    @return: ([list of modes in ascending order], opcode as int)
    '''
    s = str(s)
    l = len(s)
    op = int(s[-2:])
    modes = []
    for i in range(l - 2):
        modes.insert(0, int(s[i]))
    return (modes, op)
def val(mem, index, mode):
    '''
    @input mem the state of the program, val the value of the memory, mode the mode associated
    @output the correct value according to the mode
    '''
    value = int(mem[index])
    if mode == IMMEDIATE_MODE:
        return value

    elif mode == POS_MODE:
        return int(mem[value])

    else:
        return None

def add(ptr, mem, modes, inputs, outputs):
    # if modes[2] == IMMEDIATE_MODE:
    #     exit('Illegal parameter mode: add')
    if len(modes) == 0:
        modes = [0, 0, 1]
    elif len(modes) == 1:
        modes = modes + [0, 1]
    elif len(modes) == 2:
        modes = modes + [1]
    res = val(mem, ptr + 1, modes[0]) + val(mem, ptr + 2, modes[1])
    mem[val(mem, ptr + 3, modes[2])] = res
    return ptr + 4


OPS.append(add)

def mul(ptr, mem, modes, inputs, outputs):
    # if modes[2] == IMMEDIATE_MODE:
    #     exit('Illegal parameter mode: mul')
    
    if len(modes) == 0:
        modes = [0, 0, 1]
    elif len(modes) == 1:
        modes = modes + [0, 1]
    elif len(modes) == 2:
        modes = modes + [1]
    res = val(mem, ptr + 1, modes[0]) * val(mem, ptr + 2, modes[1])
    mem[val(mem, ptr + 3, modes[2])] = res
    return ptr + 4


OPS.append(mul)

def my_input(ptr, mem, modes, inputs, outputs):
    # if modes[0] == IMMEDIATE_MODE:
    #     exit('Illegal parameter mode: input')
    i = inputs.pop(0)

    mem[val(mem, ptr + 1, 1)] = i
    return ptr + 2

    
OPS.append(my_input)        

def output(ptr, mem, modes, inputs, outputs):
    # if modes[0] == IMMEDIATE_MODE:
    #     exit('Illegal parameter mode: input')
    if len(modes) == 0:
        modes = [0]
    out = val(mem, ptr + 1, modes[0])
    outputs.append(out)
    return ptr + 2

OPS.append(output)     

def jump_if_true(ptr, mem, modes, inputs, outputs):
    # if modes[2] == IMMEDIATE_MODE:
    #     exit('Illegal parameter mode: mul')
    
    if len(modes) == 0:
        modes = [0, 0]
    elif len(modes) == 1:
        modes = modes + [0]

    res = val(mem, ptr + 1, modes[0]) != 0
    return  val(mem, ptr + 2, modes[1]) if res else ptr + 3


OPS.append(jump_if_true)

def jump_if_false(ptr, mem, modes, inputs, outputs):
    # if modes[2] == IMMEDIATE_MODE:
    #     exit('Illegal parameter mode: mul')
    
    if len(modes) == 0:
        modes = [0, 0]
    elif len(modes) == 1:
        modes = modes + [0]

    res = val(mem, ptr + 1, modes[0]) == 0
    return  val(mem, ptr + 2, modes[1]) if res else ptr + 3

OPS.append(jump_if_false)

def less_than(ptr, mem, modes, inputs, outputs):
    if len(modes) == 0:
        modes = [0, 0, 1]
    elif len(modes) == 1:
        modes = modes + [0, 1]
    elif len(modes) == 2:
        modes = modes + [1]
    res = 1 if val(mem, ptr + 1, modes[0]) < val(mem, ptr + 2, modes[1]) else 0
    mem[val(mem, ptr + 3, modes[2])] = res
    return ptr + 4

OPS.append(less_than)

def equals(ptr, mem, modes, inputs, outputs):
    if len(modes) == 0:
        modes = [0, 0, 1]
    elif len(modes) == 1:
        modes = modes + [0, 1]
    elif len(modes) == 2:
        modes = modes + [1]
    
    res = 1 if val(mem, ptr + 1, modes[0]) == val(mem, ptr + 2, modes[1]) else 0
    mem[val(mem, ptr + 3, modes[2])] = res
    return ptr + 4

OPS.append(equals)

def run(mem, inputs, outputs):

    modes, op = parse_opcode(mem[0])
    ptr = 0
    while op != 99:
        ptr = OPS[op](ptr, mem, modes, inputs, outputs)
        modes, op = parse_opcode(mem[ptr])



if __name__ == "__main__":
    #tests
    if argv[1] == 'test':
        print(parse_opcode('1002'))

    if argv[1] == 'run':
        s = "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
        #s = "3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9"
        s = "3,225,1,225,6,6,1100,1,238,225,104,0,1001,152,55,224,1001,224,-68,224,4,224,1002,223,8,223,1001,224,4,224,1,224,223,223,1101,62,41,225,1101,83,71,225,102,59,147,224,101,-944,224,224,4,224,1002,223,8,223,101,3,224,224,1,224,223,223,2,40,139,224,1001,224,-3905,224,4,224,1002,223,8,223,101,7,224,224,1,223,224,223,1101,6,94,224,101,-100,224,224,4,224,1002,223,8,223,101,6,224,224,1,224,223,223,1102,75,30,225,1102,70,44,224,101,-3080,224,224,4,224,1002,223,8,223,1001,224,4,224,1,223,224,223,1101,55,20,225,1102,55,16,225,1102,13,94,225,1102,16,55,225,1102,13,13,225,1,109,143,224,101,-88,224,224,4,224,1002,223,8,223,1001,224,2,224,1,223,224,223,1002,136,57,224,101,-1140,224,224,4,224,1002,223,8,223,101,6,224,224,1,223,224,223,101,76,35,224,1001,224,-138,224,4,224,1002,223,8,223,101,5,224,224,1,223,224,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1008,677,677,224,1002,223,2,223,1006,224,329,1001,223,1,223,8,677,226,224,102,2,223,223,1006,224,344,101,1,223,223,1107,226,226,224,1002,223,2,223,1006,224,359,1001,223,1,223,1108,677,226,224,102,2,223,223,1005,224,374,1001,223,1,223,1007,226,226,224,102,2,223,223,1006,224,389,1001,223,1,223,108,677,677,224,1002,223,2,223,1005,224,404,1001,223,1,223,1007,677,677,224,102,2,223,223,1005,224,419,1001,223,1,223,8,226,677,224,102,2,223,223,1005,224,434,101,1,223,223,1008,677,226,224,102,2,223,223,1006,224,449,1001,223,1,223,7,677,677,224,102,2,223,223,1006,224,464,1001,223,1,223,8,226,226,224,1002,223,2,223,1005,224,479,1001,223,1,223,7,226,677,224,102,2,223,223,1006,224,494,1001,223,1,223,7,677,226,224,1002,223,2,223,1005,224,509,101,1,223,223,107,677,677,224,102,2,223,223,1006,224,524,101,1,223,223,1007,677,226,224,102,2,223,223,1006,224,539,101,1,223,223,107,226,226,224,1002,223,2,223,1006,224,554,101,1,223,223,1008,226,226,224,102,2,223,223,1006,224,569,1001,223,1,223,1107,677,226,224,1002,223,2,223,1005,224,584,101,1,223,223,1107,226,677,224,102,2,223,223,1005,224,599,101,1,223,223,1108,226,677,224,102,2,223,223,1005,224,614,101,1,223,223,108,677,226,224,102,2,223,223,1005,224,629,101,1,223,223,107,226,677,224,102,2,223,223,1006,224,644,1001,223,1,223,1108,226,226,224,1002,223,2,223,1006,224,659,101,1,223,223,108,226,226,224,102,2,223,223,1005,224,674,101,1,223,223,4,223,99,226"

        data = s.split(",")
        inputs = [5]
        outputs = []
        run(data, inputs, outputs)
        print(outputs)