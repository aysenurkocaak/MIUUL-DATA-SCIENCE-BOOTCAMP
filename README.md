## 🛠 - CASE STUDY 1 : 

# **Customer Segmentation with RFM Analysis**

## **Business Problem**
FLO, an online shoe store, aims to segment its customers and develop marketing strategies based on these segments. To achieve this, customer behaviors will be analyzed, and behavioral clusters will be created.

## **Dataset Description**
The dataset includes past shopping behaviors of customers who made their last purchases through OmniChannel (both online and offline) between 2020 and 2021 at FLO.

- **12 Variables, 19,945 Observations, 2.7MB**

| Variable | Description |
|----------|-------------|
| `master_id` | Unique customer ID |
| `order_channel` | Platform used for shopping (Android, iOS, Desktop, Mobile) |
| `last_order_channel` | Channel used for the last purchase |
| `first_order_date` | Date of the first purchase |
| `last_order_date` | Date of the last purchase |
| `last_order_date_online` | Date of the last online purchase |
| `last_order_date_offline` | Date of the last offline purchase |
| `order_num_total_ever_online` | Total number of purchases made online |
| `order_num_total_ever_offline` | Total number of purchases made offline |
| `customer_value_total_ever_offline` | Total amount spent in offline purchases |
| `customer_value_total_ever_online` | Total amount spent in online purchases |
| `interested_in_categories_12` | Categories the customer has shopped from in the last 12 months |

---

## **Project Tasks**

### **Task 1: Understanding and Preparing the Data**
**Step 1:** Read the dataset `flo_data_20K.csv` and create a copy of the DataFrame.

**Step 2:** Examine the dataset by:
  - Viewing the first 10 observations
  - Checking variable names
  - Generating descriptive statistics
  - Identifying missing values
  - Checking variable types

**Step 3:** Since OmniChannel customers shop from both online and offline platforms, create new variables for each customer's total number of purchases and total spending.

**Step 4:** Convert date-related variables to the appropriate date format.

**Step 5:** Analyze the distribution of:
  - The number of customers per shopping channel
  - The total number of products purchased
  - Total spending

**Step 6:** List the top 10 customers generating the highest revenue.

**Step 7:** List the top 10 customers with the most orders.

**Step 8:** Automate the data preprocessing steps by converting them into a function.

---

### **Task 2: Calculating RFM Metrics**
**Step 1:** Define the **Recency, Frequency, and Monetary** metrics.

**Step 2:** Compute the RFM metrics for each customer.

**Step 3:** Store the calculated metrics in a variable called `rfm`.

**Step 4:** Rename the metrics as `recency`, `frequency`, and `monetary`.
- When calculating **recency**, set the analysis date to two days after the latest purchase date.

---

### **Task 3: Calculating RF Scores**
**Step 1:** Convert **Recency, Frequency, and Monetary** values into scores between 1-5 using `qcut`.

**Step 2:** Save these scores as `recency_score`, `frequency_score`, and `monetary_score`.

**Step 3:** Combine `recency_score` and `frequency_score` into a single variable called `RF_SCORE`.

---

### **Task 4: Defining RF Score Segments**
**Step 1:** Define customer segments based on RF scores.

**Step 2:** Use the following **segmentation map** to classify RF scores into meaningful groups.

---

### **Task 5: Taking Action!**
**Step 1:** Analyze the average **recency, frequency, and monetary** values for each segment.

**Step 2:** Identify customers for the following marketing campaigns and save their IDs in a CSV file:

  - **Case 1:** FLO is launching a new **women's shoe brand** with higher-than-average prices. To promote the brand and drive sales, FLO wants to contact **loyal customers (Champions, Loyal Customers)** who have purchased from the **women’s category**. Extract and save the IDs of these customers.

  - **Case 2:** FLO is planning **a 40% discount on men’s and children’s products**. This campaign targets customers who previously had good purchase behavior but haven’t shopped in a long time. FLO aims to reach **Lost Customers and At-Risk Customers** who have previously shopped in these categories. Extract and save the IDs of these customers.



