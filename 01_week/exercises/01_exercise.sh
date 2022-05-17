
#!/bin/bash
echo Hello World!
spacer="\n\nBREAK\n\n"   # Assigns result of 'echo' command to 'a' ...


bpath=~/_work/p045_spiced/01_week/01_03

# show all files
ls -R -lrt -a -I.git $bpath

printf $spacer


# show files in first target directory

ls -a -I.git $bpath/exercise_1/directoryB/solution_1.1
printf "The first two letters are A and P"

word=`echo AP`

printf $spacer
printf "Running shell script for third letter\n\n"

source $bpath/exercise_1/directoryB/program.sh


word=`echo APT`

printf $spacer
printf "Checking for file size..\n\n"

ls -lrt $bpath/exercise_1/directoryC/

stat --printf="Size of the file is %s bytes\n" $bpath/exercise_1/directoryC/text_file.txt
printf "That corresponds to the letter E"


word=`echo APTE`

printf $spacer
text=$(cat $bpath/exercise_2/solution_2.1.txt)

echo ${text}
word=`echo APTEN`


printf $spacer
printf "The write-out letter is O"

word=`echo APTENO`

printf $spacer
mkdir -p $bpath/exercise_3/solution
cp -p $bpath/exercise_3/part1/* $bpath/exercise_3/solution/
cp -p $bpath/exercise_3/part2/* $bpath/exercise_3/solution/

ls -l $bpath/exercise_3/solution/*

printf "The letters pointed out by the markers are D and Y"
word=`echo APTENODY`

printf $spacer
ls $bpath/exercise_3/data | grep -v 'Y' 
printf "The letters pointed out by the markers are T and E"
word=`echo APTENODYTE`

printf $spacer
python $bpath/exercise_4/file.py
word=`echo APTENODYTES`

printf $spacer
printf "The final word is ${word}\n\n"

