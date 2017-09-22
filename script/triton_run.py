from triton import *
from pintool import *
from collections import OrderedDict
from copy import deepcopy
from termcolor import colored


class ElfAddrs:
    def __init__(self, filename):
        self.binary = Elf(filename)
        self.syms = self.binary.getSymbolsTable()
        self.elfStart = 0
        self.elfEnd = 0

    def getSymAddr(self, symName, flag):
        for sym in self.syms:
            if sym.getName() == symName:
                addrSymStart = sym.getValue()
                if sym.getSize() > 0:
                    addrSymEnd = addrSymStart + sym.getSize() - 1
                else:
                    addrSymEnd = addrSymStart + sym.getSize()
                # print 'symbol %s_has been founded, addr: %x - %x' %(symName,
                # addrSymStart, addrSymEnd)
                break
        if flag:
            return addrSymEnd
        else:
            return addrSymStart

    def getSelfAddr(self):
        self.elfStart = self.getSymAddr('_init', 0)
        self.elfEnd = self.getSymAddr('_end', 0)
        return (self.elfStart, self.elfEnd)

    def isLocalInstr(self, addr):
        self.getSelfAddr()
        if addr <= self.elfEnd:
            return 1
        else:
            return 0


class Input(object):
    def __init__(self, data):
        self.__data = data
        self.__bound = 0
        self.__dataAddr = dict()

    @property
    def data(self):
        return self.__data

    @property
    def bound(self):
        return self.__bound

    @property
    def dataAddr(self):
        return self.__dataAddr

    def setBound(self, bound):
        self.__bound = bound

    def addDataAddress(self, address, value):
        self.__dataAddr[address] = value


