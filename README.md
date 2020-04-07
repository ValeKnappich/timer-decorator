# timer-decorator

Timer decorator to easily measure runtime of your functions with an api to include your own summary functions

## Install

```bash
pip install timer-decorator
```

## Example

```python
from timer_decorator.Timer import Timer

my_mean = lambda l: sum(l) / len(l)

@Timer(additional_summary_names = ["My Mean"], additional_summary_functions = [my_mean])
def test1():
    return list(range(100000))

@Timer(additional_summary_names = ["My Mean"], additional_summary_functions = [my_mean])
def test2():
    return list(range(200000))

for i in range(3):
    test1()
    test2()

print(Timer.measurements, "\n\n")
print(Timer.summary())

# Results in 
{'test1': [Measurement(start=1586254255.0741284, end=1586254255.0800347, time=0.005906343460083008), Measurement(start=1586254255.103144, 
end=1586254255.1081555, time=0.005011558532714844), Measurement(start=1586254255.1314301, end=1586254255.1367857, time=0.0053555965423583984)], 'test2': [Measurement(start=1586254255.0831418, end=1586254255.0940037, time=0.010861873626708984), Measurement(start=1586254255.1131546, end=1586254255.1223178, time=0.009163141250610352), Measurement(start=1586254255.140427, end=1586254255.1504793, time=0.010052204132080078)]}


{'test1': {'num': 3, 'min': 0.005011558532714844, 'max': 0.005906343460083008, 'mean': 0.00542449951171875, 'My Mean': 0.00542449951171875}, 'test2': {'num': 3, 'min': 0.009163141250610352, 'max': 0.010861873626708984, 'mean': 0.010025739669799805, 'My Mean': 0.010025739669799805}}
```


