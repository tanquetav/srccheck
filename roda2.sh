#python utilities/srchistplot.py --dbin=/tmp/data.db --verbose --classMetrics=./metrics/srccheck-class.json --routineMetrics=./metrics/srccheck-routine.json --fileMetrics=./metrics/srccheck-file.json 
python utilities/srcscatterplot.py --dbin=/tmp/data.db  --regexIgnoreFiles="external.*" --config=./metrics/srcscatterplot-config.json
