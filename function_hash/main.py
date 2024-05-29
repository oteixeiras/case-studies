from typing import List, Tuple

path_first_file_default = "./initial_file.txt"
path_second_file_default = "./modified_file.txt"

"""
    Run the code with the command:
    1 - python main.py
"""


def hash_function(data: list[str]) -> bytes:
    hash_state = 0x811C9DC5  # Estado inicial do hash
    prime_number = 104729  # Número primo para multiplicação

    for line in data:
        for char in line:
            # Multiplica o valor ordinal do caractere pelo número primo
            hashed_value = (ord(char) * prime_number) % 32
            # Fazendo um XOR com o valor do hash
            hash_state ^= hashed_value
            # Fazendo trocas de posição dentro do hash_state
            hash_state += (
                (hash_state << 1)
                + (hash_state << 4)
                + (hash_state << 7)
                + (hash_state << 8)
                + (hash_state << 24)
            )
            # Usando uma máscara de bits para garantir o formato
            hash_state &= 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF

    return hash_state.to_bytes(32, byteorder="big")


def file_to_lines(file_path: str) -> list[str]:
    with open(file_path, "r", encoding="utf-8") as file:
        return file.readlines()


def validate_file(data: List[str], expected_digest: bytes) -> Tuple[bool, bytes]:
    new_digest = hash_function(data)
    return (new_digest == expected_digest), new_digest


def main(
    path_first_file: str = path_first_file_default,
    path_second_file: str = path_second_file_default,
) -> None:

    list_first_content = file_to_lines(path_first_file)
    initial_digest = hash_function(list_first_content)

    print(f"Hash result of file {path_first_file} is: {initial_digest.hex()}\n")

    # verify if the modified file is valid
    list_second_content = file_to_lines(path_second_file)
    has_valid, second_digest = validate_file(list_second_content, initial_digest)

    if not has_valid:
        print(
            f"File {path_second_file} is not valid - hash is different: {second_digest.hex()} x {initial_digest.hex()}"
        )
        return None

    print(
        f"the files are identical [{path_first_file}, {path_second_file}]- hash is the same:{initial_digest.hex()}"
    )
    return None


if __name__ == "__main__":
    main()
