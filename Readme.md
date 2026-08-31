```markdown
Python version: 3.8.20
```
## Test
```sh
cd .
pytest
```


<!-- USAGE EXAMPLES -->
## Statistc overtime card
```sh
python src/work_card/insert.py -c cars.xlsx -l cars_leave_logs.xlsx
```

## Send sms to the driver who owns overtime card
```sh
python src/work_card/send_sms.py -f 2026-08-31#超时转临停车辆.xlxs
```