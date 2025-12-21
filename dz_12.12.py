class Calculator:
    def __init__(self):
        self.statistics = {oper: 0 for oper in '+-*/'}
        self.history: list[str] = []
        self.memory = None
    
    def crop(self, number: float):
        return int(number) if number.is_integer() else number

    def _perform_operation(self, a, b, oper, result):
        self.history.append(f'{a} {oper} {b} = {result}')
        self.statistics[oper] += 1
        return result

    def add(self, a, b):
        return self._perform_operation(a, b, '+', a + b)

    def subtract(self, a, b):
        return self._perform_operation(a, b, '-', a - b)

    def multiply(self, a, b):
        return self._perform_operation(a, b, '*', a * b)

    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError('Деление на ноль')
        return self._perform_operation(a, b, '/', self.crop(a / b))

    def memory_save(self, number):
        self.memory = number

    def memory_recall(self):
        if self.memory is None:
            raise ValueError('Память пуста')
        return self.memory
    
    def memory_clear(self):
        self.memory = None

    def show_history(self, amount=10):
        if not self.history:
            raise ValueError('История пуста')
        if not amount.is_integer() or amount < 1:
            raise ValueError('Некорректное количество строк')
        amount = min(len(self.history), amount)
        return '\n'.join(self.history[-amount::])

    def clear_history(self):
        self.history.clear()

    def undo(self):
        if len(self.history) < 2:
            raise ValueError('Нет операций для отмены')
        prev_entry = self.history[-2].split()
        last_entry = self.history[-1].split()
        last_result = self.crop(float(prev_entry[-1]))
        self.statistics[last_entry[1]] -= 1
        self.history.pop()
        return last_result

    def get_statistics(self):
        return '\n'.join(
            f'{oper}: {amount}'
            for oper, amount in self.statistics.items()
            )

# Тесты
calc = Calculator()
res1 = calc.add(1, 1)
res2 = calc.subtract(10, 5)
res3 = calc.multiply(3, 6)
res4 = calc.divide(100, 10)
print(calc.show_history())
print(calc.get_statistics())
undo_res = calc.undo()
calc.memory_save(undo_res)
print(undo_res)
print(calc.undo())
print(calc.get_statistics())
print(calc.undo())
print(calc.show_history())
print(calc.get_statistics())
res5 = calc.add(calc.memory_recall(), 1)
print(calc.show_history())
print(calc.get_statistics())