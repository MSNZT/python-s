documents = [
    {'type': 'passport', 'number': '2207 876234', 'name': 'Василий Гупкин'},
    {'type': 'invoice', 'number': '11-2', 'name': 'Геннадий Покемонов'},
    {'type': 'insurance', 'number': '10006', 'name': 'Аристарх Павлов'}
]

directories = {
    '1': ['2207 876234', '11-2'],
    '2': ['10006'],
    '3': []
}

def get_document_number():
    return input("Введите номер документа: ")

def handle_s_command():
    doc_number = get_document_number()
    shelf_found = False
    for directory in directories:
        if doc_number in directories[directory]:
            print(f"Документ хранится на полке: {directory}")
            shelf_found = True
            break
    if not shelf_found:
        print("Документ не найден")


def handle_p_command():
    doc_number = get_document_number()
    owner_found = False
    for document in documents:
        if doc_number == document["number"]:
            print(f"Владелец документа: {document['name']}")
            owner_found = True
            break
    if not owner_found:
        print("Владелец документа не найден")


while True:
    command = input("Введите команду (p, s или q): ")
    match command:
        case "q": break
        case "p": handle_p_command()
        case "s": handle_s_command()