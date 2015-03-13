from fabric.api import env, run, cd

tables_options = {
    'lineitem' : 'L',
    'customers' : 'c',
    'nation' : 'n',
    'orders' : 'O',
    'parts' : 'P',
    'region' : 'r',
    'suppliers' : 's',
    'partsupp' : 'S'
}

def dbgen(sf=1, table=" "):
    if not table:
       table = "-T {tbl_opt}".format(tbl_opt=tables_options[table])
    chunks = len(env.hosts)
    if chunks > 0:
        chunk = env.hosts.index(env.host) + 1
    else: chunk = 0
    # print "Scale Factor = ", sf
    # print "Chunks = ", chunks
    # print "Chunk = ", chunk
    # print "Table = ", table
    with cd("~/tpch-kit/tpch/tpch_2_17_0/dbgen"):
        dbgen_exec = "./dbgen -f -s {sf} -C {chunks} " \
                     "-S {chunk} {tbl}".format(sf=sf, chunks=chunks, chunk=chunk, tbl=table)
        # print dbgen_exec
        run(dbgen_exec)
        run("mkdir -p ~/tpch-kit-datasets")
        run("for file in $(ls *.tbl*); "
            "do "
            "mv $(basename $file) ~/tpch-kit-datasets/;"
            "done")
    with cd("~/tpch-kit-datasets"):
        run("for file in $(ls *.tbl); "
            "do "
            "mv $file ${file%.*};"
            "gzip ${file%.*};"
            "done")


def list():
    with cd("~/tpch-kit-datasets"):
        run("ls -lh .")

def clean():
    with cd("~/tpch-kit-datasets"):
        run("rm -f *")

def install():
    with cd("~/"):
        run("git clone https://github.com/alexpap/tpch-kit.git")

def update():
    with cd("~/tpch-kit"):
        run("git pull")

def uninstall():
    with cd("~/"):
        run("rm -rf tpch-kit tpch-kit-datasets")

