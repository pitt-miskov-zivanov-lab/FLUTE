Offline Usage
=============


FLUTE requires Python installed on local machine (macOS, Linux and Windows are all supported). If users want to explore the interactive notebook we provided locally, Jupyter notebook installation is also required.

1. Clone the `FLUTE repository <https://github.com/pitt-miskov-zivanov-lab/FLUTE>`_, to your computer.

.. code-block:: bash

   git clone https://github.com/pitt-miskov-zivanov-lab/FLUTE.git

2. Navigate into the directory, install FLUTE and its python dependencies.

.. code-block:: bash

   cd FLUTE
   pip install -e .

3. Use either *in terminal* or *via notebook*.

*In terminal:* change working directory to src/ folder by ``cd src/``, first unzip a large file ``unzip ../supplementary/oa_file_list.txt.zip -d "../examples/input/"``, and then see what parameters are needed in run_FLUTE.py via helper

.. code-block:: bash

    python run_FLUTE.py -h
    >> usage: run_FLUTE.py [-h] [-g] [-p] [-q [PROT_QUERY]] [-r] username password host db_name input_file output_path

That's being said, **six ordered positional arguments are required**: ``username password host db_name input_file output_path``,
some optional flag/arguments can be appended to support additional features:

.. csv-table::
    :header: Python Scripts and Arguments, Examples, Descriptions
    :widths: 30, 50, 20

    No optional ones, "``python run_FLUTE.py root 12345678 localhost flute ../examples/input/example.xlsx ../examples/output/example``", Filter and score input interactions
    with ``-g`` or ``--drop_duplicates``, "``python run_FLUTE.py root 12345678 localhost flute ../examples/input/example.xlsx ../examples/output/example -g``", Also output duplicate interactions in input file
    with ``-p`` or ``--keep_recent_pps``, "``python run_FLUTE.py root 12345678 localhost flute ../examples/input/example.xlsx ../examples/output/example -p``", Also output interactions published in papers of recent years
    with ``-q [PROT_QUERY]`` or ``--prot_query [PROT_QUERY]``, "``python run_FLUTE.py root 12345678 localhost flute ../examples/input/example.xlsx ../examples/output/example -q P00533,P03386``", Also find interactions related to these given protein IDs
    with ``-r`` or ``--add_related_ints``, "``python run_FLUTE.py root 12345678 localhost flute ../examples/input/example.xlsx ../examples/output/example -r``", Also find additional interactions related that are in the same paper set
    combine ``-g -p`` or any, "``python run_FLUTE.py root 12345678 localhost flute ../examples/input/example.xlsx ../examples/output/example -g -p``", Do both

*Via notebook:* Run the provided notebook after ``cd examples/`` from FLUTE root directory. Detailed instructions can be found in markdown cells inside the notebook or at this page

.. code-block:: bash

  jupyter notebook examples/use_FLUTE.ipynb

4.	Prepare input files and interpret output files

Input and parameters includes:

    * a ``.xlsx`` file containing the machine reading interactions, best in `BioRECIPES <https://melody-biorecipe.readthedocs.io/en/latest/model_representation.html>`_ interaction format, `see example <https://github.com/pitt-miskov-zivanov-lab/FLUTE/blob/master/examples/input/example.xlsx>`_. At the minimum requirements, it shall have the following headers:
    ============== ============ ============== ============== ============ ============== =========
    Regulated Name Regulated ID Regulated Type Regulator Name Regulator ID Regulator Type Paper IDs
    ============== ============ ============== ============== ============ ============== =========

    * a score tuple ``(es, ts, ds)``, three positive numbers, denoting thresholds of escore, tscore, dscore. Default value is set to be (0,0,0), update it in ``main()`` (run in terminal) or in Cell 16 (run with notebook).
    * If using the feature of returning recent papers, integer ``x`` is needed to specify how many years to return interactions published in recent papers. Default is 5, update it in ``main()`` (run in terminal) or in Cell 25 (run with notebook).
    * If using the feature of querying protein IDs and returning related interactions, string of protein IDs is needed, e.g., ``P00533,P03386``, supported after ``-q`` (run in terminal) or in Cell 20 (run with notebook).

Output (including optional) includes:

    * list of reading interactions that pass filtration, `see example <https://github.com/pitt-miskov-zivanov-lab/FLUTE/blob/master/examples/output/example_filtered.xlsx>`_
    * the filtration scores for those filtered interactions, `see example <https://github.com/pitt-miskov-zivanov-lab/FLUTE/blob/master/examples/output/example_grd_ints_scores.xlsx>`_
    * OPTIONAL: duplicated reading interactions and their occurrences, `see example <https://github.com/pitt-miskov-zivanov-lab/FLUTE/blob/master/examples/output/example_optional_duplicated_ints.xlsx>`_
    * OPTIONAL: interactions published in recent x years, `see example <https://github.com/pitt-miskov-zivanov-lab/FLUTE/blob/master/examples/output/example_optional_recent_ints.xlsx>`_
    * OPTIONAL: interactions related to query protein IDs, `see example <https://github.com/pitt-miskov-zivanov-lab/FLUTE/blob/master/examples/output/example_optional_ints_related_to_P00533,P03386.xlsx>`_
    * OPTIONAL: interactions that are in the same papers as the input file, `see example <https://github.com/pitt-miskov-zivanov-lab/FLUTE/blob/master/examples/output/example_optional_ints_in_same_pps.xlsx>`_
