import multiprocessing
import os, glob, sys, time

# Creating the tuple of all the tests
all_test = glob.glob("*.py")

tests = {
    "coreA":[
      "boundary.py",
      "cppfunctions.py",
      "concepts.py",
      "discontinuousgalerkin.py",
      "geoview.py",
      "dune-corepy.py",
      "filteredgridview.py",
      "lineplot.py",
      "othergrids.py",
      "levelgridview.py",
      "parallelization.py",
      "elasticity.py",
      "wave.py",
      "biharmonic_IPC0.py",
    ],
    "coreB":[
      "solversInternal.py",
      "solversExternal.py",
      "dune-fempy.py",
      "laplace-adaptive.py",
      "laplace-dwr.py",
      "mcf.py",
      "mcf-algorithm.py",
      "crystal.py",
      "spiral.py",
      "backuprestore.py",
      "uzawa-scipy.py",
      "evalues_laplace.py",
      "mixed_poisson.py",
    ],
    "extensions":[
      "chemical.py",
      "chimpl.py",
      "euler.py", 
      "twophaseflow.py",      # does not terminate on MACOs
      "vemdemo.py",
      "monolithicStokes.py",
      "fieldsplitStokes.py",
      "overview_of_advection_solver.py",
      "cylinder.py"
    ]}

disabled = ["3dexample.py"]

# This block of code enables us to call the script from command line.
def execute(process):
    if sys.version_info.minor < 10 and "overview_of_advection_solver" in process:
        # Leads to ValueError: numpy.dtype size changed, may indicate binary incompatibility. Expected 96 from C header, got 88 from PyObject
        print("Skipping landlab example due to issue with Python 3.9")
        return [process,'skipped']
    print("START:",process,"...",flush=True)
    if process in disabled: return [process,'disabled']

    # first run script
    cmd = f'cd dune-fempy/doc ; PYTHONUNBUFFERED=1 python {process}'

    print("...",cmd,flush=True)
    start = time.time()
    ret = os.system(cmd)
    used = time.time() - start
    print("...",process,f"completed ({ret}) in {used}sec",flush=True)
    
    # on success also build notebook
    if ret == 0:
        notebook = process[:-3] # remove .py
        notebook += "_nb.ipynb"
        cmd = f'cd dune-fempy/doc ; make {process}'
        print("...",cmd,flush=True)
        start = time.time()
        ret = os.system(cmd)
        used = time.time() - start
        print("...",process,f"completed ({ret}) in {used}sec",flush=True)

    return [process,ret,used]

def build(tests,cores):
    tests = [t[:-3] for t in tests] # remove .py
    print("PRECOMPILE",flush=True)
    cmd = f"cd dune-fempy/data ; python build.py {cores} " + " ".join(tests)
    print("...",cmd,flush=True)
    ret = os.system(cmd)
    print(f"... preccompile completed ({ret})",flush=True)
    return ret

if __name__ == "__main__":
    examples = sys.argv[1]   # which subset of tests to execute
                             # i.e. coreA, coreB, extensions
    cores = sys.argv[2]      # how many cores are available to run scripts in parallel
                             # used only for prebuild - actual scripts are
                             # run in serial at the moment (see Pool below)

    print(f"Have {cores} cores available",flush=True)

    # prebuild to populate dune-py if possible
    ret = build(tests[examples],cores)
    # some precompilation failed but we are not yet treating this as an error
    # if not ret == 0:
    #     sys.exit(2)

    # now run the actual script subset could be in parallel but currently isn't
    process_pool = multiprocessing.Pool(processes = 1)
    ret = process_pool.map(execute, tests[examples])

    # print which script succeeded and which failed
    ret.sort()
    for r in ret:
        print(r)

    # exit with error if one or more scripts failed
    success = all([r[1]==0 or r[1]=="disabled" or r[1]=="skipped"
                   for r in ret])
    sys.exit(0 if success else 1)
