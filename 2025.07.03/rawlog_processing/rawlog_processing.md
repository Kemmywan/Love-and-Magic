# Network Log Processing 

----

## Raw Network Log Structure
- Provide an example of a raw network log entry.
- Describe the fields and their meanings.

```json
{
    "action": "<ACTION_TYPE>",
    "actorID": "<ACTOR_ID>",
    "hostname": "<HOSTNAME>",
    "id": "<EVENT_ID>",
    "object": "<OBJECT_TYPE>",
    "objectID": "<OBJECT_ID>",
    "pid": <PROCESS_ID>,
    "ppid": <PARENT_PROCESS_ID>,
    "principal": "<PRINCIPAL>",
    "properties": {
        "acuity_level": "<ACUITY_LEVEL>",
        "dest_ip": "<DESTINATION_IP>",
        "dest_port": "<DESTINATION_PORT>",
        "direction": "<DIRECTION>",
        "image_path": "<IMAGE_PATH>",
        "l4protocol": "<L4_PROTOCOL>",
        "src_ip": "<SOURCE_IP>",
        "src_port": "<SOURCE_PORT>"
    },
    "tid": <THREAD_ID>,
    "timestamp": "<TIMESTAMP>"
}
```

## Processing Workflow

### Step 1: Ingestion

- Download the raw data

### Step 2: preprocessing

auth_optc.txt的格式:

```
['timestamps', 'source', 'target', 'label',  'pid', 'ppid', 'dest_port', 'l4protocol', 'img_path']

Example: [0,736,378,0,913,891,3,1,76]
```

```
/Argus/README.md

    For [OpTC Dataset](https://github.com/FiveDirections/OpTC-data), we use the "START" events related to the 
    "FLOW" objects (i.e., network flows), and the statistics after filtering following the 
    [paper](https://ieeexplore.ieee.org/abstract/document/9789921). 
```

The paper refered in it is about ***PIKACHU***, and the article can be found on the folder.

In ```/Pikachu/dataset/optc``` there are three documents, which stored in the ***Pikachu_optc*** folder.

不过看起来auth_optc.txt的生成逻辑不难，应该就是直接从rawdata里面extracted出来对应的项，然后顺序标号来做区别，填进了auth_optc.txt里面。

除了labels，这个还需要结合groundtruth进行01标记，而在Pikachu里作者似乎是直接在optc_labels.py里面人工标记然后去匹配标签内容来labels的，具体代码暂时没有找到。

### Step 3: Spliting

应该可以直接使用split_optc.py

### Step 4: loading

应该可以直接使用load_optc.py


