class DummyUser:
    def __init__(self, id, name):
        self.id = id
        self.name = name

def paginate(data, limit, cursor = 0):
    if cursor == 0:
        data = data[:limit]
        next_cursor = limit
    else:
        data = data[cursor:(limit + cursor)]
        next_cursor = cursor + limit
        if next_cursor > len(data):
            next_cursor = ""
    return data, str(next_cursor)

def get_item_by_key_test(data, key, value):
    items = [
        item
        for item in data
        if item[key] == value
    ]
    return items[0] if len(items) == 1 else items if len(items) > 1 else None
