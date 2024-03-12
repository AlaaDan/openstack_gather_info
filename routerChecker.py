import openstack
import json

conn = openstack.connect(cloud='default')
routerDict = []


def get_l3_agents(router):
    l3_agents = conn.network.routers_hosting_l3_agents(router)

    for agent in l3_agents:
        if agent.ha_state == "active":
            return agent
        elif not agent.ha_state:
            return agent


def get_routers():
    # You can test the script against one project by adding project_id='<YOUR PROJECT ID>'
    # as an argument to the conn.network.routers()
    # like so routers = conn.network.routers(project_id='<YOUR PROJECT ID>')
    routers = conn.network.routers()
    for router in routers:
        print(f"Gathering info on Router with the ID: {router.id}")
        l3_agents = get_l3_agents(router.id)
        project = get_domain_id(router.project_id)
        routerDict.append({
            "Domain_ID": project.domain_id,
            "Router_UUID": router.id,
            "Project_ID": router.project_id,
            "HA_state": l3_agents.ha_state if l3_agents.ha_state else "None",
            "Host": l3_agents.host
        })


def get_domain_id(project):
    return conn.identity.get_project(project)


def writeIntoFile():
    get_routers()
    sorted_router_dict = sorted(routerDict, key=lambda x: x['Domain_ID'])
    with open('Region_L3_active_agents.json', 'w') as f:
        json.dump(sorted_router_dict, f, indent=4)


if __name__ == '__main__':
    writeIntoFile()
