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

rule kadai_2020h1_1:
    input:
        expand("{sid}", sid=glob.glob("data/kadai_2020h1_1/*"))
    output:
        "results/summary_kadai_2020h1_1.csv"
    script:
        "scripts/grade.py"

rule kadai_2020h1_2:
    input:
        expand("{sid}", sid=glob.glob("data/kadai_2020h1_2/*"))
    output:
        "results/summary_kadai_2020h1_2.csv"
    script:
        "scripts/grade.py"
