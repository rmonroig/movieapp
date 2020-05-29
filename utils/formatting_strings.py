
def remove_extraspaces(lst):
    result = []
    for item in lst:
        if type(item) == list:
            result.append(remove_extraspaces(item))
        else:
            item=" ".join(item.split())
            result.append(item)
    return result



def remv_str(lst, val, rep):
    result = []
    for item in lst:
        if type(item) == list:
            result.append(remv_str(item, val, rep))
        elif val in item:
            item=item.replace(val, rep)
            result.append(item)
        else:
            result.append(item)
    return result
