# Задание 1.

text = input("Введите буквы: ").strip()

if not text:
    print("Строка не может быть пустой")

middle = len(text) // 2
if len(text) % 2 == 0:
    print(f"{text[middle - 1]}{text[middle]}")
else:
    print(text[middle])



# Задание 2.

boys = ['Peter', 'Alex', 'John', 'Arthur', 'Richard', 'Michael']
girls = ['Kate', 'Liza', 'Kira', 'Emma', 'Trisha']
# boys = ['Peter', 'Alex', 'John', 'Arthur', 'Richard']
# girls = ['Kate', 'Liza', 'Kira', 'Emma', 'Trisha']

sorted_boys = sorted(boys)
sorted_girls = sorted(girls)

if len(sorted_boys) != len(sorted_girls):
    print("Внимание, кто-то может остаться без пары.")
else:
    print("Идеальные пары:")
    for i, boy in enumerate(sorted_boys):
        print(f"{sorted_boys[i]} и {sorted_girls[i]}")

