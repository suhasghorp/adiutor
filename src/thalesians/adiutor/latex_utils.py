"""
thalesians.adiutor.latex_utils
==============================

This module provides utilities for generating LaTeX-compatible tables from pandas DataFrames. 
The primary focus is on creating high-quality tables using the `booktabs` style, which is 
commonly used in academic and professional documents.

Key Features
------------
1. **Booktabs Table Generation**:
   - Converts pandas DataFrames to LaTeX tables formatted with `booktabs`.
   - Customizable captions and labels for referencing in LaTeX documents.

2. **Professional Formatting**:
   - Includes horizontal rules for separating table sections (`\hline`).
   - Ensures tables are resizable to fit within the document's layout.

Functions
---------
- **to_booktabs_table(df, caption="Table Caption", label="tab:label")**:
  - Converts a pandas DataFrame into a LaTeX-formatted table using `booktabs` style.
  
  Args:
      - `df (pd.DataFrame)`: The input DataFrame to convert.
      - `caption (str)`: Caption for the table (default: "Table Caption").
      - `label (str)`: Label for referencing the table in LaTeX (default: "tab:label").
  
  Returns:
      - `str`: A LaTeX string representing the booktabs table.

  Example:
      >>> import pandas as pd
      >>> from thalesians.adiutor.latex_utils import to_booktabs_table
      >>> data = {'Column A': [1, 2], 'Column B': [3, 4]}
      >>> df = pd.DataFrame(data)
      >>> print(to_booktabs_table(df, caption="Example Table", label="tab:example"))
      \\begin{table}[htbp]
      \\centering
      \\caption{Example Table}
      \\label{tab:example}
      \\resizebox{\\textwidth}{!}{%
      \\begin{tabular}{lcc}
      \\hline\\hline
      Column A & Column B \\\\
      \\hline
      1 & 3 \\\\
      2 & 4 \\\\
      \\hline\\hline
      \\end{tabular}
      }
      \\end{table}

Dependencies
------------
- **pandas**: For DataFrame manipulation and LaTeX table conversion.

Testing
-------
The module includes a `_test()` function for `doctest` validation.

Notes
-----
- The `to_booktabs_table` function assumes the presence of the `booktabs` package in your LaTeX document.
- The resulting table includes formatting for readability and compatibility with most LaTeX styles.

License
-------
This module is part of the `thalesians.adiutor` package. All rights reserved.
See LICENSE for details.
"""

def to_booktabs_table(df, caption="Table Caption", label="tab:label"):
    """
    Generates a professionally formatted LaTeX booktabs table from a pandas DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame.
        caption (str): Caption for the table.
        label (str): Label for referencing the table in LaTeX.

    Returns:
        str: A LaTeX string representing the booktabs table.
    """
    # Convert DataFrame to LaTeX
    latex_table = df.to_latex(
        index=False,
        escape=False,  # Allows LaTeX commands in the DataFrame
        column_format="l" + "c" * (df.shape[1] - 1),  # Align columns: first column left, others center
        bold_rows=False,
        longtable=False,
        multicolumn=False
    )
    
    # Add booktabs and formatting
    latex_table = latex_table.replace(r"\toprule", r"\hline\hline").replace(r"\midrule", r"\hline").replace(r"\bottomrule", r"\hline\hline")
    final_table = f"""
\\begin{{table}}[htbp]
\\centering
\\caption{{{caption}}}
\\label{{{label}}}
\\resizebox{{\\textwidth}}{{!}}{{%
{latex_table.strip()}
}}
\\end{{table}}
"""
    return final_table

def _test():
    import doctest
    doctest.testmod(verbose=False)

if __name__ == '__main__':
    _test()
