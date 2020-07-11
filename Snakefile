import glob

rule all:
    input:
        "summary_sample.csv"

rule sample:
    input:
        expand("{sid}", sid=glob.glob("data/sample/*"))
    output:
        "summary_sample.csv"
    script:
        "scripts/grade.py"
