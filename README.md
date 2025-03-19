# gnmic-plotter

Python-based [gnmic](https://github.com/openconfig/gnmic/) wrapper that runs the gnmic CLI command to subscribe to streaming data and displays a live-updating plot of the received metrics.

### Usage example:
```bash
./gnmic-plotter.py -a 127.0.0.1:57400 --insecure -u admin -p admin \
subscribe --path "/state/system/cpu[sample-period=300]/system/cpu-usage" --sample-interval 5s
```
![gnmic-plotter](https://github.com/user-attachments/assets/d5ff4311-478d-48d8-8479-7e2464140d8f)
