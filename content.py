import random

learning_snippets = [
    "Tip 1: Always check market trends before trading.",
    "Tip 2: Use stop-loss to manage risk.",
    "Tip 3: Diversify your portfolio.",
]

quiz_questions = [
    {"q": "Which indicator shows trend direction?", "options": ["MA", "RSI", "ATR"], "answer": "MA"},
    {"q": "Which is a cryptocurrency?", "options": ["EUR", "BTC", "USD"], "answer": "BTC"},
]

def get_random_lesson():
    return random.choice(learning_snippets)

def get_random_quiz():
    return random.choice(quiz_questions)
