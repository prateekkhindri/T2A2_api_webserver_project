# Removes spaces in request data values and returns the request data with removed spaces
def remove_space(request_data):

    for key, value in request_data.items():
        if isinstance(value, str):
            request_data[key] = value.strip()

    return request_data
