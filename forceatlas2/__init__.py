import os, pkg_resources
import pandas as pd
from subprocess import check_call


def forceatlas2(file_name, graph, n_jobs, target_change_per_node, target_steps, is3d, memory, random_state, init):

    input_graph_file = "{file_name}.net".format(file_name=file_name)
    graph.write(input_graph_file)
    print(input_graph_file + " is written.")

    output_coord_file = "{file_name}.coords.txt".format(file_name=file_name)

    classpath = (
        pkg_resources.resource_filename("forceatlas2", "ext/forceatlas2.jar")
        + ":"
        + pkg_resources.resource_filename("forceatlas2", "ext/gephi-toolkit-0.9.2-all.jar")
    )

    command = [
        "java",
        "-Djava.awt.headless=true",
        "-Xmx{memory}g".format(memory=memory),
        "-cp",
        classpath,
        "kco.forceatlas2.Main",
        "--input",
        input_graph_file,
        "--output",
        file_name + ".coords",
        "--nthreads",
        str(n_jobs),
        "--seed",
        str(random_state),
        "--targetChangePerNode",
        str(target_change_per_node),
        "--targetSteps",
        str(target_steps),
    ]
    if not is3d:
        command.append("--2d")

    if init is not None:
        if not is3d:
            df = pd.DataFrame(
                data=init, columns=["x", "y"], index=range(1, init.shape[0] + 1)
            )
        else:
            df = pd.DataFrame(
                data=init, columns=["x", "y", "z"], index=range(1, init.shape[0] + 1)
            )
        df.index.name = "id"
        init_coord_file = "{file_name}.init.coords.txt".format(file_name=file_name)
        df.to_csv(init_coord_file, sep="\t", float_format="%.2f")
        command.extend(["--coords", init_coord_file])

    print(command)
    check_call(command)

    fle_coords = pd.read_csv(output_coord_file, header=0, index_col=0, sep="\t").values

    check_call(["rm", "-f", input_graph_file])
    check_call(["rm", "-f", output_coord_file])
    if init is not None:
        os.remove("{file_name}.init.coords.txt".format(file_name=file_name))

    print("Force-directed layout is generated.")

    return fle_coords