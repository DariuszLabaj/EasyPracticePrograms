import sys

import Bagels
import Blackjack

if __name__ == "__main__":
    args = sys.argv
    if len(args) > 1:
        project = args[1].lower()
    else:
        project = "bagels"

    match project:
        case "bagels":
            window = Bagels.Window(width=640, height=480, caption="Bagels", fps=60)
        case "blackjack":
            window = Blackjack.Window(width=1100, height=480, caption="Blackjack", fps=60)
    if window:
        window.Run()
