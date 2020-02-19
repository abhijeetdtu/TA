def SetupWebdriver():
    from webdrivermanager import GeckoDriverManager
    gdd = GeckoDriverManager()
    gdd.download_and_install()

def Setup():
    SetupWebdriver()


if __name__ == "__main__":
    Setup()
