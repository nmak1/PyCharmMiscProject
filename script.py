class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        else:
            raise IndexError("pop from empty stack")

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        else:
            raise IndexError("peek from empty stack")

    def size(self):
        return len(self.items)


def is_balanced(brackets):
    stack = Stack()
    opening_brackets = {'(', '[', '{'}
    closing_brackets = {')': '(', ']': '[', '}': '{'}

    for bracket in brackets:
        if bracket in opening_brackets:
            stack.push(bracket)
        elif bracket in closing_brackets:
            if stack.is_empty():
                return False
            if stack.pop() != closing_brackets[bracket]:
                return False

    return stack.is_empty()


# Пример использования
if __name__ == "__main__":
    test_cases = [
        "(((([{}]))))",
        "[([])((([[[]]])))]{()}",
        "{{[()]}}",
        "}{}",
        "{{[(])]}}",
        "[[{())}]"
    ]

    for test in test_cases:
        if is_balanced(test):
            print(f"Сбалансированно: {test}")
        else:
            print(f"Несбалансированно: {test}")
