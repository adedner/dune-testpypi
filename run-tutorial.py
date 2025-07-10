import multiprocessing
import os, glob, sys

# Creating the tuple of all the tests
all_test = glob.glob("*.py")

tests = {
    "coreA":[
      "backuprestore.py",
      "boundary.py",
      "concepts.py",
      "discontinuousgalerkin.py",
      "dune-corepy.py",
      "dune-fempy.py",
      "filteredgridview.py",
      "geoview.py",
      "lineplot.py",
      "levelgridview.py",
      "cppfunctions.py",
      "parallelization.py",
    ],
    "coreB":[
      "othergrids.py",
      "solversInternal.py",
      "solversExternal.py",
      "laplace-adaptive.py",
      "laplace-dwr.py",
      "mcf.py",
      "mcf-algorithm.py",
      "uzawa-scipy.py",
      "evalues_laplace.py",
    ],
    "extensions":[
      "crystal.py",
      "elasticity.py",
      "spiral.py",
      "wave.py",
      "chemical.py",
      "chimpl.py",
      "euler.py",             # one of these
      # "twophaseflow.py",      # does not terminate on MACOs
      "vemdemo.py",
      "monolithicStokes.py",
      "fieldsplitStokes.py",
      # "mixed_poisson.py",
    ]}

disabled = ["3dexample.py", "limit.py"]

# This block of code enables us to call the script from command line.
def execute(process):
    print("START:",process,"...",flush=True)
    if process in disabled: return [process,'disabled']
    cmd = f'cd dune-fempy/doc ; PYTHONUNBUFFERED=1 python {process}'
    print("...",cmd,flush=True)
    ret = os.system(f'cd dune-fempy/doc ; PYTHONUNBUFFERED=1 python {process}')
    print("...",process,f"completed ({ret})",flush=True)
    return [process,ret]
def build(tests,cores):
    tests = [t[:-3] for t in tests] # remove .py
    print("PRECOMPILE",flush=True)
    cmd = f"cd dune-fempy/data ; python build.py {cores} " + " ".join(tests)
    print("...",cmd,flush=True)
    ret = os.system(cmd)
    print(f"... preccompile completed ({ret})",flush=True)
    return ret

if __name__ == "__main__":
    examples = sys.argv[1]
    cores = sys.argv[2]
    print(f"Have {cores} cores available",flush=True)

    ret = build(tests[examples],cores)
    if not ret == 0:
        sys.exit(2)

    process_pool = multiprocessing.Pool(processes = 1)
    ret = process_pool.map(execute, tests[examples])

    ret.sort()
    for r in ret:
        print(r)
    # also print which scripts are not being run by comparing with all_tests

    success = all([r[1]==0 or r[1]=="disabled" for r in ret])
    sys.exit(0 if success else 1)
