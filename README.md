# What is RFM?
It is a technique used for customer segmentation. It is a simple rule-based customer segmentation technique.
It enables customers to be divided into groups based on their purchasing habits and to develop strategies specific to these groups.
It provides the opportunity to take data-based actions on many topics for CRM studies.

RFM Metrics
Recency: Indicates the last time the customer made a purchase.
Frequency: It is the total number of purchases made by the customer. That is the number of transactions. Transaction frequency.
Monetary: It is the value of money left by the customer.

Note: In the recency value, if the customer made a purchase 1 day ago, the recency value will be smaller. If the customer has made a purchase 80 days ago, the recency value will be higher. Ex: If he did it 1 day ago, it's like 1, if he did it 80 days ago, it's like 80.
But here the value expressed by 1 is greater than 80. Because it means that the customer is shopping more often and more recently.

Note: Fruqency and monetary metrics are expected to be high.

RFM Scores: It is the process of obtaining a certain score by standardizing RFM metrics. The metrics here are arranged as string values and combined and the RFM score is obtained. Since these scores are too many and there are too many combinations, they are segmented by the score.

RFM Analysis Stages:
1) The story of the data set is checked.
2) Variables are checked.
3) Relevant libraries are loaded to make observations about the data. (Pandas, datetime)
4) Adjustments are made regarding the data set.
5) During the data set preparation, null values are checked. Relevant values are extracted from the data set.
6) RFM metrics are calculated. While calculating these metrics, deduplication is performed according to the state of the data set. Groupby is done according to the customer. The agg function is used. R F and M values are assigned to the corresponding columns.
7) Calculation of RFM scores. The point to be noted here is the Recency value. When sorting the recency, it should be sorted as the reverse of the frequency and monetary values. Tags should be ordered from largest to smallest. F and M values are ordered from smallest to largest. In addition, the rank method should be used in the frequency value.
These values are then converted to strings.
8) RFM segments are created. Here the seg_map variable is used. seg_map func. It is created according to the R and F values.
Because RFM analysis deals with r and f values.
9) Observations are made according to the separated segments.
10) Relevant segments are converted to a csv format if desired.
