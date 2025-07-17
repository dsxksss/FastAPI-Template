def badly_formatted_function(x: int, y: str) -> str:
    result = f"{x}:{y}"
    return result


class TestClass:
    def __init__(self, name: str):
        self.name = name

    def get_data(self) -> dict[str, list[int]]:
        return {"numbers": [1, 2, 3, 4, 5]}


if __name__ == "__main__":
    test = TestClass("example")
    print(badly_formatted_function(42, "hello"))
    print(test.get_data())
