from typing import List, Dict

def rod_cutting_memo(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання через мемоізацію

    Args:
        length: довжина стрижня
        prices: список цін, де prices[i] — ціна стрижня довжини i+1

    Returns:
        Dict з максимальним прибутком, списком довжин відрізків та кількістю розрізів
    """
    # Мемо для збереження результатів: key = rod length, value = (max_profit, cuts_list)
    memo = {}

    def helper(n: int):
        if n == 0:
            return (0, [])
        if n in memo:
            return memo[n]
        
        max_profit = float('-inf')
        best_cuts = []
        # Проходимо по можливим першим розрізам (i від 1 до n)
        for i in range(1, n + 1):
            # Переконуємося, що ціна для даної довжини існує
            if i <= len(prices):
                current_profit = prices[i - 1]
            else:
                # Якщо немає ціни для такого розміру, пропускаємо (за умовою довжина цін відповідає довжині стрижня)
                continue

            remaining_profit, remaining_cuts = helper(n - i)
            total_profit = current_profit + remaining_profit
            
            if total_profit > max_profit:
                max_profit = total_profit
                # Якщо rod не розрізали (тобто n == i), то повертаємо [n]
                if n - i == 0:
                    best_cuts = [i]
                else:
                    best_cuts = [i] + remaining_cuts

        memo[n] = (max_profit, best_cuts)
        return memo[n]
    
    max_profit, cuts = helper(length)
    # Кількість розрізів = (кількість частин - 1), якщо стрижень не розрізали, розрізів немає
    number_of_cuts = len(cuts) - 1 if len(cuts) > 0 else 0

    return {
        "max_profit": max_profit,
        "cuts": cuts,
        "number_of_cuts": number_of_cuts
    }

def rod_cutting_table(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання через табуляцію

    Args:
        length: довжина стрижня
        prices: список цін, де prices[i] — ціна стрижня довжини i+1

    Returns:
        Dict з максимальним прибутком, списком довжин відрізків та кількістю розрізів
    """
    # dp[j] буде кортеж (max_profit, cuts_list) для стрижня довжиною j
    dp = [(0, [])] * (length + 1)
    dp[0] = (0, [])
    
    for j in range(1, length + 1):
        max_profit = float('-inf')
        best_cuts = []
        # Проходимо всі можливі перші розрізи для довжини j
        for i in range(1, j + 1):
            if i <= len(prices):
                current_price = prices[i - 1]
            else:
                continue
            
            profit_for_remainder, cuts_for_remainder = dp[j - i]
            total_profit = current_price + profit_for_remainder
            if total_profit > max_profit:
                max_profit = total_profit
                # Якщо не залишилося частини, то розріз не відбувається
                if j - i == 0:
                    best_cuts = [i]
                else:
                    best_cuts = [i] + cuts_for_remainder
        dp[j] = (max_profit, best_cuts)
    
    max_profit, cuts = dp[length]
    number_of_cuts = len(cuts) - 1 if len(cuts) > 0 else 0

    return {
        "max_profit": max_profit,
        "cuts": cuts,
        "number_of_cuts": number_of_cuts
    }

def run_tests():
    """Функція для запуску всіх тестів"""
    test_cases = [
        # Тест 1: Базовий випадок
        {
            "length": 5,
            "prices": [2, 5, 7, 8, 10],
            "name": "Базовий випадок"
        },
        # Тест 2: Оптимально не різати
        {
            "length": 3,
            "prices": [1, 3, 8],
            "name": "Оптимально не різати"
        },
        # Тест 3: Всі розрізи по 1
        {
            "length": 4,
            "prices": [3, 5, 6, 7],
            "name": "Рівномірні розрізи"
        }
    ]

    for test in test_cases:
        print(f"\nТест: {test['name']}")
        print(f"Довжина стрижня: {test['length']}")
        print(f"Ціни: {test['prices']}")

        # Тестуємо мемоізацію
        memo_result = rod_cutting_memo(test['length'], test['prices'])
        print("\nРезультат мемоізації:")
        print(f"Максимальний прибуток: {memo_result['max_profit']}")
        print(f"Розрізи: {memo_result['cuts']}")
        print(f"Кількість розрізів: {memo_result['number_of_cuts']}")

        # Тестуємо табуляцію
        table_result = rod_cutting_table(test['length'], test['prices'])
        print("\nРезультат табуляції:")
        print(f"Максимальний прибуток: {table_result['max_profit']}")
        print(f"Розрізи: {table_result['cuts']}")
        print(f"Кількість розрізів: {table_result['number_of_cuts']}")

        print("\nПеревірка пройшла успішно!")

if __name__ == "__main__":
    run_tests()