class TritonExecution:
    program = None
    input = None
    worklist = None
    inputTested = None
    entryPoint = 0
    exitPoint = 0
    whitelist = None
    myPC = None
    AddrAfterEP = 0

    @staticmethod
    def cbefore(instruction):
        if instruction.getAddress() == TritonExecution.entryPoint:
            TritonExecution.AddrAfterEP = instruction.getNextAddress()

        if instruction.getAddress() == TritonExecution.AddrAfterEP:
            # Reset the path constraint
            TritonExecution.myPC = []
            TritonExecution.input = TritonExecution.worklist.pop()  # Take the first input
            # Add this input to the tested input
            TritonExecution.inputTested.append(TritonExecution.input)
            return

        if instruction.getAddress() == TritonExecution.entryPoint and not isSnapshotEnabled():
            print colored('[+] Take Snapshot', 'white')
            takeSnapshot()
            return

        rt_name = getRoutineName(instruction.getAddress())
        if rt_name in TritonExecution.whitelist and instruction.isBranch() and instruction.getType() != OPCODE.JMP and instruction.getOperands()[0].getType() == OPERAND.IMM:
            # print colored(getRoutineName(instruction.getAddress()) + ': ' + str(instruction), 'blue')
            # next address next from the current one
            addr1 = instruction.getNextAddress()
            # Address in the instruction condition (branch taken)
            addr2 = instruction.getOperands()[0].getValue()

            # Get the reference of the RIP symbolic register
            ripId = getSymbolicRegisterId(REG.RIP)
            # print 'symbolic_id', ripId

            # [PC id, address taken, address not taken]
            if instruction.isConditionTaken():
                TritonExecution.myPC.append([ripId, addr2, addr1])
            else:
                TritonExecution.myPC.append([ripId, addr1, addr2])
            return

        if instruction.getAddress() == TritonExecution.exitPoint:
            print colored('[+] Exit point', 'magenta')
            print colored(str(TritonExecution.myPC), 'cyan')
            # print 'Symbolic variables:', getSymbolicVariables()

            # SAGE algorithm
            # http://research.microsoft.com/en-us/um/people/pg/public_psfiles/ndss2008.pdf
            print colored('input.bound ' + repr(TritonExecution.input.bound), 'green')
            for j in range(TritonExecution.input.bound, len(TritonExecution.myPC)):
                expr = []
                for i in range(0, j):
                    ripId = TritonExecution.myPC[i][0]
                    symExp = getFullAst(
                        getSymbolicExpressionFromId(ripId).getAst())
                    addr = TritonExecution.myPC[i][1]
                    expr.append(ast.assert_(
                        ast.equal(symExp, ast.bv(addr,  CPUSIZE.QWORD_BIT))))

                ripId = TritonExecution.myPC[j][0]
                symExp = getFullAst(
                    getSymbolicExpressionFromId(ripId).getAst())

                addr = TritonExecution.myPC[j][2]
                expr.append(ast.assert_(
                    ast.equal(symExp, ast.bv(addr,  CPUSIZE.QWORD_BIT))))

                expr = ast.compound(expr)
                model = getModel(expr)
                # print colored("model: " + repr(model), 'green')

                if len(model) > 0:
                    newInput = deepcopy(TritonExecution.input)
                    newInput.setBound(j + 1)

                    for k, v in model.items():
                        symVar = getSymbolicVariableFromId(k)
                        newInput.addDataAddress(
                            symVar.getKindValue(), v.getValue())
                    # print colored('New input: ' + str(newInput.dataAddr), 'red')

                    isPresent = False

                    for inp in TritonExecution.worklist:
                        if inp.dataAddr == newInput.dataAddr:
                            isPresent = True
                            break
                    if not isPresent:
                        TritonExecution.worklist.append(newInput)

            # If there is input to test in the worklist, we restore the
            # Snapshot
            if len(TritonExecution.worklist) > 0 and isSnapshotEnabled():
                print colored('[+] Restore snapshot', 'white')
                restoreSnapshot()
            return
        return

    @staticmethod
    def fini():
        print colored('[+] Done !', 'white')
        return

    @staticmethod
    def mainAnalysis(threadId):
        print colored('[+] In main', 'white')
        CPUSIZE.REG = 8
        rdi = getCurrentRegisterValue(REG.RDI)  # argc
        rsi = getCurrentRegisterValue(REG.RSI)  # argv
        argv0_addr = getCurrentMemoryValue(
            getCurrentRegisterValue(REG.RSI), CPUSIZE.REG)  # argv[0] pointer
        argv1_addr = getCurrentMemoryValue(
            rsi + CPUSIZE.REG, CPUSIZE.REG)                 # argv[1] pointer

        print colored('[+] In main() we set :', 'magenta')
        od = OrderedDict(sorted(TritonExecution.input.dataAddr.items()))

        for k, v in od.iteritems():
            print colored('%d ' % v, 'cyan'),

        print ''

        for k, v in od.iteritems():
            print colored('%c' % v, 'cyan'),

        print ''

        for k, v in od.iteritems():
            setCurrentMemoryValue(MemoryAccess(k, CPUSIZE.BYTE), v)
            convertMemoryToSymbolicVariable(
                MemoryAccess(k, CPUSIZE.BYTE), 'addr_%d' % k)

        for idx, byte in enumerate(TritonExecution.input.data):
            if argv1_addr + idx not in TritonExecution.input.dataAddr:  # Not overwrite the previous setting
                print colored('%d %c\t' % (ord(byte), ord(byte)), 'green'),
                setCurrentMemoryValue(MemoryAccess(
                    argv1_addr + idx, CPUSIZE.BYTE), ord(byte))
                convertMemoryToSymbolicVariable(MemoryAccess(
                    argv1_addr + idx, CPUSIZE.BYTE), 'addr_%d' % idx)

        print ''

    @staticmethod
    def run(inputSeed, elfAddrs, whitelist=[]):
        TritonExecution.entryPoint = elfAddrs.getSymAddr('_start', 0)
        TritonExecution.exitPoint = elfAddrs.getSymAddr('main', 1)

        TritonExecution.worklist = [Input(inputSeed), ]
        TritonExecution.inputTested = []
        TritonExecution.whitelist = whitelist

        print colored('Before start analysis', 'yellow')
        startAnalysisFromAddress(TritonExecution.entryPoint)
        insertCall(TritonExecution.mainAnalysis,
                   INSERT_POINT.ROUTINE_ENTRY, 'main')
        insertCall(TritonExecution.cbefore,      INSERT_POINT.BEFORE)
        insertCall(TritonExecution.fini,         INSERT_POINT.FINI)

        # addCallback(TritonExecution.mainAnalysis, INSERT_POINT.ROUTINE_ENTRY, "main")
        # addCallback(TritonExecution.cbefore,      INSERT_POINT.BEFORE)
        # addCallback(TritonExecution.fini,         INSERT_POINT.FINI)

        print colored('Before run program', 'yellow')
        print runProgram()


if __name__ == '__main__':
    # Set architecture
    setArchitecture(ARCH.X86_64)

    elfAddrs = ElfAddrs("programs/o.out")
    TritonExecution.run('000000000000', elfAddrs, ["main", "check"])
