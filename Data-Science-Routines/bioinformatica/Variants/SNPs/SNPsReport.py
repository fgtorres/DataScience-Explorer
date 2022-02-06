#
# SNPs REPORT
#  This script build a report about the SNPs using a lot of VCF file.
#  (!)For to use it, is necessary to install the softwares and libraries:
#  ** VCF Tools 0.36 (https://github.com/vcftools/vcftools)

import os
import sys

# Additional functions
# Get the parameters of command line.
def getparam(param_name):
    name = False
    for param in sys.argv :
        if (name):
            name = False
            return param
        if (param == param_name):
            name = True
    return False

# This function print the help option in the console.
def printhelp():
    print("This script build a report about the SNPs using a lot of VCF file.")
    print(" (!)For to use it, is necessary to install the softwares and libraries:")
    print("     ** VCF Tools 0.36 (https://github.com/vcftools/vcftools)")
    print("")
    print("Some parameters and example command:")
    print(" python SNPsReport.py -vcf [path VCF folder] ")

#This function process the VCF files and build a merge between these files.
def addcolumndata(tab, addcolumndatafile,positioncolumn,chromosomecolumn,namenewcolumn,datacolumn, outputname):

    #Read source positions file and the new data tab file.
    sourcefile = open(tab, 'r')
    content = sourcefile.readlines()
    header = True

    #Build the dictionary of positions and snps. The idea for store this data in memory is for to improve the
    #performance of process the files.
    array_content = {}
    array_content["header"] = ("chromosome","position","ref_allele")

    #Read the snps tab file and store it in the dictionary structure.
    for line in content:
        line = line.replace("\n", "")
        arrayline = tuple(line.split("\t"))

        #if the content is a header store it in the array_content.
        if "position" in line:
            array_content["header"] = arrayline

        keyname = arrayline[chromosomecolumn] + "_" + arrayline[positioncolumn]
        array_content[keyname] = arrayline

    # Add in the header the new name of the new tab file.
    array_content["header"] = array_content["header"] + (namenewcolumn.split("_")[0],)

    # Read the additional file.
    additionalfile = open(addcolumndatafile, 'r')
    additionalcontent = additionalfile.readlines()

    #Fill the mutations positions on the dictionary.
    print("Starting filling file new mutation data...")
    for additionalline in additionalcontent:
          try:
            arrayaddline = tuple(additionalline.split("\t"))
            array_content[arrayaddline[chromosomecolumn] + "_" + arrayaddline[positioncolumn]] = \
                array_content[arrayaddline[chromosomecolumn] + "_" + arrayaddline[positioncolumn]] + \
                tuple(arrayaddline[datacolumn])
          except:
            Exception.mro()

    # Change the header and put in the final array for print in the output file.
    tempcontent = []
    header = ""
    for key in array_content["header"]:
        header = header + str(key) + "\t"
    tempcontent.append(str(header).replace("\r\n","").replace("\r","") + "\r\n")
    count_header = len(array_content["header"])

    #Store the dictionary in the output file.
    print("Preparing the final content file...")
    for data in array_content:

        #remove header of array_content, because this data is on the array already.
        if "position" in array_content[data]:
            array_content.pop(data)
            break;

        # Case the line dont has mutation, we put . in the position. If the entry continue with format problems, we
        # removed it.
        contentline = ""
        if len(array_content[data]) < count_header and "position" not in array_content[data]:
            array_content[data] = array_content[data] + tuple(".")
        elif len(array_content[data]) < count_header:
            array_content.pop(data)

        # Put every field and build the line data content.
        contentline = ""
        for key in array_content[data]:
           if "\r\n" in key :
               key = ""
           contentline = contentline + key + "\t"

        # If finished the fields, we put the breaklike symbol.
        if(len(contentline.split("\t"))>=count_header):
            tempcontent.append(str(contentline).replace("\r\n","").replace("\r","") + "\r\n")

    #Save the data in the output file.
    print("Saving the final content in the file...")
    tempfile = open(outputname, 'w')
    tempfile.writelines(tempcontent)
    tempfile.close()
    sourcefile.close()
    print("Concluded the " + addcolumndatafile + " file.")

