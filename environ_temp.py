import os

if __name__=="__main__":
    for item, value in os.environ.items():
        print(f"{item} > {value}")
