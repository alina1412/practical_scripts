# subscription_manager

## **What is the purpose?**

The script helps in comparing, merging and converting lists of subscriptions of youtube.

## **Why it's needed?**

When using different accounts and devices with different applications for representation of youtube client the list of subscriptions could get differ.

In some corresponding applications that I used the subscriptions could be uploaded from the file. It allows formats `"json"`, `"csv"`, `"db"`. This script allows you to convert the list to one of these formats, it prints a list to the screen to make the comparison easier.

I kept the field names as ["Channel ID", "Channel URL", "Channel title"] as they were the most necessary parts for uploading subscriptions.

## **How to use it?**

The default folder for files to convert is the folder `materials`. In this project it contains `demo versions` of 2 input and output files (subs_old, subs_new, merged_sub).

After running a program, the user is asked to chose the format of the output. The file would be saved with the name "merged_sub" to the folder `materials.`

The names of input files or the folder could be changed in the _main_ function.

If user gives only a "new" subscriptions, the program would take it as "all new", still suggesting to save it to one of the 3 formats to the new output file.
