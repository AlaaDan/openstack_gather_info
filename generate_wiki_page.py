import json
import argparse
from atlassian import Confluence

with open('Region_L3_active_agents.json', 'r') as f:
    router_info = json.load(f)


def create_connection(auth_token):
    # Chnage the url to match your actul domain
    confluence = Confluence(
        url='https://wiki.<DOMIAN NAME>',
        token=auth_token
    )

    return confluence


def create_page(page_domain, page_title, page_body, confluence):
    confluence.create_page(
        space=page_domain,
        title=page_title,
        body=page_body
    )


def generate_wiki_page(router_info):
    html_page = "<html><body>"
    grouped_routers = {}

    for item in router_info:
        host_group = grouped_routers.setdefault(item['Host'], {})
        domain_group = host_group.setdefault(item['Domain_ID'], {})
        domain_group.setdefault(item['Project_ID'], []).append(item)

    # Generating HTML page.
    for host, domains in grouped_routers.items():
        # This will generate an h2 for the Host name
        html_page += f"<h2><b>{host}</b></h2>"
        #Table Creation
        html_page += "<table border='1'>"
        html_page += "<tr><th>GTH ID</th><th>Domain ID</th><th>Project IDs</th><th>Router UUIDs</th><th>HA states</th></tr>"
        for domain, projects in domains.items():
            for project, routers in projects.items():
                router_uuids = ""
                ha_states = ""
                for router in routers:
                    router_uuids += f"{router['Router_UUID']}<br/>"
                    ha_states += f"{router['HA_state']}<br/>"
                html_page += f"<tr><td>GTH_ID</td><td>{domain}</td><td>{project}</td><td>{router_uuids}</td><td>{ha_states}</td></tr>"
        html_page += "</table><br/>"

    html_page += "</body></html>"

    return html_page


def main(pat, page_id, page_title, page_space):
    try:
        conn = create_connection(pat)
    except Exception:
        print("Invalid token")
    try:
        conn.get_page_by_id(page_id)
        try:
            conn.create_page(page_space, page_title, body=generate_wiki_page(router_info), parent_id=page_id, type='page', representation='storage', editor='v2', full_width=False)
        except Exception as e:
            print(f"Failed to create page: {e}")
    except Exception:
        print("Page was not found")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some arguments')
    parser.add_argument('patkey', type=str, help='A pat key is needed')
    parser.add_argument('page_id', type=str, help='A page ID is neededs')
    parser.add_argument('page_title', type=str, help='A title for the wiki page is needed')
    parser.add_argument('page_space', type=str, help='A page space ID is needed ')

    args = parser.parse_args()
    main(args.patkey, args.page_id, args.page_title, args.page_space)