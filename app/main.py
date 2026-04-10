from clients.core import ClientHTTP


def main():
    client = ClientHTTP()
    client.login(1234567890, "1234567890")


if __name__ == "__main__":
    main()
