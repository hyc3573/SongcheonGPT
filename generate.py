import sys
from typing import Dict, List
import random
import re

RECURSION_LEVEL = 3

def multiple_find_replace(s: str, substitution: Dict[str, str]) -> str:
    for i in range(RECURSION_LEVEL):
        for key, value in substitution.items():
            s = s.replace(key, value)

    return s

def expand_macro(targets: List[str]):
    regex = re.compile(
        "(<[^<>]+>|{[^{}}]+}|\\[[^\\[\\]]+\\])"
    )

    string = '\n'.join(targets)
    for i in range(RECURSION_LEVEL):
        macro_set = set()
        subs = {}

        for match in re.finditer(regex, string):
            macro_set.add(match.group(0))

        for macro in macro_set:
            result = ""
            body = macro[1:-1]
            match macro[0]:
                case "<":
                    result = random.choice(
                        body.split("|")
                    )
                case "{":
                    result = random.choice(
                        (body, "")
                    )
                case "[":
                    result = str(random.randrange(
                        *map(int, 
                             body.split("-")
                            )
                    ))

            subs[macro] = result

            string = multiple_find_replace(string, subs)

    return string

if __name__ == "__main__":
    ctx = ""
    question = []
    answer = ""
    subs = {}
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        line = multiple_find_replace(line, subs)
        if len(line):
            prefix, rest = line[0], line[1:]
        else:
            prefix = line
            rest = ""

        match prefix:
            case ";":
                key, value = rest.split("=")
                subs[key] = value
            case "~":
                ctx = rest
            case "!":
                question.append(rest)
            case "@":
                for i in range(3):
                    for q in question:
                        print(expand_macro([ctx, q, rest]))

                print("\n")
                q = []
