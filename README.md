# RevAssign
The ISMRM-AMPC reviewer assignment helper software is designed to aid the
AMPC in choosing reviewers while maintaining a ledger of how many abstracts
each reviewer has been assigned [(as detailed in Jim Pipe's ISMRM
blog)](http://www.ismrm.org/12/7T.pdf).

# Operational Overview
RevAssign is essentially a spreadsheet with
a slightly more specific sorting function that allows the user to see
information about reviewer candidates (i.e. the number of abstracts they have
been assigned *and* their 5 chosen areas of expertise) while simultaneously
viewing the meeting sessions and the number of abstracts to review.  The
reviewers are sorted based on their interest in their chosen categories (as
shown in the figure below).

![RevAssign Screen Shot](./ScreenShot1.png)

Reviewers (shown in the panel on the right) that have been over-committed
(those that have more than the set number of abstracts) are highlighted with a
gentle salmon color.
The reviewer's category affinity is shown in greyscale from *most interested* (at
the top in light grey) to *interested* (towards the bottom in dark grey) and then
the rest who did not choose to review the category are unsorted and shown in
white.  Each category is selected in the panel on the left.

# Controls
The user can navigate between panels using the Tab key and select categories
and reviewers using the space bar. These can also be navigated with the mouse.

Each column can be sorted alphabetically or numerically (depending on its
content). The columns can also be positioned to the user's tastes.

# Auto-Assign
In 2022 an "Assign" menu was added to automatically pre-assign reviewers to categories. In order to use this feature, first set maximum and minimum nr of reviewers and abstracts in the "Settings" menu, then hit "Assign" in the Assign menu. 

If the parameter settings are incompatible, review the settings and hit "Assign" again. The individual steps in the assignments can also be repeated with the other buttons in the Assign menu. After auto-assigning, you can edit assignments manually as before.

# Input data
For RevAssign to work, it is important that the input data are formatted correctly. Please see the rev_input.xls files in the example_data folder as an example.

Sessions can be saved as a `.mpc` file and later exported to a final `.xls`
spreadsheet to start the next process in the AMPC work flow.

# Installation
RevAssign can be installed and run from an Anaconda platform.

## Install Anaconda
Download the miniconda installer from: https://docs.conda.io/en/latest/miniconda.html

```bash
chmod a+x Miniconda*.sh
./Miniconda*.sh  # follow install instructions
```

## Install Python Tools
With miniconda installed, use the 'conda' command to install the dependencies:

```bash
conda install pyqt xlrd xlwt
```

## Clone the Code
Clone the latest RevAssign commit with:

```bash
git clone https://github.com/nckz/RevAssign.git
```

## Run It
Start RevAssign from the root project directory:

```bash
cd RevAssign
python3 ./RevAssign.py
```
