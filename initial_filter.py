import pandas as pd
from typing import List

#TODO:
'''
Temporary file (to delete later) to develop the filters dynamically on the excel file.
'''

def printReceivedInput(elaboratedInput) -> None:
    print('Input received:')
    if elaboratedInput == []:
        print('Nothing selected')
    else:
        print(elaboratedInput)
    print()  # leave a line of space before the next print

def getUserInput() -> str:
    userInput = input("Write here:")
    return userInput

def getUserInputList() -> List[str]:
    userInput = getUserInput()
    if userInput == '':
        return []
    else:
        return userInput.split(",")

def getUserInputListFromNumberedList(elementList: List[str]) -> List[str]:
    # the user will insert the selected elements as 1,2,3 as the position in the option list starting from 1 (e.g. 1 is elementList[0])
    userInput = getUserInputList()
    if len(userInput) == 0:  # if input is empty
        return userInput
    # otherwise:
    selectedElements = []
    for number in list(map(lambda x: int(x), userInput)):
        selectedElements.append(elementList[number-1])
    return selectedElements

def printNumberedList(list: List[str]) -> None:
    for i in range(0, len(list)):
        print(str(i + 1) + "-" + list[i])

def isNumber(string : str) -> bool:
    try:
        float(string)
        return True
    except ValueError:
        return False

print('Loading file...')
df = pd.read_excel("C:/Users/nicho/Desktop/920-22 + Merge.xlsx")
print('Completed.')

# filter 1
print("Which mutations do you want to analyze?")
print('Write your input as 1,2,5,12 (with no space around commas)')

optionInputMutations = df['Func.refGene'].unique()  # options to select
printNumberedList(optionInputMutations)

selectedMutations = getUserInputListFromNumberedList(optionInputMutations)
printReceivedInput(selectedMutations)

# filter 2
print("Genes to exclude:")
print("Write the list here(as gene1,gene2,gene3) with no space around commas")
print("Press Enter to include all.")
genesToExclude = getUserInputList()
printReceivedInput(genesToExclude)

# filter 3
print('Causative effects to exclude:')
print("Write the list here (as 2,3,14) with no space around commas")
print("Press Enter to include all.")
optionInputCausEff = df['ExonicFunc.refGene'].dropna().unique()  # options to select (removing emtpy cells from options)
printNumberedList(optionInputCausEff)
causEffToExclude = getUserInputListFromNumberedList(optionInputCausEff)
printReceivedInput(causEffToExclude)

# filter 4
print('Cutoff:')
print('(example: to set cutoff to 15%, insert 0.15 or 0,15)')
selectedCutOff = getUserInput()
selectedCutOff = selectedCutOff.replace(',', '.')
if not isNumber(selectedCutOff):
    raise Exception('The cut off is not a valid number')
selectedCutOff = float(selectedCutOff) # convert string in actual number
printReceivedInput(selectedCutOff)