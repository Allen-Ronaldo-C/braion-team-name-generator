from backend.gen import generate_names

if __name__ == "__main__":
    concepts = ["ai", "team", "innovation"]
    names = generate_names(concepts, count=10)
    print(names)
