class MyItem:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

class MyIterable:
    def __init__(self):
        self.data = {
            "Movies": [],
            "Songs": [],
            "Others": []
        }
        self.keys = list(self.data.keys())
        self.current_key_idx = 0
        self.current_idx = 0

    def __iter__(self):
        return self

    def __next__(self):
        while self.current_key_idx < len(self.keys):
            key = self.keys[self.current_key_idx]
            if self.current_idx < len(self.data[key]):
                item = self.data[key][self.current_idx]
                self.current_idx += 1
                return item
            else:
                self.current_idx = 0
                self.current_key_idx += 1

        raise StopIteration

# 使用示例:
items = MyIterable()
items.data["Movies"] = [MyItem("Movie1"), MyItem("Movie2")]
items.data["Songs"] = [MyItem("Song1")]

for item in items:
    print(item)

print(items[2])