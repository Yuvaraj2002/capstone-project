from prometheus_api_client import PrometheusConnect
from kubernetes import client, config
import subprocess

# Fetch the target CPU value for the default namespace

# Load the Kubernetes configuration
config.load_kube_config()

v1 = client.AutoscalingV2Api()

# Replace with your HPA name and namespace
hpa_name = "my-app-hpa"
namespace = "default"

try:
    # Fetch the HPA
    hpa = v1.read_namespaced_horizontal_pod_autoscaler(hpa_name, namespace)
    metrics = hpa.spec.metrics
    
    average_utilization = None  # Initialize the variable

    for metric in metrics:
        if metric.resource:
            target_cpu_value = metric.resource.target.average_utilization
            #print(target_cpu_value)
            break  # Stop after the first metric with average utilization is found

    
    #print("Metrics:", metrics)
except Exception as e:
    print("Error:", e)



# Load the Kubernetes configuration
config.load_kube_config()

# Create a Kubernetes API client
api = client.CoreV1Api()

total_cpu_requests = 0

#List all pods in the namespace
pods = api.list_namespaced_pod(namespace)

# Iterate through the pods and sum their CPU requests
for pod in pods.items:
    for container in pod.spec.containers:
        if container.resources and container.resources.requests and container.resources.requests.get("cpu"):
            cpu_request = container.resources.requests["cpu"]
            total_cpu_requests += int(cpu_request[:-1])  # Remove 'm' from millicores and convert to int







# Fetch the current CPU usage
# Define the command to fetch CPU usage for all pods in the default namespace for application
command = "kubectl top pods -l app=my-nginx --containers"

# Run the command and capture the output
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()

# Check for any errors
if process.returncode != 0:
    print("Error:", stderr.decode('utf-8'))
else:
    # Process the output to access CPU values
    output_lines = stdout.decode('utf-8').split('\n')
    # The output contains columns for NAME, CPU(cores), and MEMORY(bytes)
    # Extract the CPU values from the output
    for line in output_lines[1:]:  # Skip the header line
        if line:
            #print(line)
            pod, pod_name, cpu_usage_m, memory_usage_b= line.split()
            #print(f"Pod: {pod_name}, CPU Usage: {cpu_usage}")
            cpu_usage_m = int(cpu_usage_m.rstrip("m"))

            current_usage_value = (cpu_usage_m / total_cpu_requests)*100
            #print(cpu_usage_m)





# Rest of your custom scheduler logic
# Load the Kubernetes configuration from your kubeconfig file
config.load_kube_config()

# Create an instance of the Kubernetes API client
api = client.CoreV1Api()

# Query all the pods in the "default" namespace (change the namespace as needed)
namespace = "default"
deployment_name = "my-nginx"
label_selector = f"app={deployment_name}"
pods = api.list_namespaced_pod(namespace, label_selector=label_selector)


# Get the total number of pods in the list
total_pods = len(pods.items)
print("Total number of pods in the cluster:", total_pods)

size_of_cluster = total_pods

if size_of_cluster > 0 and current_usage_value > (size_of_cluster * target_cpu_value):
    total_pods_to_schedule = current_usage_value / target_cpu_value
    print("Total Pods to be scheduled:", total_pods_to_schedule)

    for i in range(total_pods_to_schedule):
        pod_spec = client.V1Pod(
            metadata=client.V1ObjectMeta(name=f"nginx- custom-pod-{i}"),
            spec=client.V1PodSpec(
                containers=[
                    client.V1Container(
                        name="my-nginx",
                        image="veenagarag/my-nginx-sample",
                        resources=client.V1ResourceRequirements(
                            requests={"cpu": "0.7"}
                        ),
                    )
                ]
            )
        )

    # Create the Pod in the specified namespace
    api.create_namespaced_pod(namespace, pod_spec)



else:
    print("No scheduling needed")

