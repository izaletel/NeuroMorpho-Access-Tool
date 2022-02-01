import requests
import pandas as pd
import pickle
import os
import threading
import datetime

from tkinter import *

from config import text_width


def acquisition_thread(progress_var, brain_region='All', species='All', cell_type='All'):
    th = threading.Thread(target=acquisition, args=(progress_var, brain_region, species, cell_type))
    th.start()


def acquisition(progress_var, brain_region='All', species='All', cell_type='All'):
    starttime = datetime.datetime.now()
    s = requests.Session()
    params_widg = {}
    if brain_region != 'All':
        params_widg['brain_region'] = 'brain_region:' + brain_region
    if species != 'All':
        params_widg['species'] = 'species:' + species
    if cell_type != 'All':
        params_widg['cell_type'] = 'cell_type:' + cell_type

    progress_var.set(0.0)
    print(brain_region)
    print(species)
    print(cell_type)

    params = {}
    params['page'] = 0
    params['size'] = 500
    fq = []
    first = 0
    for key, value in params_widg.items():
        if first == 0:
            first = 1
            params['q'] = value
        else:
            fq.append(value)
            params['fq'] = fq

    # based on the previous criteria the url link is created and json is called
    # in the next cell the returned info using json is transferred into a dictionary

    if brain_region == 'All' and species == 'All' and cell_type == 'All':
        url = 'http://neuromorpho.org/api/neuron'
    else:
        url = 'http://neuromorpho.org/api/neuron/select'

    first_page_response = s.get(url, params=params)

    if first_page_response.status_code == 404 or first_page_response.status_code == 500:
        print("Not found!")
        exit(1)

    totalPages = first_page_response.json()['page']['totalPages']

    df_dict = {
        'NeuronID': list(),
        'Neuron Name': list(),
        'Archive': list(),
        'Note': list(),
        'Age Scale': list(),
        'Gender': list(),
        'Age Classification': list(),
        'Brain Region': list(),
        'Cell Type': list(),
        'Species': list(),
        'Strain': list(),
        'Scientific Name': list(),
        'Stain': list(),
        'Experiment Condition': list(),
        'Protocol': list(),
        'Slicing Direction': list(),
        'Reconstruction Software': list(),
        'Objective Type': list(),
        'Original Format': list(),
        'Domain': list(),
        'Attributes': list(),
        'Magnification': list(),
        'Upload Date': list(),
        'Deposition Date': list(),
        'Shrinkage Reported': list(),
        'Shrinkage Corrected': list(),
        'Reported Value': list(),
        'Reported XY': list(),
        'Reported Z': list(),
        'Corrected Value': list(),
        'Corrected XY': list(),
        'Corrected Z': list(),
        'Slicing Thickness': list(),
        'Min Age': list(),
        'Max Age': list(),
        'Min Weight': list(),
        'Max Weight': list(),
        'Png URL': list(),
        'Reference PMID': list(),
        'Reference DOI': list(),
        'Physical Integrity': list()}

    print("Getting Neurons - total pages:" + str(totalPages))
    progress_step = 20.0/totalPages
    for pageNum in range(totalPages):
        params['page'] = pageNum
        response = s.get(url, params=params)
        print('Querying page {} -> status code: {}'.format(
            pageNum, response.status_code))
        if response.status_code == 200:  # only parse successful requests
            data = response.json()
            for row in data['_embedded']['neuronResources']:
                df_dict['NeuronID'].append(str(row['neuron_id']))
                df_dict['Neuron Name'].append(str(row['neuron_name']))
                df_dict['Archive'].append(str(row['archive']))
                df_dict['Note'].append(str(row['note']))
                df_dict['Age Scale'].append(str(row['age_scale']))
                df_dict['Gender'].append(str(row['gender']))
                df_dict['Age Classification'].append(str(row['age_classification']))
                df_dict['Brain Region'].append(str(row['brain_region']))
                df_dict['Cell Type'].append(str(row['cell_type']))
                df_dict['Species'].append(str(row['species']))
                df_dict['Strain'].append(str(row['strain']))
                df_dict['Scientific Name'].append(str(row['scientific_name']))
                df_dict['Stain'].append(str(row['stain']))
                df_dict['Experiment Condition'].append(str(row['experiment_condition']))
                df_dict['Protocol'].append(str(row['protocol']))
                df_dict['Slicing Direction'].append(str(row['slicing_direction']))
                df_dict['Reconstruction Software'].append(str(row['reconstruction_software']))
                df_dict['Objective Type'].append(str(row['objective_type']))
                df_dict['Original Format'].append(str(row['original_format']))
                df_dict['Domain'].append(str(row['domain']))
                df_dict['Attributes'].append(str(row['attributes']))
                df_dict['Magnification'].append(str(row['magnification']))
                df_dict['Upload Date'].append(str(row['upload_date']))
                df_dict['Deposition Date'].append(str(row['deposition_date']))
                df_dict['Shrinkage Reported'].append(str(row['shrinkage_reported']))
                df_dict['Shrinkage Corrected'].append(str(row['shrinkage_corrected']))
                df_dict['Reported Value'].append(str(row['reported_value']))
                df_dict['Reported XY'].append(str(row['reported_xy']))
                df_dict['Reported Z'].append(str(row['reported_z']))
                df_dict['Corrected Value'].append(str(row['corrected_value']))
                df_dict['Corrected XY'].append(str(row['corrected_xy']))
                df_dict['Corrected Z'].append(str(row['corrected_z']))
                df_dict['Slicing Thickness'].append(str(row['slicing_thickness']))
                df_dict['Min Age'].append(str(row['min_age']))
                df_dict['Max Age'].append(str(row['max_age']))
                df_dict['Min Weight'].append(str(row['min_weight']))
                df_dict['Max Weight'].append(str(row['max_weight']))
                df_dict['Png URL'].append(str(row['png_url']))
                df_dict['Reference PMID'].append(str(row['reference_pmid']))
                df_dict['Reference DOI'].append(str(row['reference_doi']))
                df_dict['Physical Integrity'].append(str(row['physical_Integrity']))
        progress_var.set(pageNum * progress_step)
    progress_var.set(20)

    print("Creating neuron Data Frame")
    neurons_df = pd.DataFrame(df_dict)
    progress_var.set(25)
    print("Pickling neurons")
    os.makedirs("./output", exist_ok=True)
    neurons_df.to_pickle("./output/neurons.pkl")
    progress_var.set(30)

    # the ID number of previously obtained neurons is used to obtain their morphometric details

    n = neurons_df['NeuronID'].to_numpy()

    print("Getting morphometry")
    morphometry = []
    progress_step = 40.0 / n.size
    progress_value = 0.0
    for i in n:
        url = "http://neuromorpho.org/api/morphometry/id/" + str(i)
        response = s.get(url)
        json_data = response.json()
        morphometry.append(json_data)
        progress_value += progress_step
        progress_var.set(30 + progress_value)
        print('Querying cells {} -> status code: {}'.format(str(i), response.status_code))
    progress_var.set(70)
    print("Creating morphometry Data Frame")
    df_dict = {}
    df_dict['Neuron ID'] = []
    df_dict['Surface'] = []
    df_dict['Volume'] = []
    df_dict['Soma surface'] = []
    df_dict['Number of stems'] = []
    df_dict['Number of bifurcations'] = []
    df_dict['Number of branches'] = []
    df_dict['Width'] = []
    df_dict['Height'] = []
    df_dict['Depth'] = []
    df_dict['Diameter'] = []
    df_dict['Euclidian distance'] = []
    df_dict['Path distance'] = []
    df_dict['Branching order'] = []
    df_dict['Contraction'] = []
    df_dict['Fragmentation'] = []
    df_dict['Partition asymmetry'] = []
    df_dict['Pk classic'] = []
    df_dict['Bifurcation angle local'] = []
    df_dict['Fractal dimension'] = []
    df_dict['Bifurcation angle remote'] = []
    df_dict['Length'] = []
    for row in morphometry:
        df_dict['Neuron ID'].append(str(row['neuron_id']))
        df_dict['Surface'].append(str(row['surface']))
        df_dict['Volume'].append(str(row['volume']))
        df_dict['Soma surface'].append(str(row['soma_Surface']))
        df_dict['Number of stems'].append(str(row['n_stems']))
        df_dict['Number of bifurcations'].append(str(row['n_bifs']))
        df_dict['Number of branches'].append(str(row['n_branch']))
        df_dict['Width'].append(str(row['width']))
        df_dict['Height'].append(str(row['height']))
        df_dict['Depth'].append(str(row['depth']))
        df_dict['Diameter'].append(str(row['diameter']))
        df_dict['Euclidian distance'].append(str(row['eucDistance']))
        df_dict['Path distance'].append(str(row['pathDistance']))
        df_dict['Branching order'].append(str(row['branch_Order']))
        df_dict['Contraction'].append(str(row['contraction']))
        df_dict['Fragmentation'].append(str(row['fragmentation']))
        df_dict['Partition asymmetry'].append(str(row['partition_asymmetry']))
        df_dict['Pk classic'].append(str(row['pk_classic']))
        df_dict['Bifurcation angle local'].append(str(row['bif_ampl_local']))
        df_dict['Fractal dimension'].append(str(row['fractal_Dim']))
        df_dict['Bifurcation angle remote'].append(str(row['bif_ampl_remote']))
        df_dict['Length'].append(str(row['length']))
    morphometry_df = pd.DataFrame(df_dict)

    progress_var.set(75)

    print("Pickling morphometry")
    morphometry_df.to_pickle("./output/morphometry.pkl")

    # the following is a list of steps used to currate the morphometric data
    # and merge the two obtained dataframes (general neuron parameters and morphometric data)
    # this results in the creation of final .pkl and .csv files at the end of the notebook

    neurons = open("./output/morphometry.pkl", "rb")
    neurons_df = pickle.load(neurons)
    neurons.close()
    progress_var.set(80)
    print(neurons_df)

    neurons_df = neurons_df.replace({'Soma surface': {'None': ''}}, regex=True)

    neurons_df["Surface"] = pd.to_numeric(neurons_df["Surface"], downcast="float")
    neurons_df["Volume"] = pd.to_numeric(neurons_df["Volume"], downcast="float")
    neurons_df["Soma surface"] = pd.to_numeric(neurons_df["Soma surface"], downcast="float")
    neurons_df["Number of stems"] = pd.to_numeric(neurons_df["Number of stems"], downcast="float")
    neurons_df["Number of bifurcations"] = pd.to_numeric(neurons_df["Number of bifurcations"], downcast="float")
    neurons_df["Number of branches"] = pd.to_numeric(neurons_df["Number of branches"], downcast="float")
    neurons_df["Width"] = pd.to_numeric(neurons_df["Width"], downcast="float")
    neurons_df["Height"] = pd.to_numeric(neurons_df["Height"], downcast="float")
    neurons_df["Depth"] = pd.to_numeric(neurons_df["Depth"], downcast="float")
    neurons_df["Diameter"] = pd.to_numeric(neurons_df["Diameter"], downcast="float")
    neurons_df["Euclidian distance"] = pd.to_numeric(neurons_df["Euclidian distance"], downcast="float")
    neurons_df["Path distance"] = pd.to_numeric(neurons_df["Path distance"], downcast="float")
    neurons_df["Branching order"] = pd.to_numeric(neurons_df["Branching order"], downcast="float")
    neurons_df["Contraction"] = pd.to_numeric(neurons_df["Contraction"], downcast="float")
    neurons_df["Fragmentation"] = pd.to_numeric(neurons_df["Fragmentation"], downcast="float")
    neurons_df["Partition asymmetry"] = pd.to_numeric(neurons_df["Partition asymmetry"], downcast="float")
    neurons_df["Pk classic"] = pd.to_numeric(neurons_df["Pk classic"], downcast="float")
    neurons_df["Bifurcation angle local"] = pd.to_numeric(neurons_df["Bifurcation angle local"], downcast="float")
    neurons_df["Fractal dimension"] = pd.to_numeric(neurons_df["Fractal dimension"], downcast="float")
    neurons_df["Number of branches"] = pd.to_numeric(neurons_df["Number of branches"], downcast="float")
    neurons_df["Bifurcation angle remote"] = pd.to_numeric(neurons_df["Bifurcation angle remote"], downcast="float")
    neurons_df["Length"] = pd.to_numeric(neurons_df["Length"], downcast="float")

    neurons_df.to_pickle("./output/neurons_float.pkl")

    neurons = open("./output/neurons.pkl", "rb")
    neurons_id_df = pickle.load(neurons)
    neurons.close()
    progress_var.set(85)
    print(neurons_id_df)

    neuron_morphometry = open("./output/neurons_float.pkl", "rb")
    neuron_morphometry_df = pickle.load(neuron_morphometry)
    neuron_morphometry.close()
    progress_var.set(90)
    print(neuron_morphometry_df)

    final_df = neurons_id_df.join(neuron_morphometry_df)

    # excess NeuronID column left when joinging two dataframes
    final_df = final_df.drop(columns=['NeuronID'])

    file_name = "./output/NM_" + \
                str(brain_region).replace(" ", "_") + "_" + \
                str(species).replace(" ", "_") + "_" + \
                str(cell_type).replace(" ", "_") + ".csv"

    final_df.to_pickle(file_name)

    final_df.to_csv(file_name, index=False)

    progress_var.set(100)
    print(final_df)

    finishtime = datetime.datetime.now() - starttime

    print(finishtime)
    print("DONE!")
    print("\n" + "#" * text_width + "\n")
    progress_var.set(0)

