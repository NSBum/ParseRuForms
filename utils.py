from typing import Optional

def matching_item_from_list(item, llist):
    try:
        g = [x for x in llist if item.__contains__(x)][0]
    except IndexError:
        g = None
    return g


def strip_if_needed(strippable: str) -> Optional[str]:
    if strippable is None:
        return None
    if len(strippable) > 0:
        return strippable.strip()
    return strippable
