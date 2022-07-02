import glob

rule all:
    input:
        "results/summary_sample.csv"

rule sample:
    input:
        expand("{sid}", sid=glob.glob("data/sample/*"))
    output:
        "results/summary_sample.csv"
    script:
        "scripts/grade.py"

rule kadai:
    input:
        expand("{sid}", sid=glob.glob(f"data/{config['kadainame']}/*"))
    output:
        f"results/summary_{config['kadainame']}.csv"
    script:
        "scripts/grade.py"
