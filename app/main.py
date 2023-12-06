import logging

from app.interface import MainApplication
from app.logger import LoggingHandler


def main() -> None:
    logger = logging.getLogger()
    logger.addHandler(LoggingHandler())

    app = MainApplication()
    app.mainloop()


if __name__ == "__main__":

    main()
