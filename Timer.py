class Timer(object):
    '''
    Timer decorator to measure function runtime, that provides an API to include custom summary functions 

    Args:
        max_n (int): Maximum number of measurements for that function
        additional_summary_functions (list): summary functions that take one argument of type list, that includes all runtimes for the respective function
        additional_summary_names (list): names of the summary functions

    Attributes:
        measurements (dict): Dictionary that holds a list of measurements under each function name as key, measurements are namedtuples with the fields start, end and time
    '''

    from collections import namedtuple

    measurements = {}
    Measurement = namedtuple("Measurement", ["start", "end", "time"])
    additional_summaries = {}

    def __init__(self, max_n=None, additional_summary_names = None, additional_summary_functions = None):
        asf_len = len(additional_summary_functions) if additional_summary_names is not None else 0
        asn_len = len(additional_summary_names) if additional_summary_names is not None else 0
        if asn_len != asf_len:
            raise ValueError("Please specify the same number of names and function for additional summary contents")

        self.max_n = max_n
        self.additional_summary_names = additional_summary_names
        self.additional_summary_functions = additional_summary_functions
    
    def __call__(self, func, *args, **kwargs):
        from functools import wraps
        import time

        cls = self.__class__

        if func.__name__ not in cls.measurements:
            cls.measurements[func.__name__] = []
            cls.additional_summaries[func.__name__] = zip(self.additional_summary_names, self.additional_summary_functions)
        
        @wraps(func)
        def inner(*args, **kwargs):
            start = time.time()
            ret = func(*args, **kwargs)
            end = time.time()
            if self.max_n is None or len(cls.measurements[func.__name__]) < self.max_n:
                cls.measurements[func.__name__].append(cls.Measurement(start=start, end=end, time=end-start))
            return ret
        
        return inner
    
    @classmethod
    def summary(cls):
        '''
        Classmethod to run the summary including the additional summary functions

        Returns:
            summary (dict): Dictionary containing the summary
        '''
        summary = {}
        for func in cls.measurements:
            times = [m.time for m in cls.measurements[func]]
            summary[func] = {
                "num": len(times),
                "min": min(times),
                "max": max(times),
                "mean": sum(times) / len(times)
            }
            for name, f in cls.additional_summaries[func]:
                summary[func][name] = f(times)
        return summary
    
    @classmethod
    def times(cls):
        '''
        Return the times only

        Returns:
            times (dict): Dictionary with a list of times (float) under each function name as key
        '''
        return {func_name: [m.time for m in cls.measurements[func_name]] for func_name in cls.measurements}
