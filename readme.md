# Incident Evaluator - Proof of Concept

## **1. Overview**

The Incident Evaluator is a Python-based software designed to assist in evaluating incidents in a Security Operations Center (SOC). It uses a game-theoretic model to reduce alert fatigue by assessing incidents based on costs and damages, as described in the accompanying master thesis.

---

## **2. Installation**

### **Prerequisites**

- Python 3.8 or higher
- Required libraries (detailed in the `requirements.txt` file, if available).

### **Installation Steps**

1. Clone or download the repository:
   ```bash
   git clone <repository_url>
   ```
2. Navigate to the project directory:
   ```bash
   cd incident-evaluator
   ```

---

## **3. Usage**

### **Running the Program**

To execute the software, run the main script:

```bash
python main.py
```

### **Input and Output**

- **Input**: Incident alert data, likely in JSON or database format, which is processed by the system.
- **Output**: Evaluated incident reports and decisions, stored in the database or presented as console logs.

---

## **4. Software Architecture**

### **Key Components**

1. **`main.py`**

   - Entry point for the application.
   - Coordinates the flow of data between modules.

2. **`AlertProcessor`**\*\* Directory\*\*

   - **`alert_processor.py`**:
     - Core logic for processing and evaluating alerts.

3. **`Database`**\*\* Directory\*\*

   - **`rule_data.py`**:
     - Manages analytic rules for incident.
   - **`database_manager.py`**:
     - Handles interactions with the database.
   - **`incident.py`**:
     - Defines the structure and attributes of an incident.
   - **`threat_history.py`**:
     - Maintains a record of historical threats for reference.
   - **`base.py`**:
     - Provides foundational database utilities.

### **Data Flow**

1. Analytic Rules are inputted into the system via the `main.py` script.
2. Incidents are processed by `alert_processor.py` using predefined rules from `rule_data.py`.
3. *Evaluated incidents are stored or updated in the database using ****`database_manager.py`****.*
4. Historical data is referenced or updated through `threat_history.py`.

## **6. Limitations and Future Work**

### **Current Limitations**

- The software is tailored to the specific use case described in the master thesis.
- Performance may vary based on the volume of alerts and database efficiency.

### **Possible Future Enhancements**

- Support for additional input formats.
- Integration with external SOC platforms.
- Optimization of the game-theory evaluation algorithm.
