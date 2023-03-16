def my_input(text):
    while True:
        data = input(text)
        if data.strip() != '':
            return data
