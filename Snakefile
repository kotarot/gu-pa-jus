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

rule kadai_2020h1_1:
    input:
        expand("{sid}", sid=glob.glob("data/kadai_2020h1_1/*"))
    output:
        "summary_kadai_2020h1_1.csv"
    script:
        "scripts/grade.py"
