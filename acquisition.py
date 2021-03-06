import requests
import pandas as pd
import pickle
import datetime
import guithread
import numpy as np
import concurrent.futures
import time

from os import makedirs
from config import text_width, max_thread_count


class Acquisition(guithread.GUIThread):
    def __init__(self, filename='default.csv', brain_region='All', species='All', cell_type='All'):

        self.filename = filename
        self.brain_region, self.species, self.cell_type = brain_region, species, cell_type
        self.session = requests.Session()

        self.params_widg = {}
        if brain_region != 'All':
            self.params_widg['brain_region'] = 'brain_region:' + brain_region
        if species != 'All':
            self.params_widg['species'] = 'species:' + species
        if cell_type != 'All':
            self.params_widg['cell_type'] = 'cell_type:' + cell_type

        self.params = {}
        self.params['page'] = 0
        self.params['size'] = 500

        fq = []
        first = 0
        for key, value in self.params_widg.items():
            if first == 0:
                first = 1
                self.params['q'] = value
            else:
                fq.append(value)
                self.params['fq'] = fq

        if brain_region == 'All' and species == 'All' and cell_type == 'All':
            self.url = 'http://neuromorpho.org/api/neuron'
        else:
            self.url = 'http://neuromorpho.org/api/neuron/select'
        super().__init__()

    def get_first_page(self):
        brain_region, species, cell_type = self.brain_region, self.species, self.cell_type
        s = self.session

        first_page_response = s.get(self.url, params=self.params)
        print(first_page_response.json())

        if first_page_response.status_code == 404 or first_page_response.status_code == 500:
            self.print_to_textbox("Unable to get CSV! Status code: " + str(first_page_response.status_code))
            return 0
        elif 'status' in first_page_response.json() and first_page_response.json()['status'] == 500:
            self.print_to_textbox("Unable to get CSV! Status code: " + str(first_page_response.json()['status']))
            return 0
        print(str(first_page_response.request.url))
        print(first_page_response.status_code)

        return first_page_response.json()['page']['totalPages'], first_page_response.json()['page']['totalElements']

    def get_morphometry(self, np_array):
        morphometry = []
        for i in np_array:
            url = "http://neuromorpho.org/api/morphometry/id/" + str(i)
            response = self.session.get(url)
            response.raise_for_status()
            json_data = response.json()
            morphometry.append(json_data)

            if response.status_code == 200:
                text_status_code = '\u2705'
            else:
                text_status_code = '\u274C'

            self.print_to_textbox('Querying cells {} -> status code: {}  {}'.format(
                str(i), response.status_code, text_status_code)
            )
        return morphometry

    def run(self):
        file_name = ""
        try:
            brain_region, species, cell_type = self.brain_region, self.species, self.cell_type
            s = self.session
            starttime = datetime.datetime.now()

            self.set_progress(0)
            self.print_to_textbox(brain_region + '\n' + species + '\n' + cell_type + '\n')
            totalPages, totalElements = self.get_first_page()

            self.print_to_textbox("Getting Neurons - total elements:" + str(totalElements) +
                                  "\nDo you want to continue?")
            timer = 10
            while self.is_paused and not self.is_killed:
                time.sleep(1)
                timer -= 1
                self.print_to_textbox("Will continue in: " + str(timer) + " seconds")
                if timer == 0:
                    break

            if self.is_killed:
                self.print_to_textbox("CANCELLED!!!")
                self.print_to_textbox("\n" + "#" * text_width + "\n")
                self.set_progress(0)
                return 0
            self.print_to_textbox("Continuing...")
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


            self.print_to_textbox("Getting Neurons - total pages:" + str(totalPages))
            progress_step = 20.0/totalPages
            for pageNum in range(totalPages):
                self.params['page'] = pageNum
                response = s.get(self.url, params=self.params)
                if response.status_code == 200:
                    text_status_code = '\u2705'
                else:
                    text_status_code = '\u274C'
                self.print_to_textbox('Querying page {} -> status code: {}  {}'.format(
                    pageNum, response.status_code, text_status_code))
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
                self.set_progress(pageNum * progress_step)
            self.set_progress(20)

            self.print_to_textbox("Creating neuron Data Frame")
            neurons_df = pd.DataFrame(df_dict)
            self.set_progress(25)
            self.print_to_textbox("Pickling neurons")
            makedirs("./output", exist_ok=True)
            neurons_df.to_pickle("./output/neurons.pkl")
            self.set_progress(30)

            # the ID number of previously obtained neurons is used to obtain their morphometric details

            np_array = neurons_df['NeuronID'].to_numpy()
            np_arrays = np.array_split(np_array, max_thread_count)

            self.print_to_textbox("Getting morphometry")
            morphometry = []
            progress_step = 40.0 / np_array.size
            progress_value = 0.0
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_thread_count) as executor:
                futures = []
                for n in np_arrays:
                    futures.append(executor.submit(self.get_morphometry, np_array=n))
                for future in concurrent.futures.as_completed(futures):
                    morphometry.extend(future.result())


            print(morphometry)
            self.set_progress(70)
            self.print_to_textbox("Creating morphometry Data Frame")
            df_dict = {}
            df_dict['NeuronID'] = []
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
            df_dict['Branch order'] = []
            df_dict['Contraction'] = []
            df_dict['Fragmentation'] = []
            df_dict['Partition asymmetry'] = []
            df_dict['Pk classic'] = []
            df_dict['Bifurcation angle local'] = []
            df_dict['Fractal dimension'] = []
            df_dict['Bifurcation angle remote'] = []
            df_dict['Length'] = []
            for row in morphometry:
                df_dict['NeuronID'].append(str(row['neuron_id']))
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
                df_dict['Branch order'].append(str(row['branch_Order']))
                df_dict['Contraction'].append(str(row['contraction']))
                df_dict['Fragmentation'].append(str(row['fragmentation']))
                df_dict['Partition asymmetry'].append(str(row['partition_asymmetry']))
                df_dict['Pk classic'].append(str(row['pk_classic']))
                df_dict['Bifurcation angle local'].append(str(row['bif_ampl_local']))
                df_dict['Fractal dimension'].append(str(row['fractal_Dim']))
                df_dict['Bifurcation angle remote'].append(str(row['bif_ampl_remote']))
                df_dict['Length'].append(str(row['length']))
            morphometry_df = pd.DataFrame(df_dict)

            self.set_progress(75)

            self.print_to_textbox("Pickling morphometry")
            morphometry_df.to_pickle("./output/morphometry.pkl")

            # the following is a list of steps used to currate the morphometric data
            # and merge the two obtained dataframes (general neuron parameters and morphometric data)
            # this results in the creation of final .pkl and .csv files at the end of the notebook

            neurons = open("./output/morphometry.pkl", "rb")
            neurons_df = pickle.load(neurons)
            neurons.close()
            self.set_progress(80)
            self.print_to_textbox(neurons_df)

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
            neurons_df["Branch order"] = pd.to_numeric(neurons_df["Branch order"], downcast="float")
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
            self.set_progress(85)
            self.print_to_textbox(neurons_id_df)

            neuron_morphometry = open("./output/neurons_float.pkl", "rb")
            neuron_morphometry_df = pickle.load(neuron_morphometry)
            neuron_morphometry.close()
            self.set_progress(90)
            self.print_to_textbox(neuron_morphometry_df)

            #neurons_id_df.set_index('NeuronID', inplace=True)
            #print("set index 1")
            #neuron_morphometry_df.set_index('NeuronID', inplace=True)
            print("set index 2")
            final_df = pd.merge(neurons_id_df, neuron_morphometry_df, on='NeuronID')
            #final_df = neurons_id_df.join(neuron_morphometry_df)

            # excess NeuronID column left when joining two dataframes
            #final_df = final_df.drop(columns=['NeuronID'])

            file_name = "./output/" + self.filename

            final_df.to_pickle(file_name)

            final_df.to_csv(file_name, index=False)

            self.set_progress(100)
            self.print_to_textbox(final_df)

            finishtime = datetime.datetime.now() - starttime

            self.print_to_textbox(str(finishtime))
            self.print_to_textbox("DONE!")
            self.print_to_textbox("\n" + "#" * text_width + "\n")
            self.set_progress(0)
        except Exception as e:
            print(e)
        finally:
            self.signals.finished.emit(file_name)

