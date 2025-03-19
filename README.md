# gnmic-plotter

Python-based [gnmic](https://github.com/openconfig/gnmic/) wrapper that runs the gnmic CLI command to subscribe to streaming data and displays a live-updating plot of the received metrics.

Usage example:
```bash
./gnmic-plotter.py -a 127.0.0.1:57400 --insecure -u admin -p admin \
subscribe --path "/state/system/cpu[sample-period=300]/system/cpu-usage" --sample-interval 5s
```