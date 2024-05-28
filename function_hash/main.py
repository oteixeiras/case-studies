from typing import List, Tuple

initial_file = "function_hash/initial_file.txt"
modified_file = "function_hash/modified_file.txt"


def hashFunction(data: list[str]) -> bytes:
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
    new_digest = hashFunction(data)
    return (new_digest == expected_digest), new_digest


def main() -> None:

    original_data = file_to_lines(initial_file)
    original_digest = hashFunction(original_data)

    print(f"Hash result of file {initial_file} is: {original_digest.hex()}\n")

    modified_data = file_to_lines(modified_file)
    has_valid, new_digest = validate_file(modified_data, original_digest)

    if not has_valid:
        print(
            f"File {modified_file} is not valid - hash is different: {new_digest.hex()} x {original_digest.hex()}"
        )
        return None

    print(
        f"the files are identical [{initial_file}, {modified_file}]- hash is the same:{original_digest.hex()}"
    )
    return None


if __name__ == "__main__":
    main()
