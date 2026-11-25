# Set up your Windows laptop

This guide sets up a Windows laptop for the whole course: Git Bash in VS Code, uv with Python 3.12, the DuckDB command-line tool, VS Code's Python and Jupyter extensions, Excel and Power BI Desktop.
**Git Bash is your terminal**, inside VS Code. After each step, run its check before you go on.
The course needs no Docker and no database server.

The versions are in [`VERSIONS.md`](../VERSIONS.md).

## Before you start

- **Windows 10 or 11.** Press Windows+R, type `winver` and press Enter to see your version.
- **At least 8 GB of memory** and **10 GB of free disk space**. Microsoft asks for at least 2 GB of free memory for Power BI Desktop, and recommends 4 GB.
- **A screen of at least 1440 x 900**, with display scale at 100 % when you use Power BI Desktop (see Step 10).
- **An administrator account** on the laptop, or a mentor who can install for you.
- **Excel**: Microsoft 365 or Excel 2024. Step 9 checks it.

## When you do each step

| Step | What | When |
|---|---|---|
| 1 | Git for Windows, with Git Bash | Launchpad task 11 (the terminal card) |
| 2 | VS Code, then its Python and Jupyter extensions | VS Code in Launchpad task 12, the extensions in task 13 |
| 3 to 6 | Git Bash in VS Code, line endings, uv, Python 3.12, UTF-8 | Launchpad task 13 ("Finish the laptop, part 1") |
| 8, then 7 | Clone the course kit, then the DuckDB command-line tool | Launchpad task 14 ("Finish the laptop, part 2") |
| 9 | Check your Excel version | Before Launchpad task 2 (your first spreadsheet); task 14 writes it down |
| 10 | Power BI Desktop | Before P4 SalesBoard (week 7). Install it in week 1 if you can: it is a big download |
| 11 | Smart App Control | Before P3 MatchStats (week 6). Do the test in week 1 |

Task 13 does Steps 3 to 6 and the extensions of Step 2. Task 14 does Step 8 first (the clone), then Steps 7 and 9.
Run every command in **Git Bash**, unless a step says PowerShell. Only the two installers (Steps 5 and 7) and the first check of Step 11 run in PowerShell.

## Step 1: Git for Windows

Install Git from https://git-scm.com/downloads/win with the default options. They include Git Bash and Git Credential Manager, which signs you in to GitHub.

Check it in Git Bash:

```bash
git --version
```

You see `git version 2.` and more numbers. Any version from 2.45 is fine.

## Step 2: VS Code and its Python and Jupyter extensions

1. Install VS Code from https://code.visualstudio.com/download with the default options.
2. Open VS Code, select **Extensions** (Ctrl+Shift+X), and install **Python** and **Jupyter**, both from Microsoft.

The Jupyter extension runs a `.py` file one cell at a time. A cell starts with a line `# %%`. VS Code shows **Run Cell** above each one, and the results open in a pane on the right. The course keeps Python analysis in `.py` files like this, never in `.ipynb` notebooks.

Check it in Git Bash: `code --version` prints a version number.

## Step 3: Make Git Bash the terminal in VS Code

1. In VS Code, press Ctrl+Shift+P and type `Terminal: Select Default Profile`.
2. Choose **Git Bash**.

Check it: open a new terminal (**Terminal**, then **New Terminal** in the top menu). The prompt shows `MINGW64`, and `uname -s` prints a line that starts with `MINGW64`.

## Step 4: Line endings

Windows ends each line of a text file with two characters (CRLF), Linux and macOS with one (LF). The course's files use LF, so that your SQL, DAX and Python files look the same on every laptop and in every diff.

1. In VS Code, open **Settings** (Ctrl+,) and search for `eol`.
2. Set **Files: Eol** to `\n`.

Check it: open a new file. The status bar at the bottom right shows `LF`, not `CRLF`. In Git Bash, this prints the setting:

```bash
grep eol "$APPDATA/Code/User/settings.json"
```

## Step 5: uv and Python 3.12

