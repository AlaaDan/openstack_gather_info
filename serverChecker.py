import openstack
import json
import argparse

conn = openstack.connect(cloud="default")  # This should replaced to matach what you hav ein your could.yml


# Collect all images in the region
def collect_images(imageName):
    images = conn.image.images(visibility="all")
    sorted_images = []
    for image in images:
        if imageName.lower() in image.name.lower():
            if image.visibility != "Private":
                sorted_images.append(image)
    return sorted_images


# Collect all the servers with the specific image and also check volumes
def collect_servers(imageName, images):
    matching_servers = []
    aggregator_servers = conn.compute.servers(all_projects=True)
    list_of_servers = []
    for server in aggregator_servers:
        if server.image.id != None:
            list_of_servers.append(server)
    aggregator_volumes = conn.block_storage.volumes(all_projects=True)
    for volume in aggregator_volumes:
        if volume.volume_image_metadata != None and imageName.lower() in volume.volume_image_metadata['image_name'].lower():
            server_id = "Not attached"
            if volume.attachments:
                server_id = volume.attachments[0]['server_id']
            matching_servers.append({
                "Type": "Volume",
                "UUID": volume.id,
                "Project_ID": volume.project_id,
                "Image ID": volume.volume_image_metadata['image_id'],
                "Image Name": volume.volume_image_metadata['image_name'],
                "Server UUID": server_id
            })

    for image in images:
        for server in list_of_servers:
            if server.image.id == image.id:
                matching_servers.append({
                    "Type": "Server",
                    "UUID": server.id,
                    "Project_ID": server.project_id,
                    "Image ID": server.image.id,
                    "Image Name": image.name
                })

    return matching_servers


# Write the data to a file.
def write_data(imageName):
    print("Collecting all the images")
    images = collect_images(imageName)
    if len(images) != 0:
        print("Sorting out all the servers")
        servers = collect_servers(imageName, images)
        print("Writing to file")
        region = input("Enter region name: \n")
        with open(f'{region}_servers.json', 'w') as f:
            json.dump(servers, f, indent=4)
    else:
        print(f"No image found with the name {imageName}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Script to find all servers (including boot from volume) of a specific image")
    parser.add_argument('image_name', type=str, help="Name of the image you looking for, the script will try and look for images that includes the name.")

    args = parser.parse_args()
    write_data(args.image_name)
