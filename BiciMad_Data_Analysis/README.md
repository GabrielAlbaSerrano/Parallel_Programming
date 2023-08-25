# BICIMAD Data Analysis

This repository contains data and scripts related to the analysis of BICIMAD, a public bicycle sharing system in Madrid, Spain. The repository includes a folder, datos, which contains the extracted information from the registers of BICIMAD for the years 2017 and 2018, and of March of 2019. Additionally, the repository includes a PDF document, Memoria_Práctica_BICIMAD___PRPA.pdf, which provides a detailed explanation of the study and the business case, showcasing the insights obtained from the analysis. The folder program contains all the necessary items to execute the analysis.

In the folder program the user will find two files. This is in case the user does not want to use the Raspberries PI cluster. In case the user wants to use the cluster, he MUST use the python script by the name of bicimad.py inside this folder, in programa_ejecutar_cluster . If not, he should use the file in the other folder.

## Files
- Ejecucion_cluster: This txt file shows the upload and execution of the script in the Raspberries PI Cluster.

- bicimad.py : This Python script (inside program) was utilized to extract and process the BICIMAD data using the PySpark framework. The script includes various functions and algorithms to clean, transform, and analyze the data, providing valuable insights into the usage patterns and trends of the BICIMAD system.

- Memoria_Práctica_BICIMAD___PRPA.pdf: This PDF document provides a comprehensive overview of the study conducted on BICIMAD data. It includes an explanation of the data analysis process, methodologies used, and the insights gained from the analysis. The document also presents a business case based on the findings.

## Usage
To use the data and script provided in this repository, follow the steps below:

Clone the repository using the following command:
git clone https://github.com/your-username/bicimad-data-analysis.git
Ensure that you have the necessary dependencies installed, including PySpark.

Open the bicimad_cluster.py script in a Python IDE or text editor to view and modify the code if needed.

Enter the cluster Raspberries PI.

Execute the script using a PySpark environment to obtain insights from the BICIMAD data.

Contribution
Contributions to this repository are welcome. If you have any improvements or suggestions, please feel free to create a pull request or raise an issue.
