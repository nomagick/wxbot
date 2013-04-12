#from your.module import your.app
import oproot
import opleaf

rootop= oproot.RootOperator(opleaf.operators)

hubfunc= lambda x:rootop.answer(x)