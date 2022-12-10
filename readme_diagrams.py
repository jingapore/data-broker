from diagrams import Diagram, Edge
from diagrams.generic.blank import Blank
from diagrams import Cluster
from diagrams.aws.compute import ECS
from diagrams.aws.database import RDS
from diagrams.aws.network import Route53

node_font_size = 16
default_node_type = {
    "style": "filled,rounded",
    "fillcolor": "lightgrey",
    "fontsize": f"{node_font_size}",
    "shape": "square",
}
with Diagram("data broker system design", show=False):
    policy_engine = Blank("policy engine", **default_node_type)
    policy_enforcer = Blank("policy enforcer", **default_node_type)

    policy_enforcer >> Edge(label="request for policy decision") >> policy_engine
    policy_engine >> Edge(label="respond with policy decision") >> policy_enforcer
    metadata_store_cluster = Cluster(
        "metadata graph", graph_attr={"fontsize": f"{int(node_font_size * 1.2)}"}
    )

    with metadata_store_cluster:
        data_resource_graph = Blank("data resource graph", **default_node_type)
        data_requester_graph = Blank("data requester graph", **default_node_type)
        (
            data_requester_graph
            >> Edge(label="permissioning policy\n(set by policy engine)")
            >> data_resource_graph
        )

    (
        policy_engine
        >> Edge(label="search for permissioning path")
        >> data_requester_graph
    )