#Function for build statistics about the file tab.
def addStatistic(tab):
    # Read source positions file and the new data tab file.
    sourcefile = open(tab, 'r')
    content = sourcefile.readlines()

    # Build the dictionary of positions and snps. The idea for store this data in memory is for to improve the
    # performance of process the files.
    array_content = {}
    # Read the tab file and calc the statistics.
    tempcontent = []
    for line in content:
        line = line.replace("\n", "").replace(" ","").replace("\t\t", "\t").replace("\r","").replace("\r\n","")
        arrayline = tuple(line.split("\t"))

        # If the content not is a header store it in the array_content.
        if "position" not in line :
            if "chr" in line:
                # Calc the counter by base and the total counter of mutations
                # Declare the variables for count.
                count_a = 0
                count_t = 0
                count_c = 0
                count_g = 0
                count_withoutmut = 0
                count_mutations = 0

                for i in range(3,len(arrayline)):
                    if "A" in arrayline[i]:
                        count_a = count_a + 1
                    if "T" in arrayline[i]:
                        count_t = count_t + 1
                    if "C" in arrayline[i]:
                        count_c = count_c + 1
                    if "G" in arrayline[i]:
                        count_g = count_g + 1
                    if "." in arrayline[i]:
                        count_withoutmut = count_withoutmut + 1

                #Add the count in the tab file.
                count_mutations = count_a + count_t + count_g + count_c
                arrayline =  arrayline + (count_a,)
                arrayline = arrayline + (count_t,)
                arrayline = arrayline + (count_c,)
                arrayline  = arrayline + (count_g,)
                arrayline = arrayline + (count_withoutmut,)
                arrayline = arrayline + (count_mutations,)

                contentline = ""
                for key in arrayline:
                    if "\r\n" not in str(key):
                        contentline = contentline + str(key) + "\t"

                tempcontent.append(contentline.replace("\r\n","").replace("\r","").replace("\n", "")+ "\r\n")
        else:
            line = line.replace("\n", "").replace(" ", "").replace("\t\t", "\t").replace("\r\n","").replace("\r","")
            arrayline = tuple(line.split("\t"))
            arrayline = arrayline + ("#Count_A",)
            arrayline = arrayline + ("#Count_T",)
            arrayline = arrayline + ("#Count_C",)
            arrayline = arrayline + ("#Count_G",)
            arrayline = arrayline + ("#Count_Without_mutations",)
            arrayline = arrayline + ("#Count_mutations",)
            contentline = ""
            for key in arrayline:
                if "\r\n" not in str(key):
                    contentline = contentline + str(key) + "\t"

            tempcontent.append(contentline.replace("\r\n","").replace("\r","").replace("\n", "")+ "\r\n")

    #Delete the old tab file.
    os.system("rm "+ tab)

    #Save the statistics in the tab file.
    print("Saving the final statistics in the file...")
    tempfile = open(tab, 'w')
    tempfile.writelines(tempcontent)
    tempfile.close()
    sourcefile.close()
    print("Concluded the " + tab + " file.")



# Main pipeline
if(getparam("-h")!= False):
    printhelp()
else:
    #Verify if mandatory parameters were filled
    validateparam = True
    if (getparam("-vcf") == False):
        print("(!)You need put the VCF folder pathway in the parameters.")
        validateparam = False

    #If everything ok, continue the script
    if(validateparam):

        # #Delete temporary files
        # os.system('rm -r *filtered*')
        # os.system('rm -r snps_concat.out.vcf.gz')
        # os.system('rm -r snps_concat.vcf.gz')
        # os.system('rm -r *temp*')
        # os.system('rm -r *recode*')
        # os.system('echo "Deleted temporary files..."')
        #
        # #Filter SNPs by min quality = 15 and min depth = 5;
        # os.system('for f in ' + getparam("-vcf") +'*.vcf.gz; do vcftools --gzvcf "$f" --minDP 5 --minGQ 15 --out' +
        #           ' "$f"  --recode --recode-INFO-all ; done')
        #
        # #Concat the VCF files and filter by DP
        # os.system('for f in *.vcf; do  bgzip "$f"; done')
        # os.system("vcf-concat *.recode.vcf.gz > snps_concat.vcf")
        # os.system('grep -v "^#" snps_concat.vcf > snps_concat.out.vcf')
        # os.system('grep "PASS" snps_concat.out.vcf | sort -k1,1 -k2,2n > snps_concat_filtered.vcf')

        #Extract every position without repetition
        # os.system('sort -k1,1 -k2,2n snps_concat_filtered.vcf | cut -f1,2,4 | uniq > snps_positions.tab')
        #
        # #Prepare the snps files for every genome
        # os.system('for f in *.recode.vcf.gz; do bgzip -d $f ; done')
        # os.system('for f in *.recode.vcf; do grep -v "^#" $f | sort -k1,1 -k2,2n | cut -f1,2,5 | '
        #           'uniq > ${f}filtered.vcf; done')

        name = "snps_positions.tab"
        for subdir, dirs, files in os.walk('./'):
            for file in files:
                if file.endswith('_snps.vcf.gz.recode.vcffiltered.vcf'):
                    addcolumndata(name,file,1,0,file,2, "temp_" + file + ".tab")
                    name =  "temp_"+ file + ".tab"

        os.system("mv " + name + " output_snps_positions.tab")
        os.system("rm *temp*")
        addStatistic("output_snps_positions.tab")

    else:
        printhelp()

