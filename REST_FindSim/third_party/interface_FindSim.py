import matplotlib.pyplot as pyplot
from FindSim.findSim import *

# What this func does:
# 1)Run innerMain
# 2)Close pyplot window generated by pyplot.show() in findSim.py
# 3)Save figure into html string and print it into stdout(so that we can find score,
# time, figure in stdout.)
def run_InnerMain():
    # Parse commandLine
    parser = argparse.ArgumentParser()
    parser.add_argument( 'script', type = str)
    parser.add_argument( '-m', '--model', type = str)
    parser.add_argument( '-d', '--dump_subset', type = str, default = "" )
    parser.add_argument( '-p', '--param_file', type = str, default = "" )
    parser.add_argument( '-hp', '--hide_plot', action="store_true")
    parser.add_argument( '-hs', '--hide_subplots', action="store_true")
    parser.add_argument( '-o', '--optimize_elec', action="store_true")
    parser.add_argument( '-s', '--scale_param', nargs=3, default=[])
    parser.add_argument( '-settle_time', '--settle_time', type=float, default=0)
    args = parser.parse_args()

    # Run innerMain in FindSim
    pyplot.ion()
    #output = subprocess.getoutput(command_FindSim)
    innerMain( args.script, modelFile = args.model, dumpFname = args.dump_subset, paramFname = args.param_file, hidePlot = args.hide_plot, hideSubplots = args.hide_subplots, optimizeElec = args.optimize_elec, scaleParam = args.scale_param, settleTime = args.settle_time )

    res_figure = mpld3.fig_to_html(pyplot.figure(1))
    pyplot.close()
    print('[Figure]'+ res_figure)
    return

if __name__ == '__main__':
    run_InnerMain()
