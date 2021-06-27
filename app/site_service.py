import os
from calc_antigens_freqs import call_calc_antigens
from zipfile import ZipFile
from os.path import basename
import shutil

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_file
)

bp = Blueprint('/', __name__, url_prefix='/')

output_path = 'static/output/probs_without_antigens_haps.csv'


@bp.route('/Home', methods=('GET', 'POST'))
def home_page():
    error = None

    hpf_path = "static/input/"
    os.makedirs(hpf_path, exist_ok=True)

    # populations = ['Kavkaz', 'Ashkenazi', 'Ethiopian', 'Sephardi', 'Others', 'Arab',
    #                "General_IL", "AFB", "AINDI", "AISC", "ALANAM", "AMIND", "CARB", "CARHIS",
    #                "CARIBI", "HAWI", "FILII", "KORI", "JAPI", "MSWHIS", "MENAFC", "NAMER", "NCHI",
    #                "SCAHIS", "SCAMB", "SCSEAI", "VIET", "AFA", "API", "CAU", "HIS", "NAM"]

    population_not_asumme = [
        'General_IL',
        'Ashkenazi',
        'Asian',
        'Ethiopia',
        'Others',
        'Sephardi',
    ]

    population_asumme_hwe = [
        'General_IL',
        'Ashkenazi',
        'Asian',
        'Ethiopian',
        'Others',
        'Sephardi',
        'AFA',
        'AFB',
        'AINDI',
        'AISC',
        'ALANAM',
        'AMIND',
        'API',
        'CARB',
        'CARHIS',
        'CARIBI',
        'CAU',
        'FILII',
        'HAWI',
        'HIS',
        'JAPI',
        'KORI',
        'MENAFC',
        'MSWHIS',
        'NAM',
        'NAMER',
        'NCHI',
        'SCAHIS',
        'SCAMB',
        'SCSEAI',
        'VIET'
    ]

    populations = []

    asumme_HWE_form = True

    if request.method == 'POST':
        hpf_files = request.files.getlist('hpf_files')
        asumme_HWE_form = request.form.get('Asumme_HWE')
        population_asumme_hwe_form = request.form['population_asumme_hwe']
        population_not_asumme_form = request.form['population_not_asumme']
        string_input = request.form['string_input']

        if asumme_HWE_form:
            pop = population_asumme_hwe_form
            asumme_HWE_form = True
        else:
            pop = population_not_asumme_form
            asumme_HWE_form = False

        print(asumme_HWE_form)

        input_counter = 0

        if not hpf_files[0].filename == '':
            for i, hpf_file in enumerate(hpf_files):
                hpf_file.save(hpf_path + 'hpf_file' + str(i) + '.csv')
                input_counter += 1
        if pop:
            pop = str(pop)
            input_counter += 1
        if string_input:
            string_input = str(string_input)
            input_counter += 1
        if input_counter == 0:
            error = "Some inputs are missing."

        if pop and string_input:
            call_calc_antigens(pop=pop, string_input=string_input, Assume_HWE=asumme_HWE_form)
        elif pop:
            call_calc_antigens(pop=pop, Assume_HWE=asumme_HWE_form)
        elif string_input:
            call_calc_antigens(string_input=string_input, Assume_HWE=asumme_HWE_form)

        if os.path.exists(output_path):
            with open(output_path, 'r') as output_file:
                output_lines = output_file.readlines()

        output_pairs = []
        for i in range(1, len(output_lines), 1):
            output_line = output_lines[i].split(',')
            output_pairs.append([item.rstrip() for item in output_line])

        print(output_pairs)
        output_table = output_pairs

        try:
            shutil.rmtree(hpf_path)
        except:
            print("")
        finally:
            pass

        # input validation
        flash(error)
        if not error:
            return render_template('home.html', active='Home', hpf_files=hpf_files, pop=pop, string_input=string_input,
                                   populations=populations, output_lines=output_lines, output_table=output_table,
                                   asumme_HWE=asumme_HWE_form,
                                   population_asumme_hwe=population_asumme_hwe,
                                   population_not_asumme=population_not_asumme)

    return render_template('home.html', active='Home',
                           populations=populations, asumme_HWE=asumme_HWE_form,
                           population_asumme_hwe=population_asumme_hwe,
                           population_not_asumme=population_not_asumme)  # can add other variables here like args.


@bp.route('/Help')
def help_page():
    return render_template('help.html', active='Help')


@bp.route('/Example')
def example_page():
    return render_template('example.html', active='Example')


@bp.route('/About')
def about_page():
    return render_template('about.html', active='About')


@bp.route('/download-outputs')
def download():
    return send_file(output_path, mimetype='csv', as_attachment=True, )


@bp.route('/download-example-files')
def download_example():
    return send_file("static/example/input_exaple_1.csv", mimetype='csv', as_attachment=True, )


def params_dict(taxonomy_level, taxnomy_group, epsilon, z_scoring, pca, comp, normalization, norm_after_rel):
    taxonomy_level_dict = {"Order": 4, "Family": 5, "Genus": 6, "Specie": 7}
    taxonomy_group_dict = {"Sub-PCA": 'sub PCA', "Mean": 'mean', "Sum": 'sum'}
    z_scoring_dict = {"Row": 'row', "Column": 'col', "Both": 'both', "None": 'No'}
    normalization_dict = {"Log": 'log', "Relative": 'relative'}
    norm_after_rel_dict = {"No": 'No', "Yes": 'z_after_relative'}
    dimension_reduction_dict = {"PCA": (comp, 'PCA'), "ICA": (comp, 'ICA'), "None": (0, 'PCA')}
    params = {
        'taxonomy_level': taxonomy_level_dict[taxonomy_level],
        'taxnomy_group': taxonomy_group_dict[taxnomy_group],
        'epsilon': epsilon,
        'normalization': normalization_dict[normalization],
        'z_scoring': z_scoring_dict[z_scoring],
        'norm_after_rel': norm_after_rel_dict[norm_after_rel],
        'std_to_delete': 0,
        'pca': dimension_reduction_dict[pca]
    }
    print(params)
    return params
