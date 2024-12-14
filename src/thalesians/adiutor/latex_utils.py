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
