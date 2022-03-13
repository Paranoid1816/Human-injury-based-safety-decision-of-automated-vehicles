# Human injury-based safety decision of automated vehicles

Qingfan Wang, Bingbing Nie, Dongyang Xu

State Key Lab of Automotive Safety and Energy, School of Vehicle and Mobility, Tsinghua University, Beijing, China



## Overview 

The data and code accompany the paper titled "Human injury-based safety decision of automated vehicles".
This paper explores whether, how, and to what extent the human injury-based decisions of automated vehicles (AVs) can enhance human protection in pursuing improved traffic safety.
Understanding the safety protection in road traffic follows a “top-down” process involving the traffic, vehicle, and human levels (Fig. a-c). Correspondingly, we propose a novel framework of an injury risk mitigation-based (IRM) decision-making algorithm that makes safety decisions towards minimal injury risk, which incorporates a “bottom-up” process (Fig. d-f).

![Figure 1](image\Figure 1.png)



### IRM algorithm

In the folder `IRM_algorithm`, you will find the IRM algorithm (a `py` file). The code detailedly demonstrates how AVs make human injury-based decisions according to the predicted, quantified human injury information via the rolling-horizon optimization.



### IRM data

In the folder `IRM_data`, you will find the data generated by the IRM algorithm. The source data for Fig 3, Fig 4, Fig5a-c, and Fig6a-b are provided with the `py` files and `npy` files.



### IRM GUI

A Python-based GUI that helps explain the IRM algorithm and visualizes the decision process and results is provided in the folder `IRM_GUI`.

<img src="image\logo.png" alt="logo" style="zoom:25%;" />



### Supplemental information

In the folder `Supplemental` the data and codes classified by different sections are provided.

Specifically, the NASS-CDS (2004-2015) crash data and the reconstructed accident data are given in the folder `Supplemental\A3. Real-world accident dataset` and `Supplemental\A7. Reconstructed accidents`, respectively.

Codes for the training and testing of three DL-based (FNN, RNN, and CNN) and five ML-based (SVM, DT, KNN, Naive Bayes, and AdaBoost) injury prediction models are provided in the folder `Supplemental\A4. Injury prediction module`.

Codes for the calculation of the equivalent economic loss are available at `Supplemental\A8. Calculating economic loss`. 



## Citation

```
@ARTICLE{Wang_2022, 
author={Q. {Wang} and Q. {Zhou} and M. {Lin} and B. {Nie}}, 
journal={...}, 
title={Human injury-based safety decision of automated vehicles}, 
year={2022}, 
}
```

If you find the above information (data, codes, and GUI) is useful, please cite the above paper.



## Terms of use

The databases are licensed under a [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/legalcode).



## Contact

Contact Information Email: wqf20@mails.tsinghua.edu.cn; nbb@tsinghua.edu.cn.