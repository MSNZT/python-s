# Первое задание
year = 2024

if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
    print("Високосный год")
else:
    print("Обычный год")


# Второе задание
number = 123321
number_to_string = str(number)
first_half_number = number_to_string[:3]
last_half_number = number_to_string[3:]

sum_first_half = 0
sum_last_half = 0
for str in first_half_number:
    sum_first_half += int(str)

for str in last_half_number:
    sum_last_half += int(str)

if sum_first_half == sum_last_half:
    print("Счастливый билет")
else:
    print("Несчастливый билет")
