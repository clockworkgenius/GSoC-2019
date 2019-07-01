import re

# Result data structure:
# Atfer running the task, return this to front-end/client
class FindSimResult():

    def __init__(self):
        self.score = 0.0
        self.time = 0.0
        self.figure = ""
        # When something is wrong,
        # front-end/client can get info from this
        self.error = ""

    def set_score(self, _score):
        self.score = _score

    def set_time(self, _time):
        self.time = _time

    def set_figure(self, _figure):
        self.figure = _figure

    def set_error(self, _error):
        self.error = _error

    def has_error(self):
        return not self.error == ''

class OptimizationResult():

    def __init__(self):
        self.score = 0.0
        self.time = 0.0
        self.model = ""
        # When something is wrong,
        # front-end/client can get info from this
        self.error = ""

    def set_score(self, _score):
        self.score = _score

    def set_time(self, _time):
        self.time = _time

    def set_model(self, _model):
        self.model = _model

    def set_error(self, _error):
        self.error = _error

    def has_error(self):
        return not self.error == ''

# Parse the output generated by interface_FindSim.py
# If the output pattern is changed, change the code here
# for adjustment.
def parse_output(output = str, error = str, output_type = str):
    if output_type == 'Calculation':
        t_result = FindSimResult()
    elif output_type == 'Optimization':
        t_result = OptimizationResult()
    else:
        raise AssertionError("Output type not found!")

    errormsg = ""

    # Get result from stdout output strings
    # Check if there is error or exception
    if error != ""\
    or re.search('time', output, re.I) == None\
    or re.search('score', output, re.I) == None:
        # Error happens, parse output to get the error messege
        if re.search('error',output, re.I) != None:
            p1 = re.compile(r'[a-zA-Z0-9.]*error.*', re.I)
            errors = p1.findall(output)
            errormsg += errors[-1] + '  '
        if re.search('exception',output, re.I) != None:
            p2 = re.compile(r'[a-zA-Z0-9]*exception.*', re.I)
            errors = p2.findall(output)
            errormsg += errors[-1] + '  '
        if re.search('error',error, re.I) != None:
            p3 = re.compile(r'[a-zA-Z0-9.]*error.*', re.I)
            errors = p3.findall(error)
            errormsg += errors[-1] + '  '
        if re.search('exception',error, re.I) != None:
            p4 = re.compile(r'[a-zA-Z0-9]*exception.*', re.I)
            errors = p4.findall(error)
            errormsg += errors[-1] + '  '
        if errormsg == "":
            errormsg += output+error
        t_result.set_error(errormsg)
        return t_result

    # No error, parse the getoutput
    if output_type == 'Calculation':
        f_loc = output.find('[Figure]')
        res_output = output[0:f_loc]
        res_figure = output[f_loc+len('[Figure]'):]
        outs = res_output.split(' ')

        t_result.set_score(outs[2])
        t_result.set_time(outs[6])
        t_result.set_figure(res_figure)

    elif output_type == 'Optimization':
        # TODO(Chen)
        t_result.set_score(outs[2])
        t_result.set_time(outs[6])
        outs = res_output.split(' ')
    else:
        raise AssertionError("output type not found!")

    return t_result

def decode_bytes(content):
    if content == None:
        return ""
    else:
        return content.decode()
