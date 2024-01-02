from pprint import pprint

from organizeit2 import load


def test_e2e():
    config = load("examples/example.zorp")
    pprint(config)
    # with open("tmp.ipynb", "w") as fp:
    #     write(gen, fp)
    # main(["tmp.ipynb", "--to=html", "--template=nbprint", "--execute"])
