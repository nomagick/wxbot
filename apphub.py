#from your.module import your.app
import oproot
import opleaf
import opplugins

rootop= oproot.RootOperator(opleaf.operators)
rootop.register_plugin(opplugins.pre_convert_event,turn= 'prerun')
rootop.register_plugin(opplugins.post_add_reminder,turn= 'postrun')


hubfunc= lambda x:rootop.wx_answer(x)