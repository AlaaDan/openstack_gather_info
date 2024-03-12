Gathering facts script

This script is designed for retrieving details for different type of services.

1- Gather all active L3 agents within a specific region. The process involves collecting information on all routers in the region, looping through each router, and identifying only the active L3 agents. The resulting data is stored in a list of dictionaries, which is then exported/json dumped to a file named `Region_L3_active_agents`.

To use the script, start by logging into the control plane  or if you have a deploy host that has the admin priviliges to perform openstask tasks, become root and attach to the utility container.

Then execute the script

```
python3 gather_info.py
```

Note that the process may take some time as it involves checking numerous routers in the region. Once completed, a file named `Region_L3_active_agents.json` will be created in the same directory. The file contains information on all active L3 agents, each represented as a dictionary with the following details:

```
{"Router_UUID": <ID>,
"Domain_ID": <ID>
"Project_ID": <ID>,
"HA_status": "status",
"Host": <NET NODE>}
```

In cases a project has multiple routers, the script organizes and lists all routers for the same project consecutively within the file.

2- Gather all servers information depending on the image the user specified in the run, it checks if the server has the image as a boot from volume or it's an ephemeral disk, then it formolate the output as json file with the 2 types of dictionaries


To execute the script

```
python3 gather_info.py
```

If the image is boot from volume the object will look like:

```
{
        "Type": "Volume",
        "UUID": "UUID",
        "Project_ID": "UUID",
        "Image ID": "UUID",
        "Image Name": "IMAGE NAME",
        "Server UUID": "SERVER UUID"
}
```

if it's ephemeral disk

```
{
        "Type": "Server",
        "UUID": "UUID",
        "Project_ID": "UUID",
        "Image ID": "UUID",
        "Image Name": "IMAGE NAME",
}
```

Generate Wiki page(WIP)

Once the script is done you would need to copy over `Region_L3_active_agents.json` to your locall laptop and then you need to run another script called `generate_wiki_page.py` to generate a wiki page.

This script requires some arguments and without them it wont work

First install a required dependency

```
pip install atlassian-python-api
```

Required arguments as follow

**Personal Access Tokens**

This can be generate it from wiki if you clock on your account Settings, then clicking on `Personal Access Tokens`

**Page ID**

You will need to navigate to the folder that you want the page to be created in and then click on the 3 dots `...`then click on Page information, in the link you will see that pageid appears and it has a number copy that and past it into the script run

**Page title**

Give you page a title, it should be unique and is not used inside the folder you are trying to create it in.

**Page space**

Lastly Page space should be passed as well to make sure the page is created in the correct place.
For example if u want to create the page in the Service operation space then, ywhat u need to do is click on the service operation icon on wiki `https://wiki.citynetwork.se/display/SOPS` <= `SOPS` is the page space for it.

To run the script

````
python3 generate_wiki_page.py <Personal Access Tokens> <Page ID> <Page title> <Page space>
````
