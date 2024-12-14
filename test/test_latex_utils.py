import unittest

import pandas as pd

import thalesians.adiutor.latex_utils as latex_utils

class TestLaTeXUtils(unittest.TestCase):
    def test_to_booktabs_table(self):
        data = {
            "Column A": [1, 2, 3],
            "Column B": [4, 5, 6],
            "Column C": ["$x$", "$y$", "$z$"]  # Escaped for LaTeX compatibility
        }
        df = pd.DataFrame(data)        
        latex_code = latex_utils.to_booktabs_table(df, caption="Example Table", label="Example Table")
        self.assertEqual(latex_code, r"""
\begin{table}[htbp]
\centering
\caption{Example Table}
\label{Example Table}
\resizebox{\textwidth}{!}{%
\begin{tabular}{lcc}
\hline\hline
Column A & Column B & Column C \\
\hline
1 & 4 & $x$ \\
2 & 5 & $y$ \\
3 & 6 & $z$ \\
\hline\hline
\end{tabular}
}
\end{table}
""")

if __name__ == '__main__':
    unittest.main()
