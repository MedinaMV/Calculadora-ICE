#!/usr/bin/env python3

import sys
import Ice
Ice.loadSlice("Calculator.ice")
import SSDD

class Calculadora(SSDD.Calculator):
    def sum(self,a:float,b:float,current=None):
        return a+b

    def sub(self,a:float,b:float,current=None):
        return a-b

    def mult(self,a:float,b:float,current=None):
        return a*b
    
    def div(self,a:float,b:float,current=None):
        if(b != 0.0):
            return a/b
        else:
            raise SSDD.ZeroDivisionError
        

class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = Calculadora()

        adapter = broker.createObjectAdapterWithEndpoints("CalculatorAdapter","tcp")
        prx = adapter.add(servant, broker.stringToIdentity("calculadora"))
        calculadora = SSDD.CalculatorPrx.uncheckedCast(prx)

        proxy = self.communicator().stringToProxy(argv[1])
        tester = SSDD.CalculatorTesterPrx.uncheckedCast(proxy)

        if not tester:
            raise RuntimeError('Invalid Proxy')

        tester.test(calculadora)

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0

if __name__ == "__main__":
    server = Server()
    sys.exit(server.main(sys.argv))