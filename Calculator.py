import math
import re
from datetime import datetime

class Calculator:
    def __init__(self):
        self.history = []
        self.memory = {}
        self.last_result = 0
        self.precision = 2
        self.operations = {
            1: ('Addition', self.add),
            2: ('Subtraction', self.subtract),
            3: ('Multiplication', self.multiply),
            4: ('Division', self.divide),
            5: ('Power', self.power),
            6: ('Modulo', self.modulo),
            7: ('Square Root', self.sqrt)
        }

    def add(self, a, b):
        return round(a + b, self.precision)

    def subtract(self, a, b):
        return round(a - b, self.precision)

    def multiply(self, a, b):
        return round(a * b, self.precision)

    def divide(self, a, b):
        if b == 0:
            raise ValueError("❌ Cannot divide by zero!")
        return round(a / b, self.precision)

    def power(self, a, b):
        return round(a ** b, self.precision)

    def modulo(self, a, b):
        if b == 0:
            raise ValueError("❌ Cannot find modulo by zero!")
        return a % b

    def sqrt(self, a):
        if a < 0:
            raise ValueError("❌ Cannot find square root of negative number!")
        return round(math.sqrt(a), self.precision)

    def validate_number(self, user_input):
        try:
            number = float(user_input)
            return True, number
        except ValueError:
            return False, None

    def safe_input(self, prompt, input_type="number"):
        while True:
            user_input = input(prompt).strip()
            if input_type == "number":
                is_valid, value = self.validate_number(user_input)
                if is_valid:
                    return value
                print("❌ Invalid input! Please enter a valid number.")

            elif input_type == "choice":
                try:
                    return int(user_input)
                except ValueError:
                    print("❌ Invalid choice! Please enter a valid integer.")

            else:
                return user_input

    def add_to_history(self, operation, input1, input2, result):
        entry = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'operation': operation,
            'input1': input1,
            'input2': input2,
            'result': result
        }
        self.history.append(entry)

    def display_history(self):
        if not self.history:
            print("\n📭 No history available yet.")
            return

        print("\n" + "=" * 70)
        print("📜 CALCULATION HISTORY")
        print("=" * 70)
        for idx, entry in enumerate(self.history, 1):
            print(f"\n{idx}. [{entry['timestamp']}]")
            print(f"   Operation: {entry['operation']}")
            print(f"   Input 1: {entry['input1']}")
            if entry['input2'] is not None:
                print(f"   Input 2: {entry['input2']}")
            print(f"   Result: {entry['result']}")
        print("\n" + "=" * 70)

    def clear_history(self):
        confirm = input("Clear calculation history? (Y/N): ").strip().upper()
        if confirm == 'Y':
            self.history.clear()
            print("✓ History cleared.")
        else:
            print("✳️ History not cleared.")

    def display_operations_menu(self):
        print("\n📌 Available operations:")
        for choice, (name, _) in self.operations.items():
            print(f"   {choice}. {name}")
        print("   0. Return to main menu")

    def display_main_menu(self):
        print("\n" + "=" * 50)
        print("🔢 ADVANCED CALCULATOR 🔢")
        print("=" * 50)
        print("1. Sequential Mode (chain operations)")
        print("2. Expression Mode (single expression)")
        print("3. Batch Mode (multiple expressions)")
        print("4. Memory Mode (variables)")
        print("5. View History")
        print("6. Settings")
        print("0. Exit")
        print("=" * 50)

    def settings(self):
        print("\n⚙️ SETTINGS")
        print(f"Current decimal precision: {self.precision}")
        precision_input = input("Enter decimal precision (1-10): ").strip()
        try:
            precision_value = int(precision_input)
            if 1 <= precision_value <= 10:
                self.precision = precision_value
                print(f"✓ Precision updated to {self.precision} decimal places.")
            else:
                print("❌ Precision must be between 1 and 10.")
        except ValueError:
            print("❌ Invalid precision value.")

    def tokenize_expression(self, expression):
        expression = expression.replace(' ', '')
        tokens = re.findall(r'\d+\.\d+|\d+|[+\-*/]', expression)
        normalized_tokens = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token == '-' and (i == 0 or normalized_tokens and normalized_tokens[-1] in '+-*/'):
                if i + 1 < len(tokens):
                    next_token = tokens[i + 1]
                    normalized_tokens.append('-' + next_token)
                    i += 2
                    continue
            normalized_tokens.append(token)
            i += 1
        return normalized_tokens

    def evaluate_expression(self, expression):
        tokens = self.tokenize_expression(expression)
        if not tokens:
            raise ValueError("Empty expression.")

        for index in range(0, len(tokens), 2):
            try:
                tokens[index] = float(tokens[index])
            except ValueError:
                raise ValueError(f"Invalid number: {tokens[index]}")

        i = 1
        while i < len(tokens):
            operator = tokens[i]
            if operator == '*':
                result = tokens[i - 1] * tokens[i + 1]
                tokens = tokens[:i - 1] + [result] + tokens[i + 2:]
            elif operator == '/':
                if tokens[i + 1] == 0:
                    raise ValueError("Division by zero.")
                result = tokens[i - 1] / tokens[i + 1]
                tokens = tokens[:i - 1] + [result] + tokens[i + 2:]
            else:
                i += 2

        result = tokens[0]
        i = 1
        while i < len(tokens):
            operator = tokens[i]
            if operator == '+':
                result += tokens[i + 1]
            elif operator == '-':
                result -= tokens[i + 1]
            i += 2

        return round(result, self.precision)

    def is_valid_variable_name(self, name):
        return bool(re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name))

    def replace_memory_variables(self, expression):
        for var_name, var_value in self.memory.items():
            pattern = r'\b' + re.escape(var_name) + r'\b'
            expression = re.sub(pattern, str(var_value), expression)
        return expression

    def evaluate_with_memory(self, expression):
        expression_with_values = self.replace_memory_variables(expression)
        return self.evaluate_expression(expression_with_values)

    def sequential_mode(self):
        print("\n" + "=" * 50)
        print("🔁 SEQUENTIAL CALCULATION MODE")
        print("=" * 50)

        result = self.safe_input("Enter first number: ", "number")
        while True:
            print(f"\n📊 Current result: {result}")
            self.display_operations_menu()

            choice = self.safe_input("Choose operation (0-7): ", "choice")
            if choice == 0:
                break

            if choice not in self.operations:
                print("❌ Invalid operation selection.")
                continue

            operation_name, operation_func = self.operations[choice]
            previous_result = result

            try:
                if choice == 7:
                    result = operation_func(result)
                    self.add_to_history(operation_name, previous_result, None, result)
                else:
                    second_number = self.safe_input("Enter second number: ", "number")
                    result = operation_func(result, second_number)
                    self.add_to_history(operation_name, previous_result, second_number, result)

                print(f"✓ {operation_name} completed. New result: {result}")
                self.last_result = result

            except ValueError as error:
                print(f"❌ Error: {error}")
                continue

            continue_input = input("Continue sequential calculation? (Y/N): ").strip().upper()
            if continue_input != 'Y':
                break

        print(f"\n✅ Final sequential result: {result}")

    def expression_mode(self):
        print("\n" + "=" * 50)
        print("📐 EXPRESSION MODE")
        print("=" * 50)
        print("Enter an expression like: 10 + 5 * 2")
        print("Supported operators: +, -, *, /")

        expression = input("Enter expression: ").strip()
        if not expression:
            print("❌ No expression entered.")
            return

        try:
            expression = self.replace_memory_variables(expression)
            result = self.evaluate_expression(expression)
            print(f"✅ Result: {result}")
            self.add_to_history("Expression", expression, None, result)
            self.last_result = result
        except ValueError as error:
            print(f"❌ Error: {error}")

    def batch_mode(self):
        print("\n" + "=" * 50)
        print("📦 BATCH MODE")
        print("=" * 50)
        print("Enter multiple expressions. Type DONE when finished.")

        expressions = []
        while True:
            expression = input(f"Expression {len(expressions) + 1}: ").strip()
            if expression.upper() == 'DONE':
                break
            if expression:
                expressions.append(expression)
            else:
                print("⚠️  Empty expression ignored.")

        if not expressions:
            print("❌ No expressions entered.")
            return

        print("\n" + "=" * 50)
        print("📊 BATCH RESULTS")
        print("=" * 50)
        for idx, expression in enumerate(expressions, 1):
            try:
                expression_with_values = self.replace_memory_variables(expression)
                result = self.evaluate_expression(expression_with_values)
                print(f"{idx}. {expression} = {result}")
                self.add_to_history("Batch Expression", expression, None, result)
            except ValueError as error:
                print(f"{idx}. {expression} = ERROR: {error}")
        print("\nBatch processing complete.")

    def memory_mode(self):
        print("\n" + "=" * 50)
        print("💾 MEMORY MODE")
        print("=" * 50)
        print("Use variable assignment like: X = 10 + 5")
        print("Commands: SHOW, DELETE <var>, CLEAR, EXIT")

        while True:
            command = input("Enter command: ").strip()
            if not command:
                continue

            upper_command = command.upper()
            if upper_command == 'EXIT':
                break

            if upper_command == 'SHOW':
                if not self.memory:
                    print("📭 No variables stored.")
                else:
                    print("\nStored variables:")
                    for var_name, var_value in self.memory.items():
                        print(f"   {var_name} = {var_value}")
                continue

            if upper_command == 'CLEAR':
                if input("Clear all variables? (Y/N): ").strip().upper() == 'Y':
                    self.memory.clear()
                    print("✓ Variables cleared.")
                continue

            if upper_command.startswith('DELETE '):
                var_name = command[7:].strip()
                if var_name in self.memory:
                    del self.memory[var_name]
                    print(f"✓ {var_name} deleted.")
                else:
                    print(f"❌ Variable {var_name} not found.")
                continue

            if '=' in command:
                var_name, expression = command.split('=', 1)
                var_name = var_name.strip()
                expression = expression.strip()

                if not self.is_valid_variable_name(var_name):
                    print("❌ Invalid variable name. Use letters, numbers, and underscore only.")
                    continue

                try:
                    expression_with_values = self.replace_memory_variables(expression)
                    result = self.evaluate_expression(expression_with_values)
                    self.memory[var_name] = round(result, self.precision)
                    print(f"✅ {var_name} = {self.memory[var_name]}")
                    self.add_to_history("Variable Assignment", var_name, expression, self.memory[var_name])
                except ValueError as error:
                    print(f"❌ Error: {error}")
                continue

            print("❌ Invalid memory command. Use SHOW, DELETE, CLEAR, EXIT or assignment.")

    def run(self):
        print("\n🎉 Welcome to the Advanced Calculator!")
        while True:
            self.display_main_menu()
            choice = self.safe_input("Choose an option (0-6): ", "choice")

            if choice == 1:
                self.sequential_mode()
            elif choice == 2:
                self.expression_mode()
            elif choice == 3:
                self.batch_mode()
            elif choice == 4:
                self.memory_mode()
            elif choice == 5:
                self.display_history()
            elif choice == 6:
                self.settings()
            elif choice == 0:
                print("\n👋 Thank you for using the Advanced Calculator!")
                break
            else:
                print("❌ Invalid choice. Please select from the menu.")

            if input("\nReturn to main menu? (Y/N): ").strip().upper() != 'Y':
                print("\n👋 Goodbye!")
                break


if __name__ == "__main__":
    calculator = Calculator()
    calculator.run()


