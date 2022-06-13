import re
from typing import TypeVar, Iterable

import pokebase


T = TypeVar("T")


class Pokedex:
    name: str
    all_entries: list
    caught: int = 0

    def __init__(self, pokedex):
        self.name = pokedex.name
        self.all_entries = pokedex.pokemon_entries
        self.load()

    def __contains__(self, item):
        return item in range(1, len(self.all_entries) + 1)

    def __len__(self) -> int:
        return round(len(self.entries) / 30)

    def _gen_entries(self):
        for i, entry in enumerate(self.all_entries):
            if self.caught | (2 ** i) != self.caught:
                yield entry

    def load(self):
        try:
            with open(self.name, "rb") as data:
                self.caught = int.from_bytes(data.read(), byteorder="little")
        except FileNotFoundError:
            pass

    def save(self):
        with open(self.name, "wb") as data:
            data.write(self.caught.to_bytes(length=round(len(self.all_entries) / 8), byteorder="little"))

    @property
    def entries(self) -> list:
        return list(self._gen_entries())

    def page(self, index: int) -> str:
        lines = []
        for line in paginate(self.entries, index - 1):
            lines.append(" ".join(f"{item.entry_number:03d} {name(item.pokemon_species):12s}" for item in line))
        return "\n".join(lines)

    def catch(self, index: int) -> None:
        self.caught |= 2 ** (index - 1)

    def uncatch(self, index: int) -> None:
        self.caught &= self.caught ^ (2 ** (index - 1))

    def detail(self, index: int) -> str:
        pokemon = self.all_entries[index - 1].pokemon_species
        output = f"{name(pokemon)}\nCatch rate: {pokemon.capture_rate}\n"
        if pokemon.is_legendary:
            output += "Legendary\n"
        if pokemon.is_mythical:
            output += "Mythical\n"
        # output += str(pokemon.evolution_chain)

        return output


def flatten(things: list[list[T]]) -> Iterable[T]:
    """Flatten a list-of-lists to a list"""
    for thing in things:
        yield from thing


def paginate(things: list[T], page: int = 0, rows: int = 5, cols: int = 6) -> list[list[T]]:
    page_size = rows * cols
    window = things[page_size * page: page_size * (page + 1)]

    return [window[i * cols:(i + 1) * cols] for i in range(rows)]


def name(thing, language: str = "en") -> str:
    """Get the localized name of a resource"""
    return next(name.name for name in thing.names if name.language.name == language)


def pick(choices: list[T], thing: str) -> T:
    """Pick from a list of options"""
    if len(choices) > 1:
        print(f"Found {len(choices)} {thing}")
        for index, choice in enumerate(choices):
            print(f" {index + 1} {name(choice)}")
        while True:
            choice = input("? ")
            try:
                return choices[int(choice) - 1]
            except (IndexError, ValueError):
                print("Try again")
    return choices[0]


def main():
    generation = pokebase.generation(int(input("Select generation: ")))
    games = list(flatten([vg.versions for vg in generation.version_groups]))
    game = pick(games, "games")
    dex = Pokedex(pick(game.version_group.pokedexes, "pokedexen"))

    catch_command = re.compile(r"(c) (\d+)", re.I)
    detail_command = re.compile(r"d (\d+)", re.I)
    page_command = re.compile(r"(p)( \d+)?", re.I)

    page = 1
    active = True
    try:
        while active:
            print(dex.page(page).strip())
            while True:
                command = input("> ")
                if match := catch_command.match(command):
                    func = dex.catch
                    if match.group(1) == "C":
                        func = dex.uncatch
                    if (item := int(match.group(2))) in dex:
                        func(item)
                    else:
                        print(f"{item} not in pokedex [1-{len(dex.all_entries)}]")
                        continue
                elif match := detail_command.match(command):
                    if (item := int(match.group(1))) in dex:
                        print(dex.detail(item))
                    else:
                        print(f"{item} not in pokedex [1-{len(dex.all_entries)}]")
                        continue
                elif match := page_command.match(command):
                    direction = 1
                    if match.group(1) == "p":
                        direction = -1

                    if match.group(2):
                        new_page = int(match.group(2).strip())
                    else:
                        new_page = page + direction
                    if new_page in range(1, len(dex) + 1):
                        page = new_page
                    else:
                        print(f"{new_page} not in [1-{len(dex)}]")
                        continue
                elif command == "q":
                    active = False
                else:
                    print("You what now?")
                    continue
                break
    except (EOFError, KeyboardInterrupt):
        pass

    dex.save()


if __name__ == "__main__":
      main()
