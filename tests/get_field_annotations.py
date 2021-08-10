import json

def get_annotations(field):
    if not isinstance(field, list):
        return []

    annotations = []

    for idx, line in enumerate(field):
        if idx == 0 or idx == len(field) - 1:
            continue # skip the header or footer

        if len(line) == 0:
            continue
        
        if line.startswith('.annotation'):
            annotations.append(idx)

            continue

        if line == '.end annotation':
            annotations[-1] = (annotations[-1], idx + 1)

    def generator():
        for annotation in annotations:
            yield [line for line in field[annotation[0]:annotation[1]] if len(line)]

    return list(generator())

sample = [
    ".field private final list:Ljava/util/List;",
    ".annotation build Landroid/annotation/TargetApi;",
    "value = 0x16",
    "",
    ".end annotation",
    "",
    ".annotation build Landroid/annotation/TargetApi;",
    "value = 0x16",
    ".end annotation",
    "",
    ".annotation build Landroid/annotation/TargetApi;",
    "value = 0x16",
    ".end annotation",
    ".annotation build Landroid/annotation/TargetApi;",
    "value = 0x16",
    ".end annotation",
    "",
    ".annotation build Landroid/annotation/TargetApi;",
    "",
    "value = 0x16",
    ".end annotation",
    ".annotation build Landroid/annotation/TargetApi;",
    "value = 0x16",
    ".end annotation",
    "",
    ".annotation build Landroid/annotation/TargetApi;",
    "value = 0x16",
    ".end annotation",
    ".annotation build Landroid/annotation/TargetApi;",
    "value = 0x16",
    ".end annotation",
    ".annotation build Landroid/annotation/TargetApi;",
    "value = 0x16",
    "",
    ".end annotation",
    ".annotation build Landroid/annotation/TargetApi;",
    "value = 0x16",
    ".end annotation",
    ".annotation build Landroid/annotation/TargetApi;",
    "value = 0x16",
    ".end annotation",
    ".annotation build Landroid/annotation/TargetApi;",
    "value = 0x16",
    ".end annotation",
    ".annotation system Ldalvik/annotation/Signature;",
    "value = {",
    "\"Ljava/util/List\",",
    "\"<\",",
    "",
    "\"Ljava/lang/String;\",",
    "\">;\"",
    "}",
    ".end annotation",
    ".end field"
]

print(json.dumps(get_annotations(sample), indent = 4))