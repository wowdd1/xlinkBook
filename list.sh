#!/bin/bash

#author: wowdd1
#data: 2014.11.19

usage="\nusage:  ${0} filename or dirname [column_num] ['keyword or regexp'] [isAlignCourseName]\n
filename or dirname: the course file or dir\n
column_num: from 1 to 3\n
keyword or regexp: the keyword for filter course\n
keyword suggest(to list keyword, please run ${0} help filename):\n"
usage2="eg: ${0} db/eecs-course-all2014 2 'Machine learning'\n
\040\040\040\040${0} db/eecs-course-all2014 1 '^cs.*Cryptography'\n
\040\040\040\040${0} db/eecs/eecs-course-edx2014 2 '' no | sort  -k1 -n -r\n"

if [ "${1}" = "" ] || [ "${1}" = "help" ]
then
    echo -e "${usage}"
    if [ "${2}" != "" ]
    then
        tr -sc "[A-Z][a-z]"  "[\012*]"  < ${2} |  \
        tr  "[A-Z]"  "[a-z]"  | \
        sort  | uniq -c |   \
        sort  -k1 -n -r  |  \
        head -500 | nl
    fi
    echo -e "${usage2}"
    exit
fi

cell_len=92  #  cell_len >= course_num_len + 1 + course_name_len + 3
course_name_len=70
course_num_len=8
file_name=${1}
column_num=${2}
keyword=${3}
isAlignCourseName=${4}


function fAlignCourseName(){
    course_num=${result%% *}
    course_name=${result#* }
    space_b=""
   
    if [ ${course_num_len} == 0 ]
    then
        return
    fi
 
    if [ ${#course_name} -gt ${course_name_len} ]
    then
       course_name=${course_name:0:${course_name_len}}"..."
    fi

    if [ ${#course_num} -lt ${course_num_len} ]
    then
        for((j=0;j<$[${course_num_len}-${#course_num}];j++))
        do
            #if [ ${j} -eq $[7-${#course_num}] ]
            #then
            #    space_b=${space_b}">"
            #else
            #    space_b=${space_b}"-"
            #fi
            space_b=${space_b}"$"
        done

        result=${course_num}${space_b}" "${course_name}
        space_2=""
        return
    fi

    result=${course_num}" "${course_name}
}


function print_list() {
    i=0
    while read line
    do
        if [ "${keyword}" != "" ] # filter course
        then
            echo "$line" |grep -iq "${keyword}"
            if [ $? -ne 0 ]
            then
                continue
            fi
        fi
    
        if [ "${isAlignCourseName}" = "no" ] # do not align course name
        then
            course_num_len=0
        fi
        result=$line
        if [[ $line =~ ":" ]]
        then
            result=${line//":"/}
        fi
    
        let i++
        if [ "${column_num}" =  "3" ] # print 3 column
        then
            if [ $[${i}%3] = "0" ]
            then
                space=""
                for((j=0;j<${cell_len}-${#pre_result_2};j++))
                do
                    space=${space}"\040"
                done
                fAlignCourseName
                text_output=${pre_result}${space}" "${result}
                echo -e ${text_output//$/\\040}

                pre_result=""
                pre_result_2=""
                text_output=""
            else
                if [ $[$[${i}-1]%3] = "0" ]
                then
                    fAlignCourseName
                    pre_result=${result}
                else
                    space=""
                    for((j=0;j<${cell_len}-${#pre_result};j++))
                    do
                        space=${space}"\040"
                    done
                    fAlignCourseName
                    pre_result_2=${result}
                    pre_result=${pre_result}${space}" "${result}
                fi
            fi
        elif [ "${column_num}" = "2" -o "${column_num}" = "" ] # print 2 column
        then    
            if [ $[${i}%2] = "0" ]
            then
                space=""
                for((j=0;j<${cell_len}-${#pre_result};j++))
                do
                    space=${space}"\040"
                done
                fAlignCourseName
                text_output=${pre_result}${space}" "${result}
                echo -e ${text_output//$/\\040}
                #echo -e ${text_output}
                pre_result=""
                text_output="" 
            else
                fAlignCourseName
                pre_result=${result}
            fi
        else  #print 1 column
            fAlignCourseName
            text_output=${result}
            echo -e ${text_output//$/\\040}
            text_output=""
        fi
    done < ${file_name}

    if [ "${pre_result}" != "" ]
    then
        echo -e ${pre_result//$/\\040}
        pre_result=""
    fi

    if [ "${keyword}" != "" ]
    then
        echo -e "\nTotal ${i} records cotain ${keyword}"
    else
        echo -e "\nTotal ${i} records"
    fi
    echo -e "File: ${file_name}\n"
}

dir=""

function print_dir() {
    local filelist=`ls ${1}`
    for file in $filelist
    do
        if [ -f "${1}${file}" ]
        then
            file_name=${1}${file}
            print_list
        elif [ -d "${dir}${file}" ]
        then
            print_dir ${1}${file}"/"
        fi
    done
}

if [ -d "${1}" ]
then
    dir="${1}"
    if [ "${dir:0-1:1}" != "/" ]
    then
        dir=${dir}"/"
    fi

    print_dir ${dir}

else
    file_name=${1}
    print_list
fi

date
