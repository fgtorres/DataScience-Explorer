#!/usr/bin/perl

use strict;
use warnings;
use Getopt::Long;

my $usage = "
Usage: $0 -r <fastq> -r2 <fastq> -f <folder> [OPTIONS]

 -r, --reads		fastq file with raw reads R1
 -r2, --reads2		fastq file with reverse reads R2
 -f, --folder		folder to save the output (sampleID)
 -q, --quality		confidence cutoff to filter new fragments [Default: 28]
 -m, --minLen		Specifies the minimum length of reads to be kept [Default: 40]
 -t, --threads		Specifies the number of cores to be used in each step [Default: 4]\n 
";
my ($help, $reads, $reads2, $folder, $email, $freebayes);
my $quality = 28;
my $cores = 4;
my $minLen = 40;
if ( @ARGV < 1 or !GetOptions('help|h' => \$help, 'reads|r=s' => \$reads, 'reads2|r2=s' => \$reads2, 
	'quality|q=s' => \$quality, 'folder|f=s' => \$folder, 'threads|t=s' => \$cores, 'minLen|m=s' => \$minLen) or defined $help ) {
	print "Unknown option: @_\n" if ( @_ );
        print $usage;
	exit;
}
if(!defined($reads) || !defined($folder)) {
        print $usage;
        exit;
}

my $sample = $folder;
#####MUDAR AQUI#####
$folder = $folder;

system("mkdir -p $folder");
system("chmod -R a+w $folder");

###MUDAR PARA A CARPETA COM OS PROGRAMAS
my $PATH = "softwares";

##Aqui a carpeta com o fasta do genoma
my $genome = "genoma/genoma.fasta";

my $fastqc = "$PATH/FastQC/fastqc";
my $trimmomatic = "java -jar $PATH/Trimmomatic-0.36/trimmomatic-0.36.jar PE -phred33 -threads $cores";
my $trimmomatic_se = "java -jar $PATH/Trimmomatic-0.36/trimmomatic-0.36.jar SE -phred33 -threads $cores";
my $picard = "java -Xmx2g -jar $PATH/picard.jar";
my $GATK = "java -jar $PATH/GenomeAnalysisTK.jar --disable_auto_index_creation_and_locking_when_reading_rods";
my $bwa = "$PATH/bwa/bwa";


my @temp = ();
my $reads_base = $reads;

