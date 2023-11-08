from kubernetes import client, config

namespace = "default"  # Replace with the name of your namespace

# Load the Kubernetes configuration
config.load_kube_config()

# Create a Kubernetes API client
api = client.CoreV1Api()

total_cpu_requests = 0

# List all pods in the namespace
pods = api.list_namespaced_pod(namespace)

# Iterate through the pods and sum their CPU requests
for pod in pods.items:
    for container in pod.spec.containers:
        if container.resources and container.resources.requests and container.resources.requests.get("cpu"):
            cpu_request = container.resources.requests["cpu"]
            total_cpu_requests += int(cpu_request[:-1])  # Remove 'm' from millicores and convert to int

print(f"Total CPU allocation in {namespace}: {total_cpu_requests}m")
