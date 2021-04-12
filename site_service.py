import os
import service
from zipfile import ZipFile
from os.path import basename

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_file
)

bp = Blueprint('/', __name__, url_prefix='/')


@bp.route('/Home', methods=('GET', 'POST'))
def home_page():
    error = None
    if request.method == 'POST':
        try:
            os.remove("static/Correlation_between_each_component_and_the_labelprognosistask.svg")
        except:
            print("")
        finally:
            pass
        otu_file = request.files['otu_file']
        tag_file = request.files['tag_file']
        taxonomy_level = request.form['taxonomy_level']
        taxnomy_group = request.form['taxnomy_group']
        epsilon = request.form['epsilon']
        z_scoring = request.form['z_scoring']
        PCA = request.form['PCA']
        comp = request.form['comp']
        normalization = request.form['normalization']
        norm_after_rel = request.form['norm_after_rel']
        if not otu_file:
            error = "OTU File should be provided."
        elif int(comp) == 0:
            error = "The number of components should be -1 or positive integer (not 0)."
        else:
            otu_file.save("OTU.csv")
            tag_flag = True
            if tag_file:
                tag_flag = False
                tag_file.save("TAG.csv")
            params = params_dict(taxonomy_level, taxnomy_group, epsilon, z_scoring, PCA, int(comp), normalization,
                                 norm_after_rel)


            service.evaluate(params, tag_flag)



            # create a ZipFile object
            with ZipFile('sampleDir.zip', 'w') as zipObj:
                # Iterate over all the files in directory
                for folderName, subfolders, filenames in os.walk("Mucositis"):
                    for filename in filenames:
                        # create complete filepath of file in directory
                        filePath = os.path.join(folderName, filename)
                        # Add file to zip
                        zipObj.write(filePath, basename(filePath))
                for folderName, subfolders, filenames in os.walk("static"):
                    for filename in filenames:
                        if not (filename == "example_input_files.zip" or filename == "Example_input_options.png"
                                or filename == "plots_example1.png" or filename == "plots_example2.png"):
                            # create complete filepath of file in directory
                            filePath = os.path.join(folderName, filename)
                            # Add file to zip
                            zipObj.write(filePath, basename(filePath))

            images_names = [
                'static/correlation_heatmap_bacteria.png',
                'static/correlation_heatmap_patient.png',
                'static/standard_heatmap.png',
                'static/samples_variance.svg',
                'static/density_of_samples.svg'

            ]

            if not tag_flag:
                images_names.append('static/Correlation_between_each_component_and_the_labelprognosistask.svg')

            try:
                os.remove("TAG.csv")
            except:
                print("")
            finally:
                pass

        # input validation

        flash(error)
        if not error:
            return render_template('home.html', active='Home', otu_file=otu_file, tag_file=tag_file,
                                   taxonomy_level=taxonomy_level,
                                   taxnomy_group=taxnomy_group, epsilon=epsilon, z_scoring=z_scoring, PCA=PCA,
                                   normalization=normalization,
                                   norm_after_rel=norm_after_rel,
                                   images_names=images_names)

    return render_template('home.html', active='Home', taxonomy_level='Specie',
                           taxnomy_group='Sub-PCA', PCA='None')


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
    return send_file("sampleDir.zip", mimetype='zip', as_attachment=True, )


@bp.route('/download-example-files')
def download_example():
    return send_file("static/example_input_files.zip", mimetype='zip', as_attachment=True, )


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