@temp = split(/\./,$reads_base);
pop(@temp);
$reads_base = join(".",@temp);
@temp = split(/\//,$reads_base);
$reads_base = pop(@temp);
my $reads2_base = "";
if(defined($reads2)) {
	$reads2_base = $reads2;
	@temp = split(/\./,$reads2_base);
	pop(@temp);
	$reads2_base = join(".",@temp);
	@temp = split(/\//,$reads2_base);
	$reads2_base = pop(@temp);
}

if(defined($reads2)) {
	system("$fastqc -t 2 $folder/$reads $folder/$reads2 -o $folder -q &");
	system("$trimmomatic $folder/$reads $folder/$reads2 $folder/R1_trimmomatic.fastq $folder/R1_trimmomatic_unpaired.fastq $folder/R2_trimmomatic.fastq $folder/R2_trimmomatic_unpaired.fastq ILLUMINACLIP:$PATH/Trimmomatic-0.36/adapters/TruSeq-all-PE.fa:2:30:10 LEADING:5 TRAILING:5 SLIDINGWINDOW:4:$quality MINLEN:$minLen"); #agregar a las opciones del programa

	my $size = -s "$folder/R1_trimmomatic.fastq";
	if($size <= 0) {
		print "Low quality reads, please decrease the quality filter\n";
		system("rm -f $folder/$reads_base\_fastqc.zip $folder/$reads2_base\_fastqc.zip");
		system("rm -f $folder/R1_trimmomatic* $folder/R2_trimmomatic*");
		exit;
	}
	system("$fastqc -t 2 $folder/R1_trimmomatic.fastq $folder/R2_trimmomatic.fastq -o $folder -q");
	system("rm -f $folder/$reads_base\_fastqc.zip $folder/$reads2_base\_fastqc.zip");
	system("rm -f $folder/R1_trimmomatic_fastqc.zip $folder/R2_trimmomatic_fastqc.zip");
	system("rm -f $folder/R1_trimmomatic_unpaired.fastq $folder/R2_trimmomatic_unpaired.fastq");
	system("$bwa mem -v 1 -M -t $cores $genome $folder/R1_trimmomatic.fastq $folder/R2_trimmomatic.fastq >$folder/aligned.sam");
} else {
	system("$fastqc $folder/$reads -o $folder -q &");
	system("$trimmomatic_se $folder/$reads $folder/R1_trimmomatic.fastq ILLUMINACLIP:$PATH/Trimmomatic-0.36/adapters/TruSeq-all-PE.fa:2:30:10 LEADING:5 TRAILING:5 SLIDINGWINDOW:4:$quality MINLEN:$minLen");
	
	my $size = -s "$folder/R1_trimmomatic.fastq";
	if($size <= 0) {
		print "Low quality reads, please decrease the quality filter\n";
		sleep 10;
		system("rm -f $folder/$reads_base\_fastqc.zip");
		system("rm -f $folder/R1_trimmomatic*");
		exit;
	}
	system("$fastqc -t 2 $folder/R1_trimmomatic.fastq -o $folder -q");
	system("rm -f $folder/$reads_base\_fastqc.zip");
	system("rm -f $folder/R1_trimmomatic_fastqc.zip");
	system("rm -f $folder/R1_trimmomatic_unpaired.fastq");
	system("$bwa mem -v 1 -M -t $cores $genome $folder/R1_trimmomatic.fastq >$folder/aligned.sam");
}

system("samtools view -Sb $folder/aligned.sam > $folder/aligned.bam");
system("$picard SortSam VALIDATION_STRINGENCY=SILENT I=$folder/aligned.bam O=$folder/aligned_sorted.bam SORT_ORDER=coordinate");
system("$picard MarkDuplicates VALIDATION_STRINGENCY=SILENT I=$folder/aligned_sorted.bam O=$folder/aligned_dups_removed.bam REMOVE_DUPLICATES=true M=$folder/metrics");
system("$picard AddOrReplaceReadGroups VALIDATION_STRINGENCY=SILENT I=$folder/aligned_dups_removed.bam O=$folder/RG.bam SO=coordinate RGLB=lib_1 RGPL=illumina RGPU=barcode_1 RGSM=sample_1 CREATE_INDEX=true");

#system("$GATK --num_threads $cores -T RealignerTargetCreator -R $genome -I $folder/RG.bam  -o $folder/ALN.intervals");
#system("$GATK -T IndelRealigner -R $genome -I $folder/RG.bam -o $folder/RG_ALN.indels.bam --maxReadsForRealignment 100000 --maxReadsInMemory 1000000 -targetIntervals $folder/ALN.intervals");
#system("$GATK -T BaseRecalibrator -R $genome -I $folder/RG_ALN.indels.bam -o $folder/ALN.grp");
#system("$GATK -T PrintReads -R $genome -I $folder/RG_ALN.indels.bam -BQSR $folder/ALN.grp -o $folder/ALN.BQSR.bam");
system("$GATK -T HaplotypeCaller -R $genome -I $folder/RG.bam -o $folder/ALIGNER.HC.raw.vcf -stand_call_conf 50");
system("$GATK  --num_threads $cores -T SelectVariants -R $genome -V $folder/ALIGNER.HC.raw.vcf -selectType SNP -o $folder/ALIGNER.HC.raw.snp.vcf");
	system("$GATK  --num_threads $cores -T SelectVariants -R $genome -V $folder/ALIGNER.HC.raw.vcf -selectType INDEL -o $folder/ALIGNER.HC.raw.indels.vcf");
	system("$GATK -T VariantFiltration -R $genome -V $folder/ALIGNER.HC.raw.snp.vcf --filterExpression \"QD < 2.0 || FS > 60.0 || MQ < 40.0 || MQRankSum < -12.5 || ReadPosRankSum < -8.0\" --filterName \"snp_filter\" -o $folder/filtered_snps.vcf");
	system("$GATK  -T VariantFiltration -R $genome -V $folder/ALIGNER.HC.raw.indels.vcf --filterExpression \"QD < 2.0 || FS > 200.0 || ReadPosRankSum < -20.0\" --filterName \"indel_filter\" -o $folder/filtered_indels.vcf");

print "Mostra $folder terminou\n";
