import fish


def main():
    fish2 = fish.Fish("Tambaqui", 48.8, 3, "Grounded")
    print(fish2.price())
    print(fish2.production(roe_speed_level=5))


if __name__ == "__main__":
    main()