uv installs Python and runs your programs. Run this in **PowerShell**:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Close every terminal and VS Code, then open Git Bash again and run:

```bash
uv --version
uv python install 3.12
uv python pin --global 3.12
```

The last command makes Python 3.12 uv's default everywhere on your laptop.

Check it:

```bash
uv run --no-project python --version
```

You see `Python 3.12.` and more numbers. This is the only Python you need. When a course command says `uv run`, uv starts it for you.

In each new Python project, pin the version right after `uv init`:

```bash
uv init --bare --python 3.12
uv python pin 3.12
```

## Step 6: Python and UTF-8

In Git Bash, Python cannot print characters such as `£` or `₹` into a pipe or a file unless UTF-8 mode is on. Turn it on once, in Git Bash (the same command works in PowerShell):

```bash
setx PYTHONUTF8 1
```

Close and reopen VS Code. Check it in Git Bash:

```bash
uv run --no-project python -c "print('£1,250.50 ₹')" | cat
```

You see `£1,250.50 ₹`. An error that names `charmap` means the setting is not on yet: reopen VS Code.

## Step 7: The DuckDB command-line tool

DuckDB is a database that runs inside one program, with no server. You use it from the command line in P2 ShopQuery and from Python in P3. Install it with DuckDB's own script, in **PowerShell**:

```powershell
powershell -NoExit -ExecutionPolicy Bypass -Command "irm https://install.duckdb.org/install.ps1 | iex"
```

