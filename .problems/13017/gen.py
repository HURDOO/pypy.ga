def get_input_output() -> list[tuple[str, str]]:
    lst = []

    for i in range(2, 10):
        out_val = []
        for j in range(1, 10):
            out_val.append(f"{i}x{j} = {i*j}")
        lst.append((f"{i}", "\n".join(out_val)))

    return lst
