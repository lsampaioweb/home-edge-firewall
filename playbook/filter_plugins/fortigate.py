def hyphen_to_underscore(value, split_keys=None):
    """Convert all hyphenated keys in a dict to underscored keys.
    Optionally, keys listed in split_keys will have their string values
    split on spaces into a list (e.g. for allowaccess-style fields)."""
    if not isinstance(value, dict):
        return value
    keys_to_split = set(split_keys) if split_keys else set()
    result = {}
    for k, v in value.items():
        new_key = k.replace('-', '_')
        if new_key in keys_to_split and isinstance(v, str):
            result[new_key] = [x for x in v.split(' ') if x]
        else:
            result[new_key] = v
    return result


class FilterModule(object):
    def filters(self):
        return {'hyphen_to_underscore': hyphen_to_underscore}
