import sys

import Bagels

if __name__ == "__main__":
    args = sys.argv
    if len(args) > 1:
        project = args[1].lower()
    else:
        project = "bagels"

    match project:
        case "bagels":
            window = Bagels.Window(width=640, height=480, caption="Bagels", fps=60)

    if window:
        window.Run()
