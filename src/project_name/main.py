import os

from dotenv import load_dotenv


def main() -> None:
    load_dotenv()
    openai_key = os.getenv("OPENAI_KEY")
    if not openai_key:
        raise RuntimeError("OPENAI_KEY is not set. Copy .env.example to .env and fill it in.")
    print("Environment loaded successfully.")


if __name__ == "__main__":
    main()
