import random
name = input("What is your name?")
adjectives = ['Sneaky', 'Invisible', 'Swift', 'Brave', 'Cunning', 'Silent']
animals = ['Otter', 'Panther', 'Falcon', 'Wolf', 'Tiger', 'Fox']
codename = random.choice(adjectives) + "" + random.choice(animals)
lucky_number = random.randint(1, 99)
print(f"\nAgent {name}, your codename is **{codename}**.")
print(f"Your lucky number for today is: **{lucky_number}**.")