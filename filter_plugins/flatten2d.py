def flatten2d(list1, list2):
    rep = [[x] * len(y) for x, y in zip(list1, list2)]
    # Flatten list using sum(..., []) https://stackoverflow.com/a/952946
    return zip(sum(rep, []), sum(list2, []))


class FilterModule(object):
    def filters(self):
        return {
            "flatten2d": flatten2d
        }
