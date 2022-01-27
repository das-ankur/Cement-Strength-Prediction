# Cement-Strength-Prediction
## Data Description:
### Cement (Input Variable) : 
    It is a quantitive variable. Measurement in kg in a m3 mixture.
### Blast Furnace Slag(Input Variable):
    It is a quantitive variable. Measurement in kg in a m3 mixture. Blast furnace slag is a nonmetallic coproduct produced in the process. It consists primarily of silicates, aluminosilicates, and calcium-alumina-silicates.
### Fly Ash(Input Variable):
    It is a quantitive variable. Measurement in kg in a m3 mixture. it is a coal combustion product that is composed of the particulates (fine particles of burned fuel) that are driven out of coal-fired boilers together with the flue gases.
### Water(Input Vraible):
    It is a quantitive variable. Measurement in kg in a m3 mixture.
### Superplasticizer(Input Vraibale):
    It is a quantitive variable. Measurement in kg in a m3 mixture. Superplasticizers (SP's), also known as high range water reducers, are additives used in making high strength concrete. Their addition to concrete or mortar allows the reduction of the water to cement ratio without negatively affecting the workability of the mixture, and enables the production of self-consolidating concrete and high performance concrete.
### Coarse Aggregate (Input Variable):
    It is a quantitive variable. Measurement in kg in a m3 mixture. Construction aggregate, or simply "aggregate", is a broad category of coarse to medium grained particulate material used in construction, including sand, gravel, crushed stone, slag, recycled concrete and geosynthetic aggregates.
### Fine Aggregate(Input Vriable):
    It is a quantitive variable. Measurement in kg in a m3 mixture. Input Variable—Similar to coarse aggregate, the constitution is much finer.
### Age(Inpiut Vraible): 
    It is a quantitive variable. Day measured in(1~365).
### Concrete Compressive Strength(Outpu Vraible):
    It is a quantitive variable. Measured by MPa.
## Data Validation:

**Name Validation:** We validate the name of the files based on the given name in the schema file. We have created a regex pattern as per the name given in the schema file to use for validation. After validating the pattern in the name, we check for the length of date in the file name as well as the length of time in the file name. If all the values are as per requirement, we move such files to "Good_Data_Folder" else we move such files to "Bad_Data_Folder."

**Number of Columns:** We validate the number of columns present in the files, and if it doesn't match with the value given in the schema file, then the file is moved to "Bad_Data_Folder."

**Name of Columns:** The name of the columns is validated and should be the same as given in the schema file. If not, then the file is moved to "Bad_Data_Folder".

**The datatype of columns:** The datatype of columns is given in the schema file. This is validated when we insert the files into Database. If the datatype is wrong, then the file is moved to "Bad_Data_Folder".

**Null values in columns:** If any of the columns in a file have all the values as NULL or missing, we discard such a file and move it to "Bad_Data_Folder".
