"""
祈愿 · 幸运观众：自定义学号池分析

Copyright © 2025 XuangeAha(轩哥啊哈OvO)

"""

class Resolver:
    def resolve(input_str):
        result = []
        exclude_set = set()
        parts = input_str.split()
        
        try:
            for part in parts:
                if part.startswith('-'):
                    exclude_set.update(map(int, part[1:].split('-')))
                elif part.startswith('+'):
                    result.extend(map(int, part[1:].split('-')))
                else:
                    start, end = map(int, part.split('-'))
                    result.extend(range(start, end + 1))
        except ValueError:
            result = [-1]

        result = list(set([num for num in result if num not in exclude_set]))
        
        return sorted(result)
    