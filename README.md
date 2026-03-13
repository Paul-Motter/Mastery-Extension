## how to use program.

### run with ```python main.py```

### Command Line Arguments

- **`-t <threshold>`**  
    Sets the minimum similarity score required for authentication.  
    The value should be a floating-point number between **0 and 1**. The defuault value is `0.975`.

- **`-stats`**  
  Runs the program in **statistics analysis mode** instead of data collection.  
  In this mode, the program evaluates stored keystroke records and computes authentication metrics such as:
  - True Acceptance Rate (TAR)
  - True Rejection Rate (TRR)
  - False Acceptance Rate (FAR)
  - False Rejection Rate (FRR)