from app import App


def main():
    app = App(lang="ru", length=5, start_word="океан")
    app.run()


if __name__ == "__main__":
    main()
