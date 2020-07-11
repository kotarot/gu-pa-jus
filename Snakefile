import glob

rule all:
    input:
        "summary.csv"

rule sample:
    input:
        expand("{id}", id=glob.glob("data/sample/*"))
    output:
        "summary.csv"
    shell:
        "ls {input} | tee summary.csv"
