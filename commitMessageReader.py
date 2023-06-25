import os

import pandas as pd
testString = "what is popping, this is just a TEST - just completed a cleanup of this tests"

df = pd.read_csv("tables/commits_2019_APACHE.csv")

def get_label(message):
    nothing_words = ["todo", "rename", "instructions", "refactor", "document", "minor", "cleanup", "clean-up", "typo", "style"]
    add_words = ["add", "implement", "provide", "introduce"]
    warning_words = ["memory leak", "leak", "does not", "doesn't", "doesnt", "causes", "fail", "cannot", "can't", "cant", "error", "retry"]
    optimize_words = ["improve", "performance", "reduce", "ensure", "perf", "filter", "enable", "must", "instead", "skip", "optim"]

    ##### CHECK REVERT FIRST #####
    if "revert" in message:
        return "revert"

    ##### Check if nothing #####
    elif any([word in message for word in nothing_words]) and "only" not in message \
            and "provide" not in message and not any([word in message for word in optimize_words]):
        return "nothing"

    ##### IMPORT #####
    elif "import" in message:
        return "import"

    ##### REMOVE #####
    elif "remove" in message:
        return "remove"

    ##### FIX #####
    elif "fix" in message or ("prevent" in message and not "not prevent" in message):
        return "fix"

    ##### warnings #####
    elif any([word in message for word in warning_words]) and "instead" not in message:
        return "attention recommended"

    ##### add #####
    elif (any([word in message for word in add_words]) or message.split()[0] == "create" or message.split()[1] == "create"\
            or message.split()[0] == "creates" or message.split()[1] == "creates") and "before add" not in message:
        return "add"

    else:
        return "optimization"


if __name__ == "__main__":
    for index, row in df.iterrows():
        message = row['Message']
        message = message.lower()
        label = get_label(message)

        print(index, message + " === " + label)  # dead.

        if index == 50:
            break
