import os, pkg_resources
import pandas as pd
from subprocess import check_call

try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:  # < Python 3.8: Use backport module
    from importlib_metadata import version, PackageNotFoundError

try:
    __version__ = version('forceatlas2-python')
    del version
except PackageNotFoundError:
    pass


def forceatlas2(file_name, graph, n_jobs, target_change_per_node, target_steps, is3d, memory, random_state, init):
    input_graph_file = "{file_name}.net".format(file_name=file_name)
    graph.write(input_graph_file)

    output_coord_file = "{file_name}.coords.txt".format(file_name=file_name)

    classpath = (
            pkg_resources.resource_filename("forceatlas2", "ext/forceatlas2.jar")
            + os.pathsep
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

    check_call(command)

    fle_coords = pd.read_csv(output_coord_file, header=0, index_col=0, sep="\t").values
    os.remove(input_graph_file)
    os.remove(output_coord_file)

    if init is not None:
        os.remove("{file_name}.init.coords.txt".format(file_name=file_name))

    return fle_coords
