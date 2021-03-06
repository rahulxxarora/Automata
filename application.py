from flask import Flask, request, json
from CommandClassifier import decode_command, init


application            = Flask(__name__)
application.secret_key = "Automata#secure#Key"


#-----------------------------------------------------------------------------
# This function loads the classifier data and configures the system to
# be ready to use.
#-----------------------------------------------------------------------------
def _run_on_start():
    print " * Loding files..."
    init()


#-----------------------------------------------------------------------------
# This route is accessed when the application starts. 
#-----------------------------------------------------------------------------
@application.route('/')
def index():
	return "Working"


#-----------------------------------------------------------------------------
# Responsible for decoding commands. Commands are sent to this route via POST 
# method. 
#
# @params {"Command":input_query}
#-----------------------------------------------------------------------------
@application.route('/decode_command', methods=['POST'])
def decode_command_post():
	try:
		command  = request.json['command']
		mod_name = decode_command(command)
		print 'Module found - \''+mod_name+'\''
		return mod_name
	except:
		return "Invalid POST Request"


#-----------------------------------------------------------------------------
# Responsible for executing modules. Commands are sent to this route via POST 
# method. 
#
# @params {"module":mod_name}
#-----------------------------------------------------------------------------
@application.route('/execute_func', methods=['POST'])
def execute_func_post():
	mod_name    = request.json['module']
	input_query = request.json['data']
	module      = __import__(mod_name)
	print 'Executing module \''+mod_name+'\''
	module.run(input_query)
	return "Module executed successfully"  


if __name__=='__main__':
	_run_on_start()
	application.run(debug=True, use_reloader=False)