It saves `duckdb.exe` in `C:\Users\<your name>\AppData\Local\duckdb\cli\2.0.1\` and puts a DuckDB shortcut on your desktop. It does not add DuckDB to your `PATH`, so tell Git Bash where it is, once:

```bash
echo 'export PATH="$PATH:$(cygpath "$LOCALAPPDATA")/duckdb/cli/2.0.1"' >> ~/.bashrc
source ~/.bashrc
```

Check it:

```bash
duckdb --version
duckdb -c "SELECT 6 * 7 AS answer;"
```

The first line prints `v2.0.1` and more. The second prints a small table with `42`.

- Do not use `winget install DuckDB.cli`: it still installs the older 1.5 release.
- If the script installed a newer version, its folder has that number: change `2.0.1` in the line in `~/.bashrc` to match (`ls "$(cygpath "$LOCALAPPDATA")/duckdb/cli"` lists it).
- Python uses its own copy of DuckDB: `uv add duckdb` in a project. Both read the same files.

## Step 8: Clone the course kit

The kit holds the course's data files, the scripts that make your own copies of the data, the Guided starters and the case-study briefs. Clone it into your home folder:

```bash
cd ~ && git clone https://github.com/Anaxionai/da-ess-kit.git
```

This makes `~/da-ess-kit`, which is `C:\Users\<your name>\da-ess-kit`. Keep it next to your course repository, never inside it. When a task says so, update it:

```bash
cd ~/da-ess-kit && git pull
```

Check it: `ls ~/da-ess-kit` lists `README.md`, `VERSIONS.md`, `setup`, `data`, `starters` and `capstone`.

## Step 9: Check your Excel version

Open Excel, select **File**, then **Account**, then **About Excel**. The first line names your version.

- **Microsoft 365** or **Excel 2024**: you have everything the course uses.
- **Excel 2021**: everything except `TEXTSPLIT`. Use `LEFT`, `MID` and `FIND`, or Flash Fill.
- **Excel 2016 or 2019**: Power Query works, but `XLOOKUP` and `TEXTSPLIT` do not. Tell your mentor in week 1.

Check Power Query: select the **Data** tab. You see a **Get & Transform Data** group with **Get Data**.

## Step 10: Power BI Desktop

Power BI Desktop is free and runs only on Windows. The course uses Desktop only: you never publish to the Power BI service, which needs a work or school account.

1. Open https://aka.ms/pbidesktopstore. It opens **Power BI Desktop** in the Microsoft Store.
2. Select **Install**. The Store version needs no administrator rights and updates itself every month.
3. Start Power BI Desktop from the Start menu. Close the sign-in box: you do not need to sign in.

Check it: in Power BI Desktop, select **Help**, then **About**. The **Version** line shows `2.` and more numbers.

- **Dialogs cut off, or buttons you cannot reach?** Microsoft's own advice: set Windows display scale to 100 % (Settings, System, Display) while you use Power BI Desktop. The screen must be at least 1440 x 900.
- **No Microsoft Store?** Download the installer from https://www.microsoft.com/download/details.aspx?id=58494 and choose the 64-bit file. It needs administrator rights.
- **Mac?** Power BI Desktop does not run on macOS. Ask your mentor for a Windows laptop or a Windows virtual desktop for week 7.

## Step 11: Smart App Control

Smart App Control is a Windows 11 security feature that blocks programs and program parts that are not signed. A new Windows 11 laptop may have it **on**. Then it blocks the small `python.exe` that uv puts in every project's `.venv` folder, and parts of `pyarrow` (which pandas uses for Parquet files). P3 MatchStats needs both.

**Check whether it is on**, in PowerShell:

```powershell
(Get-MpComputerStatus).SmartAppControlState
```

It prints `On`, `Eval` or `Off`.

**Test it** in Git Bash (the first run downloads the libraries):

```bash
uv run --no-project --with pandas --with pyarrow --with duckdb python -c "import pandas, pyarrow.parquet, duckdb; print('OK', pandas.__version__)"
mkdir -p ~/sac-test && cd ~/sac-test && uv init --bare --python 3.12 && uv run python -c "print('project OK')"
cd ~ && rm -r ~/sac-test
```

Success prints `OK 3.1.1` (or a newer pandas), then `project OK`.
If you see `An Application Control policy has blocked this file` or `Failed to spawn: python`, Smart App Control blocks them:

1. Open **Windows Security**, then **App & browser control**, then **Smart App Control settings**.
2. Select **Off** and confirm. Run the test again.

Do this only on a laptop that is yours. On a laptop that belongs to your centre or employer, ask its owner or your mentor first. Microsoft's page "What is Smart App Control?" says recent Windows updates let you turn it on again without reinstalling Windows; keep Windows updated before you switch it off. Keep Microsoft Defender Antivirus on either way.

## Final check

Run these in Git Bash in VS Code's terminal, and compare with the "You see" column.

| Command or action | You see |
|---|---|
| `git --version` | `git version 2.` and more |
| `uv run --no-project python --version` | `Python 3.12.` and more |
| `duckdb --version` | `v2.0.1` and more |
| `ls ~/da-ess-kit` | `README.md`, `VERSIONS.md` and the kit folders |
| Excel: File > Account > About Excel | Microsoft 365, or Excel 2024 |
| Power BI Desktop: Help > About | `Version: 2.` and more |
| The two Step 11 tests | `OK` and a version, then `project OK` |

## If something goes wrong

| What you see | What to do |
|---|---|
| `uv`, `code` or `duckdb` is not recognised | The terminal was open before the install. Close every terminal and VS Code, then open them again. For `duckdb`, check the line in `~/.bashrc` (Step 7) |
| `uv run python --version` shows another version | Run `uv python pin 3.12` in the project, delete `.venv`, then run the command again |
| `UnicodeEncodeError` and `charmap` | Do Step 6, then reopen VS Code |
| `An Application Control policy has blocked this file` | Do Step 11 |
| VS Code shows no **Run Cell** above `# %%` | Install the Jupyter extension (Step 2), then reopen the file. When VS Code asks for a kernel, choose the `.venv` of your project, and let it install `ipykernel` |
| Excel opens a CSV file with the dates or the `£` sign wrong | Do not double-click the file. Use **Data > From Text/CSV**, choose the file origin **65001: Unicode (UTF-8)**, and check the preview |
| Power BI Desktop shows black areas or cut-off windows | Set display scale to 100 %. Microsoft also suggests: Start, type *blurry*, turn on **Let Windows fix apps that are blurry**, then restart Power BI Desktop |
